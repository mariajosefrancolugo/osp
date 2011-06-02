from distutils.core import setup
import os

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in
    a platform-neutral way.

    Courtesy of Django's own setup.py script
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't
# have an easy way to do this

# Courtesy of Django's own setup.py script
packages = []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
osp_dir = 'osp'

for dirpath, dirnames, filenames in os.walk(osp_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(fullsplit(dirpath)))

setup(
    name = 'OSP',
    version = '1.0',
    url = 'http://code.google.com/p/osp/',
    author = 'Central Piedmont Community College',
    description = 'Early warning system for higher education institutions',
    packages = packages
)
