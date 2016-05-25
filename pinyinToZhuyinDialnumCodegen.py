#!/usr/bin/python

import csv
import sys

if len(sys.argv) < 2:
  print ( "Give me the file path" )
  exit(1)

with open(sys.argv[1], 'rb') as csvfile:
  data = csv.reader(csvfile)
  quote = "'"
  dquote = "\""
  separator = ", "
  javaUniPrefix = "\\u"
  VowelConsonant = ""
  Combination = ""
  ZhuyinSignChar = ""
  ZhuyinSound = ""
  ZhuyinSoundMappingDialerNum = ""
  theConsonantRow = None
  theConsonantRowSound = None
  theConsonantP = None
  totalCount = 0  
  for i, row in enumerate(data):
    if ( i < 1 ):
      theConsonantRow = row
      continue
    elif ( i == 1 ):
      theConsonantRowSound = row
    #
    for j, col in enumerate(row):
      if ( j < 1 ):
        continue
      if ( i == 1 and j > 1 ):
        theSign = theConsonantRow[j]
        VowelConsonant += "consonant2num.put(\"" + col + "\", \"\"); // " + theSign + "\n"
        if ( len( theSign ) < 5 ):
          theCoded = str(hex(ord(theSign.decode('utf-8'))))[2:] # No 0x prefix
          ZhuyinSignChar += quote + javaUniPrefix + theCoded + quote + separator
          ZhuyinSound += dquote + theConsonantRowSound[j] + dquote + separator
        theConsonantP = row
        continue
      elif ( j == 1 and i > 1 ):
        theSign = row[0]
        VowelConsonant += "vowel2num.put(\"" + col + "\", \"\"); // " + theSign + "\n"
        if ( len( theSign ) < 5 ):
          theCoded = str(hex(ord(theSign.decode('utf-8'))))[2:] # No 0x prefix
          ZhuyinSignChar += quote + javaUniPrefix + theCoded + quote + separator
          ZhuyinSound += dquote + row[1] + dquote + separator
        continue
        
      if ( col == "" ):
        continue
      Combination += "p2zMap.put(\"" + col + "\", consonant2num.get(\"" + theConsonantP[j] + "\")" + " + " + "vowel2num.get(\"" + row[1] + "\") " + ");" + "\n"
      totalCount += 1;
  print VowelConsonant
  print Combination
  print totalCount
  #
  print ZhuyinSignChar
  print ZhuyinSound