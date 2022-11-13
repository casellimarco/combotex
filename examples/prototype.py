from typing import Dict, Callable, Any, List

import pylatex
from pylatex import Document, Section, Enumerate, NewPage, LongTable
from combotex import Question

def question_text_1(doc: pylatex.Document, parameters: Dict[str, Any], choices: List[Any]):
    with doc.create(Section('Question 1', numbering=False)):
        doc.append(f'{parameters["a"]} + {parameters["b"]} = ' )
        with doc.create(Enumerate()) as enum:
            for choice in choices:
                enum.add_item(choice)

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
    ]
)
    
def question_text_2(doc: pylatex.Document, parameters: Dict[str, str], choices: List[str]):
    with doc.create(Section('Question 2', numbering=False)):
        doc.append(f'{parameters["a"]} x {parameters["b"]} = ' )
        with doc.create(Enumerate()) as enum:
            for choice in choices:
                enum.add_item(choice)

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
    ]
)


def generate_combinations(doc, questions, num_combinations):
    table = []
    for i in range(num_combinations):
        row = [i]
        doc.append(f"Id: {i}")
        for question in questions:
            row.append(question.append_random(doc))
        table.append(row)
        doc.append(NewPage())
    return table
            

if __name__ == '__main__':
    # Basic document
    doc = Document('basic', page_numbers=False)
    questions = [question_1, question_2]
    table = generate_combinations(doc, questions, num_combinations=4)
    # Generate data table
    with doc.create(Section("Answers' table", numbering=False)):
        with doc.create(LongTable("l l l")) as data_table:
            data_table.add_hline()
            data_table.add_row(["ID", "Q1", "Q2"])
            data_table.add_hline()
            for row in table:
                data_table.add_row(row)
                data_table.add_hline()
    doc.generate_pdf(clean_tex=False)
