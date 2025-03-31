from datetime import datetime 

from pydantic import BaseModel

class LinkCreate(BaseModel):
    long_url: str
    create_dt: datetime
    expire_dt: datetime
    last_queried_dt: datetime
    user_id: str
