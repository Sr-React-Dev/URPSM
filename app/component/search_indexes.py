# from haystack import indexes
from .models import Component
from app.component.models import Component

class ComponentIndex(indexes.SearchIndex, indexes.Indexable):
	text        = indexes.CharField(document=True, use_template=True)
	name_auto   = indexes.EdgeNgramField(model_attr='title')
	
	      

	def get_model(self):
		return Component

	def index_queryset(self, using=None):
		return self.get_model().objects.filter(sold=False, deleted=False)