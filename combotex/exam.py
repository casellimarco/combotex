from typing import List
from dataclasses import dataclass, field

from pylatex import Document, Section, Enumerate, NewPage, LongTable, NoEscape, Package


def mark(guesses, answers):
    from colorama import Fore
    out = []
    for g, a in zip(guesses, answers):
        if g==a:
            out.append(Fore.GREEN + str(g))
        else:
            out.append(Fore.RED + str(g))
    out[-1] += Fore.RESET
    return " ".join(out)  



@dataclass
class Exam:
    exam_name: str
    questions: List
    table: List = None

    def generate_exams(self, num_exams):
        doc = self.generate_file(self.exam_name)
        self.generate_combinations(doc, num_combinations=num_exams)
        doc.generate_pdf()

    def check_answers(self):
        doc = self.generate_file(self.exam_name+"check_answers")
        for question in self.questions:
            question.append_all_with_answers(doc)
            doc.append(NewPage())
        doc.generate_pdf()
    
    def generate_file(self, filename):
        doc = Document(filename, page_numbers=False)
        doc.packages.append(Package("amsmath"))
        doc.packages.append(Package("amsfonts"))
        return doc

    def generate_combinations(self, doc, num_combinations):
        table = []
        for i in range(num_combinations):
            row = [i]
            doc.append(f"Id: {i}")
            for question in self.questions:
                row.append(question.append_random(doc))
            table.append(row)
            doc.append(NewPage())
        self.table = table
    

    def marker(self):
        while True:
            print("ID ", end="")
            id = int(input())
            print("Answers: ", end="")
            answers = input().split(" ")
            print ("\033[A                             \033[A")
            correct_answers = [str(a[0]) for a in  self.table[id][1:]]
            print("          index " + " ".join(map(str, range(1, len(correct_answers) +1))))
            print("Correct answers " + " ".join(correct_answers))
            print("Student answers " + mark(answers, correct_answers))
            print("")