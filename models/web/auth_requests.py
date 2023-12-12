from pydantic import BaseModel


class login_request(BaseModel):
    ''' login http request model '''

    username: str
    password: str


class signup_request(BaseModel):
    ''' signup http request model '''

    full_name: str
    username: str
    reg_type: str
    center_name: str
    grade: str
    password: str
    phone_number: str
    parent_phone_number: str
    email: str
