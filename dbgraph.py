import sys
import random
import urllib

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


with open(sys.argv[1],'r') as infile, open("output.txt",'w') as outfile:
  data = [x.strip() for x in infile.readlines()]

  graph = {}
  for line in data:
    graph = DeBruijnGraph(k,urllib.unquote_plus(line),graph)

  '''
  for pattern,pattern_ in graph.iteritems():
    outfile.write(pattern + " -> " + ",".join(pattern_) + "\n")
  '''
  path = EulerianPath(graph)
  print path

  path = [urllib.unquote_plus(x) for x in path]
  
  original_text = path[0]

  for node in path[1:]:
    if node != original_text[-k+1:]:
      original_text+=node[-1]

  outfile.write(urllib.quote_plus(original_text))
