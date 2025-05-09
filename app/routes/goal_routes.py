from flask import Blueprint, request, Response
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model, get_models_with_sort
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

#Create a Goal: Valid Goal
@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

#Get Goals: Getting Saved Goals
@bp.get("")
def get_all_goals():
    return get_models_with_sort(Goal, request.args)

#Get One Goal: One Saved Goal
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.nested_category()

#Update Goal
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return Response(status=204, mimetype="application/json") 

#Delete Goal: Deleting a Goal
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

#Sending a List of Task IDs to a Goal
@bp.post("/<goal_id>/tasks")
def create_tasks_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    for task in goal.tasks:  #Add this to pass the test test_post_task_ids_to_goal_already_with_goals
        task.goal_id = None

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        if task.goal_id is None:
            task.goal_id = goal.id

    db.session.commit()
    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200

#Getting Tasks of One Goal
@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = [task.to_dict() for task in goal.tasks]
    response = goal.to_dict()
    response["tasks"] = tasks
    return response