
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
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    correct_answer = PYTHON_QUESTION_LIST[current_question_id]["answer"]
    selected_answer = answer
    if correct_answer == selected_answer:
        score = 1
        error = None
    else:
        score = 0
        error = "You have selected wrong aswer! Please try again"
    cumulated_score = session.get("TotalScore", None)
    if cumulated_score is None:
        session["TotalScore"] = score
    else:
        session["TotalScore"] += score

    #Try to store response:
    saved_responses = session.get("SavedResponses", None)
    if saved_responses is None:
        session["SavedResponses"] = [{"question_id":current_question_id, "answer_selected": message, "correct_answer":correct_answer}]
    else:
        session["SavedResponses"].append({"question_id":current_question_id, "answer_selected": message, "correct_answer":correct_answer})
    
    return bool(score), error


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    total_questions_count = len(PYTHON_QUESTION_LIST)
    next_question_id = current_question_id + 1
    if next_question_id <= total_questions_count -1:
        next_question = PYTHON_QUESTION_LIST[next_question_id]
        return next_question, next_question_id
    else:
        return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_score = session.get("TotalScore", None)
    if total_score is None:
        saved_responses =session.get("SavedResponses", None)
        if saved_responses is None:
            total_score = 0
        else:
            total_score = 0
            for ques in saved_responses:
                if ques["answer_selected"] == ques["correct_answer"]:
                    total_score+=1
                
    total_questions_count = len(PYTHON_QUESTION_LIST)
    if total_score < (0.4*total_questions_count):
        summary = f"Good Effort! You score is {total_score}. Better Luck Next Time!"
    else:
        summary = f"Excellent! Your score is {total_score}. Keep it up!"
    return "dummy result"
