# QuizMaster Application

## Backend
1. `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `./venv/Scripts/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Run the app: `flask run --debug`


## Frontend
1. `cd frontend`
2. Install the npm packages: `npm i`
3. Run the application: `npm run dev`

## Redis and Celery
1. `docker pull redis` Download the docker image.
2. `docker run --name redis-mad-2 -d redis -p 6379:6379` Run the docker container
3. `docker exec -it redis-mad-2 redis-cli` to access the redis cli
4. For celery: First `cd backend`
5. For celery on windows: `celery -A app:celery_app worker -l INFO -P solo`, on linux: `celery -A app:celery_app worker -l INFO`
6. Run Celery beat: `celery -A app:celery_app beat -l INFO`