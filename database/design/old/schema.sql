
CREATE TABLE coupons
(
  coupon_id    SERIAL     NOT NULL,
  coupon_text  VARCHAR(8) NOT NULL,
  coupon_value FLOAT      NOT NULL,
  PRIMARY KEY (coupon_id)
);

CREATE TABLE documents
(
  document_id      SERIAL          NOT NULL,
  lecture_id       BIGINT UNSIGNED NOT NULL,
  document_name_en VARCHAR(100)    NOT NULL,
  document_name_ar VARCHAR(100)    NOT NULL,
  document_link    VARCHAR(500)    NOT NULL,
  PRIMARY KEY (document_id)
);

CREATE TABLE lectures
(
  lecture_id      SERIAL        NOT NULL,
  lecture_name_en VARCHAR(100)  NOT NULL,
  lecture_name_ar VARCHAR(100)  NOT NULL,
  lecture_desc_en VARCHAR(2000) NOT NULL,
  lecture_desc_ar VARCHAR(2000) NOT NULL,
  thumbnail_img   VARCHAR(100)  NOT NULL,
  price           FLOAT         NOT NULL,
  duration        FLOAT         NULL    ,
  PRIMARY KEY (lecture_id)
);

CREATE TABLE payment_logs
(
  payment_log_id   SERIAL          NOT NULL,
  user_id          BIGINT UNSIGNED NOT NULL,
  lecture_id       BIGINT UNSIGNED NOT NULL,
  payment_log_text VARCHAR(4096)   NOT NULL,
  PRIMARY KEY (payment_log_id)
);

CREATE TABLE quiz_answers
(
  quiz_answer_id SERIAL          NOT NULL,
  quiz_id        BIGINT UNSIGNED NOT NULL,
  question_order INT UNSIGNED    NOT NULL,
  answer_char    CHAR            NOT NULL,
  PRIMARY KEY (quiz_answer_id)
);

CREATE TABLE quizzes
(
  quiz_id       SERIAL          NOT NULL,
  lecture_id    BIGINT UNSIGNED NOT NULL,
  quiz_name_en  VARCHAR(100)    NOT NULL,
  quiz_name_ar  VARCHAR(100)    NOT NULL,
  quiz_doc_link VARCHAR(500)    NULL    ,
  PRIMARY KEY (quiz_id)
);

CREATE TABLE users
(
  user_id             SERIAL       NOT NULL,
  full_name           VARCHAR(50)  NOT NULL,
  username            VARCHAR(50)  NOT NULL,
  pass_hash           VARCHAR(128) NOT NULL,
  user_role           VARCHAR(50)  NOT NULL,
  phone_number        VARCHAR(15)  NOT NULL,
  parent_phone_number VARCHAR(15)  NOT NULL,
  email               VARCHAR(100) NOT NULL,
  balance             FLOAT        NOT NULL,
  reg_type            VARCHAR(100) NOT NULL,
  grade               INT UNSIGNED NOT NULL,
  center_name         VARCHAR(500) NOT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE users_lectures
(
  user_id    BIGINT UNSIGNED NOT NULL,
  lecture_id BIGINT UNSIGNED NOT NULL
);

CREATE TABLE videos
(
  video_id      SERIAL          NOT NULL,
  lecture_id    BIGINT UNSIGNED NOT NULL,
  video_name_en VARCHAR(100)    NOT NULL,
  video_name_ar VARCHAR(100)    NOT NULL,
  video_desc_en VARCHAR(2000)   NOT NULL,
  video_desc_ar VARCHAR(2000)   NOT NULL,
  video_link    VARCHAR(500)    NOT NULL,
  PRIMARY KEY (video_id)
);

ALTER TABLE documents
  ADD CONSTRAINT FK_lectures_TO_documents
    FOREIGN KEY (lecture_id)
    REFERENCES lectures (lecture_id);

ALTER TABLE quizzes
  ADD CONSTRAINT FK_lectures_TO_quizzes
    FOREIGN KEY (lecture_id)
    REFERENCES lectures (lecture_id);

ALTER TABLE videos
  ADD CONSTRAINT FK_lectures_TO_videos
    FOREIGN KEY (lecture_id)
    REFERENCES lectures (lecture_id);

ALTER TABLE users_lectures
  ADD CONSTRAINT FK_users_TO_users_lectures
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE users_lectures
  ADD CONSTRAINT FK_lectures_TO_users_lectures
    FOREIGN KEY (lecture_id)
    REFERENCES lectures (lecture_id);

ALTER TABLE quiz_answers
  ADD CONSTRAINT FK_quizzes_TO_quiz_answers
    FOREIGN KEY (quiz_id)
    REFERENCES quizzes (quiz_id);

ALTER TABLE payment_logs
  ADD CONSTRAINT FK_users_TO_payment_logs
    FOREIGN KEY (user_id)
    REFERENCES users (user_id);

ALTER TABLE payment_logs
  ADD CONSTRAINT FK_lectures_TO_payment_logs
    FOREIGN KEY (lecture_id)
    REFERENCES lectures (lecture_id);
