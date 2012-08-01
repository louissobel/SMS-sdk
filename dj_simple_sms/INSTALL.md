__Installing dj\_simple\_sms on Django__

 1. Make sure that `dj_simple_sms` is on your python path
     - either install it using `setup.py install`
     - or just move the folder into your django project directory
 3. In the `INSTALLED_APPS` section of your settings.py file, add `'dj_simple_sms'`
 4. At the top of your main urls.py file, add `import dj_simple_sms`
 5. In your main urls.py file, add the urlpattern `url(r'^sms/', include(dj_simple_sms.urls))`
 7. Install the tables for this new app using `python manage.py syncdb`

