from pydantic import BaseModel
from typing import Optional
from datetime import date

class StudentPost(BaseModel):
    a_no:str
    name:str
    gender:str
    dob:date
    phone:str
    address:str
    c_id:int
    sec_id:int

class Student(BaseModel):
    a_no:Optional[str]=None
    name:Optional[str]=None
    gender:Optional[str]=None
    dob:Optional[date]=None
    phone:Optional[str]=None
    address:Optional[str]=None
    c_id:Optional[int]=None
    sec_id:Optional[int]=None

class Section(BaseModel):
    sec_id:Optional[int]=None
    sec_name:Optional[str]=None
    c_id:Optional[int]=None

class Subject(BaseModel):
    sub_id:Optional[int]=None
    sub_name:Optional[str]=None
    teach_id:Optional[int]=None

class Teachers(BaseModel):
    teach_id:Optional[int]=None
    teach_name:Optional[str]=None
    phone:Optional[str]=None
    email:Optional[str]=None
    join_date:Optional[str]=None

class attendance(BaseModel):
    s_id:int
    a_date:date
    status:str
