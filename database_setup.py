import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",      # Replace with your MySQL username
    password="mysql",  # Replace with your MySQL password
    database="face_recognition_db"
)
cursor = conn.cursor()