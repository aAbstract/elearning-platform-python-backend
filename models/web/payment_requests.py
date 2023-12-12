from pydantic import BaseModel


class make_payment_request(BaseModel):
    ''' make payment http request '''

    lecture_id: int


class recharge_balance_request(BaseModel):
    ''' recharge balance http request '''

    coupon: str
