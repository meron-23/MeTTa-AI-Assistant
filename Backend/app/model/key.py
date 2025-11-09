from pydantic import BaseModel

class KeyModel(BaseModel):
    dek: str
    service_name: str
    userid: str   

class APIKeyIn(BaseModel):
    api_key: str
    service_name: str