# backend/src/domains/auth/schemas.py
from pydantic import BaseModel

# # Skema untuk token yang akan dikirim kembali ke klien saat login berhasil.
class Token(BaseModel):
    access_token: str
    token_type: str

# # Skema untuk data yang akan disandikan di dalam JWT.
class TokenData(BaseModel):
    username: str | None = None
