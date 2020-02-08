from pygsuite.constants import CLIENTS

if __name__ == "__main__":

    DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'

    document = CLIENTS.docs_client.documents().get(documentId=DOCUMENT_ID).execute()

    print('The title of the document is: {}'.format(document.get('title')))