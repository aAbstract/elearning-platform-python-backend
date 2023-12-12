# E-Learning Platform Backend with Python and FastAPI

Welcome to my E-Learning Platform backend repository! This project serves as the backend for my Vue.js frontend, providing a robust foundation for my E-Learning Platform using FastAPI. Whether you're an educator or a learner, my backend ensures a secure and efficient learning experience.

## Features
1. **User Authentication**  
Implementing a secure user authentication system allows users to sign up, log in, and access personalized content with confidence.

2. **Course Management**  
Efficiently manage a diverse range of courses, including details such as descriptions, instructors, and ratings. Facilitate easy retrieval of course information for the frontend.

3. **Video Lectures**  
Serve interactive video lectures to users through a responsive backend, ensuring a smooth viewing experience on the frontend.

4. **Quizzes and Assessments**  
Implement a system for quizzes and assessments integrated into each course. Track user progress and provide instant feedback.

5. **Course Notes**  
Enable users to take and review course notes directly within the platform. Enhance the learning experience by providing personalized study materials.

## How to Run
```bash
pip install "fastapi[all]"
pip install mysql-connector-python
cd database && docker compose up -d
# connect to database and deploy ./database/design/schema_2.sql
python ./main.py
```
