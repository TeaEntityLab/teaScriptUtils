#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import mobiletestlib

# Check Target is existed
if(len(sys.argv) < 1 + 1):
  print 'You have to tell me the package and the target:\n\n  ./runEachTestWithDelay TARGET'
  exit() # End up Script

# Run Test 要跑測試了
target = sys.argv[1]
mobiletestlib.rebootWaitingTime = 2 # Wait 2 minutes
mobiletestlib.testType = 'CTS' # 改為你的測試類型,給人類看的
mobiletestlib.deviceName = 'G2@inhon' # 改為你要加的前綴,給人類看的
mobiletestlib.runAllByTestcase('exec ./cts-tradefed run singleCommand cts --screenshot --serial ' + target, target)

exit()
