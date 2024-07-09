-- Drop constraints for bulk loading of files

ALTER TABLE ONLY public.book_genre
    DROP CONSTRAINT pk_book_genre CASCADE;

ALTER TABLE ONLY public.book_author
    DROP CONSTRAINT pk_book_author CASCADE;

ALTER TABLE ONLY public.genre
    DROP CONSTRAINT pk_genre CASCADE;

ALTER TABLE ONLY public.rating
    DROP CONSTRAINT pk_rating CASCADE;

ALTER TABLE ONLY public.reading_list
    DROP CONSTRAINT pk_reading_list CASCADE;

ALTER TABLE ONLY public.top_recs
    DROP CONSTRAINT pk_top_recs CASCADE;

ALTER TABLE ONLY public."user"
    DROP CONSTRAINT pk_user CASCADE;

ALTER TABLE ONLY public.author
    DROP CONSTRAINT pk_author CASCADE;

ALTER TABLE ONLY public.book
    DROP CONSTRAINT pk_book CASCADE;

DROP INDEX ix_top_recs_prediction;

-- =====================================================================================================================
-- Loading csv data

\COPY public.book FROM 'data/books.csv' WITH CSV HEADER;

\COPY public.author FROM 'data/authors.csv' WITH CSV HEADER;

\COPY public.genre FROM 'data/genres.csv' WITH CSV HEADER;

\COPY public."user" FROM 'data/users.csv' WITH CSV HEADER;

\COPY public.book_genre FROM 'data/book_genres.csv' WITH CSV HEADER;

\COPY public.book_author FROM 'data/book_authors.csv' WITH CSV HEADER;

\COPY public.reading_list FROM 'data/reading_list.csv' WITH CSV HEADER;

\COPY public.rating from 'data/ratings.csv' WITH CSV HEADER;

-- =====================================================================================================================
-- Re-add the constraints

ALTER TABLE ONLY public.author
    ADD CONSTRAINT pk_author PRIMARY KEY (id);


--
-- Name: book pk_book; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.book
    ADD CONSTRAINT pk_book PRIMARY KEY (id);


--
-- Name: book_author pk_book_author; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT pk_book_author PRIMARY KEY (book_id, author_id);


--
-- Name: book_genre pk_book_genre; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT pk_book_genre PRIMARY KEY (book_id, genre_id);


--
-- Name: genre pk_genre; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT pk_genre PRIMARY KEY (id);


--
-- Name: rating pk_rating; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT pk_rating PRIMARY KEY (user_id, book_id);


--
-- Name: reading_list pk_reading_list; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.reading_list
    ADD CONSTRAINT pk_reading_list PRIMARY KEY (user_id, book_id);


--
-- Name: top_recs pk_top_recs; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.top_recs
    ADD CONSTRAINT pk_top_recs PRIMARY KEY (user_id, book_id);


--
-- Name: user pk_user; Type: CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT pk_user PRIMARY KEY (id);


--
-- Name: ix_top_recs_prediction; Type: INDEX; Schema: public; Owner: myuser
--

CREATE INDEX ix_top_recs_prediction ON public.top_recs USING btree (prediction);


--
-- Name: book_author fk_book_author_author_id_author; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT fk_book_author_author_id_author FOREIGN KEY (author_id) REFERENCES public.author(id);


--
-- Name: book_author fk_book_author_book_id_book; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT fk_book_author_book_id_book FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: book_genre fk_book_genre_book_id_book; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT fk_book_genre_book_id_book FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: book_genre fk_book_genre_genre_id_genre; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT fk_book_genre_genre_id_genre FOREIGN KEY (genre_id) REFERENCES public.genre(id);


--
-- Name: rating fk_rating_book_id_book; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT fk_rating_book_id_book FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: rating fk_rating_user_id_user; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT fk_rating_user_id_user FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: reading_list fk_reading_list_book_id_book; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.reading_list
    ADD CONSTRAINT fk_reading_list_book_id_book FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: reading_list fk_reading_list_user_id_user; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.reading_list
    ADD CONSTRAINT fk_reading_list_user_id_user FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: top_recs fk_top_recs_book_id_book; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.top_recs
    ADD CONSTRAINT fk_top_recs_book_id_book FOREIGN KEY (book_id) REFERENCES public.book(id);


--
-- Name: top_recs fk_top_recs_user_id_user; Type: FK CONSTRAINT; Schema: public; Owner: myuser
--

ALTER TABLE ONLY public.top_recs
    ADD CONSTRAINT fk_top_recs_user_id_user FOREIGN KEY (user_id) REFERENCES public."user"(id);

-- Fix sequence values
SELECT setval('user_id_seq', (SELECT max(id) from public."user"));
SELECT setval('book_id_seq', (SELECT max(id) from public.book));
SELECT setval('genre_id_seq', (SELECT max(id) from public.genre));
SELECT setval('author_id_seq', (SELECT max(id) from public.author));



