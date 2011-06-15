from setuptools import setup, find_packages

setup(
    name = 'OSP',
    version = '1.0b2',
    url = 'http://code.google.com/p/osp/',
    author = 'Central Piedmont Community College',
    description = ('Early warning system to improve retention rates '
                   'among high-risk students in higher education '
                   'institutions'),
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Education',
        ('License :: OSI Approved :: GNU Library or Lesser General '
         'Public License (LGPL)'),
        'Programming Language :: Python',
        'Programming Language :: JavaScript'
    ]
)
