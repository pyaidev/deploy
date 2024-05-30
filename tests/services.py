from tests.models import Question


def is_correct_answer(question_pk, answer_list: list) -> bool:
    correct_answers = []
    answer_list = [ans.lower() for ans in answer_list]
    question = Question.objects.get(pk=question_pk)
    answers = question.answers_set.all()
    for answer in answers:
        if answer.is_correct:
            correct_answers.append(answer.text.lower())
    correct_answers = set(correct_answers)
    answer_list = set(answer_list)

    return answer_list == correct_answers
