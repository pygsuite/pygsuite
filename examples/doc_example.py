# flake8: noqa
from pygsuite import Clients
from analytics_utility_core.secrets import secret_store
from pygsuite.docs import Document

if __name__ == "__main__":
    auth = secret_store['bi-gsuite-automation']

    Clients.authorize_string(auth)

    document = Document(id='1kJh3tPyXoDzu_TIltDAXHRiFj-X0XDlVUiOP0wz_M8E')
    for object in document.body.content:
        print(object)
        print(object.start_index)
        print(object.end_index)
        print(getattr(object, 'text', None))
    document.body.delete()

    document.body.add_text('ABC123', style=True)
    document.flush()
