from flask import Blueprint, request, Response
from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_sort
from ..db import db
from datetime import date
import os
import requests

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

#Create a Task: Valid Task With null completed_at
@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

#Get Tasks: Getting Saved Tasks
@bp.get("")
def get_all_tasks():
    return get_models_with_sort(Task, request.args)

#Get One Task: One Saved Task
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.nested_category()

#Update Task
@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json") 

#Delete Task: Deleting a Task
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

#Mark Complete on an Incomplete Task
@bp.patch("/<task_id>/mark_complete")
def complete_an_incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.is_complete = True
    task.completed_at = date.today()
    db.session.commit()

    slack_token = os.environ.get("SLACK_API_TOKEN")
    slack_url = "https://slack.com/api/chat.postMessage"
    slack_headers = {"Authorization": f"Bearer {slack_token}"}
    slack_data = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(slack_url, headers=slack_headers, json=slack_data)

    return Response(status=204, mimetype="application/json") 

#Mark Incomplete on a Completed Task
@bp.patch("/<task_id>/mark_incomplete")
def incomplete_an_complete_task(task_id):
    task = validate_model(Task, task_id)

    task.is_complete = False
    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json") 