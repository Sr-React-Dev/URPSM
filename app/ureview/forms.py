from django.forms import ModelForm
from .models import ShopReview, ServerReview
from django.contrib.contenttypes.models import ContentType
from app.shop.models import Shop
from django.utils.translation import get_language
# shop_content_type = ContentType.objects.get(model='shop')
# print shop_content_type
from django.utils.translation import ugettext_lazy as _
from django.forms import Textarea, TextInput, CharField, ModelForm, ChoiceField,Select

RATINGS = (("",""),(1,1),(2,2),(3,3),(4,4),(5,5))

class ServerReviewForm(ModelForm):
    rating =  CharField(label=_('Your rating'), widget=Select(choices=RATINGS, attrs={'class': 'form-control'}))
    content        = CharField(label=_('Your Review'), 
        widget=Textarea(attrs={'class': 'form-control', 'placeholder': _('May be you like it...')}))

    class Meta:
        model  = ServerReview
        fields = ('content','rating',)

class ShopReviewForm(ModelForm):
    rating =  CharField(label=_('Your rating'), widget=Select(choices=RATINGS, attrs={'class': 'form-control'}))
    content        = CharField(label=_('Your Review'), 
        widget=Textarea(attrs={'class': 'form-control', 'placeholder': _('May be you like it...')}))

    class Meta:
        model  = ShopReview
        fields = ('content','rating',)
        
class ShopReviewAdminForm(ModelForm):
    class Meta:
        model = ShopReview
        exclude = ("content_type",'object_id', 'extra_objecty_id','extra_item',)

    def save(self, *args, **kwargs):
        # print args, kwargs
        if not self.instance.pk:
            # self.instance.user = self.user
            self.instance.language = get_language()
        # self.instance = super(ReviewForm, self).save(*args, **kwargs)
        self.instance.object_id=0
        self.instance.content_type_id=1
        self.instance.average_rating = self.instance.get_average_rating()
        print self.instance
        self.instance.save()
        return self.instance

    def clean_data(self):
        print self.clean_data
        if not 'content_type' in self.clean_data:
            self.clean_data['content_type'] = shop_content_type
        if not 'object_id' in self.clean_data:
            self.clean_data['object_id'] = 0
        return self.clean_data



