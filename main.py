from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import asyncpg
from dotenv import load_dotenv
import os
from starlette.status import HTTP_400_BAD_REQUEST
import pysolr


app = FastAPI(docs_url="/api/docs", redoc_url=None)


# Load environment variables
load_dotenv()

# Database connection settings from environment variables
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# Security
# security = HTTPBasic()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy method to verify password (replace with your actual method)

async def execute_query(query: str):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Execute a query
        result = await conn.fetch(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        await conn.close()

@app.post("/execute/")
async def execute(start_time : datetime, end_time : datetime):
    # WARNING: Directly using input to form SQL queries is extremely dangerous
    # and vulnerable to SQL injection. This is for demonstration purposes only.
    sql_query = f"""SELECT remove_html_tags(content::json->>'description')"
                 ", id, harvest_source_id, fetch_finished, fetch_started
from harvest_object where fetch_started > '{start_time}' AND fetch_finished > '{end_time}';"""
    result = await execute_query(sql_query)
    insert_data_to_solr(result)
    return {"result": str(result)}


def insert_data_to_solr(data):
    """
    Inserts data into a Solr core using pysolr.

    :param solr_url: URL of the Solr server
    :param solr_core: Name of the Solr core
    :param data: A list of dictionaries, where each dictionary represents a document to be indexed
    """
    # Connect to Solr core
    solr_url = os.getenv("SOLR_URL")
    solr_core = os.getenv("SOLR_CORE")
    solr = pysolr.Solr(f"{solr_url}/{solr_core}", always_commit=True)

    total_data = []
    for d in data:
        push_data = {}
        push_data['text'] = d[0]
        push_data['doc_id'] = d[1]
        push_data['src_id'] = d[2]
        push_data['type'] = 'Data'
        total_data.append(push_data)

    try:
        # Add documents to the index
        for dt in total_data:
            solr.add(dt)
        print("Data successfully indexed")
        solr.commit()
    except Exception as e:
        print(f"Error during indexing: {e}")