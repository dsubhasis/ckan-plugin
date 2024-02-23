from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import asyncpg
from dotenv import load_dotenv
import os
from starlette.status import HTTP_400_BAD_REQUEST
from passlib.context import CryptContext

app = FastAPI(docs_url="/api/docs", redoc_url=None)


# Load environment variables
load_dotenv()

# Database connection settings from environment variables
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# Security
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
async def execute(sql_query: str):
    # WARNING: Directly using input to form SQL queries is extremely dangerous
    # and vulnerable to SQL injection. This is for demonstration purposes only.
    result = await execute_query(sql_query)
    return {"result": str(result)}
