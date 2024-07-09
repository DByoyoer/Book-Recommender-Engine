# Book Recommender API

Author: Michael Morikawa

Description: Python REST API that serves as the backend to the companion
mobile app which can be found at https://github.com/DByoyoer/Book_Recommender_App. 
The API is live and currently hosted at https://bookrec.azurewebsites.net/

Functionality: Basic API documentation can be found 
[here]( https://bookrec.azurewebsites.net/docs).

## Setup
The API can be run locally for development purposes with some setup. It is not super clean process but it is possible.

### Requirements: 
- Due to the use of Pandas and Scikit-Surpise it is strongly recommended to use Conda as the environment manager. 
- Docker and Docker Compose
- psql to execute the import commands used in the setup script
- Bash to run the setup script

### Steps
1. Clone this repository via `git clone git@github.com:DByoyoer/Book-Recommender-Engine.git`


2. Navigate to where you cloned the repository and run `conda env create -f environment.yml` and then activate the environment `conda activate capstone`

3. Run `mkdir app/data` and download `svd_model.dump` from this [dropbox]( https://www.dropbox.com/scl/fi/czhm9o10qslz3hk7rabbe/svd_model.dump?rlkey=82ykbm9b0ph9lznldw0mn8ap3&st=swysqklc&dl=0) and put the file in the `app/data` directory. This is a workaround to issues with the first time launch of the API docker container requiring the model to work. 

4. Change directories to the app directory `cd Book-Recommender-Engine/app`

5. Run `docker compose up` to start up the API with an empty Postgresql database

6. In a seperate session run the setup script `bash setup_database.sh`. This will download the starter data used for this project, process files to allow for easy bulk insertion to the database and then load the data into the database running in the docker container.

7. The data should now be loaded. This can be checked by going to `localhost:8000/docs` in the browser to view the interactive docs and testing by trying out the various endpoints.
