from crypt import methods
from flask import Blueprint,jsonify,make_response,request,abort
from app.models.task import Task 
from app import db

tasks_bp = Blueprint('tasks_bp',__name__, url_prefix='/tasks')

@tasks_bp.route('',methods = ['GET'])
def get_all_tasks():
    all_tasks = Task.query.all()
    result = []

    for task in all_tasks:
        result.append(task.to_dict())
    return jsonify(result), 200

def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({'msg':f'Invalid data type'}, 400))
    choosen_task = Task.query.get(task_id)

    if choosen_task is None:
        return abort(make_response({'msg':f'Cannot find provided task id {task_id}'}, 404))
    return choosen_task

@tasks_bp.route('<task_id>',methods = ['GET'])
def get_one_task(task_id):
    one_task = get_task_from_id(task_id)
    return jsonify({'task':one_task.to_json()}), 200 