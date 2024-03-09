from typing import List

from pydantic import BaseModel

from chromescraperserver.Model.OperationMessage import OperationMessage


class ResponseMessage(OperationMessage):
    result: str
    errors: List[str] = []

    def get_result(self):
        return self.result

    def set_result(self, result: str):
        self.result = result

    def get_errors(self):
        return self.errors

    def set_errors(self, errors: List[str]):
        self.errors = errors