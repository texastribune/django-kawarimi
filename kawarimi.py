"""
Load special templates based on the request.

Usage
~~~~~

Add 'kawarimi.RequestMiddleWare' to your settings.MIDDLEWARE_CLASSES.

Add 'kawarimi.Loader' to the top of your settings.TEMPLATE_LOADERS. Since this
loader is just a fancy filesystem loader, you can remove
`django.template.loaders.filesystem.Loader` if you want.


Based on work done in https://github.com/callowayproject/dynamicloader which
was based on https://github.com/johnboxall/django-ab
"""
from threading import local

from django.conf import settings
from django.template.loaders.filesystem import Loader as BaseLoader

_thread_locals = local()


class RequestMiddleWare(object):
    """
    A middleware that lets external code peek the request.

    WISHLIST common logic between this and `Loader` to change the content_type
    to application/json ?
    """
    def process_request(self, request):
        _thread_locals.request = request

    @staticmethod
    def get_current_request():
        return getattr(_thread_locals, 'request', None)



class Loader(BaseLoader):
    """
    A loader that uses `settings.KAWARIMI_TEMPLATES` depending on the request.

    Subclasses `django.template.loaders.filesystem.Loader` to get its juicy
    `load_template_source`.
    """
    is_usable = True  # reiterate this even though BaseLoader has this

    def get_template_sources(self, template_name, template_dirs=None):
        request = RequestMiddleWare.get_current_request()
        # this line is the magic:
        serve_json = ('application/json+kawarimi' in
                request.META['HTTP_ACCEPT'].split(','))
        if serve_json:
            # TODO raise ImproperlyConfigured if this setting does not exist
            template_dirs = (settings.KAWARIMI_TEMPLATES, )

        # act like nothing happened
        return super(Loader, self).get_template_sources(
                template_name, template_dirs)
