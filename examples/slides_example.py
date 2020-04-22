# flake8: noqa
from pygsuite import Clients
from analytics_utility_core.secrets import secret_store
from pygsuite.docs import Document

if __name__ == "__main__":
    auth = secret_store['bi-gsuite-automation']

    Clients.authorize_string(auth)

    document = Document(id='1kJh3tPyXoDzu_TIltDAXHRiFj-X0XDlVUiOP0wz_M8E')
    print(document._document)
    print(document.body.content)
    # print(vars(document._document))
