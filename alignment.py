import sys
import urllib
import random


MIN_OVERLAP = 3


#find longest path
def Traverse(node, adjacency, vertices):

  distance = [sys.maxint for x in range(vertices)]
  predecessor = [None for x in range(vertices)]

  distance[node] = 0

  for i in range(len(adjacency)):
    for u,v,w in adjacency:
      if distance[u] - w < distance[v] and not visited[v]:
        distance[v] = distance[u] - w
        predecessor[v] = u

  return predecessor


def Overlap(string1,string2):
  
  string1 = urllib.unquote_plus(string1)
  string2 = urllib.unquote_plus(string2)

  overlap_len = 0
  counts = []
  for i in range(len(string2))[MIN_OVERLAP-1:]:
    if string1[-1] == string2[i] and i < len(string1):
      j = i
      while j >= 0:
        if string1[j-i-1] != string2[j]:
          break
        else:
          j -= 1
      if j < 0:
        return len(urllib.quote_plus(string1[-i-1:]))
        #return urllib.quote_plus(string1+string2[i+1:])
  #return False
  return -1


with open("test2.txt",'r') as infile, open("output.txt",'w') as outfile:
  data = [x.strip() for x in infile.readlines()]

  overlapstest = [[0 for i in range(len(data))] for j in range(len(data))]
  overlaps = {}
  adjacency = []

  for i in range(len(data)):
    for j in range(len(data)):
      if j != i:
        lenOverlap = Overlap(data[i],data[j])
        overlapstest[i][j] = lenOverlap
        if lenOverlap > 0:
          if i in overlaps:
            overlaps[i][j] = lenOverlap
          else:
            overlaps[i] = {j: lenOverlap}
          adjacency.append((i,j,lenOverlap))
          if j not in overlaps:
            overlaps[j] = {}

        #overlaps[i][j] = Overlap(data[i],data[j])
  
  #print FindPath(overlaps)

  start = random.choice(overlaps.keys())
  sink = -1
  
  for node in overlaps:
    if InDegree(node, overlaps) == 0:
      start = node
    if len(overlaps[node]) == 0:
      sink = node

  path = Traverse(start,adjacency, len(data))
  print range(len(path))
  print path

  finalstring = data[sink]
  curr = sink
  prev = path[curr]

  #retrace path to start from sink
  #while curr != None and prev != None:
  for i in range(len(data)-2):
    finalstring = data[prev] + finalstring[overlaps[prev][curr]:]
    curr = prev
    prev = path[prev]
  
  print finalstring
  #outfile.write(urllib.quote_plus(data[0]))