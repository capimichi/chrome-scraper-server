from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from chromescraperserver.Model.OperationMessage import OperationMessage


class TaskMessage(BaseModel):
    task_id: str
    operation: OperationMessage
    result: Optional[str] = None
    errors: Optional[List[str]] = None
    completed: bool = False

    def get_task_id(self):
        return self.task_id

    def set_task_id(self, task_id: str):
        self.task_id = task_id

    def get_operation(self):
        return self.operation

    def set_operation(self, operation: OperationMessage):
        self.operation = operation

    def get_result(self):
        return self.result

    def set_result(self, result: Optional[str]):
        self.result = result

    def get_errors(self):
        return self.errors

    def set_errors(self, errors: Optional[List[str]]):
        self.errors = errors

    def get_completed(self):
        return self.completed

    def set_completed(self, completed: bool):
        self.completed = completed