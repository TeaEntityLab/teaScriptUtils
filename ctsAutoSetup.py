#!/usr/bin/python
# -*- coding: utf-8 -*-

# This must be imported before MonkeyRunner and MonkeyDevice,
# otherwise the import fails.

import os, sys

try:
    for p in os.environ['PYTHONPATH'].split(':'):
        if not p in sys.path:
            sys.path.append(p)
except:
    pass
    
try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
    # sys.path.append('./avc')
except:
    pass

sys.path.append('/home/teee/scriptRepo/avc')
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyView
from com.dtmilano.android.viewclient import ViewClient, View



package = 'com.android.settings'
activity = '.Settings'
component_name = package + '/' + activity
EXCLUDE_FROM_RECENTS = 0x00800000
ap_name = "Put acces point name here"

# Connect to device with the IP received as a parameter
device, serialno = ViewClient.connectToDeviceOrExit()

width = int(device.getProperty('display.width'))
height = int(device.getProperty('display.height'))

# Press the HOME button to start the test from the home screen
device.press('KEYCODE_HOME','DOWN_AND_UP')
MonkeyRunner.sleep(2)

# Open the Settings app
device.startActivity(component = component_name, flags = EXCLUDE_FROM_RECENTS)
i = 0
while str(device.getProperty('am.current.package')) != package and i<10:
   MonkeyRunner.sleep(1)
   i = i + 1
if i == 10:
   raise Exception('Cannot open package')

# Create the view client object
vc = ViewClient(device=device, serialno=serialno)

# Enable Wi-Fi
device.shell("svc wifi enable")
i = 0
while not vc.findViewWithText(ap_name) and i<30:
    MonkeyRunner.sleep(1)
    vc.dump()
    i += 1
if i == 30:
    print "Cannot enable Wi-Fi"
for i in range(5):
    device.press('KEYCODE_DPAD_RIGHT', MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(0.5)
device.press('KEYCODE_DPAD_LEFT', MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(0.5)
device.press('KEYCODE_ENTER', MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(2)
device.type(ap_name)
vc.dump()
if vc.findViewWithText('Save'):
    vc.findViewWithText('Save').touch()
    MonkeyRunner.sleep(5)

# Set Screen Lock to None
drag_start = (width*1/4, height*9/10)
drag_end = (width*1/4, height*1/10)
device.drag(drag_start, drag_end)
vc.dump()
if vc.findViewWithText('Security'):
    vc.findViewWithText('Security').touch()
MonkeyRunner.sleep(1)
vc.dump()
if vc.findViewWithText('Screen lock'):
    vc.findViewWithText('Screen lock').touch()
MonkeyRunner.sleep(1)
vc.dump()
if vc.findViewWithText('None'):
    vc.findViewWithText('None').touch()
MonkeyRunner.sleep(1)
vc.dump()

# Activate device administrator
if vc.findViewWithText('Device administrators'):
    vc.findViewWithText('Device administrators').touch()
MonkeyRunner.sleep(1)
vc.dump()
admin1 = vc.findViewWithText('android.deviceadmin.cts.CtsDeviceAdminReceiver')
if admin1:
    for aux_view in admin1.parent.parent.children:
        if aux_view['class'] == 'android.widget.CheckBox':
            break
    if aux_view['checked'] == 'false':
        admin1.touch()
        MonkeyRunner.sleep(1)
        vc.dump()
        if vc.findViewWithText('Activate'):
            vc.findViewWithText('Activate').touch()
MonkeyRunner.sleep(1)
vc.dump()
admin2 = vc.findViewWithText('android.deviceadmin.cts.CtsDeviceAdminReceiver2')
if admin2:
    for aux_view in admin2.parent.parent.children:
        if aux_view['class'] == 'android.widget.CheckBox':
            break
    if aux_view['checked'] == 'false':
        admin2.touch()
        MonkeyRunner.sleep(1)
        vc.dump()
        if vc.findViewWithText('Activate'):
            vc.findViewWithText('Activate').touch()
MonkeyRunner.sleep(1)

# Enable Delegating Accessibility Service
MonkeyRunner.sleep(1)
vc.dump()
if vc.findViewWithText('Accessibility'):
    vc.findViewWithText('Accessibility').touch()
MonkeyRunner.sleep(1)
vc.dump()
if vc.findViewWithText('Delegating Accessibility Service'):
    vc.findViewWithText('Delegating Accessibility Service').touch()
MonkeyRunner.sleep(1)
for count in range(5):
    device.press('KEYCODE_DPAD_RIGHT', MonkeyDevice.DOWN_AND_UP)
    MonkeyRunner.sleep(0.5)
device.press('KEYCODE_ENTER', MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(1)
vc.dump()
MonkeyRunner.sleep(1)
if vc.findViewWithText('Use Delegating Accessibility Service?'):
    vc.findViewWithText('OK').touch()
else:
    vc.findViewWithText('Cancel').touch()
MonkeyRunner.sleep(1)
