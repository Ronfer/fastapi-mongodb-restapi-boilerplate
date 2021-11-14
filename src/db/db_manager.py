import motor.motor_asyncio as motor


def connect_to_database(connection_string: str):
    try:
        client = motor.AsyncIOMotorClient(connection_string)
        print("Connected to MongoDB.")
        return client
    except Exception as error:
        print("Connection to the database failed!", error)