from pydantic import BaseModel


class get_user_info_request(BaseModel):
    ''' get user info admin api http request '''

    username: str


class lec_ownership_request(BaseModel):
    ''' remove lecture ownership admin api http request '''

    user_id: int
    lecture_id: int


class delete_user_request(BaseModel):
    ''' remove user admin api http request '''

    username: str


class delete_users_request(BaseModel):
    ''' remove users list admin api http request '''

    username_list: list[str]


class get_owned_lectures_request(BaseModel):
    ''' get ownded lectures admin api http request '''

    user_id: int


class update_user_request(BaseModel):
    ''' update user admin api http request model '''

    full_name: str
    username: str
    reg_type: str
    center_name: str
    grade: int
    password: str
    is_password_changed: bool
    phone_number: str
    parent_phone_number: str
    email: str

    user_role: str
    balance: float
