"""Response model"""
from typing import Any

from pydantic import BaseModel, StrictBool, StrictInt


class Response(BaseModel):
    success: StrictBool = True
    status_code: StrictInt
    data: dict[Any, Any]
