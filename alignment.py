import sys
import urllib

DOWN = 0
RIGHT = 1
DIAG = 2
INDEL = 0

def Overlap(string1,string2):
  
  string1 = urllib.unquote_plus(string1)
  string2 = urllib.unquote_plus(string2)

  overlap_len = 0
  counts = []
  for i in range(len(string2))[2:]:
    if string1[-1] == string2[i] and i < len(string1):
      j = i
      while j >= 0:
        if string1[j-i-1] != string2[j]:
          break
        else:
          j -= 1
      if j < 0:
        overlap_len = i
        return urllib.quote_plus(string1+string2[i+1:])
  return False



with open(sys.argv[1],'r') as infile, open("output.txt",'w') as outfile:
  data = [x.strip() for x in infile.readlines()]
  i = 1
  while len(data) > 1:

    i = (i%(len(data)-1))+1
    join1 = Overlap(data[0],data[i])
    join2 = join1 if join1 else Overlap(data[i],data[0])
    if join2:
      print data[0]
      print data[i]
      print join2
      del data[i]
      del data[0]
      data.append(join2)
      print data

  outfile.write(urllib.quote_plus(data[0]))