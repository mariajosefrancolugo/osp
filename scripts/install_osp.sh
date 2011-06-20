#!/bin/bash

# Upgrade all core packages
sudo apt-get update
sudo apt-get upgrade

# Install prerequisite packages
sudo apt-get install apache2 build-essential libapache2-mod-wsgi libldap2-dev libmysqlclient-dev libsasl2-dev libssl-dev mercurial mysql-server python-dev  python-setuptools vim

# Secure MySQL installation
sudo mysql_secure_installation

# Install virtualenv
sudo easy_install virtualenv
sudo easy_install virtualenvwrapper

# Create directory to store virtualenvs
sudo mkdir /opt/virtualenv
sudo chown -R $USER:$USER /opt/virtualenv

# Set virtualenv configuration settings
export WORKON_HOME=/opt/virtualenv
source /usr/local/bin/virtualenvwrapper.sh

# Create virtualenv for OSP
mkvirtualenv -p /usr/bin/python2.6 --no-site-packages osp

# Install prerequisite Python packages
easy_install mysql-python==1.2.3 python-ldap==2.3.13 xlwt==0.7.2 django==1.2.5 django-auth-ldap==1.0.9 django-cas==2.0.3

# Create directory to store Django apps
sudo mkdir /opt/django
sudo chown -R $USER:$USER /opt/django

# Clone OSP repository
cd /opt/django
hg clone https://osp.googlecode.com/hg/ osp

# Collect information from the user to create the MySQL database for OSP
echo "Collecting MySQL database information..."
echo -n "Choose a MySQL database name: "
read MYSQL_DATABASE
echo -n "Choose a MySQL username: "
read MYSQL_USERNAME
PASSWORDS_MATCH=false
while [ $PASSWORDS_MATCH == "false" ]
do
	echo -n "Choose a MySQL password: "
	stty -echo
	read MYSQL_PASSWORD_1
	stty echo
	echo ""
	echo -n "Confirm your MySQL password: "
	stty -echo
	read MYSQL_PASSWORD_2
	stty echo
	if [ $MYSQL_PASSWORD_1 == $MYSQL_PASSWORD_2 ]
	then
		PASSWORDS_MATCH=true
	else
		echo ""
		echo "Passwords do not match. Try again."
	fi
done
# Create MySQL database
echo ""
echo "Prompting for MySQL root password..."
mysql -u root -p<<EOFMYSQL
CREATE DATABASE $MYSQL_DATABASE;
GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO $MYSQL_USERNAME@localhost IDENTIFIED BY '$MYSQL_PASSWORD_1';
EOFMYSQL

# Create directory to store WSGI configuration files
sudo mkdir /opt/wsgi
sudo chown -R $USER:$USER /opt/wsgi

# Copy WSGI configuration files from OSP respository
cp /opt/django/osp/deploy/osp.wsgi /opt/django/osp/deploy/osp_settings.py /opt/wsgi/

# Open Django settings file for editing
vim /opt/wsgi/osp_settings.py

# Create the Django database tables and superuser account
export PYTHONPATH=$PYTHONPATH:/opt/wsgi:/opt/django/osp
django-admin.py syncdb --settings=osp_settings

# Overwrite default Apache configuration file with OSP one
sudo cp /opt/django/osp/deploy/osp.conf /etc/apache2/sites-available/default

# Create directory for Python egg cache and assign correct ownership
sudo mkdir /var/www/python-eggs
sudo chown -R www-data:www-data /var/www

# Symlink Django admin media directory into OSP media directory
ln -s /opt/virtualenv/osp/lib/python2.6/site-packages/Django-1.2.5-py2.6.egg/django/contrib/admin/media /opt/django/osp/osp/media/admin

# Restart Apache
sudo /etc/init.d/apache2 restart
