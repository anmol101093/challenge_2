"""
This module contains pydantic validation models.
"""
from enum import Enum
from typing import List
from pydantic import BaseModel
 
 
class Status(str, Enum):
    failure = "failure"
    success = "success"
 
 
class HealthCheckResponse(BaseModel):
    status: Status
    message: str
 
 
class SearchModel(BaseModel):
    depth_min: float
    depth_max: float