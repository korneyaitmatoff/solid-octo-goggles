"""Response model"""

from pydantic import BaseModel, StrictStr


class Task(BaseModel):
    name: StrictStr
