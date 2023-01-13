from combotex import Question, Exam

def question_text_1(parameters):
    # qui creiamo il testo della domanda utilizzando i parametri, per comodita' sono piu' strings concatenate
    # normalmente usiamo raw strings (r) cosi' da evitare che python usi i special chars
    return (r"\`E dato il sistema lineare \[\begin{cases}"
    # raw + fstrings (rf) per aggiungere parametri, occhio che qui le graffe non fanno parte del testo,
    # quindi se ci sono graffe in latex la stringa va spezzata in componenti diverse (begin{cases} e' nella stringa sopra) 
    rf"x + {parameters['a']}y + 3z = 4"
    # senza parametri e' semplicemente una raw string, possiamo farla anche multilinea (i.e. mettiamo una r prima e tre quotes)
    r"""\\x + z = 0\\kx + z = k^2-1\end{cases}\] dove $k \in \mathbb{R}$. 
Determina tutti e soli i valori di $k$ per cui il sistema ammette soluzioni.""")

question_1 = Question(
    # Il testo della domanda parametrizzato
    question_text_1,
    # I parametri del testo della domanda
    parameters = {"a":[2,3]},
    # le risposte corrette
    answers = [r"$k \neq -1,\  1$", r"$k \neq 1$"],
    # le scelte possibili
    choices = [
     r"$k \neq -1,\  1$",
     r"$k \neq 1$",
     r"$k = 0$",
     r"$k \in \mathbb{R}$",
     r"Il sistema non ha soluzione per alcun valore di $k \in \mathbb{R}$"],
    # Intestazione domanda
    question_name= "Domanda 1",
    # qua forziamo tutte le domande ad avere le stesse opzioni
    same_choices=True
)


if __name__ == '__main__':
    # Basic exam
    questions = [question_1]
    exam = Exam("basic", questions)
    exam.generate_exams(num_exams=4, clean_tex=False)
    
    # Generate all the combinations
    exam.check_answers(clean_tex=False)

    # Interactive marker
    exam.marker(correct_score=1, wrong_score=-1, missing_score=0)
