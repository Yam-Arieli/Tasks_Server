from datetime import datetime
from flask import Flask
from flask_restful import Resource, Api
from flask_server_config import *
from mongo_conn import *

app = Flask(__name__)
api = Api(app)

# when using parse_args() it returns args
# args become an variable that bond to the parser
# therfore it immutable
# mongodb add '_id' value to the dict it's get
# so we have to send a copy of the args
# and not the args themself

class Employees(Resource):
    def post(self):
        args = EMPLOYEES_POST_PARSER.parse_args()
        args_copy = args.copy()
        
        email = args_copy['email']
        if mng_employees.find_one({'email': email}):
            # TODO: fix it as an error (now it return code 200)
            return {'code': 409, 'error': 'This email is taken'}
        else:
            now = datetime.now()
            args_copy['created'] = now
            args_copy['last update'] = now
            args_copy['comments'] = []
            mng_employees.insert_one(args_copy)
            
            return {'code': 200}
    
    def put(self):
        args = EMPLOYEES_PUT_PARSER.parse_args()
        
        # check if email and password recived
        email, password = args['email'], args['password']
        
        # check if this employee exit in the database
        if not mng_employees.find_one({'email': email, 'password': password}):
            return {'code': 0, 'error': 'email and password are wrong'}
        
        update = args['update'].copy()
        update['last update'] = datetime.now()
        
        result = mng_employees.update_one({'email': email, 'password': password}, {'$set': update})
        return {'code': 200}
    
    def get(self):
        args = EMPLOYEES_GET_PARSER.parse_args().copy()
        args = fix_get_args(args)
        
        cursor = mng_employees.find(args, {'password': False})
        emp_list = list(cursor)
        
        emp_list = [convert_emp_to_json_ser(emp_doc) for emp_doc in emp_list]
        
        return {'code': 200, 'result': emp_list}



api.add_resource(Employees, '/Tasks_Manager/Employees')
# -----------------------------------------------------------------

class Tasks(Resource):
    def post(self):
        args = TASK_POST_PARSER.parse_args()
        
        # check if email and password recived
        email, password = args['email'], args['password']
        
        # check if this employee exit in the database
        if not (creator := mng_employees.find_one({'email': email, 'password': password})):
            return {'code': 0, 'error': 'email and password are wrong'}
        
        # check if this responsible exists in the database
        if not (responsible := mng_employees.find_one({'email': args['responsible']})):
            return {'code': 0, 'error': 'email and password are wrong'}
        
        # ------------------------------------------------------------------------
        
        task_data = {
            'activity': args['activity'], 'deadline': args['deadline'],
            'creator': creator['_id'], 'responsible': args['responsible'],
            'comments': [], 'created': datetime.now(), 'last update': datetime.now()
            }
        
        result = mng_tasks.insert_one(task_data)
        
        # update employee created
        mng_employees.update_one({'_id': creator['_id']}, {'$push': {'tasks created': result.inserted_id}})
        # update employee responsible
        mng_employees.update_one({'_id': responsible['_id']}, {'$push': {'tasks responsible': result.inserted_id}})
        
        return {'code': 200, 'task_id': str(result.inserted_id)}
    
    def get(self):
        args = TASK_GET_PARSER.parse_args().copy()
        args = fix_get_args(args)
        
        cursor = mng_tasks.find(args)
        c_list = list(cursor)
        
        for d in c_list:
            d['_id'] = str(d['_id'])
        
        return {'code': 200, 'result': c_list}
    
    def put(self):
        args = TASK_PUT_PARSER.parse_args()
        result = mng_tasks.update_many(args['filter'], args['update'])
        return {'code': 200, 'matched_count': result.matched_count, 'modified_count': result.modified_count}
    
    # TODO: def delete


api.add_resource(Tasks, '/Tasks_Manager/Tasks')
# -----------------------------------------------------------------
class Comments(Resource):
    def post(self):
        """
        updates/creates 3 docs:
            1) updates employee's comments list
            2) updates task's comments list
            3) creates comment doc

        Returns:
            _type_: _description_
        """
        args = COMMENTS_POST_PARSER.parse_args()
        
        # check if email and password recived
        email, password = args['email'], args['password']
        # check if this employee exists in the database
        if not (employee := mng_employees.find_one({'email': email, 'password': password})):
            return {'code': 0, 'error': 'email and password are wrong'}
        
        # check if task_id recived
        task_id = ObjectId(args['task_id'])
        # check if this task exists in the database
        if not (employee := mng_tasks.find_one({'_id': task_id})):
            return {'code': 0, 'error': 'task_id is wrong'}
        
        # ---------------------------------------------------------------------------------
        # creates comment doc
        emp_details = {'_id': employee['_id']}
        document = {'title': args['title'], 'content': args['content'], 'employee details': emp_details, 'created': datetime.now()}
        result = mng_comments.insert_one(document)
        
        # update task
        mng_tasks.update_one({'_id': task_id}, {'$push': {'comments': result.inserted_id}})
        
        # update employee
        mng_employees.update_one({'email': email, 'password': password}, {'$push': {'comments': result.inserted_id}})
        
        return {'code': 200}
    
    def get(self):
        args = COMMENTS_GET_PARSER.parse_args().copy()
        args = fix_get_args(args)
        
        cursor = mng_comments.find(args)
        c_list = list(cursor)
        
        for d in c_list:
            d['_id'] = str(d['_id'])
            d['employee details'] = str(d['employee details'])
            d['created'] = str(d['created'])
        
        return {'code': 200, 'result': c_list}


api.add_resource(Comments, '/Tasks_Manager/Comments')
# -----------------------------------------------------------------



if __name__ == '__main__':
    app.run(debug=True)