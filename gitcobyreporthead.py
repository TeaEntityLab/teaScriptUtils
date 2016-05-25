#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import subprocess

def cd(thePath):
    os.chdir(thePath)

def runAndReturnRETURNCODE(theCmd):
    child = subprocess.Popen(theCmd, stdout=subprocess.PIPE)
    streamdata = child.communicate()[0]
    returncode = child.returncode
    print (streamdata)
    return returncode

def parseDirAndGenCmd(dirAndVersionFile):
    # Current Working DIR
    cwd = os.getcwd()
    # Open file
    theFile = open(dirAndVersionFile, "r")
    # Split Columns of one record
    regexSplitor = re.compile('[ \t\n\r]+')
    # Constants
    cdcmd = "cd"
    gitcmd = "git"
    gitcheckoutcmd = "checkout"
    gitforceoption = "-f"
    # while Read line by line
    for line in theFile.readlines():
        data = regexSplitor.split(line)
        # CD to there and
        targetdir = data[0]
        print ("cd to " + targetdir)
        cd(targetdir)
        # git checkout -f $version 
        cocmd = []
        cocmd.extend([gitcmd, gitcheckoutcmd, gitforceoption])
        cocmd.append(data[1])
        print (cocmd)
        runAndReturnRETURNCODE(cocmd)
        # CD back to root
        print ("cd to " + cwd)
        cd(cwd)




parseDirAndGenCmd(sys.argv[1])

def testCD():
    originalcwd = os.getcwd()
    cd(os.getcwd() + "/" + "vendor")
    print os.getcwd()
    cd(originalcwd)
    print os.getcwd()

