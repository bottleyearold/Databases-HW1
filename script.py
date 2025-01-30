import sqlite3
import json
import sys
import os



def read(file, sql_file):
# I did not take in the database or the json in command line oops!
# read in json file
    with open(file, "r", encoding="utf-8") as file:
        wot_data = json.load(file)

    # creating the sqlite database and initiating connection
    connection = sqlite3.connect(sql_file)
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


def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    json_file = sys.argv[1]
    sqlite_file = sys.argv[2]

    if not os.path.isfile(json_file):
        print(f"Error: File '{json_file}' does not exist.")
        sys.exit(1)
    
    if json_file == 'wheel_of_time.json':
        read(json_file,sqlite_file)

if __name__ == "__main__":
    main()