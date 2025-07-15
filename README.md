# **FastAPI CRUD API with PostgreSQL (Docker)**

<img width="300" height="168" alt="image" src="https://github.com/user-attachments/assets/ae4237f6-58a6-42b4-9a0d-8c6a1215e915" />


This project demonstrates how to build a **CRUD (Create, Read, Update, Delete)** API using **FastAPI** and **PostgreSQL** (running in Docker). It also includes instructions on testing the endpoints with **Postman** and `curl`.

---

##  **Project Overview**

* **Framework:** FastAPI
* **Database:** PostgreSQL (Docker container)
* **Schema:** `mainschema`
* **Table:** `students`
* **CRUD Operations:**

  * **Create:** Add a new student
  * **Read:** Get student details by ID
  * **Update:** Modify student information
  * **Delete:** Remove student record

---

##  **Step 1: Set Up PostgreSQL in Docker**

Run the following command to start a Postgres container:

```bash
docker run -d --name mypgcontainer \
-e POSTGRES_DB=maindb \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=postgres \
-v mypgvolume:/var/lib/postgresql/data \
-p 5432:5432 postgres:latest
```

### **Check container is running**

```bash
docker ps
```

---

##  **Step 2: Create Database Schema and Table**

Connect to Postgres using **DBeaver** or `psql`, then run:

```sql
CREATE SCHEMA IF NOT EXISTS mainschema;

CREATE TABLE mainschema.students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    date_of_birth DATE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    major VARCHAR(100),
    year_level INTEGER CHECK (year_level BETWEEN 1 AND 4),
    gpa DECIMAL(3,2) CHECK (gpa BETWEEN 0.00 AND 4.00),
    is_active BOOLEAN DEFAULT TRUE,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

##  **Step 3: Install Dependencies**

```bash
pip install fastapi uvicorn psycopg2-binary
```

---


## **Step 4: Run the FastAPI Server**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open Swagger Docs at:

```
http://localhost:8000/docs
```

---

##  **Step 5: Test API Endpoints**

### **Using Postman**

#### **1. Create Student (POST)**

* **URL:** `http://localhost:8000/students/`
* **Body (raw JSON):**

```json
{
  "first_name": "Alice",
  "last_name": "Green",
  "email": "alice.green@university.edu",
  "phone": "555-1234",
  "date_of_birth": "2002-03-15",
  "major": "Computer Science",
  "year_level": 3,
  "gpa": 3.8,
  "address": "123 Main Street"
}
```

#### **2. Read Student (GET)**

```
GET http://localhost:8000/students/1
```

#### **3. Update Student (PUT)**

* **URL:** `http://localhost:8000/students/1`
* **Body:**

```json
{
  "first_name": "Alice",
  "last_name": "Green Updated",
  "email": "alice.green@university.edu",
  "phone": "555-5678",
  "date_of_birth": "2002-03-15",
  "major": "Data Science",
  "year_level": 4,
  "gpa": 3.9,
  "address": "456 New Street"
}
```

#### **4. Delete Student (DELETE)**

```
DELETE http://localhost:8000/students/1
```


## **Project Summary**

* Learn how to:

  * **Run PostgreSQL in Docker**
  * **Create schema and tables**
  * **Build FastAPI CRUD APIs**
  * **Test using Postman and curl**
