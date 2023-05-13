from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv())

# Change to your own mongodb path
CONNECTION_MONGODB = 'mongodb://localhost:27017'
mongo_client = MongoClient(CONNECTION_MONGODB)
db = mongo_client.Tasks_Manager


mng_tasks = db.tasks
mng_employees = db.employees
mng_comments = db.comments