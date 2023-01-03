from typing import Dict, Callable, List
from pylatex import Enumerate, NoEscape, Section
import random

from dataclasses import dataclass, field

@dataclass
class Question:
    question_text: Callable
    parameters: Dict
    answers: List
    question_name: str
    choices: List[List]
    answers_index: Dict[int,int] = field(default_factory=dict)
    same_choices: bool = False

    def __post_init__(self):
        if self.same_choices:
            self.choices = [self.choices]*len(self.answers)
    
        assert len(self.answers) == len(self.choices), "Number of answers must be equal to number of choices"
        for i, answer in enumerate(self.answers):
            possible_answers = self.choices[i]
            assert answer in possible_answers, f"Possible answers {possible_answers} must contain the correct answer {answer}"
            self.answers_index[i] = possible_answers.index(answer)

    def append_random(self, doc):
        index = random.randrange(len(self.answers))
        return self.append(doc, index)

    def append(self, doc, index):
        possible_answers = self.choices[index]
        shuffled_indices = list(range(len(possible_answers)))
        random.shuffle(shuffled_indices)
        parameters = {k:v[index] for k, v in self.parameters.items()}
        with doc.create(Section(self.question_name, numbering=False)):
            doc.append(NoEscape(self.question_text(parameters)))
        with doc.create(Enumerate(r"\alph*)")) as enum:
            for i in shuffled_indices:
                enum.add_item(NoEscape(possible_answers[i]))

        # TODO: Assuming alphabetic indexing, generalise to any indexing.
        return chr(shuffled_indices.index(self.answers_index[index])+97), self.answers[index]

    def append_all_with_answers(self, doc):
        for i in range(len(self.answers)):
            answer_index, answer = self.append(doc, i)
            doc.append(f"Correct answer: {answer_index}) ")
            doc.append(NoEscape(answer))