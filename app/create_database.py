from sqlalchemy import create_engine, event, exc, select
import pandas as pd
from sqlalchemy.orm import Session

from models import Base
from models.book import Book
from models.user import User
from models.author import Author
from models.rating import Rating
from models.book_genre import Genre
from models.reading_list import ReadingList

DATA_DIR = "data/good_books_10k_extended/"
BOOK_FILE_NAME = DATA_DIR + "books_enriched.csv"
RATINGS_FILE_NAME = DATA_DIR + "ratings.csv"
READING_LIST_FILE_NAME = DATA_DIR + "to_read.csv"


def create_book_df():
    df = pd.read_csv(
        BOOK_FILE_NAME,
        dtype={"pages": "Int16", "isbn": "string", "isbn13": "string", "publishDate": "string",
               "original_publication_year": "Int16",
               },
    )

    # TODO: Convert to use_col in pd.read_csv instead of dropping
    drop_columns = ["Unnamed: 0", "index", "average_rating", "books_count", "ratings_count", "ratings_1", "ratings_2",
                    "ratings_3", "ratings_4", "ratings_5", "small_image_url", "work_ratings_count",
                    "work_text_reviews_count", ]

    df.drop(drop_columns, axis=1, inplace=True)
    # There are some cases where original_title has no value but title has a value
    df['original_title'] = df['original_title'].fillna(df['title'])

    # Convert columns that are lists to be actual python lists
    # Note: Relies on the format of the data to have python list syntax
    df["authors"] = df["authors"].apply(eval)
    df["authors_2"] = df["authors_2"].apply(eval)
    df["genres"] = df["genres"].apply(eval)

    return df


def create_ratings_df():
    df = pd.read_csv(RATINGS_FILE_NAME)
    return df


def create_reading_list_df():
    df = pd.read_csv(READING_LIST_FILE_NAME)
    return df


def create_fake_user_df(ratings_df: pd.DataFrame, reading_list_df: pd.DataFrame):
    ratings_user_ids = set(ratings_df["user_id"])
    reading_list_user_ids = set(reading_list_df["user_id"])

    # TODO: Find nicer way of doing this, low priority though
    user_ids = list(ratings_user_ids.union(reading_list_user_ids))
    usernames = [f"User_{user_id}" for user_id in user_ids]

    return pd.DataFrame({"user_id": user_ids, "username": usernames})


def main():
    engine = create_engine("sqlite+pysqlite:///data/db/test.db")

    # Workaround for disk I/O error when trying to use begin_nested() to handle database integrity errors in the creation code
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#pysqlite-serializable
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-concurrency
    @event.listens_for(engine, "connect")
    def do_connect(dbapi_connection, connection_record):
        # disable pysqlite's emitting of the BEGIN statement entirely.
        # also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None

    @event.listens_for(engine, "begin")
    def do_begin(conn):
        # emit our own BEGIN
        conn.exec_driver_sql("BEGIN")

    Base.metadata.create_all(engine)

    book_df = create_book_df()
    ratings_df = create_ratings_df()
    reading_list_df = create_reading_list_df()
    fake_user_df = create_fake_user_df(ratings_df, reading_list_df)

    with Session(engine) as session, session.begin():
        for row in book_df.itertuples():
            # TODO: See if this type manipulation can be done better
            # a = type(row)
            # row = a._make(map(lambda x: x if pd.notna(x) else None, row))
            book = Book(
                id=row.book_id,
                title=row.title if pd.notna(row.title) else None,
                pages=int(row.pages) if pd.notna(row.pages) else None,
                isbn=row.isbn if pd.notna(row.isbn) else None,
                lang_code=row.language_code if pd.notna(row.language_code) else None,
                description=row.description if pd.notna(row.description) else None,
                cover_url=row.image_url if pd.notna(row.image_url) else None,
                original_publication_year=int(row.original_publication_year) if pd.notna(
                    row.original_publication_year
                ) else None,
            )

            try:
                with session.begin_nested():
                    session.add(book)
                    for name in row.authors:
                        name = " ".join(name.split())
                        author = session.scalar(select(Author).where(Author.name == name))
                        if author is None:
                            author = Author(name=name)
                            session.add(author)
                        # A few books have the same author listed twice
                        # Maybe an author/secondary role type of thing
                        # For now ignore the duplicate name in list
                        if author not in book.authors:
                            book.authors.append(author)
            except exc.IntegrityError as error:
                print(f"Error: {error} when inserting book {book}")
                print(f"Book: {book.title}, Authors: {[author.name for author in book.authors]}")



        # Insert authors into author table getting generated id
        # Insert book id and author id into the book_genre_association?
        # Same for genres


if __name__ == "__main__":
    main()
