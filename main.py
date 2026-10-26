import os
from fastapi import FastAPI, HTTPException
import psycopg2

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "my_postgres")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_db_connection():
  return psycopg2.connect(
      dbname=DB_NAME,
      user=DB_USER,
      password=DB_PASSWORD,
      host=DB_HOST,
      port=DB_PORT,
)
@app.on_event("startup")
def startup_db():
  conn = get_db_connection()
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        );
    """)
  conn.commit()
  cursor.close()
  conn.close()
  
@app.get("/")
def read_root():
    return {"message": "Hello"}

@app.get("/test-db")
def test_db_connection():
    try:
        connection = get_db_connection()
        connection.close
        return{
            "status": "success",
            "message": "Successfully connected to PostgreSQL via Docker!",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed connection: {str(e)}"}
    
@app.post("/notes")
def create_note(content: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notes (content) VALUES (%s) RETURNING id;", (content,)
        )
        note_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return {"id": note_id, "content": content, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        