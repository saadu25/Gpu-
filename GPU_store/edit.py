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

class EditPage(webapp2.RequestHandler):
    def get(self, name):
        
        if name:
            gkey = ndb.Key('Gpu', name)
            gpu = gkey.get()
        
            if gpu == None:
                self.redirect('/')
            
            template_values = {
                'logout_url' : users.create_logout_url(self.request.uri),
                'gpu' : gpu,
                
                }
        
            template = JINJA_ENVIRONMENT.get_template('edit.html')
            self.response.write(template.render(template_values))
            
        else:
            self.redirect('/')
        
        
    def post(self, gname):
        
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
            
            
        user = users.get_current_user()
        
        if user == None:
            self.redirect('/')
         
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        error = ""
        
        gkey = ndb.Key('Gpu', gname)
        gpu = gkey.get()
        
        if gpu == None:
            self.redirect('/')
            
        if action == 'Update':
            
            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            dateissued= self.request.get('dateissued')
            
            geometryShader = self.request.get('geometryShader') == 'on'
            tesselationShader= self.request.get('tesselationShader') =='on'
            shaderInt16 = self.request.get('shaderInt16') == 'on'
            sparseBinding = self.request.get('sparseBinding') == 'on'
            textureCompressionETC2 = self.request.get('textureCompressionETC2') =='on'

            vertexPipelineStoresAndAtomics= self.request.get('vertexPipelineStoresAndAtomics') =='on'
           

            if name and dateissued:
                            
                dateissued = datetime.strptime(dateissued, '%Y-%m-%d')
                    
                if name != gpu.name:
                    nkey = ndb.Key('Gpu', name)
                
                    if nkey.get():
                        error = "gpu with the name already exist."
                        
                    else:
                        gpu.key.delete()
                        
                        gpu = Gpu(id=name, 
                                name=name)
                    
                if error == "":
                    gpu.populate( 
                                manufacturer=manufacturer, 
                                dateissued=dateissued, 
                                geometryShader=geometryShader, 
                                tesselationShader=tesselationShader, 
                                shaderInt16=shaderInt16,
                                sparseBinding=sparseBinding, 
                                textureCompressionETC2=textureCompressionETC2, 
                                vertexPipelineStoresAndAtomics=vertexPipelineStoresAndAtomics)
                    if gpu.put():
                        
                        error = 'gpu updated'
                    else:
                        error = 'gpu not updated'
                
            else: 
                error = 'name OR dateissued cannot be empty'

            
                
        template_values = {
        'logout_url' : users.create_logout_url(self.request.uri),
        'gpu' : gpu,
        'error':error
        }
        
        
        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_values))


    