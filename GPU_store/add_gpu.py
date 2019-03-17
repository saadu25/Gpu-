import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from gpu import Gpu
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class AddPage(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')
        
        
    def post(self):
        
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
            
            
        user = users.get_current_user()
         
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        
        
        if action == 'Add Gpu' :
            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            dateissued= self.request.get('dateissued')
            
            geometryShader = self.request.get('geometryShader') == 'on'
            tesselationShader= self.request.get('tesselationShader') =='on'
            shaderInt16 = self.request.get('shaderInt16') == 'on'
            sparseBinding = self.request.get('sparseBinding') == 'on'
            textureCompressionETC2 = self.request.get('textureCompressionETC2') == 'on'
            vertexPipelineStoresAndAtomics= self.request.get('vertexPipelineStoresAndAtomics') =='on'
            error = ""

            if name:
                gkey = ndb.Key('Gpu', name)
                gpu = gkey.get()
            
                if gpu == None:
                    dateissued = datetime.strptime(dateissued, '%Y-%m-%d')
                    gpu = Gpu(id=name, name=name, manufacturer=manufacturer, dateissued=dateissued, 
                                  geometryShader=geometryShader, 
                                  tesselationShader=tesselationShader, 
                                  shaderInt16=shaderInt16, 
                                  sparseBinding=sparseBinding, 
                                  textureCompressionETC2=textureCompressionETC2, 
                                  vertexPipelineStoresAndAtomics=vertexPipelineStoresAndAtomics)
                    gpu.put()
                    self.redirect('/')
                
                else:
                    error = name+" GPU already exist"
    #             myuser.gpu.append(new_Gpu)
    #             myuser.put()
            else: 
                # gpu already exixts
                error = "Name is empty"
            
                    
            template_values = {
            'logout_url' : users.create_logout_url(self.request.uri),
            'gpu' : Gpu.query().fetch(),
            'error': error
            }
            
            
            template = JINJA_ENVIRONMENT.get_template('login_page.html')
            self.response.write(template.render(template_values))
            
        
        
        
        elif action == 'Delete':
            name = self.request.get('index')
            
            user = users.get_current_user()
            
            gkey= ndb.Key('Gpu', name)
            gpu = gkey.get()
            
            if gkey != None:
                gpu.key.delete()
            
            self.redirect('/')
    