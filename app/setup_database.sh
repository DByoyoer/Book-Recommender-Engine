#! /bin/bash

goodbooks_dir="data/good_books_10k_extended"

echo "Downloading Goodbooks-10k-Extended Data"
mkdir $goodbooks_dir

goodbooks_files=("books_enriched.csv" "ratings.csv" "to_read.csv")
export PGPASSWORD="mypassword"
export DATABASE_URL='postgresql+psycopg://myuser:mypassword@localhost:5432/mydatabase'

for file in "${goodbooks_files[@]}"
do
  wget -P data/good_books_10k_extended https://raw.githubusercontent.com/malcolmosh/goodbooks-10k-extended/master/$file
done

python prep_database_files.py

psql -h localhost -p 5432 -U myuser -d mydatabase -f populate_data.sql


