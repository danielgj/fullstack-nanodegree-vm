from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

DBSession = sessionmaker(bind = engine)

session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        
        if self.path.endswith("/restaurants/new"):            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>New Restaurant</h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Restaurant name</h2><input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
            output +="</body></html>"            
            self.wfile.write(output)
            return
        
        if self.path.endswith("/edit"):
            restaurantID = self.path.split("/")[2]
            restuarantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
            if restuarantQuery != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>''' % restuarantQuery.id
                output +=  '''<h2>Restaurant name</h2><input name="name" type="text" value="%s"><input type="submit" value="Submit"> </form>''' % restuarantQuery.name
                output +="</body></html>"            
                self.wfile.write(output)
        
        if self.path.endswith("/delete"):
            restaurantID = self.path.split("/")[2]
            restuarantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
            if restuarantQuery != []:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Remove Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>''' % restuarantQuery.id
                output +=  '''<h2>Are you sure you want to remove %s?</h2><input type="submit" value="Delete"> </form>''' % restuarantQuery.name
                output +="</body></html>"            
                self.wfile.write(output)
                return

        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Restaurants</h1>"
            output +="<ul>"
            restaurants = session.query(Restaurant).all()
            for item in restaurants:
                output += '''<li> %s <a href="/restaurants/%s/edit">Edit</a> <a href="/restaurants/%s/delete">Delete</a> </li>''' % (item.name, item.id, item.id)
            output +="</ul>"
            output += '''<a href="/restaurants/new">Add new Restaurant</a>'''
            output +="</body></html>"
            self.wfile.write(output)
            return
        
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Hello!</h1>"            
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output +="</body></html>"
            self.wfile.write(output)
            
        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>Hola! <a href='/hello'>Back to Hello</a>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output +="</body></html>"
            self.wfile.write(output)

        else:
            self.send_error(404, 'File Not Founddd: %s' % self.path)

    def do_POST(self):
        
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    myFirstRestaurant = Restaurant(name=messagecontent[0])
                    session.add(myFirstRestaurant)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
            if self.path.endswith("/edit"):                                
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    restaurantID = self.path.split("/")[2]
                    restuarantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                    if restuarantQuery != []:
                        restuarantQuery.name = messagecontent [0]
                        session.add(restuarantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-Type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()

            if self.path.endswith("/delete"):                                
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    restaurantID = self.path.split("/")[2]
                    restuarantQuery = session.query(Restaurant).filter_by(id=restaurantID).one()
                    if restuarantQuery != []:
                        session.delete(restuarantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-Type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()


            """ self.send_response(201)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output """

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()