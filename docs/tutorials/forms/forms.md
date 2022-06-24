# Forms

`pygsuite` can help you work with Google Forms. 

In this tutorial, we'll create a multiple choice form to rate the seasons.

While pygsuite offers a higher level API, at the lower level it directly exposes the 
[api documented here](https://developers.google.com/forms/api/reference/rest/v1/forms). 

This means you can refer to that document for all basic operations, classes, and types. 

## Creating a Form

Get started by creating a new form:

```python
from pygsuite import Form

form = Form.create(
    name="My First Form",
)
print(form.url)
```

Congrats! You've made a form. Load the URL and you will see your form has one default question. 

### Modifying the Form

How can you add to this form?

In the low level API, everything in a Form is an "Item".

That includes text, questions, pagebreaks, and everything else.

Let's start by adding a bit of text. 
```python
from pygsuite.forms import Item, TextItem
form.items.append(Item(text_item = TextItem(), description='This form will collect info on your favorite seasons, so the universe can make improvements.', title='What you should expect'))

```

As typical in pygsuite, you've only made this change locally. To synchronize your local copy with the
server form, we need to `flush` our changes. (this is a performance optimization; submitting local changes in bulk to the remote
significantly improves performances and reduces your chance of hitting API quotas. Think of this like saving a file from memory).

To flush changes, call that function on the form, then print and reload the URL.
```python
form.flush()
print(form.url)
```

You should see a new row in the form, containing the text you defined.


### Adding a Question

Questions get a little more complicated. If we refer to the API model, we see that the base Question object can
be customized via child objects and needs to be wrapped in a QuestionItem.

And to add a basic question, we're *not even setting any properties*. We're just adding those models to the API.

So ou final line looks like the below - the item is passed a QuestionItem which has a Question which is a TextQuestion.
*whew*. This is why you'll want to explore some of the higher level APIs later.

But first, give it a shot by running the below code. 

```python
from pygsuite.forms import QuestionItem, Question, TextQuestion
form.items.append(Item(question_item=QuestionItem(question=Question(text_question=TextQuestion())),
                       description="We're talking calendar year, not motels", title="Can you one of the four seasons?"))
form.flush()
print(form.url)

```
Refresh your form. Do you see what you expect?


### Adding a QuestionGroup

Now let's get fancy and rate things.

A question group is a grouping of many questions that have the same options.

Fortunately, it's not that much more complicated than the above example.

Take a look at the below code.

We'll first define an array of `Questions` - the same object we had before. But these are subclassed with a
`RowQuestion`, which lets you set a title. 

Then we define a row of `Options`, which we'll pass into a `Grid`, whose columns are a `ChoiceQuestion`, with the
type RADIO and the options being the option array we defined.

Alright, it's a bit more a complicated.

Go ahead and run it.

```python
from pygsuite.forms import QuestionGroupItem, Option, ChoiceQuestion, Grid, RowQuestion

season_questions = [Question(row_question=RowQuestion(title=season)) for season in
                    ['Spring', 'Summer', 'Fall', 'Winter']]

ratings = [Option(value='Awful'),
           Option(value='Okay'),
           Option(value='Great'),
           ]
form.items.append(Item(question_group_item=QuestionGroupItem(questions=season_questions,
                                                             grid=Grid(columns=ChoiceQuestion(type='RADIO',
                                                                                              options=ratings))), ))

form.flush()
print(form.url)


```

Now refresh the form and make sure you see what you can expect.

You should now have a basic idea of how to manipulate forms and see how you can avoid the tedium of manual configuration.

What if you wanted to rate the months instead? It would be easy for you to modify the questions to include an arbitrarily
large array. Poke around and review the API documentation to see what other question types you can use! Maybe 
try a slider selector, or a range.

Happy forming!

Check out the reference and how to guides for next steps and other detailed documentation.

