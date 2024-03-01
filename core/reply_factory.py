
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        if next_question_id > 0:
            bot_responses = []
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    answer = answer.strip()
    print(current_question_id,"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not session.get("score") and session.get("score") != 0:
        print("pppppppppppppppppppppp")
        session["score"] = 0
        session.save()
    if not session.get("user_record"):
         session["user_record"] = []
         session.save()
    user_record =  session.get("user_record")
    if current_question_id is not None and int(current_question_id)>0:
        if answer:
            available_options = PYTHON_QUESTION_LIST[int(current_question_id)-1]['options']
            if answer not in available_options:
                return False, "Please Enter a Valid Answer"
            else:
                if int(current_question_id) not in user_record:
                    print("++++++++++++++++000000")
                    user_record.append({int(current_question_id): answer})
                if answer == PYTHON_QUESTION_LIST[int(current_question_id)-1]["answer"]:
                    print("#########################",session["score"])
                    session["score"] += 1
                    session.save()
                print(user_record,"************/////***********",session["score"])
                return True, ""
    elif  current_question_id is not None and int(current_question_id)==0 and answer.lower() != "yes":
        return False, "Please Enter <b>'yes'</b> to continue"
    else:
        return True, ""


def get_next_question(current_question_id):
    if current_question_id is not None and int(current_question_id) > len(PYTHON_QUESTION_LIST)-1:
        return None,None
    if current_question_id is not None and int(current_question_id) >= 0:
         next_question_id = int(current_question_id)+1
         question = PYTHON_QUESTION_LIST[current_question_id]["question_text"]
         options =  PYTHON_QUESTION_LIST[current_question_id]["options"]
         next_questions = f"question: {question}\n\n options: {options}"
         return next_questions,next_question_id
    else:
         return "Enter <b>'yes'</b> to start the test", 0
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''




def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_score = session.get("score")
    if total_score is not None:
        return f"Your total score is {total_score} out of {len(PYTHON_QUESTION_LIST)}"
    else:
        return f"There is a issue ocured please contact the <b>Quizbot</b> developer team"
