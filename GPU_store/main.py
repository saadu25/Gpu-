import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from gpu import Gpu
from view_gpu import ViewPage
from add_gpu import AddPage
from edit import EditPage
from search import Search

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user == None:
            template_values = {
                'login_url' : users.create_login_url(self.request.uri)
                }
            template = JINJA_ENVIRONMENT.get_template('loginpage_guest.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()
            
            
        template_values = {
        'logout_url' : users.create_logout_url(self.request.uri),
        'gpu' : Gpu.query().fetch()
            }
        
        
        template = JINJA_ENVIRONMENT.get_template('login_page.html')
        self.response.write(template.render(template_values))
        
        
    
app = webapp2.WSGIApplication([
            ('/', MainPage),
            ('/add_gpu', AddPage),
            ('/view_gpu/(.*)', ViewPage),
            ('/edit_gpu/(.*)', EditPage),
            ('/search', Search),
], debug=True)
    
    
    
    
    
    
    
    