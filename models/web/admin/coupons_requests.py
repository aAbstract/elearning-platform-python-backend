from pydantic import BaseModel


class gen_coupon_list_request(BaseModel):
    ''' generate coupon list admin http request '''

    coupons_list_count: int
    coupons_value: float


class delete_coupons_list_request(BaseModel):
    ''' remove coupons list admin http request '''

    coupons_list: list[str]
