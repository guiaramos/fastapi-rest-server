from .connection import db
from ...models import users as user_models

userRepo = db.users


#  create_one creates one User on DB
def create_one(user: user_models.UserInDB):
    # if has attr id, deletes before insert on db
    if hasattr(user, 'id'):
        delattr(user, 'id')

    # inserts on db
    ret = userRepo.insert_one(user.dict(by_alias=True))

    # add the generated id
    user.id = str(ret.inserted_id)

    return user
