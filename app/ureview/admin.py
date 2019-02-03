"""Admin classes for the review app."""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# from hvad.admin import TranslatableAdmin

from .models import ShopReview, ServerReview
# from forms import ShopReviewAdminForm

# class URPSMRatingAdmin(admin.ModelAdmin):
#     list_display = ['review', 'category', 'value', ]
#     raw_id_fields = ['review', ]


class ShopReviewAdmin(admin.ModelAdmin):
    model         = ShopReview
    list_display = [ 'shop', 'user', 'language', 'creation_date']
    # exclude      = ['content_type', 'object_id','extra_object_id','extra_content_type']

class ServerReviewAdmin(admin.ModelAdmin):
    model         = ServerReview
    list_display = ['server', 'user', 'language', 'creation_date']
    # exclude      = ['content_type', 'object_id','extra_object_id','extra_content_type']


# class URPSMReviewExtraInfoAdmin(admin.ModelAdmin):
#     list_display = ['type', 'review', 'content_object']


# class URPSMReviewCategoryChoiceAdmin(TranslatableAdmin):
#     list_display = ['ratingcategory', 'value', 'get_label']
#     list_select_related = []

#     def get_label(self, obj):
#         return obj.label
#     get_label.short_description = _('Label')

admin.site.register(ShopReview, ShopReviewAdmin)
admin.site.register(ServerReview, ServerReviewAdmin)
# admin.site.register(models.RatingCategory, TranslatableAdmin)
# admin.site.register(models.Review, URPSMReviewAdmin)
# admin.site.register(models.ReviewExtraInfo, URPSMReviewExtraInfoAdmin)
# admin.site.register(models.RatingCategoryChoice, URPSMReviewCategoryChoiceAdmin)
