SMS SDK for android / django
=========================

Development and prototyping platform
that can connect an android device to a django application

What is here?
-----------------

This repository has three main components:

 1. dj\_simple\_sms - A django app that exposes an endpoint and
    logic to receive, process, and send SMSs
 2. SMSToolkit - An android application that runs a server on an
    Android device that is available to send and receive text messages.
 3. sms\_pipeline - a python application that is capable of connecting
    the Android device to a running django app. It also has the ability
    to use both of them in isolation.

Instructions for setting up the individual components can be found in a INSTALL.md
file with the subfolder.

Instructions for using the sms\_pipeline to develop with SMS are found in the INSTRUCTIONS.md file.

There's also a django project, `smstest` that you can use to test just by adding a symlink to dj\_simple\_sms:
`ln -s dj_simple_sms sms_test/dj_simple_sms`

 

