import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.web import Application, asynchronous, RequestHandler
import	threading, time

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

count = 20

def doAdd(tmp):
	greeting = tmp.get_argument('greeting', 'Hello')
	tmp.write(greeting + ', tornado!')
	global count
	if count > 0:
		count-=5
	time.sleep(count)
	tmp.finish()

class IndexHandler(tornado.web.RequestHandler):
	@asynchronous
	def get(self):
		threading.Thread(target=doAdd, kwargs=dict(tmp=self)).start()
	def on_complete(self, res):
		self.finish()

class LargeHandler(tornado.web.RequestHandler):
	@asynchronous
	def get(self):
		self.write("test")
		self.finish()
	def on_complete(self, res):
		self.finish()

if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application([(r"/", IndexHandler), (r"/large", LargeHandler)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()