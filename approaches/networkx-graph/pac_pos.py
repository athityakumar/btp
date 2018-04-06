import operator
import os
import networkx as nx
from helper_methods import *
from pac_library import *
import _pickle as pickle

def parse_metadata_words(language='english', quality='low'):
  metadata_words = {}
  filepath = "../daru-dataframe/spec/fixtures/{}-train-{}".format(language, quality)
  file = open(filepath,'r')
  for line in file.readlines():
    source, dest, metadata = line.split("\t")
    if not "*" in source and not "*" in dest:
      metadata = metadata.strip()
      if metadata in metadata_words:
        metadata_words[metadata].append((source, dest))
      else:
        metadata_words[metadata] = []
  return(metadata_words)

def parse_metadata_fca(metadata_words):
  metadata_fca = {}
  for metadata in metadata_words:
    wordpairs = metadata_words[metadata]
    print(wordpairs)
    concept = init_concept_from_wordpairs(wordpairs)
    if len(concept.objects()) > 0:
      start1 = time.clock()
      pac = concept.pac_basis(concept.is_member, 0.1, 0.1)
      end1 = time.clock() - start1
    else:
      pac, end1 = None, None
    metadata_fca[metadata] = (concept, pac, end1)
  return(metadata_fca)

languages = os.listdir('../daru-dataframe/spec/fixtures/')
langs = set()

for l in languages:
    if '-train' not in l:
        continue
    else:
        langs.add(l.split('-train')[0])

quality = 'medium'

for language in langs:
  metadata_words = parse_metadata_words(language=language, quality=quality)
  metadata_fca = parse_metadata_fca(metadata_words)
  print(metadata_fca)
  for metadata in metadata_fca:
    print(metadata)
    concept, pac, end1 = metadata_fca[metadata]
    j=0
    if pac:
      for (antecedent_attrs, consequent_attrs) in pac:
        j += 1
        print("PAC Implication", j, ":", len(antecedent_attrs), "attributes:", " ->", len(consequent_attrs), "attributes with", len(concept.attributes_extent(set(consequent_attrs))), "objects : ", concept.attributes_extent(set(consequent_attrs)))

      print("# of objects:", len(concept.objects()))
      print("# of attributes:", len(concept.attributes()))
      print("# of Implications:", len(pac))
      print(end1)

  with open("{}_{}_pac.p".format(language, quality), 'wb') as pacout:
    pickle.dump(metadata_fca, pacout)
