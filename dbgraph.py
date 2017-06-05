import sys
import urllib

def Composition(k, Text):
  kmers = []
  for i in range(len(Text)-k+1):
    kmers.append(Text[i:i+k])
  return kmers

def DeBruijnGraph(k, Text):
  adjacency = {}
  Patterns = Composition(k-1,Text)
  for i in range(len(Patterns)-1):
    if Patterns[i] not in adjacency:
      adjacency[Patterns[i]] = [Patterns[i+1]]
    else:
      adjacency[Patterns[i]].append(Patterns[i+1])
  return adjacency

with open(sys.argv[1],'r') as infile, open("output.txt",'w') as outfile:
  data = [x.strip() for x in infile.readlines()]