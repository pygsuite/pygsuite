
def test_document_parsing(test_document):
    assert test_document.title == 'Test Document'


def test_document_body(test_document):
    from pygsuite.docs.doc_elements.paragraph import Paragraph
    assert len(test_document.body.content) == 4

    first_paragraph = test_document.body[1]
    assert isinstance(first_paragraph, Paragraph)

    assert first_paragraph.text == 'Hello There!\n'