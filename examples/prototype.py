from typing import Dict, Any
from combotex import Question, Exam

def question_text_1(parameters: Dict[str, Any]):
    return f'{parameters["a"]} + {parameters["b"]} = '

question_1 = Question(
    question_text_1,
    parameters = {
        "a": [0, 1, 2],
        "b": [3, 4, 5],
    },
    answers = [3, 5, 7],
    choices = [
        [0, 1, 3],
        [4, 5, 6],
        [7, 8, 9]
    ],
    question_name= "Question 1"
)

def question_text_2(parameters: Dict[str, str]):
    return f'{parameters["a"]} x {parameters["b"]} = ' 

question_2 = Question(
    question_text_2,
    parameters = {
        "a": [0, 1, 2],
        "b": [3, 4, 5],
    },
    answers = [0, 4, 10],
    choices = [
        [0, 1, 3],
        [4, 5, 6],
        [7, 8, 10]
    ],
    question_name= "Question 2"
)


if __name__ == '__main__':
    # Basic exam
    questions = [question_1, question_2]
    exam = Exam("basic", questions)
    exam.generate_exams(num_exams=4)
    
    # Generate all the combinations
    exam.check_answers()

    # Interactive marker
    exam.marker(correct_score=1, wrong_score=-1, missing_score=0)

