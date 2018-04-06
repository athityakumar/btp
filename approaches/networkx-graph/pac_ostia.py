import operator
import os
import networkx as nx
from helper_methods import *
from pac_library import *
import _pickle as pickle
import ostia_regex
import os
import json

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


languages = os.listdir('../daru-dataframe/spec/fixtures/')
langs = set()

for l in languages:
    if '-train' not in l:
        continue
    else:
        langs.add(l.split('-train')[0])

lang_acc_map = {}

quality = 'medium'
for language in langs:
  pac = pickle.load(open("{}_{}_pac.p".format(language, quality), 'rb'))
  testing_data = fetch_testing_data(language=language)
  n = c = 0

  for (source, metadata, expected_dest) in testing_data:
    scores = []
    if metadata not in pac:
      continue
    concept, cluster, _ = pac[metadata]
    if not cluster:
      continue
    for (antecedent_attrs, consequent_attrs) in cluster:
      print(len(consequent_attrs))
      ostia = ostia_regex.OSTIA(consequent_attrs)
      scores.append(ostia.matches_any_path(source))

    min_score, score_tup = sorted(scores, key=operator.itemgetter(0))[0]
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
    print("due to {} with score {}".format(score_tup, min_score))
    n += 1
    # do operations
  lang_acc_map[language]=  100*float(c)/ n


with open('pac_ostia_lang_acc.json', 'w') as pac_os_out:
  json.dump(lang_acc_map, pac_os_out)
