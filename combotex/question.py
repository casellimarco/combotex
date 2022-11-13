from typing import Dict, Callable, Any, List
import random

from dataclasses import dataclass

@dataclass
class Question:
    question_text: Callable
    parameters: Dict
    answers: List
    choices: List[List]
    
    def __post_init__(self):
        assert len(self.answers) == len(self.choices), "Number of answers must be equal to number of choices"
        for answer, possible_answers in zip(self.answers, self.choices):
            assert answer in possible_answers, f"Possible answers {possible_answers} must contain the correct answer {answer}"

    def append_random(self, doc):
        index = random.randrange(len(self.answers))
        return self.append(doc, index)

    def append(self, doc, index):
        possible_answers = self.choices[index]
        answer_index = possible_answers.index(self.answers[index])
        parameters = {k:v[index] for k, v in self.parameters.items()}
        self.question_text(doc, parameters, possible_answers)
        return answer_index+1, self.answers[index]