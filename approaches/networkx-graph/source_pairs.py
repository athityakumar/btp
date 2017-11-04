from helper_methods import *
from difflib import SequenceMatcher

def mod_levenshtein(s1, s2):
  if len(s1) < len(s2):
    return(mod_levenshtein(s2, s1))

  if len(s2) == 0:
    return(len(s1))


  if s1 == s2:
    return(0)

  previous_row = range(len(s2) + 1)
  for i, c1 in enumerate(s1):
    current_row = [i + 1]
    for j, c2 in enumerate(s2):
      insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
      deletions = current_row[j] + 1       # than s2

      # Modification to prevent substitutions
      substitutions = previous_row[j] + (c1 != c2) * 1000

      current_row.append(min(insertions, deletions, substitutions))
    previous_row = current_row

  return(previous_row[-1])


from difflib import SequenceMatcher

def find_common_chunks(string1, string2):
  match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))

  if match.size == 0:
    return([])
  else:
    common = string1[match.a: match.a + match.size]
    return([(match.a, match.a+match.size)] + find_common_chunks(string1.replace(common, '<'*match.size, 1), string2.replace(common, '>'*match.size, 1)))

def find_chunks(string1, string2):
  common_chunks = find_common_chunks(string1, string2)
  common_chunks = sorted(
    common_chunks,
    key=lambda data : data[0]
  )

  chunks = list()

  left = 0
  right = 0

  for common in common_chunks:
    start, stop = common
    right = start
    chunks += list(string1[left:right])
    chunks.append(string1[start:stop])
    left = stop

  chunks += list(string1[left:])

  return(chunks)

def export_source_graph_to_csv(source_G, csv_filename):
  sorted_edges = tuple(
    sorted(
      source_G.edges(data=True),
      key=lambda data : data[2]['weight'],
      reverse=True
    )
  )

  file = open(csv_filename,'w')
  file.write("Source,Target,Weights\n")

  for sorted_edge in sorted_edges:
    from_node, to_node, weight = sorted_edge
    file.write(from_node + ',' + to_node + ',' + str(weight['weight']) + "\n")

  file.close()

def import_source_graph_from_csv(csv_filename):
  file = open(csv_filename, 'r')
  source_G = nx.DiGraph()

  for line in file.readlines():
    if not line == "Source,Target,Weights\n":
      from_node, to_node, weight = line.split(',')
      source_G.add_edge(from_node, to_node, weight=int(weight))

  return(source_G)

if __name__ == '__main__':
  print('Started reading words')

  # FIXME: Add CLI ARGV support for below options, for batch operation on server
  language     = 'polish'
  qualities    = ['low', 'medium', 'high']
  quality      = qualities[2]
  filename     = "csv/" + language + "_" + quality
  modes        = ['import', 'export']
  mode         = modes[0]

  if mode == 'export':

    # FIXME: Have this filepath to conll2017/all/task1/ given in .env file
    # as environment variable

    filepath     = '../../../conll2017/all/task1/' + language + '-train-' + quality
    wordpairs    = read_wordpairs(filepath)
    words        = set([word for word in wordpairs])
    n_closest    = 10
    print(len(words))

    # words = ['live', 'dive', 'give', 'giver', 'peal', 'seal', 'heal', 'halar']
    # print(words)
    # n_closest = int(len(words)/4)

    print('Done reading words : ', len(words))
    nodes = set()
    lDist = dict()
    representation = dict()
    source_G       = nx.DiGraph()
    source_G.add_node('start')
    source_G.add_node('stop')

    print('Started computing mod lDist')
    for word_1 in words:
      lDist[word_1] = set()
      for word_2 in words:
        if not word_1 == word_2:
          lDist[word_1].add((word_2, mod_levenshtein(word_1, word_2)))
    print('Done computing mod lDist')

    wrong = 0

    print('Started computing chunks and nodes')
    for word in words:
      representation[word] = dict()
      closest_words = sorted(lDist[word], key=lambda neighbors: neighbors[1])[:int(n_closest)]
      for closest_word, closest_word_distance in closest_words:
        merged_chunks  = find_chunks(word, closest_word)
        if not ''.join(merged_chunks) == word:
          print(word, closest_word, merged_chunks)
          wrong += 1
        representation[word] = update_dict(representation[word], ' '.join(merged_chunks), 1)
        source_G  = force_add_weight(source_G, 'start', merged_chunks[0], 1)
        source_G  = force_add_weight(source_G, merged_chunks[-1], 'stop', 1)
        for i in range(0, len(merged_chunks)-1):
          from_node = merged_chunks[i]
          to_node   = merged_chunks[i+1]
          source_G  = force_add_weight(source_G, from_node, to_node, 1)
 
    pretty_print_graph(source_G)
    print(wrong)

    export_source_graph_to_csv(source_G, filename+'.csv')
    source_G.remove_node('start')
    source_G.remove_node('stop')
    source_G = nx.relabel_nodes(source_G, {' ': '?'})
    export_source_graph_to_csv(source_G, filename+'-gephi.csv')

  else:

    print('Started importing saved graph')
    source_G = import_source_graph_from_csv(filename+'.csv')
    pretty_print_graph(source_G)
    source_G.remove_node('start')
    source_G.remove_node('stop')
    pretty_print_graph(source_G)
