class OTST:
  def __init__(self, T):
    """
    :param T: An input*output mapping
    """

    # self.T = T
    # tou = T
    # self.tou = tou

  def first:
    """
    :return first_element: First element in the OTST
    """


  def last:
    """
    :return last_element: Last element in the OTST
    """

  def next(a):
    """
    :param T: An element in the OTST
    :return next_element: Next element to a, in the OTST
    """

  def merge(a, b):
    """
    :param a: An element in the OTST
    :param b: An element in the OTST
    :return merged_otst: OTST with elements a & b merged
    """

  def subseq:
    """
    :return bool: True if tou is subsequent, else False
    """

  def find_subseq_violation:
    """
    (r,a,v,s) and (r,a,w,t) are 2 edges of tou that violate subseq condition,
    with s<t

    :return (r, a, v, s, w, t): Tuple
    """

  def push_back(element, edge):
    """
    :param element: An element in the OTST
    :param edge: An edge in the OTST, as a tuple (r, a, v, s)
    :return tou: OTST with element pushed back from the edge
    """  

def prefixed_with(str, prefix):
  """
  :param str: An input word / sub-word
  :param prefix: A prefix to check in the word / sub-word
  :return bool: True if prefix, else False
  """

def lcp(set_of_strings):
  # What's this? Longest common prefix
  # Given on page 449

def eliminate_prefix(u, v):
  """
  If v = uw (u=prefix, w=suffix),
  w = inverse(u)v

  Returns suffix after eliminating prefix

  :param str: An input word / sub-word
  :return inv_str: An inversed string
  """

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
