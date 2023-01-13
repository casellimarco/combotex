from typing import List
from dataclasses import dataclass, field

from pylatex import Document, Section, Enumerate, NewPage, LongTable, NoEscape, Package, NewLine
from collections import namedtuple

Scoring = namedtuple('Scoring', 'correct wrong missing')

def mark(guesses, answers, scoring):
    from colorama import Fore
    out = []
    score = 0
    if len(guesses) != len(answers):
        print(Fore.RED + f" --- WARNING: misalignement between guesses and answers: there are {len(guesses)} guesses and {len(answers)} answers." + Fore.RESET)
    for g, a in zip(guesses, answers):
        if g==a:
            out.append(Fore.GREEN + str(g))
            score += scoring.correct
        elif g in ["m", "M"]:
            out.append(Fore.YELLOW + str(g))
            score += scoring.missing
        else:
            out.append(Fore.RED + str(g))
            score += scoring.wrong
    out[-1] += Fore.RESET
    return " ".join(out), score  



@dataclass
class Exam:
    exam_name: str
    questions: List
    pre_questions: str = ""
    post_questions: str = ""
    table: List = None

    def generate_exams(self, num_exams, **kwargs):
        doc = self.generate_file(self.exam_name)
        self.generate_combinations(doc, num_combinations=num_exams)
        doc.generate_pdf(**kwargs)

    def check_answers(self, **kwargs):
        doc = self.generate_file(self.exam_name+"_check_answers")
        for question in self.questions:
            question.append_all_with_answers(doc)
            doc.append(NewPage())
        doc.generate_pdf(**kwargs)
    
    def generate_file(self, filename):
        doc = Document(filename, page_numbers=False)
        doc.packages.append(Package("amsmath"))
        doc.packages.append(Package("amsfonts"))
        return doc

    def generate_combinations(self, doc, num_combinations):
        table = []
        for i in range(num_combinations):
            row = [i]
            doc.append(rf"Id: {i}")
            doc.append(NewLine())
            doc.append(self.pre_questions)
            for question in self.questions:
                row.append(question.append_random(doc))
            table.append(row)
            doc.append(self.post_questions)
            doc.append(NewPage())
        self.table = table
    

    def marker(self, correct_score, wrong_score, missing_score):
        scoring = Scoring(correct=correct_score, wrong=wrong_score, missing=missing_score)
        print("Input the answers in order and space-separated. Use `m` or `M` for missing ones.")
        while True:
            print("ID ", end="")
            id = int(input())
            print("Answers: ", end="")
            answers = input().strip().split(" ")
            print ("\033[A                             \033[A")
            correct_answers = [str(a[0]) for a in  self.table[id][1:]]
            print("          index " + " ".join(map(str, range(1, len(correct_answers) +1))))
            print("Correct answers " + " ".join(correct_answers))
            student_answers, score = mark(answers, correct_answers, scoring)
            print("Student answers " + student_answers)
            print("  -----")
            print("Student score   " + str(score))
            print("")