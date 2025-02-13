from crypt import methods
from flask import Blueprint,jsonify,make_response,request,abort
from app.models.task import Task 
from app import db
from datetime import datetime

tasks_bp = Blueprint('tasks_bp',__name__, url_prefix='/tasks')

@tasks_bp.route('',methods = ['GET'])
def get_all_tasks():
    sorted = request.args.get('sort')
    if sorted == 'asc':
        all_tasks = Task.query.order_by(Task.title.asc())
    elif sorted == 'desc':
        all_tasks = Task.query.order_by(Task.title.desc())
    else:
        all_tasks = Task.query.all()
    
    result = []
    for task in all_tasks:
        result.append(task.to_dict())
    return jsonify(result), 200

@tasks_bp.route('/<task_id>',methods = ['GET'])
def get_one_task(task_id):
    single_task = get_task_from_id(task_id)
    return jsonify({'task':single_task.to_dict()}), 200 


@tasks_bp.route('',methods = ['POST'])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(title = request_body['title'],
                    description = request_body['description'])
    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201

#helper function 
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({'msg':f'Invalid data type'}, 400))
    choosen_task = Task.query.get(task_id)

    if choosen_task is None:
        return abort(make_response({'msg':f'Cannot find provided task id {task_id}'}, 404))
    return choosen_task

@tasks_bp.route('<task_id>', methods = ['PUT'])
def update_one_task(task_id):
    request_body = request.get_json()
    single_task = get_task_from_id(task_id)
    single_task.title = request_body['title']
    single_task.description = request_body['description']
    db.sesssion.commit()
    return make_response(jsonify({'task':single_task.to_json()}),200)

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_a_task(task_id):
    task_to_delete = get_task_from_id(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({'details': f'Task {task_id} {task_to_delete.title} successfully deleted'}),200

@tasks_bp.route('/<task_id>/mark_incomplete', methods=['PATCH'])
def mark_task_incomplete(task_id):
    task = get_task_from_id(task_id)
    task.completed_at = None
    task.is_complete = False

    db.session.commit()
    return make_response(jsonify({'task': task.to_dict()}), 200)

@tasks_bp.route('/<task_id>/mark_complete', methods=['PATCH'])
def mark_task_complete(task_id):
    task = get_task_from_id(task_id)
    task.completed_at = datetime.now()
    task.is_complete = True

    db.session.commit()
    return make_response(jsonify({'task': task.to_dict()}), 200)


