from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] 
    is_complete : Mapped[Optional[bool]] 
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        if self.completed_at:
            task_as_dict["completed_at"] = self.completed_at
        if self.is_complete:
            task_as_dict["is_complete"] = self.is_complete
        else:
            task_as_dict["is_complete"] = False

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id

        return task_as_dict
    
    def nested_category(self):
        updated_task_as_dict = {}
        updated_task_as_dict["task"] = self.to_dict()
        return updated_task_as_dict

    
    @classmethod
    def from_dict(cls, task_data):
        goal_id = task_data.get("goal_id")

        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at", None),
            is_complete=task_data.get("is_complete", False),
            goal_id=goal_id
        )

        return new_task