from app import app
from twisted.internet import reactor
from twisted.web.wsgi import WSGIResource
from twisted.web.server import Site


resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)

reactor.listenTCP(5000, site)


if __name__ == "__main__":
	reactor.run()