import os
import pandas as pd
import psycopg

from surprise import Dataset, dump, Reader, SVD

from config import settings


def build_model():
    print("Loading data from database")
    rating_df = pd.read_sql_table(
        table_name="rating", con=settings.database_url,
        columns=["user_id", "book_id", "score"]
    )
    print("Loading ratings into a surprise Dataset")

    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(rating_df, reader)
    print("Data load complete")

    # Train the algorithm
    print("Training the algorithm.")
    trainset = data.build_full_trainset()
    algo = SVD(verbose=True)
    algo.fit(trainset)

    print("Done.")

    return algo


if __name__ == "__main__":
    model = build_model()
    dump.dump("data/svd_model.dump", algo=model)
