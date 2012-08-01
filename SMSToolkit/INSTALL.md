__Installing for Android__

 1. Download and install the Android SDK for your system.
 2. Open up the SDK manager and install the Platform Tools for your platform
     - Note that it is not necessary for you to install any libraries, just the platform tools
 3. Navigate to the 'platform-tools' directory in your sdk folder
 4. Plug in a working android phone running version 1.6 or higher.
 5. Follow the instructions on android's site [here](http://developer.android.com/tools/device.html)
    and make sure that your device is visible using the command `./adb devices`
 6. Install the toolkit on your phone using  `./adb install -d /PATH/TO/SMS-sdk/SMSToolkit/SMSToolkit.apk`
    (where `/PATH/TO` is the path to the folder holding the SMS-sdk folder)
    This will install the toolkit software on the android device.