import os
import psycopg2
import dotenv

dotenv.load_dotenv()

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host = os.getenv("DB_HOST", "localhost"), 
        port = os.getenv("DB_PORT", "5432"), 
        dbname = os.getenv("DB_NAME"), user = os.getenv("DB_USER"), password = os.getenv("DB_PASS")
    )

    # Create cursor
    cursor = conn.cursor()

    # Get author name from user
    author_name = input("Enter author name: ")

    # Parameterized query
    query = """
        SELECT b.title
        FROM books b
        JOIN book_authors ba
            ON b.book_id = ba.book_id
        JOIN authors a
            ON ba.author_id = a.author_id
        WHERE a.author_name = %s;
    """

    cursor.execute(query, (author_name,))

    books = cursor.fetchall()

    if books:
        print("\nBooks written by", author_name)

        for book in books:
            print("-", book[0])

    else:
        print("No books found.")

except :
    conn.rollback()

finally:
    if 'cursor' in locals():
        cursor.close()

    if 'conn' in locals():
        conn.close()

    print("\nDatabase connection closed.")