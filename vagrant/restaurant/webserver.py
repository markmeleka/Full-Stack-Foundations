from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import pdb

def make_session():
		engine = create_engine('sqlite:///restaurantmenu.db')
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind = engine)
		session = DBSession()
		return session

class WebServerHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path.endswith("/hello"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = ""
			output += "<html><body>"
			output += "<h1>Hello!</h1>"
			output += '''<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2><input name="message" type = "text"><input type="submit" value="Submit"></form>'''
			output += "</body></html>"
			self.wfile.write(output)
			print output
			return
		elif self.path.endswith("/hola"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = ""
			output += "<html><body>"
			output += "<h1>&#161hola!</h1> <a href= '/hello'>Back to Hello!</a>"
			output += '''<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2><input name="message" type = "text"><input type="submit" value="Submit"></form>'''
			output += "</body></html>"
			self.wfile.write(output)
			print output
			return
		elif self.path.endswith("/restaurants"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = ""
			output += "<html><body>"
			output += "<a href='/restaurants/new'>Make new restaurant</a></br></br>"
			session = make_session()
			restaurants = session.query(Restaurant).all()
			for restaurant in restaurants:
				output += "%s</br>" % restaurant.name
				output += "<a href='/restaurants/%s/edit'>Edit</a></br>" % restaurant.id
				output += "<a href='/restaurants/%s/delete'>Delete</a></br>" % restaurant.id
				output += "</br>"
			
			output += "</body></html>"
			self.wfile.write(output)
			print output
			return
		elif self.path.endswith("/restaurants/new"):
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			output = ""
			output += "<html><body>"
			output += "<h1>Create a new Restaurant!</h1>"
			output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'>"
			output += "<input name='newRestaurantName' type = 'text'>"
			output += "<input type='submit' value='Create'>"
			output += "</form></body></html>"
			self.wfile.write(output)
			print output
			return
		elif self.path.endswith("/edit"):
			session = make_session()
			restaurantID = self.path.split('/')[-2]
			try:
				restaurant = session.query(Restaurant).filter_by(id= restaurantID).one()
			except:
				self.send_error(404, 'Restaurant ID not found: %s') % restaurantID
			if restaurant:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Edit restaurant name</h1>"
				output += "<h2>Restaurant: %s</h1>" % restaurant.name
				output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/%i/edit'>" % restaurant.id
				output += "<input name='newRestaurantName' type = 'text' placeholder = '%s'>" % restaurant.name
				output += "<input type='submit' value='Edit'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				print output
			return

		elif self.path.endswith("/delete"):
			session = make_session()
			restaurantID = self.path.split('/')[-2]
			try:
				restaurant = session.query(Restaurant).filter_by(id= restaurantID).one()
			except:
				self.send_error(404, 'Restaurant ID not found: %s') % restaurantID
			if restaurant:
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Delete restaurant</h1>"
				output += "<h2>Are you sure you want to delete restaurant: %s</h1>" % restaurant.name
				output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/%i/delete'>" % restaurant.id
				output += "<input type='submit' value='Delete'>"
				output += "</form></body></html>"
				self.wfile.write(output)
				print output
			return

		else:
			self.send_error(404, 'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				# pdb.set_trace()

				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')
				output = ""
				output += "<html><body>"
				output += "<h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]
				output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2><input name='message' type = 'text'><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output

			elif self.path.endswith("/restaurants/new"):

				# pdb.set_trace()

				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')

					newRestaurant = Restaurant(name = messagecontent[0])
					session = make_session()
					session.add(newRestaurant)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
			
			elif self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')

					session = make_session()
					restaurantID = self.path.split('/')[-2]
					restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
					restaurant.name = messagecontent[0]
					session.add(restaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
			
			elif self.path.endswith("/delete"):
				ctype, pdict = cgi.parse_header(
					self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':

					session = make_session()
					restaurantID = self.path.split('/')[-2]
					restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
					session.delete(restaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					self.send_header('Location', '/restaurants')
					self.end_headers()
		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), WebServerHandler)
		print "Web Server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()

