import sys
import random
import urllib
import copy

MIN_OVERLAP = 3
k = 4


#Generate kmer composition of text
#parameters: k - int length of kmer
#            Text - string fragment of text
#return: list of kmers

def Composition(k, Text):
  kmers = []
  for i in range(len(Text)-k+1):
    kmers.append(Text[i:i+k])
  return kmers



#Add kmer composition of fragment to DeBruijn graph
#parameters: k - int length of kmer
#            Text - string fragment of text to add to graph
#            adjacency - dictionary DeBruijn graph
#return: DeBruijn graph with fragment added

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



#Find length of overlap between two strings
#parameters: string1 - prefix string 
#            string2 - suffix string
#return: length of overlap, or -1 if not overlapping

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



#Minimize number of fragments by finding non-branching paths
#parameters: graph - dictionary adjacency graph
#            data - set of fragments
#returns: new list of fragments with contigs

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



#Find in degree of node (number of nodes pointing to it)
#parameters: Node - int to search for
#            Graph - adjacency list to search in
#returns: number of edges pointing to Node

def InDegree(Node, Graph):
  return sum(Node in x for x in Graph.values())




#Find Eulerian path in DeBruijn graph, starting from node that
#has no incoming edges
#parameters: adjacency - dictionary adjacency list
#returns: list of nodes in order of traversal

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




#Given set of fragments with overlapping ends, find the original text
#parameters: data - list of fragments (strings)
#returns: re-assembled source text

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
  
  if path:
    original_text = path[0]
    
    for node in path[1:]:

      if node != original_text[-k+1:]:
        original_text = original_text[:-k+2] + node

    return urllib.unquote_plus(original_text)

  else:
    return None