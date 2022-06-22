from pygsuite.forms import Item, QuestionItem, Question, TextQuestion

BRIGHT_GREEN_HEX = "#72FF33"


def test_form(test_form):
    new_item = Item(
        question_item=QuestionItem(question=Question(text_question=TextQuestion(paragraph=True))),
        description="A new question",
        title="My fun question",
    )
    test_form.items.append(new_item)
    test_form.flush()
