from sqlalchemy import create_engine, event, exc, select
import pandas as pd
from sqlalchemy.orm import Session, scoped_session, sessionmaker
import csv

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


def create_book_df() -> pd.DataFrame:
    # column_list =["index","authors","average_rating","best_book_id","book_id","books_count","description","genres","goodreads_book_id","image_url","isbn","isbn13","language_code","original_publication_year","original_title","pages","publishDate","ratings_1","ratings_2","ratings_3","ratings_4","ratings_5","ratings_count","small_image_url","title","work_id","work_ratings_count","work_text_reviews_count","authors_2"]
    use_cols = ["authors", "best_book_id", "book_id", "description", "genres", "image_url", "isbn", "isbn13",
                "language_code", "original_publication_year", "pages", "title"]

    book_df = pd.read_csv(
        BOOK_FILE_NAME,
        usecols=use_cols,
        dtype={"pages": "Int16", "isbn": "string", "isbn13": "string", "publishDate": "string",
               "original_publication_year": "Int16",
               },
    )
    # Reorder columns to be in same order as database table declaration
    book_df = book_df[
        ["book_id", "authors", "best_book_id", "title", "description", "isbn", "isbn13", "language_code", "genres",
         "pages", "image_url",
         "original_publication_year"]]

    # Convert to python lists
    book_df["authors"] = book_df["authors"].apply(eval)
    book_df["genres"] = book_df["genres"].apply(eval)

    # Remove extra spaces in author names and add workaround to handle author attributed multiple times for a book
    book_df["authors"] = book_df["authors"].apply(lambda l: set(map(lambda x: " ".join(x.split()), l)))

    return book_df


def export_book_data(book_df: pd.DataFrame):
    modified_book_df = book_df.drop(['genres', 'authors'], axis=1)
    modified_book_df.rename(
        columns={"book_id": "id", "best_book_id": "goodreads_id", "language_code": "lang_code",
                 "image_url": "cover_url"}, inplace=True
    )
    modified_book_df.to_csv("data/books.csv", index=False)


def export_genre_data(book_df: pd.DataFrame):
    book_genres_df = book_df[["book_id", "genres"]].explode("genres")
    genres_df = pd.DataFrame(book_genres_df["genres"].unique(), columns=["name"])
    genres_df.index.rename("id", inplace=True)
    genres_df.to_csv("data/genres.csv")

    book_genres_df["genres"] = book_genres_df["genres"].apply(
        # Replace genre name with id generated in genre_df
        lambda x: genres_df.index[genres_df["name"] == x].to_list()[0]
    )
    book_genres_df.rename(columns={"genres": "genre_id"}, inplace=True)
    book_genres_df.to_csv("data/book_genres.csv", index=False)


def export_author_data(book_df: pd.DataFrame):
    # Create book author association dataframe
    book_authors_df = book_df[["book_id", "authors"]].explode("authors")

    authors_df = pd.DataFrame(book_authors_df["authors"].unique(), columns=["name"])
    authors_df.index.rename("id", inplace=True)
    authors_df.to_csv("data/authors.csv")

    book_authors_df["authors"] = book_authors_df["authors"].apply(
        # Replace author name with id generated in authors_df
        lambda x: authors_df.index[authors_df["name"] == x].to_list()[0]
    )
    book_authors_df.rename(columns={"authors": "author_id"}, inplace=True)
    book_authors_df.to_csv("data/book_authors.csv", index=False)

    book_df.drop(['genres', 'authors'], axis=1, inplace=True)
    book_df.rename(columns={"book_id": "id", "best_book_id": "goodreads_id"}, inplace=True)
    book_df.to_csv("data/book_data.csv", index=False)


def export_fake_user_data():
    ratings_df = pd.read_csv(RATINGS_FILE_NAME)
    reading_list_df = pd.read_csv(READING_LIST_FILE_NAME)

    ratings_user_ids = set(ratings_df["user_id"])
    reading_list_user_ids = set(reading_list_df["user_id"])

    user_ids = ratings_user_ids.union(reading_list_user_ids)
    user_data = [{"id": user_id, "username": f"User_{user_id}"} for user_id in user_ids]
    user_df = pd.DataFrame(user_data)
    user_df.to_csv("data/users.csv", index=False)


def main():
    engine = create_engine("sqlite+pysqlite:///data/db/test.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    book_df = create_book_df()
    print("Exporting book data")
    export_book_data(book_df)
    print("Exporting genre data")
    export_genre_data(book_df)
    print("Exporting author data")
    export_author_data(book_df)
    print("Exporting user data")
    export_fake_user_data()



if __name__ == "__main__":
    main()
