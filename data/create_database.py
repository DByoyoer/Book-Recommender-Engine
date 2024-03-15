from sqlalchemy import create_engine
import pandas as pd
import numpy as np


DATA_DIR = "good_books_10k_extended/"
BOOK_FILE_NAME = DATA_DIR + "books_enriched.csv"


def main():
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    df = pd.read_csv(
        BOOK_FILE_NAME,
        index_col='book_id'
    )
    drop_columns = [
        "Unnamed: 0",
        "index",
        "average_rating",
        "books_count",
        "ratings_1",
        "ratings_2",
        "ratings_3",
        "ratings_4",
        "ratings_5",
        "small_image_url",
        "work_ratings_count",
        "work_text_reviews_count",
    ]

    df.drop(drop_columns, axis=1, inplace=True)
    df['original_title'] = df['original_title'].fillna(df['title'])
    
    # Convert the authors column to be a proper list of strings
    df["authors"] = df["authors"].apply(eval)
    df["authors_2"] = df["authors_2"].apply(eval)
    df["genres"] = df["genres"].apply(eval)
    
    




if __name__ == "__main__":
    main()
