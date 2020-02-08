from pygsuite.constants import CLIENTS
from pygsuite.docs import Document

if __name__ == "__main__":
    document = Document(id = '1Hn8CM_3DXulIsrpyMqFhneitbAReTF8vj9ekKWyBIk8')
    print(document._document)
    print(document.body.content)
    # print(vars(document._document))