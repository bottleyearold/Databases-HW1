import sqlite3
import json

# I did not take in the database or the json in command line oops!
# read in json file
with open('wheel_of_time.json', "r", encoding="utf-8") as file:
    wot_data = json.load(file)

# creating the sqlite database and initiating connection
connection = sqlite3.connect("wheel_of_time.sqlite")
cursor = connection.cursor()

# I wasn't sure if I should make a different primary key or just not have one
# becasue not all books have an order number
# Here I did add an id but let me know what you think
cursor.execute("""
CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_order INT,
    title TEXT NOT NULL,
    sandersonCoWrote BOOLEAN,
    goodreadsAverage REAL, 
    mcburneyScore INT, 
    mcburneyReview TEXT
);
""")

# Inserting the books into the table
for book in wot_data['books']:
    cursor.execute("""
    INSERT INTO books (book_order, title, sandersonCoWrote, goodreadsAverage, mcburneyScore, mcburneyReview)
    VALUES (?, ?, ?, ?, ?, ?);
    """, (
        book.get("order"),
        book.get("title"),
        book.get("sandersonCoWrote"),
        book.get("goodreadsAverage"),
        book.get("mcburneyScore"),
        book.get("mcburneyReview")
    ))

# close transaction
connection.commit()
connection.close()
