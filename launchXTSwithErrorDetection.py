#!/usr/bin/python

import mobiletestlib
import os
import sys

#== Main Flow ==

# Check Target is existed 檢查Target有沒有給
if(len(sys.argv) < 2):
  print 'You have to tell me the target:\n\n  ./launchXTSwithErrorDetection.sh TARGET'
  exit() # End up Script

# Run Test 要跑測試了
target = sys.argv[1]
mobiletestlib.testType = 'XTS' # 改為你的測試類型,給人類看的
mobiletestlib.deviceName = 'G2@Ntut' # 改為你要加的前綴,給人類看的

if(mobiletestlib.isPOSIX()):
  # POSIX(Unix-like) OS can run xts directly
  mobiletestlib.runTestProcess('exec ./xts-tradefed run xts --plan XTS --serial ' + target, target) # 直接下Command line
else:
  XTS_HOME = os.environ['XTS_HOME'] # Set Env Path Var just for Windows
  XTS_ROOT = os.environ['XTS_ROOT']
  # Run java because of Capturing Running STDOUT under WindowsNT Family Platform
  mobiletestlib.runWinTestProcess( ['java','-Xmx512M','-cp','%s\\tools\\xts-tradefed.jar;%s\\tools\\hosttestlib.jar;%s\\tools\\ddmlib-prebuilt.jar;%s\\tools\\tradefed-prebuilt.jar'%(XTS_HOME,XTS_HOME,XTS_HOME,XTS_HOME),'-DXTS_ROOT=%s'%(XTS_ROOT),'com.android.xts.tradefed.command.XtsConsole','run','xts','--plan','XTS','--serial',target], target)

exit()