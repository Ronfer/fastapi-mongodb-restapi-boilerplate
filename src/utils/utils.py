import datetime

# from passlib.context import CryptContext
from bson.objectid import ObjectId

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
curr_time = datetime.datetime.now()


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# def hash(password: str): 
#     return pwd_context.hash(password)

# def verify_pwd(plain_pwd, hashed_pwd):
#     return pwd_context.verify(plain_pwd, hashed_pwd)