from pygsuite.forms import Item, QuestionItem, Question, TextQuestion, Form
import json
import pytest


@pytest.mark.run(order=1)
def test_form(test_form):
    new_item = Item(
        question_item=QuestionItem(question=Question(text_question=TextQuestion(paragraph=True))),
        description="A new question",
        title="My fun question",
    )
    test_form.items.append(new_item)
    test_form.items.append(new_item)
    test_form.flush()


@pytest.mark.run(order=2)
def test_auto_sync(test_form):
    candidate = test_form.items[0]
    cached = candidate.item_id
    candidate.title = "At first"
    test_form.items.move(0, 1)
    test_title = "whose on second?"
    candidate.title = test_title
    test_form.flush()
    assert test_form.items[1].item_id == cached
    assert test_form.items[1].title == test_title


@pytest.mark.run(order=3)
def test_empty_assignment(test_form):
    test_form.items = []
    test_form.flush()
    new_item = Item(
        question_item=QuestionItem(question=Question(text_question=TextQuestion(paragraph=True))),
        description="A new question",
        title="My fun question",
    )
    test_form.items.append(new_item)
    test_form.flush()
    assert len(test_form.items) == 1


def test_complex_parsing():
    from os.path import dirname, join

    with open(join(dirname(__file__), "test_form.json_capture"), "r", encoding="utf-8") as f:
        form = f.read()

    test = Form(_form=json.loads(form), local=True)
    assert test.items[0].question_group_item.questions
