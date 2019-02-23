from threading import Thread

from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site


class WebhookHandler(Resource):
    isLeaf = True

    def render_GET(self, request):
        if request.uri == b'/':
            return (b'<html>'
                    b'<head>'
                    b'<!-- <meta http-equiv="refresh" content="5"> -->'
                    b'</head'
                    b'<body>'
                    b'<img style="max-width: 100%; height: auto; width: auto;" src="/preview.jpg" alt="Preview image">'
                    b'</body>'
                    b'</html>')

        elif request.uri == b'/preview.jpg':
            with open('./current.jpg', 'rb') as f:
                return f.read()


class Server(Thread):
    def run(self):
        print('Starting http server on localhost:8080')

        site = Site(WebhookHandler())
        reactor.listenTCP(8080, site)

        # Signal handlers have to be set to false when the server is not running in the main thread.
        # Don't ask me why.
        reactor.run(installSignalHandlers=False)
