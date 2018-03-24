from pac_library import *

def fetch_training_words(language):
  return(read_wordpairs('../daru-dataframe/spec/fixtures/'+language+'-train-high'))

def fetch_testing_words(language):
  return(read_wordpairs('../daru-dataframe/spec/fixtures/'+language+'-dev'))

def fetch_common_words(language):
  training_words = fetch_training_words(language)
  testing_words  = fetch_testing_words(language)
  common_words = set()
  same_words   = set()
  for word in testing_words:
    if word in training_words:
      common_words.add(word)
      if testing_words[word] == training_words[word]:
        same_words.add(word)
  return(same_words)

def guess_cluster_from_pac(pac, word):
  # Pick implication with least number of consequent attrs,
  # and return shared objects (operations)

  cluster = None
  count = None

  for (antecedent_attrs, consequent_attrs) in pac:
    if word in consequent_attrs:
      if count is None or count < len(consequent_attrs):
        count = len(consequent_attrs)
        cluster = consequent_attrs

  return(cluster)

def apply_operations(word, operations):
  operations = sorted(operations)
  for operation in operations:
    operation_type, value = operation.split('_')
    if operation_type == 'insert':
      word += value
    else:
      word = word.rstrip(value)
  return(word)

language = 'english'
testing_words = fetch_testing_words(language)
common_words = fetch_common_words(language)
concept = init_dataset(language)
print('Initialized concept')

start1 = time.clock()
pac = concept.pac_basis(concept.is_member, 0.3, 0.4)
end1 = time.clock() - start1

exact_word_match = 0
n_words = 0
valid_operation_match = 0
n_operations = 0
ldist = 0

for word in common_words:
  words_cluster = guess_cluster_from_pac(pac, word)
  if words_cluster is None:
    print("No cluster found containing Source:", word)
    next
  else:
    n_words += 1
    actual_operations = concept.attributes_extent(set(words_cluster))
    actual_word = apply_operations(word, actual_operations)
    expected_word = testing_words[word]

    print("Source:", word, "Expected:", expected_word, "PAC suggested operations:", actual_operations, "PAC suggested word:", actual_word)
    if actual_word == expected_word:
      exact_word_match += 1

print(exact_word_match/len(common_words), "exact word matches.")
print(exact_word_match/n_words, "exact word matches when there are matching clusters.")
