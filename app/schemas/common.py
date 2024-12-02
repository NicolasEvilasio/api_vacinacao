from datetime import time
from pydantic import BaseModel, field_validator
from enum import Enum


class Weekday(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    
class Schedule(BaseModel):
    start: time
    end: time
    weekday: Weekday
    
    @field_validator('end')
    @classmethod
    def end_must_be_after_start(cls, v: time, info) -> time:
        start = info.data.get('start')
        if start and v < start:
            raise ValueError('O horário final deve ser posterior ao horário inicial')
        return v


    def model_dump(self) -> dict:
        return {
            "start": self.start.strftime("%H:%M:%S"),
            "end": self.end.strftime("%H:%M:%S"),
            "weekday": self.weekday.value
        }