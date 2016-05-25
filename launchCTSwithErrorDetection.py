#!/usr/bin/python

import mobiletestlib
import os
import sys

#== Main Flow ==

# Check Target is existed 檢查Target有沒有給
if(len(sys.argv) < 2):
  print 'You have to tell me the target:\n\n  ./launchCTSwithErrorDetection.sh TARGET'
  exit() # End up Script

# Run Test 要跑測試了
target = sys.argv[1]
mobiletestlib.testType = 'CTS' # 改為你的測試類型,給人類看的
mobiletestlib.deviceName = 'G2@inhon' # 改為你要加的前綴,給人類看的

mobiletestlib.runTestProcess('exec ./cts-tradefed run singleCommand cts --plan CTS --serial ' + target, target) # 直接下Command line

exit()
