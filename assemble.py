import sys
from dbgraph import GetTextFromOverlaps

#read from file
if len(sys.argv) == 2:
  with open(sys.argv[1],'r') as infile:
    data = [x.strip() for x in infile.readlines()]
    print GetTextFromOverlaps(data)

#read from stdin
elif len(sys.argv) == 1:
  data = [x.strip() for x in sys.stdin.readlines()]
  print GetTextFromOverlaps(data)
#error
else:
  print "Run with command"
  print "python assemble.py [optional: filename]"