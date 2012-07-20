SMS SDK for android / sms
=========================

Development and prototyping platform
that can connect an android device to a django application

To use (after cloning)
----------------

__Installing on Django__

 1. From within the repository, type `sudo python setup.py install`. This will install the sms app.
 2. In your django requirements.txt file, add the line
    
    `-e git+http://github.com/louissobel/SMS-sdk.git#egg=dj_simple_sms`

    This will allow your heroku site to also use this app.
 3. Now go to the folder containing your django app.
 3. In the `INSTALLED_APPS` section of your settings.py file, add `'dj_simple_sms'`
 4. At the top of your main urls.py file, add `import dj_simple_sms`
 5. In your main urls.py file, add the urlpattern `url(r'^sms/', include(dj_simple_sms.urls))`
 6. In your settings.py file, add:
    
    ```python
    SMS_HANDLERS = (
        'dj_simple_sms.sample_sms_handler',
    )
    ```
 7. Install the tables for this new app using `python manage.py syncdb`

__Using on Django__

 1. Start your django app using `python manage.py runserver`
 2. Go the the admin page, and find the 'devices' model
 3. Click it, then add a new device (call it 'python sms' or anything you want)
 4. Back in the list view, you should now see a random key for that device. Copy it.
 2. In __another__ terminal window, go to the `python-client` folder
 3. Open up the file `main.py`
 4. Fill in the `DJANGO_KEY` setting with the key from the admin panel
 5. Check the `DJANGO_URL` setting to make sure that it matches the django app you have running
 6. Install the requirements for python-client: run the command `sudo pip install -r requirements.txt`
    from within the python-client folder
 3. Run `python main.py terminal django`
 4. Try sending a message from the terminal, monitoring the django output. You should see
    the message appear in the django terminal output.
 5. Go to your django admin, and create a new SMS. When you click send, you should see it appear in the
    terminal in which you are running `main.py` (note that this get mixed up with the "To:, From:" prompts
    but don't let that confuse you)
 7. Hooray! To now, to use your own SMS\_HANDLER function, add it to the SMS\_HANDLERS tuple.
 8. To quit the `main.py` program, hit `Ctrl-C`

