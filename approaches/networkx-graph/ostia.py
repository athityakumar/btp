import operator
import os
import networkx as nx
from helper_methods import *

class Transducer(nx.DiGraph):
  def add_state(self, newest_state=None):
    """
    Adds a new state, depending on the max added state and returns that state id
    """

    if newest_state is None:
      newest_state = self.new_state()
    self.add_node(newest_state, type='state')
    return(newest_state)

  def new_state(self):
    """
    :return new_state_index: Returns possible new state in Transducer network
    """

    states = self.states()
    if states:
      return(max(states)+1)
    else:
      return(1)

  def states(self):
    """
    :return states: All states present in the Transducer
    """

    # states = []
    # for (node, data) in self.nodes(data=True):
    #   print(data)
    #   try:
    #     if data['type'] == 'state':
    #       states.append(node)
    #   except KeyError:
    #     print("LOLWA")
    states = [node for (node, data) in self.nodes(data=True) if 'type' in data and data['type'] == 'state']
    return(states)

  def add_metadata(self, metadata):
    """
    Adds a metadata node, to connect to different states
    """

    self.add_node(metadata, type='metadata')

  def metadatas(self):
    """
    :return metadatas: All metadata nodes present in the Transducer
    """

    metadatas = [node for (node, data) in self.nodes(data=True) if data['type'] == 'metadata']
    return(metadatas)

  def contextual_subgraph(self, metadatas=[]):
    """
    :param metadatas: A list of metadatas for context
    :return contextual_subgraph: Transducer network corresponding to given metadatas
    """

    contextual_states = set(self.states())
    contextual_states.add(0)
    contextual_states.add(-1)

    for metadata in metadatas:
      try:
        contextual_states = contextual_states.intersection(set(self[metadata]))
      except KeyError:
        contextual_states = contextual_states

    contextual_subgraph = self.subgraph(list(contextual_states))
    return(contextual_subgraph)

  def add_arc(self, from_state, input, output, to_state):
    self.add_edge(from_state, to_state, input=input, output=output)

class OTST:
  def __init__(self, T):
    """
    Initializes a Networkx DiGraph FST
    :param T: An input*output mapping
    """

    self.graph = self.form_digraph(T)

  def states(self):
    """
    :return states: A list of all states (nodes)
    """

    return list(self.graph.states())

  def state(self, index):
    """
    :return state: The index-th state
    """
    state = self.states()[index]
    return state

  def first(self):
    """
    :return first_element: First element in the OTST
    """
    return self.state(0)

  def last(self):
    """
    :return last_element: Last element in the OTST
    """
    return self.state(-1)

  def next(self, a):
    """
    :param T: An element in the OTST
    :return next_element: Next element to a, in the OTST
    """

    all_states = self.states()
    if not a in all_states:
      return self.next(a+1)
    index_of_a = all_states.index(a)
    if index_of_a == len(all_states)-1:
      next_element = a
    else:
      next_element = self.state(index_of_a+1)
    return next_element

  def merge(self, a, b):
    """
    :param a: A state in the OTST
    :param b: A state in the OTST
    :return merged_otst: OTST with states a & b merged
    """

    graph = self.graph

    for (from_state, _) in graph.in_edges(b):
      try: 
        input = graph[from_state][b]['input']
        output = graph[from_state][b]['output']
        # print(input, output)
        graph.add_edge(from_state, a, input=input, output=output)
      except KeyError:
        graph.add_edge(from_state, a)

    for to_state in graph[b]:
      input = graph[b][to_state]['input']
      output = graph[b][to_state]['output']
      # print(input, output)
      graph.add_edge(a, to_state, input=input, output=output)      

    graph.remove_node(b)
    self.graph = graph
    return self

  def subseq(self):
    """
    :return bool: True if tou is subsequent, else False
    """

    violation = self.find_subseq_violation()
    return(violation is None)

  def find_subseq_violation(self):
    """
    (r,a,v,s) and (r,a,w,t) are 2 edges of tou that violate subseq condition,
    with s<t

    :return (r, a, v, s, w, t): Tuple
    """

    # Iterate through all edge pairs
    # If determinism condition present for any pair, (v==w and s==t)
    #   return edges
    # Else return None
    
    graph = self.graph
    states = graph.states()
    for state in states:
      neighbors = graph[state]
      # print(len(neighbors))
      for neighbor_1 in neighbors:
        for neighbor_2 in neighbors:
          if neighbor_1 != neighbor_2:
            # print("Yo")
            edge_1 = graph[state][neighbor_1]
            edge_2 = graph[state][neighbor_2]
            if edge_1['input'] == edge_2['input'] and edge_1['output'] == edge_2['output']:
              return((state, edge_1['input'], edge_1['output'], neighbor_1, edge_2['output'], neighbor_2))

  def push_back(self, element, edge):
    """
    :param element: An element in the OTST
    :param edge: An edge in the OTST, as a tuple (r, a, v, s)
    :return tou: OTST with element pushed back from the edge
    """  

    graph = self.graph
    input_state, input_text, output_text, output_state = edge

    graph[input_state][output_state]['output'] = eliminate_suffix(output_text, element)
    outgoing_states = graph[output_state]
    for state in outgoing_states:
      graph[output_state][state]['output'] = element + graph[output_state][state]['output']
 
    self.graph = graph
    return self

  def form_digraph(self, T):
    """
    :param T: A set of all input/output pairs
    :return graph: A directed networkx graph
    """

    graph = Transducer()

    graph.add_node('start')
    graph.add_node('stop')

    graph.add_node(0)  # For start
    graph.add_node(-1) # For stop

    for (input_word, metadatas, output_word) in T:
      for metadata in metadatas:
        graph.add_metadata(metadata)

      io_chunks = get_io_chunks(input_word, output_word)
      io_chunks += [('#','#')]

      # print(input_word, output_word, io_chunks)
      for (i, (input_chunk, output_chunk)) in enumerate(io_chunks):
        from_state = 0 if i == 0 else to_state
        to_state = -1  if i == len(io_chunks)-1 else graph.add_state()
        for metadata in metadatas:
          graph.add_edge(metadata, from_state)
          graph.add_edge(metadata, to_state)
        graph.add_arc(from_state, input_chunk, output_chunk, to_state)


    print("Done forming the directed FST graph")      
    # Do something
    # Add naive edges and states
    # States merging will be taken care of, by OSTIA
    # Should lpos and rpos also be incorporated as inputs too in edges?
    # That way, maybe something like induced subgraphs can be used when required.

    return(graph)

  def guess_output_for(self, word, metadatas):
    def word_from_path(graph, path):
      path_input_word = ''

      for i in range(0, len(path)-1):
        edge = graph[path[i]][path[i+1]]
        path_input_word += edge['input']

      # print(path_input_word)
      return(path_input_word[:-1])

    def closeness_score(word, path_input_word):
      distance = mod_levenshtein(word, path_input_word)
      if distance >= len(word):
        score = 0.0
      else:
        score = 1.0 - float(distance/len(word))

      return score

    def compatibility_score(graph, path, word):
      n = 0
      c = 0
      j = 0
      for i in range(0, len(path)-1):
        n += 1
        edge = graph[path[i]][path[i+1]]
        if edge['input']:
          if edge['input'] != edge['output']:
            if edge['input'] == word[j]:
              c += 1
        if edge['input'] == word[j]:
          c += 1
          j += 1

      score = float(c/n)
      return score

    def normalized_score(closeness_score, compatibility_score):
      return (closeness_score+compatibility_score)/2.0

    output = ''
    induced_subgraph = self.graph.contextual_subgraph(metadatas)
    paths = nx.all_simple_paths(induced_subgraph, 0, -1)
    path_ways = []
    for i, path in enumerate(paths):
      path_word = word_from_path(induced_subgraph, path)
      closeness = closeness_score(word, path_word)
      compatibility = compatibility_score(induced_subgraph, path, word)
      normalized = normalized_score(closeness, compatibility)
      path_ways.append((path, normalized))

    path = sorted(path_ways, key=operator.itemgetter(1))[0][0]
    # print(path)
    # print(word_from_path(induced_subgraph, path))

    j = 0
    for i in range(0, len(path)-1):
      edge = induced_subgraph[path[i]][path[i+1]]
      # print(edge, i, j, output)
      if edge['input']:
        if j < len(word):
          if edge['input'] == word[j]:
            output += edge['output']
          else:
            output += word[j]
          j += 1
      else:
        output += edge['output']

    return output

def is_prefixed_with(str, prefix):
  """
  :param str: An input word / sub-word
  :param prefix: A prefix to check in the word / sub-word
  :return bool: True if prefix, else False
  """
  return(str.find(prefix) == 0)

def lcp(strings):
  """
  Computes longest common prefix of given set of strings, given on page 449
  :param strings: A set of strings
  :return prefix: The longest common prefix
  """

  prefix = os.path.commonprefix(list(strings))
  return prefix

def eliminate_suffix(v, w):
  """
  If v = uw (u=prefix, w=suffix),
  u = v w-1

  Returns suffix after eliminating prefix

  :param str: An input word / sub-word
  :return inv_str: An inversed string
  """

  u = v.rstrip(w)
  return(u)

def eliminate_prefix(u, v):
  """
  If v = uw (u=prefix, w=suffix),
  w = u-1 v

  Returns suffix after eliminating prefix

  :param str: An input word / sub-word
  :return inv_str: An inversed string
  """

  w = u.lstrip(v)
  return(w)

def OSTIA(T):
  """
  :param T: Finite set of input*output pairs
  :return OSTIA OTST
  """

  exit_condition_1 = exit_condition_2 = False

  tou = tou_dup = OTST(T)
  pretty_print_graph(tou.graph)

  q = tou.first()
  while q < tou.last():
    q = tou.next(q)
    # print(q)
    p = tou.first()
    # print(p<q)
    while p < q and not exit_condition_1:
      tou_dup = tou
      # tou = tou.merge(p, q)
      tou = tou.merge(q, p)
      while not tou.subseq() and not exit_condition_2:
        r, a, v, s, w, t = tou.find_subseq_violation()

        print(r, a, v, s, w, t)
        # '#' depicts end of string
        exit_condition_2 = (v!=w and a=='#') or (s<q and not is_prefixed_with(v, w))
        if not exit_condition_2:
          u = lcp([v, w])
          tou = tou.push_back(eliminate_prefix(u, v), (r, a, v, s))
          tou = tou.push_back(eliminate_prefix(u, w), (r, a, w, t))
          # tou = tou.merge(s, t)
          tou = tou.merge(t, s)
          # pretty_print_graph(tou.graph)

      if not tou.subseq():
        tou = tou_dup
      else:
        exit_condition_1 = True

      if not exit_condition_1:
        p = tou.next(p)
    if not tou.subseq():
      tou = tou_dup

  pretty_print_graph(tou.graph)
  return tou

def fetch_input_output_pairs(language='english', quality='low'):
  filepath = "../daru-dataframe/spec/fixtures/{}-train-{}".format(language, quality)
  T = list()
  file = open(filepath,'r')
  for line in file.readlines():
    source, dest, metadata = line.split("\t")
    if not "*" in source and not "*" in dest:
      metadata = metadata.strip("\n").split(";")
      T.append((source, metadata, dest))
      # print("{} + {} = {}".format(source, " + ".join(metadata), dest))
  print("Providing all words in structured manner, to OSTIA")
  T = sorted(T, key=operator.itemgetter(0))
  return T

def fetch_testing_data(language='english'):
  filepath = "../daru-dataframe/spec/fixtures/{}-dev".format(language)
  T = list()
  file = open(filepath,'r')
  for line in file.readlines():
    source, expected_dest, metadata = line.split("\t")
    if not "*" in source and not "*" in expected_dest:
      metadata = metadata.strip("\n").split(";")
      T.append((source, metadata, expected_dest))
      # print("{} + {} = {}".format(source, " + ".join(metadata), dest))
  print("Providing all test words in structured manner, to OSTIA")
  T = sorted(T, key=operator.itemgetter(0))
  return T

def check_all_testing_data(model):
  c = n = 0
  l = {}
  T = fetch_testing_data(language='english')
  for (source, metadatas, expected_dest) in T:
    try:
      predicted_dest = model.guess_output_for(source, metadatas)
      if predicted_dest == expected_dest:
        print("{} + {} was expected and received as {}".format(source, metadatas, predicted_dest))
        c += 1
      else:
        dist = mod_levenshtein(expected_dest, predicted_dest)
        if dist in l:
          l[dist] += 1
        else:
          l[dist] = 1
        print("{} + {} was expected to be {}, but received {} instead".format(source, metadatas, expected_dest, predicted_dest))
      n += 1
    except IndexError:
      print("Some error with the source word {}".format(source))
  print("\n\nExact word-match accuracy: {}". format(100.00*float(c)/float(n)))
  print("\n Levenshtein distribution:", l)

T = fetch_input_output_pairs(language='english', quality='low')
T = OSTIA(T)
# print(len(T.graph[0]))
# print(len(T.graph.in_edges(-1)))
# for path in nx.all_simple_paths(T.graph, source=0, target=-1):
#   print(path)

check_all_testing_data(T)
# print(T.guess_output_for('match', ['V', 'PST']))