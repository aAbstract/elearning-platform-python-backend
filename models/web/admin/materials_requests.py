from pydantic import BaseModel


class add_vid_doc_request(BaseModel):
    ''' add video or document admin api http request model '''

    linked_lec_id: int
    mat_type: str
    mat_order: int
    mat_name_en: str
    mat_name_ar: str
    mat_link: str


class mat_type_map(BaseModel):
    is_quiz: bool
    mat_id: int


class delete_materials_request(BaseModel):
    ''' remove materials admin api http request model '''

    items: list[mat_type_map]


class update_vid_doc_request(BaseModel):
    ''' update video or document admin api http request model '''

    mat_id: int
    linked_lec_id: int
    mat_type: str
    mat_order: int
    mat_name_en: str
    mat_name_ar: str
    mat_link: str


class quiz_answer(BaseModel):
    question_order: int
    question_answer: str


class update_quiz_request(BaseModel):
    ''' update quiz admin api http request '''

    mat_id: int
    linked_lec_id: int
    mat_type: str
    mat_order: int
    mat_name_en: str
    mat_name_ar: str
    mat_link: str
    quiz_answers: list[quiz_answer]


class add_quiz_request(BaseModel):
    ''' add quiz admin api http request model '''

    linked_lec_id: int
    mat_type: str
    mat_order: int
    mat_name_en: str
    mat_name_ar: str
    mat_link: str
    quiz_answers: list[quiz_answer]
