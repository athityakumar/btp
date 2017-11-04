from helper_methods import *

def recursive_fetch_next_character(G, node, word_id, lpos):
  neighbors    = G[node]
  required_uid = str(word_id)+"_"+str(lpos)


  for neighbor in neighbors:
    if required_uid in G[node][neighbor]['uid']:
      return(neighbor + recursive_fetch_next_character(G, neighbor, word_id, lpos+1))

  return('')

def fetch_exact_words_from_graph(G):
  guess_words = list()

  beginnings = dict(G['start'])
  for key in beginnings:
    word_ids = beginnings[key]['uid']
    for word_id in word_ids:
      guess_words.append(key + recursive_fetch_next_character(G, key, word_id, 0))

  return(guess_words)

def generate_exact_graph_from_words(words):
  letters = set()
  G       = nx.DiGraph()

  for word in words:
    for letter in list(word):
      letters.add(letter)

  G.add_nodes_from(letters)
  G.add_node('start')
  G.add_node('stop')


  for i, word in enumerate(words):
    G = force_add_uid(G, 'start', word[0], i)
    G = force_add_uid(G, word[-1], 'stop', i)

    for lpos in range(0, len(word)-1):
      from_node = word[lpos]
      to_node   = word[lpos+1]
      uniq_id   = str(i) + "_" + str(lpos)
      G         = force_add_uid(G, from_node, to_node, uniq_id)

  return(G)

def generate_guess_graph_from_words(words, start_weight, stop_weight, node_weight):
  letters = set()
  G       = nx.DiGraph()

  for word in words:
    for letter in list(word):
      letters.add(letter)

  G.add_nodes_from(letters)
  G.add_node('start')
  G.add_node('stop')


  for i, word in enumerate(words):
    G = force_add_weight(G, 'start', word[0], start_weight)
    G = force_add_weight(G, word[-1], 'stop', stop_weight)

    # G = force_add_weight(G, word[0], 'start', marker_weight)
    # G = force_add_weight(G, 'stop', word[-1], marker_weight)


    for lpos in range(0, len(word)-1):
      from_node = word[lpos]
      to_node   = word[lpos+1]
      G         = force_add_weight(G, from_node, to_node, node_weight)
      # G         = force_add_weight(G, to_node, from_node, node_weight)

  return(G)

def fetch_guess_words_from_graph(G, node, prefix=''):
  sort = sorted(G.edges([node], data=True), key=lambda data : -1*data[2]['weight'])
  if sort[0][1] == 'stop' and sort[0][2] == sort[1][2]:
    max_weighed_neighbor = sort[1][1]
  else:
    max_weighed_neighbor = sort[0][1]

  # print(max_weighed_neighbor)
  G[node][max_weighed_neighbor]['weight'] -= 1

  if max_weighed_neighbor == 'stop':
    return(G, prefix + '')
  else:
    return(fetch_guess_words_from_graph(G, max_weighed_neighbor, prefix=prefix+max_weighed_neighbor))

def guess_words_from_graph(G):
  words = list()
  nodes = list()
  return(words)

def inverse_weight(graph, weight='weight'):
  copy_graph = graph.copy()
  for n in copy_graph:
    eds = copy_graph[n]
    for ed, eattr in eds.items():
      copy_graph[n][ed][weight] = eattr[weight] * -1
  return(copy_graph)

def longest_path_and_length(graph, s, t, weight='weight'):
  i_w_graph = inverse_weight(graph, weight)
  length, path = nx.bidirectional_dijkstra(i_w_graph, s, t)
  # path = nx.dijkstra_path(i_w_graph, s, t)
  # length = nx.dijkstra_path_length(i_w_graph, s, t) * -1
  # path = nx.astar_path(i_w_graph, s, t)
  # length = nx.astar_path_length(i_w_graph, s, t)
  return(path, length)

def map_weights_to_probability(G):
  for node in G:
    sum_of_all_weights = 0
    for neighbor in G[node]:
      sum_of_all_weights += G[node][neighbor]['weight']
    for neighbor in G[node]:
      G[node][neighbor]['weight'] /= sum_of_all_weights

  return(G)

def map_weights_to_probability_with_weights(G):
  for node in G:
    sum_of_all_weights = 0
    for neighbor in G[node]:
      sum_of_all_weights += G[node][neighbor]['weight']
    for neighbor in G[node]:
      G[node][neighbor]['probability'] = G[node][neighbor]['weight'] / sum_of_all_weights

  return(G)


def simple_cycles(G):
  return(list(nx.simple_cycles(G)))

def remove_cycles(G):
  G.add_node('loop_from')
  G.add_node('loop_to')

  while not len(simple_cycles(G)) == 0:
    cycle = simple_cycles(G)[0]
    print(cycle)

    min_weight_from_node = cycle[-1]
    min_weight_to_node   = cycle[0]
    min_weight = G[min_weight_from_node][min_weight_to_node]['weight']

    for i in range(0, len(cycle)-1):
      weight = G[cycle[i]][cycle[i+1]]['weight']
      if weight < min_weight:
        min_weight = weight
        min_weight_from_node = cycle[i]
        min_weight_to_node   = cycle[i+1]

    print(min_weight, min_weight_from_node, min_weight_to_node, G[min_weight_from_node][min_weight_to_node])

    G.remove_edge(min_weight_from_node, min_weight_to_node)

    G = force_add_weight(G, min_weight_from_node, 'loop_from', min_weight)
    G = force_add_weight(G, 'loop_to', min_weight_to_node, min_weight)

    # G = force_add_weight(min_weight_from_node, 'stop', 1)
    G = map_weights_to_probability_with_weights(G)

    if not cycle[-1] == min_weight_from_node and not cycle[0] == min_weight_to_node:
      G[cycle[i]][cycle[i+1]]['weight'] -= min_weight
    for i in range(0, len(cycle)-1):
      if not cycle[i] == min_weight_from_node and not cycle[i+1] == min_weight_to_node:
        G[cycle[i]][cycle[i+1]]['weight'] -= min_weight

    # edges_to_remove.add((min_weight_from_node, min_weight_to_node))

  return(G)

# def djikstra_algo(G, source):
# #  3      create vertex set Q
#   Q = set()
#   infinity = 100000
# #  4
# #  5      for each vertex v in Graph:             // Initialization
# #  6          dist[v] ← INFINITY                  // Unknown distance from source to v
# #  7          prev[v] ← UNDEFINED                 // Previous node in optimal path from source
# #  8          add v to Q                          // All nodes initially in Q (unvisited nodes)
#   prev = dict()
#   dist = dict()
#   for node in G:
#     dist[node] = 0
#     prev[node] = None
#     Q.add(node)

# #  9
# # 10      dist[source] ← 0                        // Distance from source to source
#   dist[source] = infinity
# # 11      
# # 12      while Q is not empty:
#   while not len(Q) == 0:
#     print(Q)
# # 13          u ← vertex in Q with min dist[u]    // Node with the least distance
# # 14                                                      // will be selected first
# # 15          remove u from Q 
#     u = list(dist.keys())[list(dist.values()).index(min([dist[vertex] for vertex in Q]))]
#     print(u)
#     Q.remove(u)
# # 16          
# # 17          for each neighbor v of u:           // where v is still in Q.
# # 18              alt ← dist[u] + length(u, v)
# # 19              if alt < dist[v]:               // A shorter path to v has been found
# # 20                  dist[v] ← alt 
# # 21                  prev[v] ← u 
#     for v in G[u]:
#       alt = dist[u] + G[u][v]['weight']
#       if alt > dist[v]:
#         dist[v] = alt
#         prev[v] = u
# # 22
# # 23      return dist[], prev[]
#   return(list(dist) + list(prev))

def open_loops(G):
  G = force_add_weight(G, 'loop_from', 'loop_to', 0)
  return(G)

if __name__ == '__main__':
  # words = ['flatten', 'tantrum', 'rum', 'drum', 'drama']
  # words = ['flatten', 'flatter']
  words = ['rum', 'drum', 'drambler', 'drain']

  # wordpairs    = read_wordpairs('../btp/spec/fixtures/polish/polish-train-high')
  # words        = [word for word in wordpairs]
  # words        = words[0:20]

  start_weight  = 1
  stop_weight   = 1
  node_weight   = 1
  source_G      = generate_guess_graph_from_words(words, start_weight, stop_weight, node_weight)
  # source_G      = map_weights_to_probability(source_G)
  source_G      = map_weights_to_probability_with_weights(source_G)
  source_G      = remove_cycles(source_G)

  if len(source_G.edges) < (len(source_G.nodes) * len(source_G.nodes)) / 5 or len(source_G.nodes) < 10:
    pretty_print_graph(source_G)
    # visualize_graph(source_G, 'weight')
    # visualize_network(source_G, 'weight')

  # try:
  #   sp=nx.shortest_path(source_G, 'start', 'stop')
  #   for n in sp:
  #     print(n)
  # except nx.NetworkXNoPath:
  #   print("None")

  # brute_force_guess_words = list()
  # for path in nx.all_simple_paths(source_G, source='start', target='stop'):
  #   brute_force_guess_words.append(''.join(path[1:-1]))

  # print("Words back from the graph are", brute_force_guess_words)
  # compare(words, brute_force_guess_words)

  # brute_force_guess_words = list()
  # for path in nx.all_simple_paths(source_G, source='start', target='stop'):
  #   brute_force_guess_words.append(''.join(path[1:-1]))

  # print("Words back from the graph are", brute_force_guess_words)
  # compare(words, brute_force_guess_words)

  guess_words = list()
  while not empty_graph(source_G):
    try:
      max_weighted_path, weights = longest_path_and_length(source_G, 'start', 'stop')
      # max_weighted_path, weights = longest_path_and_length(source_G, 'start', 'stop')
      # max_weighted_path, weights = longest_path_and_length(source_G, 'stop', 'start')

      max_weighted_path_nodes   = max_weighted_path[1:-1]
      # print(''.join(max_weighted_path_nodes)[::-1])
      # print(''.join(max_weighted_path_nodes))
      guess_words.append(''.join(max_weighted_path_nodes))
      print(''.join(max_weighted_path_nodes))
      for i in range(0, len(max_weighted_path)-1):
        from_node = max_weighted_path[i]
        to_node   = max_weighted_path[i+1]
        weight    = source_G[from_node][to_node]['weight'] 
        if from_node == 'start':
          if weight == start_weight:
            source_G.remove_edge(from_node, to_node)
          else:
            source_G[from_node][to_node]['weight'] -= start_weight
        elif to_node == 'stop':
          if weight == stop_weight:
            source_G.remove_edge(from_node, to_node)
          else:
            source_G[from_node][to_node]['weight'] -= stop_weight
        else:
          if weight == node_weight:
            source_G.remove_edge(from_node, to_node)
          else:
            source_G[from_node][to_node]['weight'] -= node_weight
    except nx.NetworkXNoPath:
      source_G = open_loops(source_G)
      pretty_print_graph(source_G)
      break

  compare(words, guess_words)
  # guessed_words = guess_words_from_graph(source_G)
  # print("Words back from the graph are", guessed_words)
  # compare(words, guessed_words)
