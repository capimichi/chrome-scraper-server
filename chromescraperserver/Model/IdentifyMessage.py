from pydantic import BaseModel


class IdentifyMessage(BaseModel):
    type: str

    def get_type(self):
        return self.type

    def set_type(self, type: str):
        self.type = type
