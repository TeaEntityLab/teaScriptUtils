# -*- coding: utf-8 -*-
import os
import platform
import sys
import signal
import subprocess
import re
import datetime
import time
import smtplib
import ctypes
from email.mime.text import MIMEText

import ctsparsinglib

#== Constants 常數 ==

# The Test Process 測試的Process,為Global變數
theProcess = None

# From,To 寄件者, 收件者
fromPeople = 'inhoncts@gmail.com' # 你所用來寄信的Email
toList = ['john.lee@inhon.com', 'gohome.lee@inhon.com', 'kathy.chang@inhon.com'] # 收件者,可以自己改
toPeople = ", ".join(toList) # Separate with comma 把他們以隔號分隔,合成單一字串
testType = 'CTS' # Default CTS 測試類型,用來寄信及紀錄LOG使用(給人類看的)
deviceName = '' # Default Device Name 裝置的Serial ID
rebootWaitingTime = 5 # Default 5(mins) 五分鐘

#== Process Functions == 與Process相關的Function

# For Debug 只是除錯用
def checkProcess(p):
  if( theProcess == None):
    print 'None'
  else:
    print 'Running'

# Run Process 實際去執行一個Process(Under Unix-like)
def runProcess(exe):
  # Open Process 開啟(Unix-like)Process
  p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
  checkProcess(p)
  #
  global theProcess # Tell python theProcess is global one, not local one 告知Python要存取Global變數
  theProcess = p # Update global CTS to New Process 將全域的Process設為新產生的Process
  #
  while(True):
    retcode = theProcess.poll() # Returns None while subprocess is running 若回傳None則Process還活著
    line = theProcess.stdout.readline()
    yield line
    if(retcode is not None): # 不為None,則Process死了
      break

# Run Process in Windows 在Win下的執行Process
def runWinProcess(exe):
  # Open Process 開啟Process(Win)
  p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize = 0, creationflags=0x208)
  checkProcess(p)
  #
  global theProcess # Tell python theProcess is global one, not local one 告知Python要存取Global變數
  theProcess = p # Update global CTS to New Process 將全域的Process設為新產生的Process
  return

# Kill Process 殺程序
def killProcess(p):
  if( isPOSIX() ): # 若為Unix-like
    os.killpg(p.pid, signal.SIGKILL) # Send SIGKILL to the process group 傳送Kill sig
  else:
    ctypes.windll.kernel32.TerminateProcess(int(p._handle), -1) # Windows Kill Method 在Win下的專屬方法

#== Parsing String Functions == 字串分析函數

# Parsing Packages' result 分析總結字串
def parseResultInformation(info):
  m = re.search(r'.*\sPassed\s(\d*),\sFailed\s(\d*),\sNot\sExecuted\s(\d*).*', info) # Package Report Pattern 每個Package回報總結的字串Pattern
  if(m is not None): # Detect Package Report 若有偵測到
    FailedCount = m.group(2) # Second Match(\d*) is Failed Count 第二個Match到的數字,是Failed數
    NotExecutedCount = m.group(3) # Third Match(\d*) is Not Excuted Count 第三個Match到的數字,是未執行數
    return str( int(FailedCount) + int(NotExecutedCount) ) # Return the Count Num 回傳兩者加總
  else:
    return '0' # Return non-err(=0) 若沒看到任何總結,就當它沒錯吧

# Parse test case result 分析單一測試
def isAnyFailed(info):
  m = re.search(r'\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s.*\sFAIL\b', info) # Testcase Err Pattern 單一測試
  if(m is not None or parseResultInformation(info) != '0'): # If any error 若有任何錯或者總結有問題,就算錯
    return True
  else:
    return False

#== Main Test Running Process == 主要的進行流程

# Reset and Start Test 重設並重新開始測試
def resetTestEnv(target):
  # TODO Remaining Factory Reset 還欠FactoryReset
  subprocess.Popen('adb -s ' + target + ' reboot', shell=True)# Reboot the specific device 重開目標裝置
  time.sleep(rebootWaitingTime * 60) # Wait for rebooting completed 等待它開好

# Detect Failure in one line, and do Reset 進行監測(對單一行)
def checkFailureAndResetTest(line, cmd, target):
  print line
  if( isAnyFailed(line) ): # If any err 若有任何問題
    print "Failed: " + line # Echo Err msg on STDOUT 印出
    nowStr = genTimeNow() # Get Now Timestamp 得到現在的時間
    # Mail Failure to other, and log it 寄信然後寫下LOG檔
    logAndNotify(fromPeople,toPeople,deviceName + ' ' + target + ' ' + testType + ' Failed at ' + nowStr, deviceName + ' ' + target + ' ' + testType + ' \n' + nowStr + '\n' + line)
    return False # Return False 回傳失敗
    #killProcess(theProcess) # Send the signal to all the process groups 殺程序
    #resetTestEnv(target) 重設環境
    #runTestProcess(cmd, target) # Run again recursively... 再跑一次
    # TODO Remaining Windows Detection 還欠WIN的部份
  else: # No err,then Do Nothing 沒錯
    return True # Return True and Check Next line 回傳成功

# Detect Failure in one line, and do Reset 進行監測(對單一行)
def checkFailureAndResetTestDontMail(line, cmd, target):
  print line
  if( isAnyFailed(line) ): # If any err 若有任何問題
    print "Failed: " + line # Echo Err msg on STDOUT 印出
    nowStr = genTimeNow() # Get Now Timestamp 得到現在的時間
    # Mail Failure to other, and log it 寄信然後寫下LOG檔
    logDown(deviceName + ' ' + target + ' ' + testType + ' \n' + nowStr + '\n' + line)
    return False # Return False 回傳失敗
  else: # No err,then Do Nothing 沒錯
    return True # Return True and Check Next line 回傳成功

# Run Test and Check Failure line by line 執行CTS,並且一行行監看CTS的STDOUT的結果
def runTestProcess(cmd, target):
  print 'Start test'
  isSuccess = True # Default OK 一開始先假設會過
  for line in runProcess(cmd): # Run Process and Fetch Process STDOUT line by line 跑程式並一行行抓出來
    isSuccess = isSuccess and checkFailureAndResetTest(line, cmd, target) # Check it 進行Check單一行
  # Test Finishing... 測試終了
  if(not isSuccess): # 不成功的話
    resetTestEnv(target) # 重設環境
    runTestProcess(cmd, target) # Run again recursively... 再跑一次
  else:
    # Succeed! 成功
    # TODO blablabla 可能還要幹嘛
    logAndNotify(fromPeople,toPeople,deviceName + ' ' + testType + ' Succeeded at ' + genTimeNow(),'Test End at ' + genTimeNow()) # 寫信通知

# Run Test and Check Failure line by line(Windows Version) 執行CTS,並且一行行監看CTS的STDOUT的結果(WIN版)
def runWinTestProcess(cmd, target):
  runWinProcess(cmd) # Run process 跑程式
  global theProcess
  print 'Wait test'
  isSuccess = True # Default OK 一開始先假設會過
  while True:
    if theProcess == None: # Wait for Process running 等待程式跑起來
      print 'Waiting'
      continue
    line = theProcess.stdout.readline() # Fetch Process STDOUT line by line 一行行抓出來
    if line == '' and theProcess.poll() != None: # If no output and process is DEAD, exit. 若程式死了又沒STDOUT輸出,就收工了
      break
    isSuccess = isSuccess and checkFailureAndResetTest(line, cmd, target) # Check it 進行Check單一行
  # Test Finishing... 測試終了
  if(not isSuccess):
    resetTestEnv(target)
    runWinTestProcess(cmd, target) # Run again recursively... 再跑一次
  else:
    # Succeed! 成功
    # TODO blablabla 可能還要幹嘛
    logAndNotify(fromPeople,toPeople,deviceName + ' ' + testType + ' Succeeded at ' + genTimeNow(),'Test End at ' + genTimeNow()) # 寫信通知

# Run Test and Check Failure line by line,but never run again when failed
# 執行CTS,並且一行行監看CTS的STDOUT的結果,但失敗時不會重新開始
def runTestProcessDontRunAgain(cmd, target):
  print 'Start test'
  isSuccess = True # Default OK 一開始先假設會過
  for line in runProcess(cmd): # Run Process and Fetch Process STDOUT line by line 跑程式並一行行抓出來
    isSuccess = isSuccess and checkFailureAndResetTestDontMail(line, cmd, target) # Check it 進行Check單一行
  # Test Finishing... 測試終了
  if(not isSuccess): # 不成功的話
    resetTestEnv(target) # 重設環境

# Run Specific Package Children 單一Pkg的子測案例與測試獨立執行
def runPkgChild(cmd, pkg, target):
  data = ctsparsinglib.findTargetInAllFiles(pkg)
  if data == None:
    print 'Error! No such package:\t' + pkg
    exit(1)
  for testcase in data[ctsparsinglib.cTestCase]:
    runTestProcessDontRunAgain(cmd + ' --class ' + testcase, target)
  for testdata in data[ctsparsinglib.cTest]:
    test = testdata[ctsparsinglib.cTest]
    testcase = testdata[ctsparsinglib.cTestCase]
    runTestProcessDontRunAgain(cmd + ' --class ' + testcase + ' --method ' + test, target)

def runPkgByTestcase(cmd, pkg, target):
  data = ctsparsinglib.findTargetInAllFiles(pkg)
  if data == None:
    print 'Error! No such package:\t' + pkg
    exit(1)
  for testcase in data[ctsparsinglib.cTestCase]:
    runTestProcessDontRunAgain(cmd + ' --class ' + testcase, target)

def runAllByTestcase(cmd, target):
  data = ctsparsinglib.parsingPackagesInPlanFile(ctsparsinglib.testplanDefPath + ctsparsinglib.ctsplanFileName)
  for pkg in data[ctsparsinglib.cEntry]:
    runPkgByTestcase(cmd, pkg, target)

#== Util Functions == 小工具區

# Check System type 系統類型
def isPOSIX():
  if(os.name == 'posix'): # OS is unix-like 若為Unix-like
    return True
  else: # OS is not unix-like 若非則False
    return False

# Write Once then Close 寫檔案,一次完成
def writeFileOnce(name, content):
  theFile = open(name, 'w') # Open Writeable File 開啟寫入模式的檔案
  theFile.write(content) # Write down 寫進去
  theFile.close() # Close 關閉

# Generate Humanbeing Readable Time String 產生人類看得懂的時間字串
def genTimeformat(timestamp):
  st = datetime.datetime.fromtimestamp(timestamp).strftime('%Y.%m.%d-%H.%M.%S') # Year.Mon.Day-Hour.Min.Sec 年.月.日-時.分.秒
  return st

# Generate Humanbeing Readable Time Now 生成當下的時間(以人類看得懂的方式)
def genTimeNow():
  return genTimeformat(time.time())

def logDown(content):
  writeFileOnce('log-' + genTimeNow() + '.txt', content) # Write log txt with Timestamp filename 檔名加入時間字串

# Log and Mail Msg, such like SuccessMsg or FailureMsg (寫入訊息至檔案並且寄出信件
def logAndNotify(fromWho, toWho, title, content):
  logDown(content)
  #return '' # Because of no network, don't mail 若無網路時,打開這行就不會寄信出去
  try:
    mailTo(fromWho, toWho, title, content)
  except Exception as e:
    print "Send Email Error: " + str(type(e))
  return 'send successed'

# Mail to others 寄出信件
def mailTo(fromWho, toWho, title, content):
  strMessage = MIMEText(content)
  strMessage['From'] = fromWho
  strMessage['To'] = toWho
  strMessage['Subject'] = title
  mailServer = smtplib.SMTP('smtp.gmail.com', 587) # 若為公司內部,則改為mail.inhon.com
  mailServer.set_debuglevel(1)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login('inhoncts', 'inhonctstesting') # TODO Your ID and Password 若在公司內部,請改用你自己的帳密,不然不能寄信
  mailServer.sendmail(fromWho, toList, strMessage.as_string())
  mailServer.close()
  
