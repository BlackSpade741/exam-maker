import exam_maker
import exam_maker_io
import sys
NEWLINE = '\n'
END = '!end'
MENU = '!menu'
exam = None


def ui_start():
    """ Start menu of the program. This function is called when the program is
    ran initially.

    @rtype: None
    """

    choice = input("""Welcome to Exam Maker 1.0!
[Main Menu]
Please select an option:
1. Make a new exam
2. Import an exam from a file
""")

    if choice == '1':
        ui_new_exam()
    elif choice == '2':
        ui_import_exam()


def ui_new_exam():
    """ Menu to make a new exam. Called in ui_main().

    @rtype: None
    """

    print("""[New Exam]
Enter information on the exam as prompted.""")
    name = input("Please enter the title of the exam:")
    subject = input("Please enter the subject:")
    school = input('Please enter the school:')
    instructor = input('Please enter the instructor:')

    global exam
    exam = exam_maker.Exam(name, subject, school, instructor)

    end = False

    while not end:
        question = input("Enter a question, '{}' if no more.".format(END))

        if question == END:
            end = True
        else:
            correct = input('Please enter the correct answer:')
            result = exam.add_question(question, [correct], 0)

            if not result:
                print('Error! Try again!')
            else:
                end_question = False

                while not end_question:
                    answer = input("Please enter another answer, \
'!end' if no more.")

                    if answer == END:
                        end_question = True
                    else:
                        result = exam.add_answer(question, answer)

                        if result:
                            print('Answer successfully added!')
                        else:
                            print('Error! Try again!')

                print('Success! \nThis is the question added:')
                num = exam.find_question(question)
                print(exam.str_question(num))
                print('Correct answer: ' + str(exam.content[num][2] + 1))

    print('Success!')
    ui_main()


def ui_import_exam():
    print('[Import Exam]')

    while True:
        file_name = input('Please enter the file name.')

        try:
            file = open(file_name, 'r')
            break
        except FileNotFoundError:
            print('Error! Invalid file name! Try again!')

    global exam
    exam = exam_maker_io.import_exam(file)
    print('Success!')
    ui_main()


def ui_main():
    """ Main menu of the program, called in ui_new_exam() or ui_import_exam()
    after an exam has been created/imported into the program.

    @rtype: None
    """

    global exam

    while True:
        print(NEWLINE + '[Main Menu]')
        print("Exam information:")
        print(str(exam) + NEWLINE)
        option = input("""Please select an option:
1. View your exam
2. Find a question
3. Export a student copy
4. Save to a file
0. Quit the exam maker
""")

        if option == '1':
            print('[Exam Viewing]')
            file_name = exam.name + '_instructor.txt'
            file_out = open(file_name, 'w')
            exam_maker_io.export_exam_user(exam, file_out)
            print('The exam has been exported to {} for view. '.
                  format(file_name))
            file_out.close()
        elif option == '2':
            print('[Find a Question]')
            option = input("""How would you like to find your question?
            1. With the question number
            2. With the question itself""")

            if option == '1':
                while True:
                    num = int(input('Please enter the question number:'))

                    if 0 <= num < len(exam.content):
                        ui_question(num - 1)
                    else:
                        print('Error! Invalid index! Try again!')
            elif option == '2':
                while True:
                    question = input('Please enter the question:')

                    index = exam.find_question(question)

                    if index == -1:
                        print('Error! Invalid input! Try again!')
                    else:
                        ui_question(index)
            else:
                print('Error! Invalid input! Try again!')
        elif option == '3':
            print('[Export Student Copy]')
            copy = exam.shuffle_exam()

            print('Exporting version No. {}...'.format(copy.versions))
            copy_file = open(copy.name + '_{}.txt'.format(copy.versions), 'w')
            answer_file = open(copy.name + '_{}_answers.txt'.
                               format(copy.versions), 'w')

            exam_maker_io.export_copy(copy, copy_file)
            exam_maker_io.export_answer_key(copy, answer_file)

            copy_file.close()
            answer_file.close()

            print('The copy and its answer key has been exported!')
        elif option == '4':
            print('[Save to File]')
            file_name = input('Please enter a file name to save to. '
                              'Enter nothing to save to the name of the exam.')
            if file_name == '':
                file_name = exam.name

            file = open(file_name + '.txt', 'w')
            exam_maker_io.export_exam(exam, file)
            file.close()
            
            print('The exam has been saved! Input the file name at launch to '
                  'use this exam next time. ')
        elif option == '0':
            while True:
                option = input("""Are you sure you want to exit the program?
                Any unsaved changes are lost.
                1. Yes
                2. No""")

                if option == '1':
                    sys.exit()
                elif option == '2':
                    break
                else:
                    print('Error! Invalid input!')


def ui_question(question_i):
    """ Menu with options to change a particular question.

    @type question_i: int
        the index of a particular question in exam.content
    @rtype: None
    """

    global exam

    question = exam.content[question_i][0]
    while True:
        print('[Question Number {}]'.format(question_i + 1))
        print(exam.str_question(question_i))
        print('Correct answer: {}'.format(exam.content[question_i][2]))

        option = input("""Please select an option:
1. Add an answer
2. Delete an answer
3. Modify an answer
4. Modify the correct answer number
5. Delete this question
0. Go back to main menu""")
        if option == '1':
            print('[Add Answer]')
            answer = input('Please enter a new answer:')
            success = exam.add_answer(question, answer)

            if success:
                print('Answer successfully added!')
            else:
                print('Question cannot be added ;( Try again!')

        elif option == '2':
            print('[Delete Answer]')
            let = input('Please enter the answer letter you would like to \
            delete. ')

            num = exam_maker.letter_to_int(let)

            if num == exam.content[question_i][2]:
                print('Error! Cannot delete the correct answer! Try again!')
            elif 0 <= num < len(exam.content[question_i][1]):
                exam.content[question_i][1].delete(num)
                print('Success!')
            else:
                print('Error! Invalid input!')
        elif option == '3':
            print('[Modify Answer]')
            let = input('Please enter the answer letter you would like to \
                        modify. ')

            num = exam_maker.letter_to_int(let)

            if 0 <= num < len(exam.content[question_i][1]):
                answer = input('Please enter the new answer:')
                exam.content[question_i][1][num] = answer
                print('Success!')
            else:
                print('Error! Invalid input!')
        elif option == '4':
            print('[Change Correct Answer]')
            let = input('Please enter the letter you would like to change the \
                        correct answer to. ')
            num = exam_maker.letter_to_int(let)

            if 0 <= num < len(exam.content[question_i][1]):
                exam.content[question_i][2] = num
                print('Success!')
            else:
                print('Error! Invalid input!')
        elif option == '5':
            print('[Delete Question]')
            option = input('''Are you sure you want to delete this question?
            1. Yes
            2. No''')

            if option == '1':
                exam.content.delete(question_i)
                print('Question deleted.')
                ui_main()
            elif option != '2':
                print('Error! Invalid input!')
        elif option == '0':
            ui_main()
        else:
            print('Error! Invalid input!')

ui_start()