import sys
import urllib
import random
import copy

MIN_OVERLAP = 3


#return in-degree of node in graph
def InDegree(Node, Graph):
  return sum(Node in x for x in Graph.values())


#return length of overlap between two strings in unicode
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
        
  return -1

#return true if path contains the same node twice
def RevisitsNode(path):
  return len(path) != len(set(path))

#returns true if all nodes have been visited once in path
def VisitsAll(path, nodes):
  return set(path) == set(nodes)
  

#return adjacency dictionary with values as dictionaries of {node: length of overlap}
def OverlapDict(data):

  overlaps = {}

  for i in range(len(data)):
    for j in range(len(data)):
      if j != i:
        lenOverlap = Overlap(data[i],data[j])
        if lenOverlap > 0:
          if i in overlaps:
            overlaps[i][j] = lenOverlap
          else:
            overlaps[i] = {j: lenOverlap}
          if j not in overlaps:
            overlaps[j] = {}

  return overlaps


def bfs(graph, start, end):
  queue = []
  queue.append([start])

  while queue:
    path = queue.pop()
    print len(path)
    node = path[-1]

    if node == end and VisitsAll(path, graph.keys()):
      return path

    for adjacent in sorted(graph[node],key=lambda k: graph[node].values())[::-1]:
      new_path = list(path)
      new_path.append(adjacent)
      if not RevisitsNode(new_path) and new_path not in queue:
        queue.append(new_path)



def FindSourceSink(graph):
  source = 0
  sink = -1

  for node in graph:
    if InDegree(node, graph) == 0:
      source = node
    if len(graph[node]) == 0:
      sink = node

  return source, sink


def GetContigs(graph,data):

  contigs = []
  inContig = []

  for node in graph:
    if not (InDegree(node, graph) == 1 and len(graph[node]) == 1):
      for neighbor in graph[node]:
        if len(graph[neighbor]) == 1 and InDegree(neighbor, graph) == 1:
          inContig.append(node)
          inContig.append(neighbor)
          path = data[node] + data[neighbor][graph[node][neighbor]:]
          curr = neighbor
          prev = neighbor
          while InDegree(curr, graph) == 1 and len(graph[curr]) == 1:
            prev = curr
            curr = graph[curr].keys()[0]
            path += data[curr][graph[prev][curr]:]
            inContig.append(curr)
          contigs.append(path)
  for node in graph:
    if node not in inContig:
      contigs.append(data[node])
  return contigs


with open("tests/Shake-frags.txt",'r') as infile, open("output.txt",'w') as outfile:
  data = [x.strip() for x in infile.readlines()]

  overlaps = OverlapDict(data)

  contigs = GetContigs(overlaps,data)
  simplified = OverlapDict(contigs)

  overlaps2 = OverlapDict(contigs)
  contigs2 = GetContigs(overlaps2, contigs)
  simplified2 = OverlapDict(contigs2)

  print "Simplified by " + str(len(overlaps) - len(simplified)) + " nodes"
  print "Simplified by " + str(len(simplified) - len(simplified2)) + " nodes"

  source, sink = FindSourceSink(simplified)

  print "Found Source: " + str(source)
  print "Found Sink: " + str(sink)

  #path = bfs(simplified, source, sink)
  path = [1]
  finalstring = contigs[path[0]]
  prev = path[0]

  for i in path[1:]:
    finalstring += contigs[i][simplified[prev][i]:]
    prev = i

  outfile.write(urllib.unquote_plus(finalstring))
