from sqlalchemy import create_engine
import pandas as pd
from models import Base
from models.book import Book
from models.user import User
from models.author import Author
from models.rating import Rating
from models.book_genre import Genre
from models.reading_list import ReadingList

DATA_DIR = "data/good_books_10k_extended/"
BOOK_FILE_NAME = DATA_DIR + "books_enriched.csv"



def create_book_df():
    df = pd.read_csv(BOOK_FILE_NAME)
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


    return df


def main():
    engine = create_engine("sqlite+pysqlite:///data/db/test.db", echo=True)
    Base.metadata.create_all(engine)




if __name__ == "__main__":
    main()
