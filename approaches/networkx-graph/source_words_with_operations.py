from helper_methods import *

def generate_operations_for_a_wordpair(source, dest):
  operations = list()

  source_length = len(source)
  dest_length   = len(dest)
  max_length    = max(source_length, dest_length)
  for i in range(0, max_length):
    if i >= source_length:
      operations.append("insert_"+dest[i]+"_"+str(i-dest_length))
    elif i >= dest_length:
      operations.append("delete_"+source[i]+"_"+str(i-source_length))
    elif not source[i] == dest[i]:
      operations.append("delete_"+source[i]+"_"+str(i-source_length))
      operations.append("insert_"+dest[i]+"_"+str(i-dest_length))

  return(operations)

def generate_operations_for_wordpairs(wordpairs):
  operations = set()

  for source in wordpairs:
    dest = wordpairs[source]
    operations.union(set(generate_operations_for_a_wordpair(source, dest)))

  return(operations)

def generate_exact_graph_from_operations(G, wordpairs, operations):
  G.add_nodes_from(operations)

  for i, source in enumerate(wordpairs):
    dest            = wordpairs[source]
    word_operations = generate_operations_for_a_wordpair(source, dest)
    if word_operations:

      if word_operations[0].split("_")[0] == "delete":
        from_node = word_operations[0].split("_")[1]
      else:
        rpos = int(word_operations[0].split("_")[2])-1
        if rpos * -1 >= len(source):
          from_node = source[-1]
        else:
          from_node = source[rpos]
      to_node   = word_operations[0]
      uniq_id   = str(i)
      G         = force_add_uid(G, from_node, to_node, uniq_id)           

      for j in range(0, len(word_operations)-1):
        if int(word_operations[j].split("_")[2]) is int(word_operations[j+1].split("_")[2]):
          from_node = word_operations[j]
          to_node   = word_operations[j+1]
          uniq_id   = str(i) + "_" + str(j)
          G         = force_add_uid(G, from_node, to_node, uniq_id)
        else:
          # print(source, dest, word_operations, j)
          if word_operations[j+1].split("_")[0] == "delete":
            from_node = word_operations[j+1].split("_")[1]
          else:
            rpos = int(word_operations[j+1].split("_")[2])-1
            if rpos * -1 >= len(source):
              from_node = source[-1]
            else:
              from_node = source[rpos]
          to_node   = word_operations[j+1]
          uniq_id   = str(i) + "_" + str(j)
          G         = force_add_uid(G, from_node, to_node, uniq_id)           

  return(G)

def generate_links_between_words_and_operations(source_G, operations_G):
  combined_G = nx.compose(source_G, operations_G)

  for word_id, word in enumerate(fetch_exact_words_from_graph(source_G)):
    for letter in list(word):
      for operation in operations_G['start']:
        from_node  = letter
        to_node    = operation
        combined_G = force_add_uid(combined_G, from_node, to_node, word_id)

  return(combined_G)

if __name__ == '__main__':
  import networkx as nx

  # words = ['flatten', 'tantrum', 'rum', 'drum', 'drama']
  # words = ['flatten', 'flatter']
  wordpairs    = dict((('run','running'), ('fly','flying'), ('sky','skying')))
  # wordpairs    = read_wordpairs('btp/spec/fixtures/polish/polish-train-high')
  words        = [word for word in wordpairs]
  source_G     = generate_exact_graph_from_words(words)

  operations          = generate_operations_for_wordpairs(wordpairs)
  source_operations_G = generate_exact_graph_from_operations(source_G, wordpairs, operations)
  source_operations_G = map_edges_uid_to_weight(source_operations_G)

  # pretty_print_graph(source_G)
  # pretty_print_graph(operations_G)

  # combined_G = generate_links_between_words_and_operations(source_G, operations_G)
  # combined_G = map_edges_uid_to_weight(combined_G)
  # print(sorted(combined_G.edges), key=lambda data : -1*data[2]['uid'])
  # print(sorted(source_operations_G.edges(data=True), key=lambda data : data[2]['uid']))
  # print("Words : " + str(words) + "\n")

  new_wordpairs = read_wordpairs('btp/spec/fixtures/polish/polish-uncovered-test')
  # new_wordpairs = {'gly': 'glying'}
  atleast_one_correct_guess = 0
  n_correct_guesses = 0
  n_actual_opns = 0
  for new_source in new_wordpairs:
    # new_source    = list(new_wordpairs)[1]
    new_dest      = new_wordpairs[new_source]

    print(new_source, new_dest)
    actual_operations = generate_operations_for_a_wordpair(new_source, new_dest)
    n_actual_opns += len(actual_operations)
    print("Actual operations", actual_operations)

    guess_operations = dict()

    for node in list(new_source):
      guess = sorted(
        source_operations_G.edges([node], data=True),
        key=lambda data: data[2]['uid'] if data[1].count("_") is not 0 else 0,
        reverse=True
      )[0:1]

      for g in guess:
        key, opn, uid = g
        try:
          guess_operations[opn] += uid['uid']
        except KeyError:
          guess_operations[opn] = uid['uid']

      # print(node, guess)

    sorted_guess_operations = sorted(guess_operations, key=lambda k: guess_operations[k], reverse=True)
    intersection = set(sorted_guess_operations).intersection(set(actual_operations))
    if intersection:
      atleast_one_correct_guess += 1
      n_correct_guesses         += len(intersection)

    # print("\nGuessed max weight operations")
  #   for o in sorted_guess_operations:
  #     print(o, guess_operations[o])
  #   print("\n")

  # print(atleast_one_correct_guess, "/", len(new_wordpairs), "words had atleast one operation guessed correctly")
  # print(n_correct_guesses, "/", n_actual_opns, "operations among correctly guessed")


  # for node in source_G:
  #   print("Node " + str(node) + " : " + str(source_G[node]))

  # visualize_graph(G)
  # exact_words = fetch_exact_words_from_graph(G)
  # print("Words back from the graph are", exact_words)
  # visualize_network(G)
