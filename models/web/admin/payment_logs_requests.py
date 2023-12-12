from pydantic import BaseModel


class delete_payment_logs_request(BaseModel):
    ''' delete payment logs admin api http request '''

    payment_log_ids: list[int]
