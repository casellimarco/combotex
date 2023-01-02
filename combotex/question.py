from typing import Dict, Callable, Any, List
from pylatex import Enumerate
import random

from dataclasses import dataclass, field

@dataclass
class Question:
    question_text: Callable
    parameters: Dict
    answers: List
    choices: List[List]
    answers_index: Dict[int,int] = field(default_factory=dict)

    def __post_init__(self):
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
        parameters = {k:v[index] for k, v in self.parameters.items()}
        self.question_text(doc, parameters)
        with doc.create(Enumerate()) as enum:
            for choice in possible_answers:
                enum.add_item(choice)

        # TODO: Assuming enumerate indexing, generalise to any indexing.
        return self.answers_index[index]+1, self.answers[index]

    def append_all_with_answers(self, doc):
        for i in range(len(self.answers)):
            answer_index, answer = self.append(doc, i)
            doc.append(f"Correct answer: {answer_index}) {answer}.")