import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb


from gpu import Gpu
from myuser import MyUser



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Search(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }

            template = JINJA_ENVIRONMENT.get_template('loginpage_guest.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

        search_query = Gpu().query().fetch()

        template_values = {
            'logout_url': users.create_logout_url(self.request.uri),
            'gpu_user':search_query

        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        if self.request.get('button') == 'Submit':

            geometryShader = bool(self.request.get('search_geometryShader'))
            tesselationShader = bool(self.request.get('search_tesselationShader'))
            shaderInt16 = bool(self.request.get('search_shaderInt16'))
            sparseBinding = bool(self.request.get('search_sparseBinding'))
            textureCompressionETC2 = bool(self.request.get('search_textureCompression'))
            vertextPipelineStoresandAtomics = bool(self.request.get('search_vertexPipelineStoresAndAtomics'))
            
            mysearchlist = Gpu.query()
            
            if geometryShader:
                mysearchlist = mysearchlist.filter(Gpu.geometryShader == True)
            if tesselationShader:
                mysearchlist = mysearchlist.filter(Gpu.tesselationShader == True)
            if shaderInt16:
                mysearchlist = mysearchlist.filter(Gpu.shaderInt16 == True)
            if sparseBinding:
                mysearchlist = mysearchlist.filter(Gpu.sparseBinding == True)
            if textureCompressionETC2:
                mysearchlist = mysearchlist.filter(Gpu.textureCompressionETC2 == True)
            if vertextPipelineStoresandAtomics:
                mysearchlist = mysearchlist.filter(Gpu.vertexPipelineStoresAndAtomics == True)

        for i in mysearchlist:
            self.response.write(i.name + '<br/>' )