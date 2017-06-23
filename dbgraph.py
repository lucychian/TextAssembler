import sys
import random
import urllib
import copy

MIN_OVERLAP = 3
k = 4

def Composition(k, Text):
  kmers = []
  for i in range(len(Text)-k+1):
    kmers.append(Text[i:i+k])
  return kmers

def DeBruijnGraph(k, Text, adjacency):
  Patterns = Composition(k-1,Text)
  Patterns = [urllib.quote_plus(x) for x in Patterns]

  for i in range(len(Patterns)-1):
    if Patterns[i] not in adjacency:
      adjacency[Patterns[i]] = [Patterns[i+1]]
    else:
      adjacency[Patterns[i]].append(Patterns[i+1])
    if Patterns[i+1] not in adjacency:
      adjacency[Patterns[i+1]] = []

  return adjacency

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


def GetContigs(graph,data):

  contigs = []
  inContig = []

  for node in graph:
    if not (InDegree(node, graph) == 1 and len(graph[node]) == 1):
      for neighbor in graph[node]:
        if len(graph[neighbor]) == 1 and InDegree(neighbor, graph) == 1:
          inContig.append(node)
          path = data[node] + data[neighbor][graph[node][neighbor]:]
          curr = neighbor
          prev = neighbor
          while InDegree(curr, graph) == 1 and len(graph[curr]) == 1:
            inContig.append(curr)
            prev = curr
            curr = graph[curr].keys()[0]
            path += data[curr][graph[prev][curr]:]
          contigs.append(path)
  
  for node in graph:
    if node not in inContig:
      contigs.append(data[node])
  return contigs

def InDegree(Node, Graph):
  return sum(Node in x for x in Graph.values())

def EulerianPath(adjacency):
  
  stack = []
  circuit = []

  curr = random.choice(adjacency.keys())
  
  for node in adjacency:
    if InDegree(node, adjacency) == 0:
      curr = node

  stack.append(curr)

  while len(stack) > 0:
    if len(adjacency[curr]) == 0:
      circuit.append(curr)
      curr = stack.pop()
    else:
      stack.append(curr)
      neighbor = adjacency[curr][0]
      del adjacency[curr][0]
      curr = neighbor
  return circuit[::-1]


def GetTextFromOverlaps(data):

  graph = {}
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
  
  for line in GetContigs(overlaps,data):
    graph = DeBruijnGraph(k,urllib.unquote_plus(line),graph)
  
  temp = copy.deepcopy(graph)
  path = EulerianPath(temp)

  path = [urllib.unquote_plus(x) for x in path]
  original_text = path[0]
  
  for node in path[1:]:

    if node != original_text[-k+1:]:
      original_text = original_text[:-k+2] + node

  return urllib.unquote_plus(original_text)


'''
with open("test2.txt",'r') as infile:
  data = [x.strip() for x in infile.readlines()]
  print GetTextFromOverlaps(data)
'''
