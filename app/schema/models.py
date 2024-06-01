from pydantic import BaseModel
from typing import (
    List, 
    Dict, 
    Any, 
    Optional
    )

class Notification(BaseModel):
    type: str
    data: Dict[str, Any]

class User(BaseModel):
    fb_id: str
    name: str
    last_name: str
    email_id: str
    about: Optional[str] = None
    notifications: Optional[List[Notification]] = []
    friends_list: Optional[List[Dict[str, str]]] = []
    chat_rooms_joined: Optional[List[Dict[str, str]]] = []
    chat_rooms_created: Optional[List[Dict[str, str]]] = []
    profile_pic: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    about: Optional[str] = None
    email_id: Optional[str] = None

class CreateUserResponse(BaseModel):
    user: User

class IsUserResponse(BaseModel):
    is_user:bool
    user:Optional[User] = None
