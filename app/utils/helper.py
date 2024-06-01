

def user_to_dict(user) -> dict:
    user_dict = user.copy()
    user_dict["_id"] = str(user_dict["_id"])
    return user_dict