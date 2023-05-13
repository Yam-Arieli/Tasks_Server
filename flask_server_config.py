from flask_restful import reqparse
from bson.objectid import ObjectId
from datetime import datetime



# -----------------------------------------------------------------
# EMPLOYEES

EMPLOYEES_POST_PARSER = reqparse.RequestParser()
EMPLOYEES_POST_PARSER.add_argument('first name', type=str, help='first name is required', required=True)
EMPLOYEES_POST_PARSER.add_argument('last name', type=str, help='last name is required', required=True)
EMPLOYEES_POST_PARSER.add_argument('email', type=str, help='email is required', required=True)
EMPLOYEES_POST_PARSER.add_argument('password', type=str, help='email is required', required=True)
EMPLOYEES_POST_PARSER.add_argument('role', type=str, help='role is required', required=True)

EMPLOYEES_GET_PARSER = reqparse.RequestParser()
EMPLOYEES_GET_PARSER.add_argument('first name', type=str, required=False)
EMPLOYEES_GET_PARSER.add_argument('last name', type=str, required=False)
EMPLOYEES_GET_PARSER.add_argument('email', type=str, required=False)
EMPLOYEES_GET_PARSER.add_argument('_id', type=str, required=False)
EMPLOYEES_GET_PARSER.add_argument('role', type=str, required=False)
EMPLOYEES_GET_PARSER.add_argument('created', type=str, required=False)
EMPLOYEES_GET_PARSER.add_argument('last update', type=str, required=False)

EMPLOYEES_PUT_PARSER = reqparse.RequestParser()
EMPLOYEES_PUT_PARSER.add_argument('email', type=str, help='email is required', required=True)
EMPLOYEES_PUT_PARSER.add_argument('password', type=str, help='password is required', required=True)
EMPLOYEES_PUT_PARSER.add_argument('update', type=dict, help='update is required', required=True)

# EMPLOYEES_DELETE_PARSER = reqparse.RequestParser()
# EMPLOYEES_DELETE_PARSER.add_argument('_id', type=str, help='_id is required', required=True)
# EMPLOYEES_DELETE_PARSER.add_argument('update', type=dict, default={})

# -----------------------------------------------------------------
# TASKS
TASK_GET_PARSER = reqparse.RequestParser()
TASK_GET_PARSER.add_argument('filter', type=dict)
TASK_GET_PARSER.add_argument('projection', type=dict)


TASK_POST_PARSER = reqparse.RequestParser()
TASK_POST_PARSER.add_argument('email', type=str, help='email is required', required=True)
TASK_POST_PARSER.add_argument('password', type=str, help='password is required', required=True)
TASK_POST_PARSER.add_argument('activity', type=str, help='activity is required', required=True)
TASK_POST_PARSER.add_argument('responsible', type=str,
                           help='the email of the responsible (the person who is in charge of this task) is required', required=True)
TASK_POST_PARSER.add_argument('deadline', type=str)
TASK_POST_PARSER.add_argument('comments', type=list, default=[])


TASK_PUT_PARSER = reqparse.RequestParser()
TASK_PUT_PARSER.add_argument('filter', type=dict, default={})
TASK_PUT_PARSER.add_argument('update', type=dict, default={})

# -----------------------------------------------------------------
# COMMENTS
COMMENTS_GET_PARSER = reqparse.RequestParser()
EMPLOYEES_GET_PARSER.add_argument('_id', type=str, required=False)
EMPLOYEES_GET_PARSER.add_argument('title', type=str, required=False)
EMPLOYEES_GET_PARSER.add_argument('employee details', type=str, required=False)
EMPLOYEES_GET_PARSER.add_argument('last update', type=str, required=False)


COMMENTS_POST_PARSER = reqparse.RequestParser()
COMMENTS_POST_PARSER.add_argument('email', type=str, help='email is required', required=True)
COMMENTS_POST_PARSER.add_argument('password', type=str, help='password is required', required=True)
COMMENTS_POST_PARSER.add_argument('task_id', type=str, help='task_id is required', required=True)
COMMENTS_POST_PARSER.add_argument('title', type=str, help='title is required', required=True)
COMMENTS_POST_PARSER.add_argument('content', type=str, help='content is required', required=True)


COMMENTS_DELETE_PARSER = reqparse.RequestParser()
COMMENTS_DELETE_PARSER.add_argument('_id', type=str, help='_id is required', required=True)
COMMENTS_DELETE_PARSER.add_argument('update', type=dict, default={})



def array_of_obj_to_json_ser(ar: list):
    new = [str(obj) for obj in ar]
    return new

def convert_emp_to_json_ser(emp: dict):
    new = emp.copy()
    new.pop('password', None)
    
    new['_id'] = str(new['_id'])
    new['created'] = str(new['created'])
    new['last update'] = str(new['last update'])
    new['comments'] = array_of_obj_to_json_ser(new['comments'])
    
    if 'tasks created' in new:
        new['tasks created'] = array_of_obj_to_json_ser(new['tasks created'])
    
    if 'tasks responsible' in new:
        new['tasks responsible'] = array_of_obj_to_json_ser(new['tasks responsible'])
    
    return new

def fix_get_args(args: dict) -> dict:
    args = {k: args[k] for k in args if args[k]}
    
    if '_id' in args:
        args['_id'] = ObjectId(args['_id'])
    if 'created' in args:
        args['created'] = datetime.strptime(args['created'], r'%Y-%m-%dT%H:%M:%S.%f%z')
    if 'last update' in args:
        args['last update'] = datetime.strptime(args['last update'], r'%Y-%m-%dT%H:%M:%S.%f%z')
    
    return args