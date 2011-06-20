#!/bin/bash

# Upgrade all core packages
sudo apt-get update
sudo apt-get upgrade

# Install prerequisite packages
sudo apt-get install apache2 build-essential libapache2-mod-wsgi libldap2-dev libmysqlclient-dev libsasl2-dev libssl-dev mercurial mysql-server python-dev  python-setuptools vim

echo -n "Secure MySQL installation? [Y/n] "
read SECURE_MYSQL

if [ "$SECURE_MYSQL" == "Y" ] || [ "$SECURE_MYSQL" == "y" ] || [ "$SECURE_MYSQL" == "" ]
then
    SECURE_MYSQL="y"
else
    SECURE_MYSQL="n"
fi

if [ $SECURE_MYSQL == "y" ]
then
    # Secure MySQL installation
    sudo mysql_secure_installation
fi

# Install virtualenv
sudo easy_install virtualenv virtualenvwrapper

if [ ! -d "/opt/virtualenv" ]
then
    # Create directory to store virtualenvs
    sudo mkdir /opt/virtualenv
fi

# Correct ownership of virtualenv directory
sudo chown -R $USER:$USER /opt/virtualenv

# Set virtualenv configuration settings
export WORKON_HOME=/opt/virtualenv
source /usr/local/bin/virtualenvwrapper.sh

if [ ! -d "/opt/virtualenv/osp" ]
then
    # Create virtualenv for OSP
    mkvirtualenv -p /usr/bin/python2.6 --no-site-packages osp
fi

# Make sure we're inside the right virtualenv
workon osp

# Install prerequisite Python packages
easy_install mysql-python==1.2.3 python-ldap==2.3.13 xlwt==0.7.2 django==1.2.5 django-auth-ldap==1.0.9 django-cas==2.0.3


if [ ! -d "/opt/django" ]
then
    # Create directory to store Django apps
    sudo mkdir /opt/django
fi

# Correct ownership of Django directory
sudo chown -R $USER:$USER /opt/django

if [ ! -d "/opt/django/osp" ]
then
    mkdir /opt/django/osp
    cd ..
    cp -R * /opt/django/osp
fi

# Collect information from the user to create the MySQL database for OSP
echo -n "Create MySQL database? [Y/n] "
read CREATE_DATABASE

if [ "$CREATE_DATABASE" == "Y" ] || [ "$CREATE_DATABASE" == "y" ] || [ "$CREATE_DATABASE" == "" ]
then
    CREATE_DATABASE="y"
else
    CREATE_DATABASE="n"
fi

if [ $CREATE_DATABASE == "y" ]
then
    echo "Collecting MySQL database information..."
    echo -n "Choose a MySQL database name: "
    read MYSQL_DATABASE
    echo -n "Choose a MySQL username: "
    read MYSQL_USERNAME
    PASSWORDS_MATCH="false"
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
            PASSWORDS_MATCH="true"
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
fi

if [ ! -d "/opt/wsgi" ]
then
    # Create directory to store WSGI configuration files
    sudo mkdir /opt/wsgi
fi

# Correct ownership of WSGI directory
sudo chown -R $USER:$USER /opt/wsgi

echo -n "Copy WSGI configuration files? [Y/n] "
read COPY_WSGI_CONFIG

if [ "$COPY_WSGI_CONFIG" == "Y" ] || [ "$COPY_WSGI_CONFIG" == "y" ] || [ "$COPY_WSGI_CONFIG" == "" ]
then
    COPY_WSGI_CONFIG="y"
else
    COPY_WSGI_CONFIG="n"
fi

if [ $COPY_WSGI_CONFIG == "y" ]
then
    # Copy WSGI configuration files from OSP respository
    cp /opt/django/osp/deploy/osp.wsgi /opt/django/osp/deploy/osp_settings.py /opt/wsgi/
fi

# Open Django settings file for editing
echo "Opening Django settings file for editing..."
sleep 3
vim /opt/wsgi/osp_settings.py

echo -n "Create Django database tables and superuser account? [Y/n] "
read DO_SYNCDB

if [ "$DO_SYNCDB" == "Y" ] || [ "$DO_SYNCDB" == "y" ] || [ "$DO_SYNCDB" == "" ]
then
    DO_SYNCDB="y"
else
    DO_SYNCDB="n"
fi

if [ $DO_SYNCDB == "y" ]
then
    # Create the Django database tables and superuser account
    export PYTHONPATH=$PYTHONPATH:/opt/wsgi:/opt/django/osp
    django-admin.py syncdb --settings=osp_settings
fi

echo -n "Copy Apache configuration files? [Y/n] "
read COPY_APACHE_CONFIG

if [ "$COPY_APACHE_CONFIG" == "Y" ] || [ "$COPY_APACHE_CONFIG" == "y" ] || [ "$COPY_APACHE_CONFIG" == "" ]
then
    COPY_APACHE_CONFIG="y"
else
    COPY_APACHE_CONFIG="n"
fi

if [ $COPY_APACHE_CONFIG == "y" ]
then
    # Overwrite default Apache configuration file with OSP one
    sudo cp /opt/django/osp/deploy/osp.conf /etc/apache2/sites-available/default
fi

if [ ! -d "/var/www/python-eggs" ]
then
    # Create directory for Python egg cache
    sudo mkdir /var/www/python-eggs
fi

# Correct ownership of Python egg cache directory
sudo chown -R www-data:www-data /var/www

if [ ! -L "/opt/django/osp/osp/media/admin" ]
then
    # Symlink Django admin media directory into OSP media directory
    ln -s /opt/virtualenv/osp/lib/python2.6/site-packages/Django-1.2.5-py2.6.egg/django/contrib/admin/media /opt/django/osp/osp/media/admin
fi

# Restart Apache
sudo /etc/init.d/apache2 restart
