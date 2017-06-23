import sys
import urllib
import random
import copy

MIN_OVERLAP = 3
k = 4

def InDegree(Node, Graph):
  return sum(Node in x for x in Graph.values())

def Composition(k, Text):
  kmers = []
  for i in range(len(Text)-k+1):
    kmers.append(Text[i:i+k])
  return kmers

'''
#find longest path
def Traverse(source, sink, overlaps, vertices):

  queue = []
  path = []

  #add all neighbors to queue
  #if path reaches end with nodes unvisited, pop until last unvisited node
  queue.append(source)

  while queue:

    curr = queue.pop()
    path.append(curr)

    if curr == sink and len(path) == vertices:
      return path
    elif curr == sink:
      print "wrong path"
      print path

      backtrack = 0

      #backtrack to first branch
      while len(overlaps[path[backtrack]]) < 2:
        backtrack += 1
      print "deleting " + str(path[backtrack]) + "][" + str(path[backtrack+1])
      del overlaps[path[backtrack]][path[backtrack+1]]
      path = path[:backtrack+1]
      queue = []
      curr = path[backtrack]
      print "backtrack to " + str(backtrack)
      print "new path " + str(path)

    for neighbor,w in overlaps[curr].iteritems():
      if neighbor not in path:
        queue.append(neighbor)

'''

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
  print "graph"
  print graph

  for node in graph:
    print node
    if not (InDegree(node, graph) == 1 and len(graph[node]) == 1):
      if len(graph[node]) > 0:
        for neighbor in graph[node]:
          path = data[node] + data[neighbor][graph[node][neighbor]:]
          curr = neighbor
          while InDegree(curr, graph) == 1 and len(graph[curr]) == 1:
            print "making contig"
            prev = curr
            curr = graph[curr].keys()[0]
            path += data[curr][graph[prev][curr]:]
          contigs.append(path)
    
  return contigs



with open("test2.txt",'r') as infile, open("output.txt",'w') as outfile:
  data = [x.strip() for x in infile.readlines()]

  overlaps = {}
  adjacency = []

  for i in range(len(data)):
    for j in range(len(data)):
      if j != i:
        lenOverlap = Overlap(data[i],data[j])
        if lenOverlap > 0:
          if i in overlaps:
            overlaps[i][j] = lenOverlap
          else:
            overlaps[i] = {j: lenOverlap}
          adjacency.append((i,j,lenOverlap))
          if j not in overlaps:
            overlaps[j] = {}

  start = random.choice(overlaps.keys())
  sink = -1
  
  for node in overlaps:
    if InDegree(node, overlaps) == 0:
      start = node
    if len(overlaps[node]) == 0:
      sink = node

  #print overlaps
  contigs = GetContigs(overlaps,data)
  print len(contigs)
  print contigs

  graph = {}
  for line in contigs:
    graph = DeBruijnGraph(k,urllib.unquote_plus(line),graph)

  temp = copy.deepcopy(graph)
  path = EulerianPath(temp)

  path = [urllib.quote_plus(x) for x in path]

  print path

  original_text = path[0]

  for node in path[1:]:
    if node != original_text[-k+1:]:
      original_text+=node[-1]

'''
  path = Traverse(0, sink, overlaps, len(data))



  if path:
    finalstring = data[path[0]]
    prev = path[0]

    for i in path[1:]:
      finalstring += data[i][overlaps[prev][i]:]
      prev = i

    print finalstring
    outfile.write(finalstring)
'''