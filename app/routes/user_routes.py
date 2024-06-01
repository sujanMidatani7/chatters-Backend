import base64
from fastapi import APIRouter, HTTPException, UploadFile, File
from PIL import Image
import io
from typing import List, Optional, Dict, Any
from fastapi.responses import StreamingResponse
from app.config.db import DB
from app.schema.models import *
from app.utils.helper import *

router = APIRouter()

# Initialize DB instance
db_instance = DB()
users_collection = db_instance.get_collection("chatters_db", "users")

# Pydantic models and helper functions (as previously defined)

@router.post("/createUser", response_model=CreateUserResponse)
async def create_user(user: User):
    
    if users_collection.find_one({"fb_id": user.fb_id}):
        raise HTTPException(status_code=400, detail="User already exists")
    users_collection.insert_one(user.dict())
    return CreateUserResponse(user)


@router.get("/getUser", response_model=CreateUserResponse)
async def get_user(fb_id: str):
    user = users_collection.find_one({"fb_id": fb_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return CreateUserResponse(user)

@router.get("/isUser", response_model=IsUserResponse)
async def is_user(email: str):
    user = users_collection.find_one({"email_id": email})
    if user:
        return IsUserResponse(True, user=user)
    else:
        return IsUserResponse(False)

@router.put("/updateUser", response_model=CreateUserResponse)
async def update_user(fb_id: str, user_update: UserUpdate):
    result = users_collection.update_one({"fb_id": fb_id}, {"$set": user_update.dict(exclude_unset=True)})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return CreateUserResponse(get_user(fb_id))

@router.put("/updateUserPic")
async def update_user_pic(fb_id: str, file: UploadFile = File(...)):
    # Read the image file
    image = Image.open(file.file)
    buffered = io.BytesIO()
    image.save(buffered, format=image.format)
    
    # Convert the image to a base64 string
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # Update the user profile picture in the database
    result = users_collection.update_one({"fb_id": fb_id}, {"$set": {"profile_pic": img_str}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return await get_user_pic(fb_id)

@router.get("/getUserPic")
async def get_user_pic(fb_id: str):
    user = users_collection.find_one({"fb_id": fb_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    profile_pic = user.get("profile_pic", "")
    if not profile_pic:
        raise HTTPException(status_code=404, detail="Profile picture not found")
    
    # Decode the base64 string to binary data
    img_data = base64.b64decode(profile_pic)
    
    # Convert binary data to BytesIO stream
    img_stream = io.BytesIO(img_data)
    
    # Set appropriate headers for image streaming
    headers = {
        "Content-Disposition": f'inline; filename="{fb_id}.jpg"',
        "Content-Type": "image/jpeg"
    }
    
    return StreamingResponse(img_stream,status_code=200, media_type="image/jpeg", headers=headers)

@router.put("/updateNotifications")
async def update_notifications(fb_id: str, notifications: List[Notification]):
    new_notifications = [notification.dict() for notification in notifications]
    result = users_collection.update_one(
        {"fb_id": fb_id},
        {"$push": {"notifications": {"$each": new_notifications, "$position": 0}}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_collection.find_one({"fb_id": fb_id})
    return {"updated_notifications": user.get("notifications", [])}

@router.post("/addFriend")
async def add_friend(fb_id: str, friend_fb_id: str):
    user = users_collection.find_one({"fb_id": fb_id})
    friend = users_collection.find_one({"fb_id": friend_fb_id})
    if not user or not friend:
        raise HTTPException(status_code=404, detail="User or Friend not found")
    users_collection.update_one({"fb_id": fb_id}, {"$push": {"friends_list": {"friend_id": friend_fb_id, "name": friend["name"]}}})
    return {"status": "success"}

@router.delete("/removeFriend")
async def remove_friend(fb_id: str, friend_fb_id: str):
    user = users_collection.find_one({"fb_id": fb_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    result = users_collection.update_one({"fb_id": fb_id}, {"$pull": {"friends_list": {"friend_id": friend_fb_id}}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Friend not found")
    return {"status": "success"}

@router.get("/getFriends")
async def get_friends(fb_id: str)-> Dict[str, Any]:
    user = users_collection.find_one({"fb_id": fb_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"friends_list": user_to_dict(user).get("friends_list", [])}

@router.on_event("shutdown")
def shutdown_event():
    db_instance.close_connection()