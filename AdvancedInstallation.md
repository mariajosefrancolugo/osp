# Prerequisites #

Online Student Profile requires the following system packages:

  * Apache
  * mod\_wsgi
  * MySQL
  * Python

OSP has been thoroughly tested with Apache 2.2, MySQL 5.1, and Python 2.6. Using versions other than these may yield unexpected results. Please submit any bugs you encounter.

OSP also requires the following Python packages. It is recommended that you install these via either `easy_install` or `pip`.

  * mysql-python
  * python-ldap
  * xlwt
  * django
  * django-auth-ldap
  * django-cas
  * south

It is recommended that you run OSP inside a virtual environment, if possible, but that is outside the scope of this document.

# Installation #

The first step in the process is to create directories to house the various components of OSP.

<pre>
$ sudo mkdir -p /opt/django/osp<br>
$ sudo mkdir /opt/wsgi<br>
</pre>

Next, you'll want to download and extract the latest OSP source tarball. You can find the latest package on the [Downloads](http://code.google.com/p/osp/downloads/list) page.

Once you've extracted the tarball, you're going to copy the necessary files to their appropriate locations.

<pre>
$ cd osp/<br>
$ cp -R * /opt/django/osp<br>
$ cp /opt/django/osp/deploy/osp_settings.py /opt/wsgi/<br>
</pre>

Next, you're going to create a WSGI configuration file for OSP. This will be saved to `/opt/wsgi/osp.wsgi`. Here is an example script for you to start with. Adjust the paths as necessary:

```python

import os
import site
import sys

# Add the app code to the path
sys.path.append('/opt/django/osp')

# Add wsgi directory to path
sys.path.append('/opt/wsgi')

# Set DJANGO_SETTINGS_MODULE env var
os.environ['DJANGO_SETTINGS_MODULE'] = 'osp_settings'

# Start the app
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
```

You'll want to create an Apache configuration to pair with your WSGI configuration. Here is an example config to start with. Adjust the paths as necessary:

```
<VirtualHost *:80>
ServerAdmin webmaster@localhost

ErrorLog /var/log/apache2/error.log
CustomLog /var/log/apache2/access.log combined

Alias /media/  /opt/django/osp/osp/media/

<Directory /opt/django/osp/osp/media>
Order deny,allow
Allow from all


Unknown end tag for &lt;/Directory&gt;



WSGIScriptAlias / /opt/wsgi/osp.wsgi

<Directory /opt/wsgi>
Order allow,deny
Allow from all


Unknown end tag for &lt;/Directory&gt;




Unknown end tag for &lt;/VirtualHost&gt;

```