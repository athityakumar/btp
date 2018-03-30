import os
import networkx as nx

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

    return list(self.graph.nodes)

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
    index_of_a = all_states.index(a)
    if index_of_a == len(all_states)-1:
      next_element = a
    else:
      next_element = self.state(index_of_a+1)
    return next_element

  # TODO
  def merge(self, a, b):
    """
    :param a: An element in the OTST
    :param b: An element in the OTST
    :return merged_otst: OTST with elements a & b merged
    """

    merged_otst = self.graph
    # DO the merging
    self.graph = merged_otst

  def subseq(self):
    """
    :return bool: True if tou is subsequent, else False
    """

    violation = self.find_subseq_violation()
    return(violation is None)

  # TODO
  def find_subseq_violation(self):
    """
    (r,a,v,s) and (r,a,w,t) are 2 edges of tou that violate subseq condition,
    with s<t

    :return (r, a, v, s, w, t): Tuple
    """

    # Iterate through all edge pairs
    # If determinism condition present for any pair,
    #   return edges
    # Else return None

  # TODO
  def push_back(self, element, edge):
    """
    :param element: An element in the OTST
    :param edge: An edge in the OTST, as a tuple (r, a, v, s)
    :return tou: OTST with element pushed back from the edge
    """  

  # TODO
  def form_digraph(self, T):
    """
    :param T: A set of all input/output pairs
    :return graph: A directed networkx graph
    """

    graph  = nx.DiGraph()
    for (input_word, metadata, output_word) in T:

    return(graph)


def prefixed_with(str, prefix):
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

def eliminate_prefix(u, v):
  """
  If v = uw (u=prefix, w=suffix),
  w = u-1 v

  Returns suffix after eliminating prefix

  :param str: An input word / sub-word
  :return inv_str: An inversed string
  """

  if v.find(u) == 0:
    w = v[len(u):]
  else:
    w = v
  return(w)

def OSTIA(T):
  """
  :param T: Finite set of input*output pairs
  :return OSTIA OTST
  """

  exit_condition_1 = exit_condition_2 = False

  tou = OTST(T)
  q = tou.first()
  while q < tou.last():
    q = tou.next()
    p = tou.first()
    while p < q and not exit_condition_1:
      tou_dup = tou
      tou = tou.merge(p, q)
      while not tou.subseq() and not exit_condition_2:
        r, a, v, s, w, t = tou.find_subseq_violation()

        # '#' depicts end of string
        exit_condition_2 = (v!=w and a='#') or (s<q and not prefixed_with(v, w)):
        if not exit_condition_2:
          u = lcp(v, w)
          tou = tou.push_back(eliminate_prefix(u, v), (r, a, v, s))
          tou = tou.push_back(eliminate_prefix(u, w), (r, a, w, t))
          tou = tou.merge(s, t)
      if not tou.subseq():
        tou = tou_dup
      else:
        exit_condition_1 = True

      if not exit_condition_1:
        p = tou.next(p)
    if not tou.subseq():
      tou = tou_dup

  return tou
