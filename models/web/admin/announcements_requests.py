from pydantic import BaseModel


class add_announcement_request(BaseModel):
    ''' add announcement admin api http request model '''

    announcement_desc_en: str
    announcement_desc_ar: str
    announcement_link: str
    announcement_datetime: str


class delete_announcement_request(BaseModel):
    ''' delete announcement admin api http request model '''

    announcement_ids: list[int]
