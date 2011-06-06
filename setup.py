from setuptools import setup, find_packages

setup(
    name = 'OSP',
    version = '1.0',
    url = 'http://code.google.com/p/osp/',
    author = 'Central Piedmont Community College',
    description = ('Early warning system to improve retention rates '
                   'among high-risk students in higher education '
                   'institutions'),
    packages = find_packages(),
    include_package_data = True
)
