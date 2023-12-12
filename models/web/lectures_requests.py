from pydantic import BaseModel


class get_lec_cont_request(BaseModel):
    ''' get lecture content http request model '''

    lec_id: int


class get_quiz_answers_request(BaseModel):
    ''' get quiz answers http request model '''

    quiz_id: int
