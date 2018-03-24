from pac_library import *
from regexp_naive import *

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

def compute_suffix_regexp(concept, pac):
  suffix_regexp_data = []
  for (antecedent_attrs, consequent_attrs) in pac:
    suffixes = dict()
    count = 0
    for word in consequent_attrs:
      suffix_set = fetch_suffixes(word)
      for suffix in suffix_set:
        if suffix in suffixes:
          suffixes[suffix] += 1
        else:
          suffixes[suffix] = 1
    suffix_regexp = sorted(suffixes.items(), key=operator.itemgetter(1), reverse=True)
    for (suffix, count) in suffix_regexp:
      prob = count/len(consequent_attrs)
      shared_operations = concept.attributes_extent(consequent_attrs)
      shared_words = consequent_attrs
      suffix_regexp_data.append((suffix, count, prob, shared_operations, shared_words))

  return(sorted(suffix_regexp_data, key=operator.itemgetter(2), reverse=True))

def compute_prefix_regexp(concept, pac):
  prefix_regexp_data = []
  for (antecedent_attrs, consequent_attrs) in pac:
    prefixes = dict()
    count = 0
    for word in consequent_attrs:
      prefix_set = fetch_prefixes(word)
      for prefix in prefix_set:
        if prefix in prefixes:
          prefixes[prefix] += 1
        else:
          prefixes[prefix] = 1

    prefix_regexp = sorted(prefixes.items(), key=operator.itemgetter(1), reverse=True)
    for (prefix, count) in prefix_regexp:
      prob = count/len(consequent_attrs)
      shared_operations = concept.attributes_extent(consequent_attrs)
      shared_words = consequent_attrs
      prefix_regexp_data.append((prefix, count, prob, shared_operations, shared_words))

  return(sorted(prefix_regexp_data, key=operator.itemgetter(2), reverse=True))


def guess_cluster_from_pac2(prefix_regexp_data, suffix_regexp_data, given_word):
  # Pick implication with least number of consequent attrs,
  # and return shared objects (operations)
  matching_suffixes = []
  matching_prefixes = []

  for (suffix, count, prob, shared_operations, shared_words) in suffix_regexp_data:
    if given_word.endswith(suffix):
      for (prefix, count, prob, shared_operations2, shared_words) in prefix_regexp_data:
        if given_word.startswith(suffix):
          return(set(shared_operations).union(shared_operations2))
  return(None)

def guess_cluster_from_pac(prefix_regexp_data, suffix_regexp_data, given_word):
  # Pick implication with least number of consequent attrs,
  # and return shared objects (operations)
  for (suffix, count, prob, shared_operations, shared_words) in suffix_regexp_data:
    if given_word.endswith(suffix):
      return(shared_operations)
  return(None)

def apply_operations(word, operations):
  operations = sorted(operations)
  for operation in operations:
    operation_type, value = operation.split('_')
    if operation_type == 'insert':
      word += value
    else:
      word = word.rstrip(value)
  return(word)

language = 'polish'
testing_words = fetch_testing_words(language)
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

# common_words = fetch_common_words(language)
common_words = testing_words
prefix_regexp_data = compute_prefix_regexp(concept, pac)
suffix_regexp_data = compute_suffix_regexp(concept, pac)

for word in common_words:
  words_cluster_operations = guess_cluster_from_pac(prefix_regexp_data, suffix_regexp_data, word)
  if words_cluster_operations is not None:
    n_words += 1
    actual_word = apply_operations(word, words_cluster_operations)
    expected_word = testing_words[word]
    ldist += levenshtein(actual_word, expected_word)

    print("Source:", word, "Expected:", expected_word, "PAC suggested operations:", words_cluster_operations, "PAC suggested word:", actual_word)
    if actual_word == expected_word:
      exact_word_match += 1

print("Average ldist / word:", ldist/len(common_words))
print(exact_word_match/len(common_words), "exact word matches.")
print(exact_word_match/n_words, "exact word matches when there are matching clusters.")
