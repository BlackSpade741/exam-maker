import exam_maker
NEWLINE = '\n'


def import_exam(file):
    """ Return an Exam based on info from file for I/O purposes.

    === File Format ===
    name
    school
    subject
    instructor
    versions
    number of questions

    question 1
    correct answer num
    answer
    answer
    answer

    question 2
    correct answer num
    answer
    answer
    answer
    ...
    === End of File ===

    @type file: file open for reading
    @rtype: Exam
    """

    exam = exam_maker.Exam(file.readline().strip(), file.readline().strip(), 
                           file.readline().strip(), file.readline().strip())
    versions = file.readline().strip()
    exam.versions = int(versions)
    num = int(file.readline().strip())
    temp = file.readline()

    for i in range(num):
        question = file.readline().strip()
        correct = int(file.readline())
        answer = []

        line = file.readline().strip()

        while line != NEWLINE:
            answer.append(line.strip())
            line = file.readline()

        exam.add_question(question, answer, correct)

    return exam


def export_exam(exam, file):
    """ Export exam to a file for IO purposes.

    === File Format ===
    name
    school
    subject
    instructor
    versions
    number of questions

    question 1
    correct answer num
    answer
    answer
    answer

    question 2
    correct answer num
    answer
    answer
    answer
    ...
    === End of File ===

    @type exam: Exam
    @type file: file open for writing
    @rtype: None
    """

    file.write(exam.name + NEWLINE)
    file.write(exam.school + NEWLINE)
    file.write(exam.subject + NEWLINE)
    file.write(exam.instructor + NEWLINE)
    file.write(str(exam.versions) + NEWLINE)
    file.write(str(len(exam.content)+ NEWLINE))
    file.write(NEWLINE)

    for question in exam.content:
        file.write(question[0] + NEWLINE)
        file.write(str(question[2]) + NEWLINE)

        for answer in question[1]:
            file.write(answer + NEWLINE)

        file.write(NEWLINE)


def export_copy(exam, file):
    """ Export a copy of exam to file.

    @type exam: Exam
    @type file: file opened for writing
        the file to export to.
    @rtype: None
    """

    file.write(exam.name + NEWLINE)
    file.write(exam.school + NEWLINE)
    file.write('Subject: ' + exam.subject + NEWLINE)
    file.write('Instructor: ' + exam.instructor + NEWLINE)
    file.write('Version Number: ' + str(exam.versions) + NEWLINE * 2)
    file.write(NEWLINE)
    file.write('===== Start of Exam =====' + NEWLINE)
    file.write(NEWLINE)

    for i in range(len(exam.content)):
        file.write(str(i + 1) + '. ' + exam.str_question(i))
        file.write(NEWLINE)


def export_exam_user(exam, file):
    """ Export a user-friendly copy of exam to file for instructors.

    @type exam: Exam
    @type file: file opened for writing
        the file to export to.
    @rtype: None
    """
    file.write('Exam name:' + exam.name + NEWLINE)
    file.write('School: ' + exam.school + NEWLINE)
    file.write('Subject: ' + exam.subject + NEWLINE)
    file.write('Instructor: ' + exam.instructor + NEWLINE)
    file.write(NEWLINE)

    for i in range(len(exam.content)):
        file.write(str(i + 1) + '. ' + exam.str_question(i))
        file.write('Correct answer: ' + 
                   exam_maker.int_to_letter(exam.content[i][2] + 1) + NEWLINE)
        file.write(NEWLINE)


def export_answer_key(exam, file):
    """ Export the correct answer indices to file. Each line in the file
    contains one answer, in the same order as the questions appear in exam.

    @type exam: Exam
    @type file: file open for writing
    @rtype: None
    """

    for question in exam.content:
        file.write("{}\n".format(question[2]))
