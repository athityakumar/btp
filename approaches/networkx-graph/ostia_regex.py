import operator
import os
import networkx as nx
from helper_methods import *
import sys, codecs, string, getopt
from functools import wraps

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
    :param T: A set of input words
    :return graph: A directed networkx graph
    """

    graph = Transducer()

    graph.add_node('start')
    graph.add_node('stop')

    graph.add_node(0)  # For start
    graph.add_node(-1) # For stop

    for input_word in T:
      io_chunks = list(input_word)
      io_chunks += ['>']

      # print(input_word, output_word, io_chunks)
      for (i, input_char) in enumerate(io_chunks):
        from_state = 0 if i == 0 else to_state
        to_state = -1  if i == len(io_chunks)-1 else graph.add_state()
        graph.add_arc(from_state, input_char, input_char, to_state)

    print("Done forming the directed FST graph")      
    # Do something
    # Add naive edges and states
    # States merging will be taken care of, by OSTIA
    # Should lpos and rpos also be incorporated as inputs too in edges?
    # That way, maybe something like induced subgraphs can be used when required.

    return(graph)

  def matches_any_path(self, new_word):
    def word_from_path(graph, path):
      path_input_word = ''

      for i in range(0, len(path)-1):
        edge = graph[path[i]][path[i+1]]
        print(edge)
        path_input_word += edge['input']

    graph = self.graph
    paths = nx.all_simple_paths(graph, 'start', 'stop')
    words = [word_from_path(graph, path) for path in paths]
    min_ldist = len(new_word)
    closest_word = new_word
    for word in words:
      print(word, new_word)
      lp, lr, ls, rp, rr, rs = alignprs(word, new_word)
      lp = lp.replace('_', '')
      lr = lr.replace('_', '')
      ls = ls.replace('_', '')
      rp = rp.replace('_', '')
      rr = rr.replace('_', '')
      rs = rs.replace('_', '')
      score = levenshtein(lp, rp)[-1] + levenshtein(ls, rs)[-1] + levenshtein(lr, rr)[-1]
      score = float(score) / (len(word) + len(new_word))
      if score < min_ldist:
        min_ldist = score
        closest_word = word
    return((min_ldist, closest_word))

  def guess_output_for(self, lang, quality):
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

    # out = ''
    # metadatas = []
    # word = ''
    # induced_subgraph = self.graph.contextual_subgraph(metadatas)
    # paths = nx.all_simple_paths(induced_subgraph, 0, -1)
    # path_ways = []
    # for i, path in enumerate(paths):
    #   path_word = word_from_path(induced_subgraph, path)
    #   closeness = closeness_score(word, path_word)
    #   try:
    #     compatibility = compatibility_score(induced_subgraph, path, word)
    #   except IndexError:
    #     compatibility = 0
    #   normalized = normalized_score(closeness, compatibility)
    #   path_ways.append((path, normalized))

    # path = sorted(path_ways, key=operator.itemgetter(1))[0][0]
    # print(path)
    # print(word_from_path(induced_subgraph, path))

    # j = 0
    # for i in range(0, len(path)-1):
    #   edge = induced_subgraph[path[i]][path[i+1]]
    #   # print(edge, i, j, output)
    #   if edge['input']:
    #     if j < len(word):
    #       if edge['input'] == word[j]:
    #         out += edge['output']
    #       else:
    #         out += word[j]
    #       j += 1
    #     else:
    #       out += edge['output']
    runningavgLow, runningavgMed, runningavgHigh, numiterLow, numiterMed, numiterHigh = 0.0, 0.0, 0.0, 0, 0, 0

    pb, sb = 0, 0
    lines = [line.strip() for line in codecs.open("../daru-dataframe/spec/fixtures/{}-train-{}".format(lang, quality), "r", encoding="utf-8")]
    for l in lines:
      print(l.split(u'\t'))
      lemma, form, _ = l.split(u'\t')
      aligned = halign(str(lemma), str(form))
      print(lemma, form, aligned)
      if ' ' not in aligned[0] and ' ' not in aligned[1] and '-' not in aligned[0] and '-' not in aligned[1]:
        pb += numleadingsyms(aligned[0],'_') + numleadingsyms(aligned[1],'_')
        sb += numtrailingsyms(aligned[0],'_') + numtrailingsyms(aligned[1],'_')

    allprules, allsrules = {}, {}
    for l in lines:
      if pb > sb:
        lemma = lemma[::-1]
        form = form[::-1]
      lemma, form, pos = l.split(u'\t')
      pos = pos.strip()
      prules, srules = prefix_suffix_rules_get(lemma, form)

      if pos not in allprules and len(prules) > 0:
        allprules[pos] = {}
      if pos not in allsrules and len(srules) > 0:
        allsrules[pos] = {}

      for r in prules:
        if (r[0],r[1]) in allprules[pos]:
          allprules[pos][(r[0],r[1])] = allprules[pos][(r[0],r[1])] + 1
        else:
          allprules[pos][(r[0],r[1])] = 1

      for r in srules:
        if (r[0],r[1]) in allsrules[pos]:
          allsrules[pos][(r[0],r[1])] = allsrules[pos][(r[0],r[1])] + 1
        else:
          allsrules[pos][(r[0],r[1])] = 1

    # morphological calculations
    devlines = [line.strip() for line in open("../daru-dataframe/spec/fixtures/{}-dev".format(lang), "r").readlines()]
    numcorrect = 0
    numguesses = 0
    print(len(allsrules))
    print(len(allprules))
    for l in devlines:
      lemma, correct, pos = l.split(u'\t')
      lemmaorig = lemma
      if pb > sb:
        lemma = lemma[::-1]
      outform = apply_best_rule(lemma, pos, allprules, allsrules)
      if pb > sb:
        outform = outform[::-1]
      if outform == correct:
        numcorrect += 1
      numguesses += 1
    print(numcorrect)
    print(numcorrect/float(numguesses))
    return True


def apply_best_rule(lemma, pos, allprules, allsrules):
  bestrulelen = 0
  base = "<" + lemma + ">"
  if pos not in allprules and pos not in allsrules:
    return lemma # Haven't seen this inflection, so bail out

  if pos in allsrules:
    applicablerules = [(x[0],x[1],y) for x,y in allsrules[pos].items() if x[0] in base]
    if applicablerules:
      print(applicablerules)
      bestrule = max(applicablerules, key = lambda x: (len(x[0]), x[2], len(x[1])))         
      print(bestrule)
      base = base.replace(bestrule[0], bestrule[1])
      
  if pos in allprules:
    applicablerules = [(x[0],x[1],y) for x,y in allprules[pos].items() if x[0] in base]
    if applicablerules:
      bestrule = max(applicablerules, key = lambda x: (x[2]))
      base = base.replace(bestrule[0], bestrule[1])
              
  base = base.replace('<', '')
  base = base.replace('>', '')
  return base

def numleadingsyms(s, symbol):
  return len(s) - len(s.lstrip(symbol))
    
def numtrailingsyms(s, symbol):
  return len(s) - len(s.rstrip(symbol))

def hamming(s,t):
  return mod_levenshtein(s, t)
  # return sum(1 for x,y in zip(s,t) if x != y)    

def halign(s,t):
  """Align two strings by Hamming distance."""
  slen = len(s)
  tlen = len(t)
  minscore = len(s) + len(t) + 1
  for upad in range(0, len(t)+1):
    upper = '_' * upad + s + (len(t) - upad) * '_'
    lower = len(s) * '_' + t
    score = hamming(upper, lower)
    if score < minscore:
      bu = upper
      bl = lower
      minscore = score

  for lpad in range(0, len(s)+1):
    upper = len(t) * '_' + s
    lower = (len(s) - lpad) * '_' + t + '_' * lpad
    score = hamming(upper, lower)
    if score < minscore:
      bu = upper
      bl = lower
      minscore = score

  zipped = zip(bu,bl)
  newin  = ''.join(i for i,o in zipped if i != '_' or o != '_')
  zipped = zip(bu,bl)
  newout = ''.join(o for i,o in zipped if i != '_' or o != '_')
  return((newin, newout))

def prefix_suffix_rules_get(lemma, form):
  lp,lr,ls,fp,fr,fs = alignprs(lemma, form) # Get six parts, three for in three for out

  # Suffix rules
  ins  = lr + ls + ">"
  outs = fr + fs + ">"    
  srules = set()
  for i in range(min(len(ins), len(outs))):
    srules.add((ins[i:], outs[i:]))
  srules = {(x[0].replace('_',''), x[1].replace('_','')) for x in srules}

  # Prefix rules
  prules = set()
  if len(lp) >= 0 or len(fp) >= 0:
    inp = "<" + lp
    outp = "<" + fp
    for i in range(0,len(fr)):
      prules.add((inp + fr[:i],outp + fr[:i]))
      prules = {(x[0].replace('_',''), x[1].replace('_','')) for x in prules}

  return prules, srules


def alignprs(lemma, form):
  al = levenshtein(lemma, form, substcost = 1.1) # Force preference of 0:x or x:0 by 1.1 cost
  alemma, aform = al[0], al[1]
  # leading spaces
  lspace = max(len(alemma) - len(alemma.lstrip('_')), len(aform) - len(aform.lstrip('_')))
  # trailing spaces
  tspace = max(len(alemma[::-1]) - len(alemma[::-1].lstrip('_')), len(aform[::-1]) - len(aform[::-1].lstrip('_')))
  return alemma[0:lspace], alemma[lspace:len(alemma)-tspace], alemma[len(alemma)-tspace:], aform[0:lspace], aform[lspace:len(alemma)-tspace], aform[len(alemma)-tspace:]

def levenshtein(s, t, inscost = 1.0, delcost = 1.0, substcost = 1.0):
  """Recursive implementation of Levenshtein, with alignments returned."""
  @memolrec
  def lrec(spast, tpast, srem, trem, cost):
    if len(srem) == 0:
      return spast + len(trem) * '_', tpast + trem, '', '', cost + len(trem)
    if len(trem) == 0:
      return spast + srem, tpast + len(srem) * '_', '', '', cost + len(srem)

    addcost = 0
    if srem[0] != trem[0]:
      addcost = substcost
        
    return min((lrec(spast + srem[0], tpast + trem[0], srem[1:], trem[1:], cost + addcost),
               lrec(spast + '_', tpast + trem[0], srem, trem[1:], cost + inscost),
               lrec(spast + srem[0], tpast + '_', srem[1:], trem, cost + delcost)),
               key = lambda x: x[4])

  answer = lrec('', '', s, t, 0)
  return answer[0],answer[1],answer[4]

def memolrec(func):
  """Memoizer for Levenshtein."""
  cache = {}
  @wraps(func)
  def wrap(sp, tp, sr, tr, cost):
    if (sr,tr) not in cache:
      res = func(sp, tp, sr, tr, cost)
      cache[(sr,tr)] = (res[0][len(sp):], res[1][len(tp):], res[4] - cost)
    return sp + cache[(sr,tr)][0], tp + cache[(sr,tr)][1], '', '', cost + cache[(sr,tr)][2]
  return wrap

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
#   pretty_print_graph(tou.graph)

#   q = tou.first()
#   while q < tou.last():
#     q = tou.next(q)
#     # print(q)
#     p = tou.first()
#     # print(p<q)
#     while p < q and not exit_condition_1:
#       tou_dup = tou
#       # tou = tou.merge(p, q)
#       tou = tou.merge(q, p)
#       while not tou.subseq() and not exit_condition_2:
#         r, a, v, s, w, t = tou.find_subseq_violation()

#         print(r, a, v, s, w, t)
#         # '#' depicts end of string
#         exit_condition_2 = (v!=w and a=='#') or (s<q and not is_prefixed_with(v, w))
#         if not exit_condition_2:
#           u = lcp([v, w])
#           tou = tou.push_back(eliminate_prefix(u, v), (r, a, v, s))
#           tou = tou.push_back(eliminate_prefix(u, w), (r, a, w, t))
#           # tou = tou.merge(s, t)
#           tou = tou.merge(t, s)
#           # pretty_print_graph(tou.graph)

#       if not tou.subseq():
#         tou = tou_dup
#       else:
#         exit_condition_1 = True

#       if not exit_condition_1:
#         p = tou.next(p)
#     if not tou.subseq():
#       tou = tou_dup

#   pretty_print_graph(tou.graph)
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

def check_all_testing_data(model, lang, quality):
  c = n = 0
  l = {}
  # T = fetch_testing_data(language=lang)
  # for (source, metadatas, expected_dest) in T:
  #   try:
  prediction = model.guess_output_for(lang, quality)
      # if predicted_dest == expected_dest:
      #   print("{} + {} was expected and received as {}".format(source, metadatas, predicted_dest))
      #   c += 1
      # else:
      #   dist = mod_levenshtein(expected_dest, predicted_dest)
      #   if dist in l:
      #     l[dist] += 1
      #   else:
      #     l[dist] = 1
      #   print("{} + {} was expected to be {}, but received {} instead".format(source, metadatas, expected_dest, predicted_dest))
      # n += 1
    # except IndexError:
    #   print("Some error with the source word {}".format(source))
  # print("\n\nExact word-match accuracy: {}". format(100.00*float(c)/float(n)))
  # print("\n Levenshtein distribution:", l)
