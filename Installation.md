# Introduction #

**This is a draft installation instruction**

python-electric requires the following software in order to use all features
  * [Apache](http://httpd.apache.org/docs/2.0/install.html)
  * [Python 2.7](http://www.python.org/download/releases/2.7/)
  * [Django 1.4](http://docs.djangoproject.com/en/dev/topics/install/)
  * [MySQL](http://dev.mysql.com/doc/refman/5.1/en/installing.html)
  * [matplotlib](http://matplotlib.sourceforge.net/users/installing.html)
  * [GChartWrapper](http://code.google.com/p/google-chartwrapper/source/checkout)

If you only need to collect the data from the TED 5000, you only need MySQL and Python.

It is best to follow the installation instructions linked on the packages above for your specific OS.  Then download python-electric to a directory of your choice:

> `# cd /home/username/path/to/projects/`

> `# svn checkout http://python-electric.googlecode.com/svn/trunk/ python-electric`

make sure python-electric is on the python path.

If you do not have a database capturing TED data, run the following command from the python-electric directory to create the tables:

> `# python manage.py syncdb`

You have two options to serve the static media files:

Create a symbolic link to the python-electric and Django admin media files from within your Apache document root. This way, all of your Django-related files -- code and templates -- stay in one place, and you'll still be able to svn update your code to get the latest templates, if they change.

> `# cd /var/www/media/`

> `# sudo ln -s /path/to/python_electric/media/ python_electric`

Or, copy the media files so that they live within your Apache document root.

> `# cd /var/www/media/`

> `# sudo cp  /path/to/python_electric/media/ python_electric (??)`

add a crontab job:

> `# sudo crontab -e`

add the following line to crontab (ie. for every five minutes):

> `*/5 * * * * python /path/to/python_electric/apps/electric/iterator.py`

Configure [WSGI](http://docs.djangoproject.com/en/dev/howto/deployment/modwsgi/) to serve static media files.