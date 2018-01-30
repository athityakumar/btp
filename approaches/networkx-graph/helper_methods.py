import networkx as nx
import matplotlib.pyplot as plt
import string
import re

# Iterative longest contiguous sequence. No one character matchings

import string
import re

# Iterative longest contiguous sequence. No one character matchings

def lcs(s1,s2):
  longest = ""
  i = 0
  for x in s1:
    if re.search(x, s2):
      s = x
      while re.search(s, s2):
        if len(s)>len(longest):
          longest = s
        if i+len(s) == len(s1):
          break
        s = s1[i:i+len(s)+1]
    i += 1
  return longest

def iterLCS(pdf):
  # print(pdf)
  sw1 = pdf['source']
  sw2 = pdf['target']
  longList = []
  while True:
    tempVal = lcs(sw1,sw2)
    if len(tempVal)  <= 1:
      break
    
    longList.append(tempVal)
    sw1 = sw1.replace(tempVal,'#',1)
    sw2 = sw2.replace(tempVal,'!',1)
  #return [longList,[item for item in sw1.split('#') if len(item) > 0],[item for item in sw2.split('!') if len(item) > 0]]
  pdf['common'] = longList
  pdf['deleted'] = [item for item in sw1.split('#') if len(item) > 0]
  
  # if len(pdf['deleted']) == 0:
  #   pdf['deleted'] = ['ϵ']
  
  pdf['added'] = [item for item in sw2.split('!') if len(item) > 0]
  
  # if len(pdf['added']) == 0:
  #   pdf['added'] = ['ϵ']
  
  return pdf

def compare(expected, actual):
  expected = set(expected)
  actual   = set(actual)

  n_expected = len(expected)
  n_actual   = len(actual)

  intersection = expected.intersection(actual)
  n_intersection = len(intersection)

  print("Expected", n_expected, "results")
  print("Received", n_actual, "results")
    # print("There are", n_intersection, "intersecting results")
  print("There are", n_intersection, "intersecting results : ", intersection)

  missing = expected - intersection
  # print("There are", n_expected - n_intersection, "missing results")
  print("There are", n_expected - n_intersection, "missing results : ", missing)

  extra = actual - intersection
  # print("There are", n_actual - n_intersection, "extra (wrongly guessed) results")
  print("There are", n_actual - n_intersection, "extra (wrongly guessed) results : ", extra)

def force_add_uid(G, from_node, to_node, uid):
  try:
    G[from_node][to_node]['uid'].add(uid)
  except KeyError:
    G.add_edge(from_node, to_node, uid=set([uid]))

  return(G)

def force_add_weight(G, from_node, to_node, weight):
  try:
    G[from_node][to_node]['weight'] += weight
  except KeyError:
    G.add_edge(from_node, to_node, weight=weight)

  return(G)

def visualize_graph(G, attr):
  if attr == 'uid':
    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if len(d['uid']) >2]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if len(d['uid']) <=2]
  else:
    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >2]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=2]

  pos=nx.spring_layout(G) # positions for all nodes
  nx.draw_networkx_nodes(G,pos,node_size=700)
  nx.draw_networkx_edges(G,pos,edgelist=elarge,width=6)
  nx.draw_networkx_edges(G,pos,edgelist=esmall,width=6,alpha=0.5,edge_color='b',style='dashed')
  nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
  plt.axis('off')
  plt.savefig("weighted_graph.png")
  plt.show()

def visualize_network(G, attr):
  labels = list()
  for node in G:
    for neighbor in G[node]:
      labels.append(G[node][neighbor][attr])
  graph_pos = nx.spring_layout(G)
  edge_labels = dict(zip(G.edges, labels))
  nx.draw_networkx_nodes(G, graph_pos, node_size=1000, node_color='blue', alpha=0.3)
  nx.draw_networkx_edges(G, graph_pos, width=2,alpha=0.1,style='dashed')
  nx.draw_networkx_labels(G, graph_pos, font_size=15, font_family='sans-serif')
  nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, font_size=8)
  plt.axis('off')
  plt.show()

def empty_graph(G):
  return(len(G.edges) == 0)

def update_dict(dictionary, key, value):
  if key in dictionary:
    dictionary[key] += value
  else:
    dictionary[key] = value

  return(dictionary)

def read_wordpairs(path):
  file = open(path,'r')
  wordpairs = dict()
  for line in file.readlines():
    source, dest = line.split("\t")[0:2]
    # if len(source) < 10 and len(dest) < 15:
    wordpairs[source] = dest

  return(wordpairs)

def map_edges_uid_to_weight(G):
  for node in G:
    for neighbor in G[node]:
      G[node][neighbor]['uid'] = len(G[node][neighbor]['uid'])

  return(G)

def pretty_print_graph(G):
  print("\n")
  for node in G:
    print("Node " + str(node) + " : " + str(G[node]))
  print("Number of nodes : ", len(G.nodes))
  print("Number of edges : ", len(G.edges))

  length_freq = dict()
  total_len   = 0
  for node in G:
    length_freq = update_dict(length_freq, len(node), 1)
    total_len  += len(node)
  total_length = sum([length*count for length, count in length_freq.items()])
  print("Frequency of string-length of nodes : ", length_freq)
  print("Average string-length of nodes : ", total_length / len(G.nodes))
