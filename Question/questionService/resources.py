from import_export import resources
from .models import Question, ReferenceLink, Image

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question

class ReferenceLinkResource(resources.ModelResource):
    class Meta:
        model = ReferenceLink
        
class ImageResource(resources.ModelResource):
    class Meta:
        model = Image