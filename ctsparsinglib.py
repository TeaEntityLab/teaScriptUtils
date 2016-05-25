#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from os import walk
import fnmatch, re

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#== Constants 常數 ==
cTestPkg = "TestPackage"
cTestSuite = "TestSuite"
cTestCase = "TestCase"
cTest = "Test"
cEntry = "Entry"
cPkgAttr = "appPackageName"
cNameAttr = "name"
cUriAttr = "uri"

kSuccess = 'success'
testplanDefPath = "./../repository/plans/"
ctsplanFileName = "CTS.xml"
testcaseDefPath = "./../repository/testcases/"

#== String Comparing 字串比對 ==

# is it TestPackage tag?
def isTestPkg(name):
    return name == cTestPkg

# is it TestSuite tag?
def isTestSuite(name):
    return name == cTestSuite

# is it TestCase tag?
def isTestCase(name):
    return name == cTestCase

# is it Test tag?
def isTest(name):
    return name == cTest

def isThisFileRightPkg(name, target):
    return name == target

def isXMLFile(name):
    return fnmatch.fnmatch(name, '*.xml')

#== Utils 小工具 ==

def combineByDot(a,b):
    return a + '.' + b

#== Real Parsing actions 真實分析動作 ==

def recursivelyParseTestElementChild(element, result, path):
    for child in element:
        parseRecursiveToBuildTestcaseTestFullName(child, result, path)

def parseRecursiveToBuildTestcaseTestFullName(element, result, path):
    attrName = element.get(cNameAttr)
    tagName = element.tag
    if isTest(tagName):
        TestDataWithClassAndMethod = {}
        TestDataWithClassAndMethod[cTest] = attrName
        TestDataWithClassAndMethod[cTestCase] = path
        result[cTest].append(TestDataWithClassAndMethod)
    elif isTestCase(tagName):
        path = combineByDot(path, attrName)
        result[cTestCase].append(path)
        recursivelyParseTestElementChild(element, result, path)
    elif isTestSuite(tagName):
        if path == '':
            path = path + attrName
        else:
            path = combineByDot(path, attrName)
        recursivelyParseTestElementChild(element, result, path)
    elif isTestPkg(tagName):
        recursivelyParseTestElementChild(element, result, path)

def parsingFileAndFindTarget(filename, target):
    isCurrectTestPkg = False # Default False
    testsuiteList = [] # No Use
    testcaseList = []
    testList = []
    result = {}
    result[cTestSuite] = testsuiteList # No Use
    result[cTestCase] = testcaseList
    result[cTest] = testList
    tree = ET.ElementTree(file=filename)
    root = tree.getroot()
    parseRecursiveToBuildTestcaseTestFullName(root, result, '');
    
    isCurrectTestPkg = isThisFileRightPkg(root.get(cPkgAttr), target)
    result[kSuccess] = isCurrectTestPkg
    return result

def parsingPackagesInPlanFile(filename):
    result = {}
    result[cEntry] = []
    for event, element in ET.iterparse(filename):
        if event == 'end':
            tagName = element.tag
            if tagName == cEntry:
                attrUri = element.get(cUriAttr)
                result[cEntry].append(attrUri)
        element.clear() # discard the element
    
    return result;

def getAllFile(path):
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    return f

def getXMLFiles():
    f = getAllFile(testcaseDefPath)
    result = []
    for file in f:
        if isXMLFile(file):
            result.append(file)
    return result
        
def findTargetInAllFiles(target):
    result = None
    for file in getXMLFiles():
        temp = parsingFileAndFindTarget(testcaseDefPath + file, target)
        if temp[kSuccess] == True:
            result = temp
            break
    return result
