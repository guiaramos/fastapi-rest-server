from .connection import db
from ...models import users as user_models


# user_coll is a collection for the users
user_coll = db.users


#  create_one creates one User on DB
def create_one(collection: db.users, user: user_models.UserInDB):
    # if has attr id, deletes before insert on db
    if hasattr(user, 'id'):
        delattr(user, 'id')

    # inserts on db
    ret = collection.insert_one(user.dict(by_alias=True))

    # add the generated id
    user.id = str(ret.inserted_id)

    return user
