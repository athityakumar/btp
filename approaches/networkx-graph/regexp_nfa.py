from pac_library import *
import operator
import json

def save_clusters(concept, pac):
  i = 1
  for (antecedent_attrs, consequent_attrs) in pac:
    with open('cluster_'+str(i)+'.json', 'w') as outfile:
      json.dump([consequent_attrs, list(concept.attributes_extent(consequent_attrs))], outfile)
    i += 1

def load_cluster(path):
  return(json.loads(open(path).read()))

def add_next_layer(prefix_tree, words, index):
  for word in words:
    if index == 0:
      prefix_tree = force_add_weight(prefix_tree, 'start', word[0]+'_0', 1)      
    else:
      from_node = word[index-1] + '_' + str(index-1)
      to_node = word[index] + '_' + str(index)
      prefix_tree = force_add_weight(prefix_tree, from_node, to_node, 1)
  return(prefix_tree)

def remove_empty_words(words, index):
  new_words = []
  for word in words:
    if len(word) > 0:
      new_words.append(words)
  return(new_words)

language = 'english'
concept = init_dataset(language)
print('Initialized concept')

start1 = time.clock()
pac = concept.pac_basis(concept.is_member, 0.3, 0.4)
end1 = time.clock() - start1

save_clusters(concept, pac)
words, operations = load_cluster('cluster_1.json')

prefix_tree = nx.Graph()
prefix_tree.add_node('start')
prefix_tree.add_node('stop')

index = 0
while len(words) > 0:
  prefix_tree = add_next_layer(prefix_tree, words, index)
  words = remove_empty_words(words, index)
  index += 1
