SMS SDK for android / sms
=========================

Development and prototyping platform
that can connect an android device to a django application

To use (after cloning)
----------------

__Installing on Django__

 1. Copy and paste the dj\_simple\_sms folder into your django project
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


__Installing for Android__

 1. Download and install the Android SDK for your system. Note that it is not necessary for you to install any libraries,
    what is important is the Android Debug Bridge (adb) program that comes with the SDK.
 2. Plug in the working android phone to your computer using a USB connector.
 3. Go to the folder '.../platform-tools' that contains the adb program.
 4. Run `adb install -d /PATH/TO/sms_sdk/SMSToolkit.apk` (where `/PATH/TO` is the path to the folder holding the sms_sdk folder)
    This will install the toolkit software on the android device.

__Using on Android__

 1. Make sure that the Android device is plugged in and is turned on.
 2. Go to the folder containing the `adb` command and run `adb -d forward tcp:7800 tcp:7800`. This sets up your computer to forward
    all communication on port 7800 of your computer to port 7800 of the android device.
 3. On the android device, start the SMSToolkit program. Don't quit it, or you will have to manually shut it down to start a new one.
 4. Go to the `python-client` folder, and run `python main.py android terminal`.
 5. If there are no error messages, try sending a SMS from the terminal to your own phone number. Then try sending one back. Hooray!
 6. To quit the main program, press `Ctl-C`

__Using with Django and Android__

 1. Follow the steps in `Using on Django` and `Using on Android` but just don't run the main program.
 2. Then, run `python main.py android django` and you can now send and receive messages in your Django app to and from any phone number.
 

