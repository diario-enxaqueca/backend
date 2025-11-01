from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class UserUpdate(BaseModel):
    nome: Optional[constr(min_length=3, max_length=100)] = None
    email: Optional[EmailStr] = None
    senha: Optional[constr(min_length=8, max_length=72)] = None
