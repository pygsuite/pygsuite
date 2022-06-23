from pygsuite.forms import Item, QuestionItem, Question, TextQuestion, Form
import json


def test_form(test_form):
    new_item = Item(
        question_item=QuestionItem(question=Question(text_question=TextQuestion(paragraph=True))),
        description="A new question",
        title="My fun question",
    )
    test_form.items.append(new_item)
    test_form.flush()


def test_complex_parsing():
    from os.path import dirname, join

    with open(join(dirname(__file__), "test_form.json"), "r", encoding="utf-8") as f:
        form = f.read()

    test = Form(_form=json.loads(form), local=True)
    assert test.items[0].question_group_item.questions
