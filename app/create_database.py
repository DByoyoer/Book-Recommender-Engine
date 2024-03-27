from sqlalchemy import create_engine, event, exc, select
import pandas as pd
from sqlalchemy.orm import Session, scoped_session, sessionmaker
import csv

# from models import Base
# from models.book import Book
# from models.user import User
# from models.author import Author
# from models.rating import Rating
# from models.book_genre import Genre
# from models.reading_list import ReadingList

DATA_DIR = "data/good_books_10k_extended/"
BOOK_FILE_NAME = DATA_DIR + "books_enriched.csv"
RATINGS_FILE_NAME = DATA_DIR + "ratings.csv"
READING_LIST_FILE_NAME = DATA_DIR + "to_read.csv"


def create_book_df():
    # column_list =["index","authors","average_rating","best_book_id","book_id","books_count","description","genres","goodreads_book_id","image_url","isbn","isbn13","language_code","original_publication_year","original_title","pages","publishDate","ratings_1","ratings_2","ratings_3","ratings_4","ratings_5","ratings_count","small_image_url","title","work_id","work_ratings_count","work_text_reviews_count","authors_2"]
    use_cols = ["authors", "best_book_id", "book_id", "description", "genres", "image_url", "isbn", "isbn13",
                "language_code", "original_publication_year", "original_title", "pages", "publishDate",
                "small_image_url", "title"]
    df = pd.read_csv(
        BOOK_FILE_NAME,
        usecols=use_cols,
        dtype={"pages": "Int16", "isbn": "string", "isbn13": "string", "publishDate": "string",
               "original_publication_year": "Int16",
               },
    )

    # There are some cases where original_title has no value but title has a value
    df['original_title'] = df['original_title'].fillna(df['title'])

    # Convert columns that are lists to be actual python lists
    # Note: Relies on the format of the data to have python list syntax
    df["authors"] = df["authors"].apply(eval)
    df["genres"] = df["genres"].apply(eval)

    exploded_df = df["genres"].explode()
    genres = exploded_df.unique()
    genre_df = pd.DataFrame(genres, columns=["name"])
    genre_df.index.rename("genre_id", inplace=True)
    genre_df.to_csv("data/genres.csv")

    book_genre_associations = {"book_id": [], "genre_id": []}
    for row in df.itertuples(name="book"):
        for genre in row.genres:
            book_genre_associations["book_id"].append(row.book_id)
            book_genre_associations["genre_id"].append(genre_df.index[genre_df["name"]==genre].to_list()[0])

    book_genre_associations_df = pd.DataFrame(book_genre_associations)
    book_genre_associations_df.to_csv("data/book_genre.csv", index=False)

    return df


def create_ratings_df():
    df = pd.read_csv(RATINGS_FILE_NAME)
    return df


def create_reading_list_df():
    df = pd.read_csv(READING_LIST_FILE_NAME)
    return df


# def populate_book_data(engine):
#     book_df = create_book_df()
#     with Session(engine) as session, session.begin():
#         for row in book_df.itertuples():
#             # TODO: See if this type manipulation can be done better
#             # a = type(row)
#             # row = a._make(map(lambda x: x if pd.notna(x) else None, row))
#             book = Book(
#                 id=row.book_id,
#                 title=row.title if pd.notna(row.title) else None,
#                 pages=int(row.pages) if pd.notna(row.pages) else None,
#                 isbn=row.isbn if pd.notna(row.isbn) else None,
#                 lang_code=row.language_code if pd.notna(row.language_code) else None,
#                 description=row.description if pd.notna(row.description) else None,
#                 cover_url=row.image_url if pd.notna(row.image_url) else None,
#                 original_publication_year=int(row.original_publication_year) if pd.notna(
#                     row.original_publication_year
#                 ) else None,
#             )
#
#             try:
#                 with session.begin_nested():
#                     session.add(book)
#                     for name in row.authors:
#                         # TODO: Move this to create_book_df
#                         name = " ".join(name.split())
#                         author = session.scalar(select(Author).where(Author.name == name))
#                         if author is None:
#                             author = Author(name=name)
#                             session.add(author)
#                         # A few books have the same author listed twice
#                         # Maybe an author/secondary role type of thing
#                         # For now ignore the duplicate name in list
#                         if author not in book.authors:
#                             book.authors.append(author)
#             except exc.IntegrityError as error:
#                 print(f"Error: {error} when inserting book {book}")
#                 print(f"Book: {book.title}, Authors: {[author.name for author in book.authors]}")
#
#
# def populate_user_data(engine):
#     ratings_df = create_ratings_df()
#     reading_list_df = create_reading_list_df()
#
#     ratings_user_ids = set(ratings_df["user_id"])
#     reading_list_user_ids = set(reading_list_df["user_id"])
#
#     # TODO: Find nicer way of doing this, low priority though
#     user_ids = list(ratings_user_ids.union(reading_list_user_ids))
#     users = [User(id=user_id, username=f"User_{user_id}") for user_id in user_ids]
#
#     # Insert user data
#     try:
#         with Session(engine) as session, session.begin():
#             session.add_all(users)
#     except exc.IntegrityError:
#         print("Skipped adding users.")
#         pass
#
#     ratings = [{"book_id": row.book_id, "user_id": row.user_id, "rating": row.rating} for row in
#                ratings_df.itertuples()]
#     # Use SQLAlchemy core for some speed
#     with engine.connect() as conn:
#         conn.execute(Rating.__table__.insert(), ratings)


def main():
    # engine = create_engine("sqlite+pysqlite:///data/db/test.db")
    #
    # # Workaround for disk I/O error when trying to use begin_nested() to handle database integrity errors in the creation code
    # # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#pysqlite-serializable
    # # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#sqlite-concurrency
    # @event.listens_for(engine, "connect")
    # def do_connect(dbapi_connection, connection_record):
    #     # disable pysqlite's emitting of the BEGIN statement entirely.
    #     # also stops it from emitting COMMIT before any DDL.
    #     dbapi_connection.isolation_level = None
    #
    # @event.listens_for(engine, "begin")
    # def do_begin(conn):
    #     # emit our own BEGIN
    #     conn.exec_driver_sql("BEGIN")
    #
    # Base.metadata.create_all(engine)

    book_df = create_book_df()

    # Insert authors into author table getting generated id
    # Insert book id and author id into the book_genre_association?
    # Same for genres


if __name__ == "__main__":
    main()
