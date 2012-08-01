__Using with just Django__

 1. Make sure you have installed the dj\_simple\_sms app in your django project
 6. In your settings.py file, add:
   
	```python
	SMS_HANDLERS = (
	    'dj_simple_sms.sample_sms_handler',
	)
	```
	
 1. Start your django app using `python manage.py runserver`
 2. Go the the admin page, and find the 'Devices' model
 3. Click it, then add a new device (call it 'python sms' or anything you want)
 4. Back in the list view, you should now see a random key for that device. Copy it.
 2. In __another__ terminal window, go to the `sms_pipeline` folder
 3. Open up the file `pipeline.py`
 4. Fill in the `DJANGO_KEY` setting with the key you copied from the admin panel
 5. Check the `DJANGO_URL` setting to make sure that it matches the django app you have running
 6. Install the requirements for the sms\_pipeline:
     - `pip install -r requirements.txt`
 3. Run `python pipeline.py terminal django`
 5. You should see some output indicating that things have started up, and a prompt, "To: "
 4. Try sending a message from the terminal, by manually entering data for the "To:", 
    "From:", and "Body:" fields. Watch the terminal that django is running in - you should see your
    message appear there.
 5. Go again to your django admin, and create a new SMS. When you click save, you should see it appear in the
    terminal in which you are running `pipeline.py` (note that this may get mixed up with the "To:, From:" prompts,
	but don't worry about it).
 7. Hooray! To use your own function to do something interesting with a received SMS,
    write a function similar to the `sample_sms_handler` and add a string with its python path
    to the SMS\_HANDLERS tuple.
 8. To quit the `pipeline.py` program, hit `Ctrl-C`

__Using with just Android__

 2. Go to the folder containing the `adb` command and run `./adb -d forward tcp:7800 tcp:7800`. This sets up your computer to forward
    all communication on port 7800 of your computer to port 7800 of the android device.
 3. On the android device, start the SMSToolkit program. Don't quit it!
 4. Go to the `sms_pipeline` folder, and run `python pipeline.py android terminal`.
 5. If there are no error messages, try sending a SMS from the terminal to your own phone number. Then try sending one back. Hooray!
 6. To quit the main program, press `Ctl-C`


__Using with Django and Android__

If:
 
 - `python pipeline.py android terminal` is working
 - `python pipeline.py terminal django` is working

Then connecting your android phone to your Django application is as simple as:

 `python pipeline.py android django`
