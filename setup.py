from setuptools import setup

setup(
    name='django-kawarimi',
    version='0.0.0',
    author='The Texas Tribune',
    author_email='tech@texastribune.org',
    url='https://github.com/texastribune/django-kawarimi',
    maintainer_email='c@crccheck.com',
    license='Apache',
    py_modules=['kawarimi'],
    include_package_data=True,
    platform='any',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Ninjas',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
