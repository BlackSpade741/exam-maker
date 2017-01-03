import random
import copy
A_LOWER = 97
A_UPPER = 65
NEWLINE = '\n'


class Exam:
    """ An exam.

    === Attributes ===
    @type name: str
        The name of the exam.
    @type subject: str
        The subject of the exam.
    @type school: str
        The school giving the exam.
    @type instructor: str
        The instructor giving the exam.
    @type versions: int
        The number of versions this exam has. Every run of export_copy
        increments this value by one.
    @type content: list[list[str, list[str], int]]
        The content of the exam. The items in the list are individual questions,
        which are individual lists of the form question, list of answers,
        correct answer index.

    """

    def __init__(self, name, subject, school, instructor):
        """ Initialize an Exam object.

        @type self: Exam
        @type name: str
        @type subject: str
        @type school: str
        @type instructor: str
        """

        self.name = name
        self.subject = subject
        self.school = school
        self.instructor = instructor
        self.versions = 0
        self.content = []

    def add_question(self, question, answer, correct):
        """ Modify self.content to add a new question, return True if
        successful.

        @type question: str
            The question to be added.
        @type answer: list[str]
            A list of answers to question.
            Precondition: len(answer) >= 1
        @type correct: int
            The index of the correct answer in answer.
            Precondition: 0 <= correct < len(answer)
        @rtype: bool
            A bool indicating if the question was successfully added.
        """

        dup = self.find_question(question)

        if dup != -1:
            return False

        self.content.append([question, answer, correct])

        return True

    def find_question(self, question):
        """ Return the index if question is a question in self.content, -1 if
        not.

        @type self: Exam
        @type question: str
        @rtype: int
            The index of question.
        """

        for i in range(len(self.content)):
            if self.content[i][0] == question:
                return i

        return -1

    def add_answer(self, question, answer):
        """ Add answer to question and return True if found, return False if
        question cannot be found.

        @type self: Exam
        @type question: str
        @type answer: str
        @rtype: bool
            A bool indicating if the answer was successfully added.
        """

        q_index = self.find_question(question)

        if q_index == -1:
            return False

        self.content[q_index][2].append(answer)
        return True

    def add_answer_int(self, question, answer):
        """ Add answer to the question indicated by the index question.

        @type self: Exam
        @type question: int
        @type answer: str
        @rtype: None
        """

        self.content[question][2].append(answer)

    def __str__(self):
        """ Return a brief description of the exam.

        @type self: Exam
        @rtype: str
        """

        return """Exam name:{}
        Subject: {}
        School: {}
        Instructor: {}
        Number of questions: {}""".format(self.name, self.subject, self.school,
                                          self.instructor, len(self.content))

    def str_question(self, q):
        """ Return a str representation of the question indicated by q,
        including its answers.

        @type self: Exam
        @type q: int
            Index of a question in self.content
            Precondition: q < len(self.content)
        @rtype: str
        """

        s = self.content[q][0] + NEWLINE

        for i in range(len(self.content[q][1])):
            s += chr(A_LOWER + i) + '. '
            s += self.content[q][1][i] + NEWLINE

        return s

    def shuffle_exam(self):
        """ Return a deep-copy of exam that has been shuffled.

        @type self: Exam
            Precondition: use only with the original exam.
        @rtype: Exam
        """

        new = copy.deepcopy(self)
        self.versions += 1
        new.versions += 1

        for question in new.content:
            new.shuffle_answers(question)

        random.shuffle(new.content)
        return new

    def shuffle_answers(self, q):
        """ Shuffle the answers to the question indicated by q.

        @type self: Exam
        @type q: int
            The index of the question to shuffle.
        @rtype: None
        """

        correct = self.content[q][2]
        random.shuffle(self.content[q][1])
        self.content[q][2] = self.content[q][1].find(correct)
