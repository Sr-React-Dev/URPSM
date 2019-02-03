from django import forms
from django.utils.html import mark_safe



class AdminImageWidget(forms.FileInput):

    """A ImageField Widget for admin that shows a thumbnail."""

    def __init__(self, attrs={}):   # pylint: disable=E1002,W0102
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):  # pylint: disable=E1002
        output = []
        css = {'style': 'clear:left;float:left;margin:1em 1em 0 0;'}
        output.append(super(AdminImageWidget, self).render(name, value,
                                                           attrs=css))
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img class="img-polaroid" src="%s" alt="" '
                           'style="float:right;width:64px;height:64px;" /></a>'
                           % (value.url, value.url)))
        return mark_safe(u''.join(output))


class FrontImageWidget(forms.FileInput):

    """A ImageField Widget for admin that shows a thumbnail."""

    def __init__(self, attrs={}):   # pylint: disable=E1002,W0102
        super(FrontImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):  # pylint: disable=E1002
        output = []
        css = {'style': 'display:block; clear:left;margin:1em 1em 0 0;'}
        output.append(super(FrontImageWidget, self).render(name, value,
                                                           attrs=css))
        # print value.url
        if value and hasattr(value, "url"):
            output.append(('<br/><div class="row"><div class="col-md-12">'
                           '<img class="img img-responsive img-thumbnail" src="%s" alt="" '
                           'style="width:64px;height:64px;" /></div></div>'
                           % (value.url)))
        return mark_safe(u''.join(output))
