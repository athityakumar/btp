import operator
import os
import networkx as nx
from helper_methods import *
from pac_library import *
import _pickle as pickle
import ostia_regex

def fetch_testing_data(language='english'):
  filepath = "../daru-dataframe/spec/fixtures/{}-dev".format(language)
  T = list()
  file = open(filepath,'r')
  for line in file.readlines():
    source, expected_dest, metadata = line.split("\t")
    if not "*" in source and not "*" in expected_dest:
      metadata = metadata.strip("\n")
      T.append((source, metadata, expected_dest))
      # print("{} + {} = {}".format(source, " + ".join(metadata), dest))
  print("Providing all test words in structured manner")
  T = sorted(T, key=operator.itemgetter(0))
  return T

def inflect(word, operations):
  for operation in operations:
    method, chunk = operation.split('_')
    if method == 'delete':
      word = word.rstrip(chunk)
    else:
      word = word + chunk
  return word

pac = pickle.load(open('global_high_pac.p', 'rb'))
testing_data = fetch_testing_data()
n = c = 0
scores = []

for (source, metadata, expected_dest) in testing_data:
  if metadata not in pac:
    continue
  concept, cluster, _ = pac[metadata]
  if not cluster:
    continue
  for (antecedent_attrs, consequent_attrs) in cluster:
    ostia = ostia_regex.OSTIA(consequent_attrs)
    scores.append(ostia.matches_any_path(source))

  min_score, score_tup = min(scores, key=operator.itemgetter(0))
  just_scores = [s for s, _ in scores]
  index_of_min_score = just_scores.index(min_score)
  _, cluster_words = list(cluster)[index_of_min_score]
  operations = concept.objects_intent(set(cluster_words))
  computed_dest = inflect(source, operations)
  if computed_dest == expected_dest:
    c += 1
    print("{} + {}: Expected and found {}".format(source, metadata, computed_dest))
  else:
    print("{} + {}: Expected {} but found {}".format(source, metadata, expected_dest, computed_dest))
  n += 1
  # do operations
print(100*float(c)/ n)