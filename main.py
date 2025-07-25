from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr 
from typing import Optional
import psycopg2  
from psycopg2.extras import RealDictCursor 

DB_CONFIG = {
    "dbname": "maindb",  
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

# Pydantic model
class Student(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None  # YYYY-MM-DD
    major: Optional[str] = None
    year_level: Optional[int] = None
    gpa: Optional[float] = None
    address: Optional[str] = None

app = FastAPI(title="Students CRUD API")

BASE_PATH = "/students"

# Create
@app.post(f"{BASE_PATH}/")
def create_student(student: Student):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mainschema.students 
            (first_name, last_name, email, phone, date_of_birth, major, year_level, gpa, address)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING student_id;
        """, (student.first_name, student.last_name, student.email, student.phone, student.date_of_birth,
              student.major, student.year_level, student.gpa, student.address))
        student_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Student added successfully", "student_id": student_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Read
@app.get(f"{BASE_PATH}/{{student_id}}")
def get_student(student_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM mainschema.students WHERE student_id = %s;", (student_id,))
        student = cursor.fetchone()
        cursor.close()
        conn.close()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update
@app.put(f"{BASE_PATH}/{{student_id}}")
def update_student(student_id: int, student: Student):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE mainschema.students
            SET first_name=%s, last_name=%s, email=%s, phone=%s, date_of_birth=%s, 
                major=%s, year_level=%s, gpa=%s, address=%s, updated_at=NOW()
            WHERE student_id=%s RETURNING student_id;
        """, (student.first_name, student.last_name, student.email, student.phone, student.date_of_birth,
              student.major, student.year_level, student.gpa, student.address, student_id))
        updated = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        if not updated:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student updated successfully", "student_id": student_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Delete
@app.delete(f"{BASE_PATH}/{{student_id}}")
def delete_student(student_id: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mainschema.students WHERE student_id=%s RETURNING student_id;", (student_id,))
        deleted = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        if not deleted:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully", "student_id": student_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

