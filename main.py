from fastapi import FastAPI
import psycopg2

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello"}

@app.get("/test-db")
def test_db_connection():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="secret",
            host="my_postgres",
            port="5432"
        )
        connection.close
        return{
            "status": "success",
            "message": "Successfully connected to PostgreSQL via Docker!",
        }
    except Exception as e:
        return{"status": "error", "message": f"Error connecting to the database: {str(e)}"}

