from pydantic import BaseModel


class add_lecture_request(BaseModel):
    ''' add lecture admin api http request model '''

    lec_name_en: str
    lec_name_ar: str
    lec_desc_en: str
    lec_desc_ar: str
    thumbnail: str
    duration: float
    price: float


class update_lecture_request(BaseModel):
    ''' update lecture admin api http request model '''

    lec_id: int
    lec_name_en: str
    lec_name_ar: str
    lec_desc_en: str
    lec_desc_ar: str
    thumbnail: str
    duration: float
    price: float


class delete_lectures_request(BaseModel):
    ''' remove lectures list admin api http request '''

    lec_ids: list[int]
