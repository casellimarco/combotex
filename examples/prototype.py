from typing import Dict, Callable, Any, List

import pylatex
from pylatexenc import latexencode
from pylatex import Document, Section, Enumerate, NewPage, LongTable, NoEscape, Package
from combotex import Question

def question_text_1(doc: pylatex.Document, parameters: Dict[str, Any]):
    with doc.create(Section('Question 1', numbering=False)):
        doc.append(f'{parameters["a"]} + {parameters["b"]} = ' )
        doc.append(NoEscape(rf"\newline Questo \'e un esempio con un input copioincollato da latex ed un parametro dentro la formula \[3^5 +{parameters['a']}\]"))
        doc.append(NoEscape(r"""\`E dato il sistema lineare \[\begin{cases}x + 2y + 3z = 4\\x + z = 0\\kx + z = k^2-1\end{cases}\] dove $k \in \mathbb{R}$. Determina tutti e soli i valori di $k$ per cui il sistema ammette soluzioni.
    \begin{enumerate}
    \item $k \neq -1,\  1$
    \item $k \neq 1$
    \item $k = 0$
    \item $k \in \mathbb{R}$
    \item Il sistema non ha soluzione per alcun valore di $k \in \mathbb{R}$
    \end{enumerate}

Sapendo che $\vec{\beta}_1 = \begin{bmatrix}1\\1\\1\end{bmatrix}$ e $\vec{\beta}_2 = \begin{bmatrix}1\\0\\0\end{bmatrix}$ e che le coordinate di $\vec{v}$ rispetto alla base $\mathcal{B}$ sono date da $[\vec{v}]_{\mathcal{B}} = \begin{bmatrix}1\\2\\3\end{bmatrix}$, quale tra questi \`e $\vec{\beta}_3$?
    \begin{enumerate}
    \item $[-2/3,\ -1/3, \ 0]^T$
    \item $[-1/3,\ -2/3, \ 0]^T$
    \item $[1/3,\ 0,\ 2/3]^T$
    \item $[-1/3,\ 2/3,\ 0]^T$
    \item $[-2/3,\ 0 ,\ -1/3]^T$
    \end{enumerate}"""))

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

def question_text_2(doc: pylatex.Document, parameters: Dict[str, str]):
    with doc.create(Section('Question 2', numbering=False)):
        doc.append(f'{parameters["a"]} x {parameters["b"]} = ' )

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

def marker(table):
    while True:
        print("ID ", end="")
        id = int(input())
        print("Answers: ", end="")
        answers = input().split(" ")
        print ("\033[A                             \033[A")
        correct_answers = [str(a[0]) for a in  table[id][1:]]
        print("          index " + " ".join(map(str, range(1, len(correct_answers) +1))))
        print("Correct answers " + " ".join(correct_answers))
        print("Student answers " + mark(answers, correct_answers))
        print("")


if __name__ == '__main__':
    # Basic document
    doc = Document('basic', page_numbers=False)
    doc.packages.append(Package("amsmath"))
    doc.packages.append(Package("amsfonts"))
    questions = [question_1, question_2]
    table = generate_combinations(doc, questions, num_combinations=4)
    doc.generate_pdf()
    
    # Generate all the combinations
    doc = Document('check_answers')
    doc.packages.append(Package("amsmath"))
    doc.packages.append(Package("amsfonts"))
    question_1.append_all_with_answers(doc)
    doc.append(NewPage())
    question_2.append_all_with_answers(doc)
    doc.generate_pdf()

    marker(table)
