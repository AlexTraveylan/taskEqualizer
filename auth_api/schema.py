
from pydantic import BaseModel, Field

class RegisterCreateSchema(BaseModel):

    family_name: str = Field(min_lenght=5, max_length=100)
    description: str = Field(min_lenght=5, max_length=1000)
    username: str = Field(min_lenght=5, max_length=100)
    password: str = Field(min_lenght=5, max_length=100)


class RegisterInviteSchema(BaseModel):

    username: str = Field(min_lenght=5, max_length=100)
    password: str = Field(min_lenght=5, max_length=100)
    invitation_code: str = Field(min_lenght=5, max_length=10)