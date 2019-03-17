from google.appengine.ext import ndb

class Gpu(ndb.Model):
    name = ndb.StringProperty()
    manufacturer  = ndb.StringProperty()
    dateissued = ndb.DateProperty()
    geometryShader= ndb.BooleanProperty()
    tesselationShader =ndb.BooleanProperty()
    shaderInt16 = ndb.BooleanProperty()
    sparseBinding = ndb.BooleanProperty()
    textureCompressionETC2 = ndb.BooleanProperty()
    vertexPipelineStoresAndAtomics = ndb.BooleanProperty()