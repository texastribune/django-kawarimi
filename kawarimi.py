"""
Steathfully replace Django templates based on the request.


Intro
~~~~~

If you want to dynamically change the ``{% extends ... %}`` in your Django
templates, you would normally have to use a variable ``{% extends
template_to_extend %}``. That sucks because you have to get that variable into
your context and now you can't grep for template names used. Django-Kawarimi
lets you switch to a parallel set of templates based on the request.


Usage
~~~~~

Add 'kawarimi.RequestMiddleWare' to your settings.MIDDLEWARE_CLASSES like::

    MIDDLEWARE_CLASSES = [
        'kawarimi.RequestMiddleWare',
        ...,
    ]

Add 'kawarimi.Loader' to the top of your settings.TEMPLATE_LOADERS. Since this
loader is just a fancy filesystem loader, you can remove
`django.template.loaders.filesystem.Loader` if you want::

    TEMPLATE_LOADERS = [
        'kawarimi.Loader',
        # 'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]

Finally, add ``KAWARIMI_TEMPLATES`` to your settings like:

    KAWARIMI_TEMPLATES = os.path.join(BASE_PATH, 'project/bizzaro_templates/')


A Warning
~~~~~~~~~

This is super sneaky. After adding this to your projects, you will find a
problem a few months later and have no idea what's going on. You will spend
hours trying to figure out the problem. You will discover that you changed the
template using this and curse me.


Prior Art
~~~~~~~~~

Based on work done in https://github.com/callowayproject/dynamicloader which was
based on https://github.com/johnboxall/django-ab. If you need more features, you
should check those projects out.
"""
from threading import local

from django.conf import settings
from django.template.loaders.filesystem import Loader as BaseLoader

_thread_locals = local()


class RequestMiddleWare(object):
    """
    A middleware that lets external code peek the request.
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
