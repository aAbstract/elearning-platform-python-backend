from typing import Optional, Any
from pydantic import BaseModel


class database_api_response(BaseModel):
    ''' database api response object '''
    
    success: Optional[bool] = True
    msg: Optional[str] = ''
    record: Optional[Any] = []
