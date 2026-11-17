
import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")
conn.commit()

# Title
st.title("Student Record Management System")

# Menu
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students",
     "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("Add Student")

    roll = st.number_input("Roll Number", min_value=1)
    name = st.text_input("Student Name")
    age = st.number_input("Age", min_value=1)
    course = st.text_input("Course")

    if st.button("Add Student"):
        if name and course:
            try:
                cursor.execute(
                    "INSERT INTO students VALUES (?, ?, ?, ?)",
                    (roll, name, age, course)
                )
                conn.commit()
                st.success("Student added successfully!")
            except sqlite3.IntegrityError:
                st.error("Roll number already exists!")
        else:
            st.warning("Please fill all fields.")

# READ
elif menu == "View Students":
    st.subheader("All Student Records")

    df = pd.read_sql_query(
        "SELECT * FROM students", conn
    )
    st.dataframe(df)

# UPDATE
elif menu == "Update Student":
    st.subheader("Update Student")

    roll = st.number_input("Roll Number", min_value=1)
    name = st.text_input("New Name")
    age = st.number_input("New Age", min_value=1)
    course = st.text_input("New Course")

    if st.button("Update Student"):
        cursor.execute(
            """UPDATE students
               SET name=?, age=?, course=?
               WHERE roll_no=?""",
            (name, age, course, roll)
        )
        conn.commit()

        if cursor.rowcount > 0:
            st.success("Student updated successfully!")
        else:
            st.error("Student not found!")

# DELETE
elif menu == "Delete Student":
    st.subheader("Delete Student")

    roll = st.number_input("Roll Number", min_value=1)

    if st.button("Delete Student"):
        cursor.execute(
            "DELETE FROM students WHERE roll_no=?",
            (roll,)
        ) 
        conn.commit()

        if cursor.rowcount > 0:
            st.success("Student deleted successfully!")
        else:
            st.error("Student not found!")

conn.close()
