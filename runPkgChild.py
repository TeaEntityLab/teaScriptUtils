#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import mobiletestlib

# Check Target is existed
if(len(sys.argv) < 2 + 1):
  print 'You have to tell me the package and the target:\n\n  ./runPkgChild TARGET PKG'
  exit() # End up Script

# Run Test 要跑測試了
pkg = sys.argv[2]
target = sys.argv[1]
mobiletestlib.testType = 'CTS' # 改為你的測試類型,給人類看的
mobiletestlib.deviceName = 'G2@inhon' # 改為你要加的前綴,給人類看的
mobiletestlib.runPkgChild('exec ./cts-tradefed run singleCommand cts --serial ' + target, pkg, target)

exit()
