from pac_library import *
import operator

def fetch_suffixes(word):  
  suffixes = set()
  word = word[1:]

  while len(word) >= 1:
    suffixes.add(word)
    word = word[1:]

  return(suffixes)

def fetch_prefixes(word):  
  prefixes = set()
  word = word[:-1]

  while len(word) >= 1:
    prefixes.add(word)
    word = word[:-1]

  return(prefixes)

# language = 'english'
# concept = init_dataset(language)
# print('Initialized concept')

# start1 = time.clock()
# pac = concept.pac_basis(concept.is_member, 0.3, 0.4)
# end1 = time.clock() - start1

# for (antecedent_attrs, consequent_attrs) in pac:
#   prefixes = dict()
#   suffixes = dict()
#   for word in consequent_attrs:
#     prefix_set = fetch_prefixes(word)
#     suffix_set = fetch_suffixes(word)

#     for prefix in prefix_set:
#       if prefix in prefixes:
#         prefixes[prefix] += 1
#       else:
#         prefixes[prefix] = 1

#     for suffix in suffix_set:
#       if suffix in suffixes:
#         suffixes[suffix] += 1
#       else:
#         suffixes[suffix] = 1

#   print("Implication with operations", concept.attributes_extent(consequent_attrs), ", sample words:", consequent_attrs[:4])

#   print("Prefix regexp:", sorted(prefixes.items(), key=operator.itemgetter(1), reverse=True)[:4])
#   print("Suffix regexp:", sorted(suffixes.items(), key=operator.itemgetter(1), reverse=True)[:4])
