from sqlmodel import Field, Relationship, SQLModel

class Message(SQLModel):
    message: str