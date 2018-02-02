import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.web import Application, asynchronous, RequestHandler
import	threading, time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	@asynchronous
	def get(self):
		try:
			greeting = self.get_argument('greeting', None)
			if greeting is not None:
				self.write(greeting+'hello world')
			self.finish()
		finally:
			self.write('501 error')
			self.finish()
	def on_complete(self, res):
		self.finish()

class LargeHandler(tornado.web.RequestHandler):
	@asynchronous
	def get(self, webPage):
		try:
			self.render(webPage)
			self.finish()
		finally:
			self.write('501 error')
			self.finish()
	def on_complete(self, res):
		self.finish()

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application([(r"/", IndexHandler), (r"/(.+)", LargeHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()