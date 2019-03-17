import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from gpu import Gpu

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class ViewPage(webapp2.RequestHandler):       
        
    def get(self, name):
        
        self.response.headers['Content-Type'] = 'text/html'
            
            
        user = users.get_current_user()
        
        if user == None:
            self.redirect('/')
         
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        
        
        if name:
            gkey = ndb.Key('Gpu', name)
            gpu = gkey.get()
        
            if gpu == None:
                self.redirect('/')

            
                    
            template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'gpu' : gpu,
            }
            
            
            template = JINJA_ENVIRONMENT.get_template('view_gpu.html')
            self.response.write(template.render(template_values))
            
        else:
            self.redirect('/')


    