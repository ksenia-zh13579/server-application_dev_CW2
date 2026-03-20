from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(gt=0, default=18)
    is_subscribed: bool = False