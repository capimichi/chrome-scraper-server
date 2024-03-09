from typing import Optional, Dict, Any

from pydantic import BaseModel


class OperationMessage(BaseModel):
    operation: str
    arguments: Optional[Dict[str, Any]] = None

    def get_operation(self):
        return self.operation

    def set_operation(self, operation: str):
        self.operation = operation

    def get_arguments(self):
        return self.arguments

    def set_arguments(self, arguments: Optional[Dict[str, Any]]):
        self.arguments = arguments
