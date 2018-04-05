from helper_methods import *
import itertools
import math
import time
import random
import pprint

# def print(*args):
#   pp = pprint.PrettyPrinter(indent=4)
#   for arg in args:
#     pp.pprint(arg)

class Concept(nx.Graph):
  """A formal concept (K) has the following properties:

  Attributes:
    objects (G)    : A set of objects
    attributes (M) : A set of attributes
    relations (I)  : A set of relations between objects (G) & attributes (M)
  """

  nqueries = 0
  pn_ratio = 0
  max_pn_ratio = 2

  # def __init__(self, name):
  #   """Return a Customer object whose name is *name*.""" 
  #   self.name = name

  def add_object(self, object_name):
    self.add_node(object_name, type='object')

  def add_objects(self, object_names):
    [self.add_object(object_name) for object_name in object_names]

  def add_attribute(self, attribute_name):
    self.add_node(attribute_name, type='attribute')

  def add_attributes(self, attribute_names):
    [self.add_attribute(attribute_name) for attribute_name in attribute_names]

  def add_relation(self, object_name, attribute_name):
    self.add_object(object_name)
    self.add_attribute(attribute_name)

    self.add_edge(object_name, attribute_name)

  def add_relations(self, relations):
    for (object_name, attribute_name) in relations:
      self.add_relation(object_name, attribute_name)

  def objects(self, attribute_name=None):
    if attribute_name is None:
      objects = [node for (node,data) in self.nodes(data=True) if data['type'] == 'object']
    else:
      objects = self[attribute_name]

    objects = list(objects)
    objects.sort()
    return(objects)

  def attributes(self, object_name=None):
    if object_name is None:
      attributes = [node for (node,data) in self.nodes(data=True) if data['type'] == 'attribute']
    else:
      attributes = self[object_name]

    attributes = list(attributes)
    attributes.sort()
    return(attributes)

  """Given a subset A of objects from G,
  A' = attributes shared by objects in A = objects intent
  """
  def objects_intent(self, object_names):
    if len(object_names) is 0:
      return(self.attributes())
    else:
      attribute_sets = [set(self.attributes(object_name)) for object_name in object_names]
      shared_attributes = set.intersection(*attribute_sets)
      return(shared_attributes)

  """Given a subset B of attributes from m,
  B' = objects shared by attributes in B = attributes extent
  """
  def attributes_extent(self, attribute_names):
    if len(attribute_names) is 0:
      return(self.objects())
    else:
      object_sets = [set(self.objects(attribute_name)) for attribute_name in attribute_names]
      shared_objects = set.intersection(*object_sets)
      return(shared_objects)

  """Given a subset A of objects from G,
  A'  = attributes shared by objects in A = objects intent
  A'' = objects that share attributes in A'
  """
  def objects_superset(self, object_names):
    return(self.attributes_extent(self.objects_intent(object_names)))

  """Given a subset B of attributes from G,
  B'  = objects shared by attributes in B = attributes extent
  B'' = attributes that share objects in B'
  """
  def attributes_superset(self, attribute_names):
    return(self.objects_intent(self.attributes_extent(attribute_names)))

  def all_subsets(self, master_set):
    all_subsets = []

    for subset_size in range(1, len(master_set)+1):
      all_subsets += sorted(list(itertools.combinations(master_set, subset_size)))

    return(all_subsets)

  """All matching attribute subsets such that B = B''
  """
  def set_of_intents(self):
    all_attribute_subsets = self.all_subsets(self.attributes())

    matching_attribute_subsets = set()
    for attribute_subset in all_attribute_subsets:
      if set(attribute_subset) == self.attributes_superset(attribute_subset):
        matching_attribute_subsets.add(attribute_subset)

    return(matching_attribute_subsets)

  def relations(self):
    return(self.edges)

  def pretty_print(self):
    print("\n------------------------------------------------")
    print("Brief overview of this concept")
    print("------------------------------------------------")
    for object_name in self.objects():
      print("Object " + str(object_name) + " : " + str(self.attributes(object_name)))
    print("Number of objects : ", len(self.objects()))
    print("Number of attributes : ", len(self.attributes()))
    print("Number of relations : ", len(self.relations()))
    print("------------------------------------------------")

  """A set of all possible implications between attributes within B
  """
  def implications(self, attribute_names=None):
    if attribute_names is None:
      attribute_names = self.attributes()

    attribute_subsets = self.all_subsets(attribute_names)
    matching_attribute_pairs = set()

    all_attribute_pairs = itertools.combinations(attribute_subsets, 2)
    for (attr_1, attr_2) in all_attribute_pairs:
      attr_1_prime = self.attributes_extent(attr_1)
      attr_2_prime = self.attributes_extent(attr_2)

      if attr_1_prime.issubset(attr_2_prime):
        matching_attribute_pairs.add((attr_1, attr_2))
        # print(attr_1, '->', attr_2)
      else:
        if attr_2_prime.issubset(attr_1_prime):
          matching_attribute_pairs.add((attr_2, attr_1))
          # print(attr_2, '->', attr_1)

    return(matching_attribute_pairs)

  """The set A is closed under a set of implications L if A is closed under every implication in L
  """
  def is_model_of_implication(self, attribute_names, antecedent_attrs, consequent_attrs):
    attribute_names  = set(attribute_names)
    antecedent_attrs = set(antecedent_attrs)
    consequent_attrs = set(consequent_attrs)
    return((not antecedent_attrs.issubset(attribute_names)) or (consequent_attrs.issubset(attribute_names)))

  def is_model_of_implications(self, attribute_names, implications):
    for (antecedent_attrs, consequent_attrs) in implications:
      if not self.is_model_of_implication(attribute_names, antecedent_attrs, consequent_attrs):
        return(False)

    return(True)

  """The set of all sets closed under L, the models of L, is denoted by Mod(L).
  """
  def models(self, set_of_implications=None, attribute_names=None):
    if set_of_implications is None:
      set_of_implications = self.implications()

    if attribute_names is None:
      attribute_names = self.attributes()

    all_attribute_subsets = self.all_subsets(self.attributes()) #! Should these be all attrs?
    matching_attribute_subsets = set()

    for attribute_subset in all_attribute_subsets:
      is_closed = True
      for (antecedent_attrs, consequent_attrs) in set_of_implications:
        is_closed = is_closed and self.is_model_of_implication(attribute_subset, antecedent_attrs, consequent_attrs)

      if is_closed:
        matching_attribute_subsets.add(attribute_subset)
    return(matching_attribute_subsets)

  """For an implication to be valid, X' should be subset of Y'.
  """
  def valid_implication(self, antecedent_attrs, consequent_attrs):
    antecedent_attrs_prime = self.attributes_extent(set(antecedent_attrs)) 
    consequent_attrs_prime = self.attributes_extent(set(consequent_attrs))
    return(antecedent_attrs_prime.issubset(consequent_attrs_prime))

  """The set of all implications valid in K is the theory of K, denoted by Th(K).
  """
  def theory(self):
    all_implications = self.implications()
    matching_implications = set()

    for (antecedent_attrs, consequent_attrs) in all_implications:
      if self.valid_implication(antecedent_attrs, consequent_attrs):
        matching_implications.add((antecedent_attrs, consequent_attrs))

    return(matching_implications)

  """A set L ⊆ Imp(M) is a basis of K if the models of L are the intents of K.
  """
  def is_basis(self, implications):
    return(self.models(implications) == self.set_of_intents())

  """A basis L of K is called irredundant if no strict subset of L is a basis of K
  """
  def is_irredundant_basis(self, implications):
    for subset_size in range(1, len(implications)):
      for implications_subset in itertools.combinations(implications, subset_size):
        if self.is_basis(implications_subset):
          return(False)
    return(True)

  def closure_under_implications(self, attributes, implications):
    stable = False

    while not stable:
      stable = True
      remove_implications = set()
      for (antecedent_attrs, consequent_attrs) in implications:
        if set(antecedent_attrs).issubset(attributes):
          attributes = attributes.union(set(consequent_attrs))
          stable = False
          remove_implications.add((antecedent_attrs, consequent_attrs))

      implications = implications - remove_implications

    return(attributes)

  def nextClosure(self, previous_closure, attribute_names=None, closure_operator=None):
    if previous_closure is None:
      previous_closure = set()

    if attribute_names is None:
      attribute_names = self.attributes()

    attribute_names = list(attribute_names)
    attribute_names.reverse()

    next_closure = set()
    # print('Attributes reversed by lectic order:', attribute_names)

    for attribute_name in attribute_names:
      if attribute_name in previous_closure:
        previous_closure = previous_closure - {attribute_name}
      else:
        next_set = previous_closure.union({attribute_name})
        if closure_operator is None:
          print("''")
          next_closure = self.attributes_superset(next_set)
        else:
          # print("Closing",  previous_closure ,"by", len(closure_operator) ,"implications:", closure_operator)
          next_closure = self.closure_under_implications(next_set, closure_operator)

          # print('Next closure:', next_closure)

        # print('Closure diff:', next_closure - previous_closure)

        if self.hasNoElementLecticallyLessThan(next_closure - previous_closure, attribute_names, attribute_name):
          return(next_closure)

    return(set())


  def hasNoElementLecticallyLessThan(self, subset, complete_list, value):
    sublist       = list(subset)

    index = complete_list.index(value)
    for element in sublist:
      element_index = complete_list.index(element)
      if element_index < index:
        return(False)
    return(True)

  def canonical_basis(self, attribute_names=None):
    # if attribute_names is None:
    #   attribute_names = self.attributes()

    # print(attribute_names)

    implications = set()
    attributes_subset = set()
    attribute_names = self.attributes()

    while attributes_subset != set(attribute_names):
      attributes_superset = self.attributes_superset(attributes_subset)
      # print('Attributes superset:', attributes_superset)

      if attributes_subset != attributes_superset:
        implications = implications.union({(tuple(attributes_subset),tuple( attributes_superset))})
      attributes_subset = self.nextClosure(attributes_subset, attribute_names, implications)
      print(set(attribute_names) - attributes_subset)

    return(implications)

  # Querying for PAC base

  def is_member(self, hypothesis, attributes_subset):
    attributes_subset = set(attributes_subset)
    return(attributes_subset == self.attributes_superset(attributes_subset))

  def generate_subset(self, any_set):
    subset = set()
    for element in any_set:
      if random.random() > 0.5:
        subset.add(element)

    return(subset)

  def generate_negative_counterexample(self, H):
    i = 0
    H_list = list(H)

    # random_implication = H_list[int(random.random()*len(H_list))]
    # random_antecedant, random_consequent = random_implication

    try_index = set()

    for antecedent_attrs, consequent_attrs in H_list:
      if len(self.attributes_extent(set(consequent_attrs))) == 0:
        try_index.add(i)
      i += 1

    while len(self.attributes_extent(set(random_consequent))) != 0:
      random_implication = H_list[int(random.random()*len(H_list))]
      random_antecedant, random_consequent = random_implication    

    return(self.attributes_superset(set(random_antecedant)))

    # index = random.random()
    # for (antecedent_attrs, consequent_attrs) in H:
    #   print((1.0-1.0*i/len(H)))
    #   if not done and index > (1.0-1.0*i/len(H)):
    #     negative_counterexample = set(antecedent_attrs)
    #     done = True
    #     print("Forced counter-example", len(self.attributes_superset(negative_counterexample)))
    #     return(self.attributes_superset(negative_counterexample))
    #   else:
    #     i = i+1

    # print("Forced counter-example", len(negative_counterexample))
    # return(set(self.attributes_superset(negative_counterexample)))
    # li_times = self.li_times(self.nqueries, epsilon, delta)
    # print(li_times)
    # for i in range(int(li_times)):
    # for new_negative_counterexample in self.all_subsets(negative_counterexample):
    #   # new_negative_counterexample = self.generate_subset(negative_counterexample)
    #   print(len(new_negative_counterexample))
    #   if (self.is_member(H, new_negative_counterexample) and not self.is_model_of_implications(new_negative_counterexample, H)):
    #     return(new_negative_counterexample)
    # return(True)

  def generate_positive_counterexample(self, H, M, li_times, is_member):
    for i in range(int(li_times)):
      X = self.generate_subset(M)
      member = is_member(H, X)
      model  = self.is_model_of_implications(X, H)
      if (member and not model) or (not member and model):
        return(X)
    return(True)


  def is_approx_equivalent(self, is_member, epsilon=0.5, delta=0.5):
    M = self.attributes()

    def query_oracle(hypothesis):
      self.nqueries = self.nqueries + 1
      li_times = self.li_times(self.nqueries, epsilon, delta)

      if self.pn_ratio < self.max_pn_ratio:
        self.pn_ratio = self.pn_ratio + 1
        return(self.generate_positive_counterexample(hypothesis, M, li_times, is_member))
        # for i in range(int(li_times)):
        #   # X = random.sample(M, int(random.random()*len(M))+1)
        #   X = self.generate_subset(M)
        #   member = is_member(hypothesis, X)
        #   # print("Membership?", member)
        #   model  = self.is_model_of_implications(X, hypothesis)
        #   # print("Model?", model)
        #   if (member and not model) or (not member and model):
        #     # print("Counter-example:", X)
        #     return(X)
        # return(True)

      else:
        print("Giving negative counter-example")
        self.pn_ratio = 0
        H = hypothesis

        for i in range(int(li_times)):
          for antecedent_attrs, consequent_attrs in H:
            if len(self.attributes_extent(set(consequent_attrs))) == 0:
              antecedent_superset = self.attributes_superset(set(antecedent_attrs))
              if len(self.attributes_extent(antecedent_superset)) != 0:
                print(len(antecedent_superset))
                return(antecedent_superset)

          print("Redirecting to usual positive counter-example")
          return(self.generate_positive_counterexample(H, M, li_times, is_member))


          # X = random.sample(M, int(random.random()*len(M))+1)
          # X = self.generate_negative_counterexample(hypothesis)
          # member = is_member(hypothesis, X)
          # print("Membership?", member)
          # model  = self.is_model_of_implications(X, hypothesis)
          # print("Model?", model)
          # if (member and not model) or (not member and model):
            # print("Counter-example:", X)
            # return(X)
        # return(True)

      #   # while True:
      #   #   X = self.generate_subset(M)
      #   #   member = is_member(hypothesis, X)
      #   #   # print("Membership?", member)
      #   #   model  = self.is_model_of_implications(X, hypothesis)
      #   #   # print("Model?", model)
      #   #   if (not member and model):
      #   #     # print("Counter-example:", X)
      #   #     return(X)
        # return(self.generate_negative_counterexample(hypothesis))

        # self.pn_ratio = self.pn_ratio + 1
        # for i in range(int(li_times)):
        #   # X = random.sample(M, int(random.random()*len(M))+1)
        #   X = self.generate_subset(M)
        #   member = is_member(hypothesis, X)
        #   # print("Membership?", member)
        #   model  = self.is_model_of_implications(X, hypothesis)
        #   # print("Model?", model)
        #   if (not member and model):
        #     # print("Counter-example:", X)
        #     return(X)


    return(query_oracle)

  def li_times(self, i, epsilon, delta):
    return((1.0/epsilon)*(i-(math.log(delta)/math.log(2))))

  def implications_not_respecting_attributes(self, attribute_names, implications):
    disrespectful_implications = set()
    for (antecedent_attrs, consequent_attrs) in implications:
      if not self.is_model_of_implication(attribute_names, antecedent_attrs, consequent_attrs):
        disrespectful_implications.add((antecedent_attrs, consequent_attrs))

    return(disrespectful_implications)

  def replace_disrespectful_implications(self, implications, disrespectful_implications, attribute_names):
    # replace all disrepectful implications A->B by A->BnC
    final_implications = set()
    for implication in implications:
      if implication in disrespectful_implications:
        antecedent_attrs, consequent_attrs = implication
        consequent_attrs = tuple(sorted(set(consequent_attrs).intersection(attribute_names)))
        final_implications.add((antecedent_attrs, consequent_attrs))
      else:
        final_implications.add(implication)

    return(final_implications)

  def find_not_members(self, implications, attribute_names, is_member):
    for (antecedent_attrs, consequent_attrs) in implications:
      antecedent_attrs = set(antecedent_attrs)
      consequent_attrs = set(consequent_attrs)
      attribute_names  = set(attribute_names)

      if attribute_names.intersection(antecedent_attrs) != antecedent_attrs and not is_member(implications, attribute_names.intersection(antecedent_attrs)):
        return((tuple(sorted(antecedent_attrs)), tuple(sorted(consequent_attrs))))

  def clean_hypothesis(self, H):
    all_shared_objects = set()
    H2 = set()
    for (antecedent_attrs, consequent_attrs) in H:
      shared_objects = tuple(sorted(self.attributes_extent(set(consequent_attrs))))
      if shared_objects not in all_shared_objects and len(shared_objects) > 0:
        all_shared_objects.add(shared_objects)
        H2.add((antecedent_attrs, consequent_attrs))
    return(H2)

  def horn1(self, is_member, is_equivalent):
    H = set()

    # print("\n --------------------------------------------------------------------")
    C = is_equivalent(H)
    while C is not True:
      # print("Old hypothesis:", H)
      # print("Counter-example:", C)
      # if some A->B belonging to H does not respect C: not(A doesnt belong to C or B belongs to C)
      disrespectful_implications = self.implications_not_respecting_attributes(C, H)
      if len(disrespectful_implications) is not 0:
        print("Negative counter-example")
        print("Block 1")
        # replace all such implications A->B by A->BnC
        H = self.replace_disrespectful_implications(H, disrespectful_implications, C)
      else:
        print("Positive counter-example")

        # find first A->B belonging to H such that CnA not equal to A and not is_member(H, CnA)
        such_implication = self.find_not_members(H, C, is_member)
        # if such A->B doesnt exist:
        if such_implication is None:
          # add C->M to H
          print("Block 3")
          H.add((tuple(sorted(C)), tuple(self.attributes())))
        else:
          # replace A->B by CnA -> BU(A-C)
          print("Block 2")
          C = set(C)
          H.discard(such_implication)
          antecedent_attrs, consequent_attrs = such_implication
          antecedent_attrs = set(antecedent_attrs)
          consequent_attrs = set(consequent_attrs)
          antecedent_attrs = C.intersection(antecedent_attrs)
          consequent_attrs = consequent_attrs.union(antecedent_attrs - C)
          H.add((tuple(sorted(antecedent_attrs)), tuple(sorted(consequent_attrs))))

      # print("New hypothesis:", H)
      # print("\n --------------------------------------------------------------------")
      C = is_equivalent(H)
      # print("Counter-example:", C)
      # wait_till_user_responds = input("Press enter to go through next loop")
      j = 0
      for (antecedent_attrs, consequent_attrs) in H:
        j += 1
        print("PAC Implication", j, ":", len(antecedent_attrs), "attributes:", " ->", len(consequent_attrs), "attributes with", len(self.attributes_extent(set(consequent_attrs))), "objects:", self.attributes_extent(set(consequent_attrs)))

      # time.sleep(5)

    # print("Number of iterations:", n)
    H = self.clean_hypothesis(H)
    return(H)

  def is_equivalent_probabilistic(self, H):
    M = self.attributes()

    for i in range(int(math.pow(2, len(self.attributes())))):
      X = self.generate_subset(M)
      member = self.is_member(H, X)
      model  = self.is_model_of_implications(X, H)
      if (member and not model) or (not member and model):
        return(X)
    return(True)

  def is_equivalent_deterministic(self, H):
    M = self.attributes()

    for X in self.all_subsets(M):
      member = self.is_member(H, X)
      model  = self.is_model_of_implications(X, H)
      if (member and not model) or (not member and model):
        return(X)
    return(True)

  def pac_basis(self, is_member, epsilon=0.8, delta=0.5):
    return(self.horn1(is_member, self.is_approx_equivalent(is_member, epsilon, delta)))

def generate_operations_for_a_wordpair(source, dest):
  operations = list()

  source_length = len(source)
  dest_length   = len(dest)
  max_length    = max(source_length, dest_length)
  for i in range(0, max_length):
    if i >= source_length:
      operations.append("insert_"+dest[i])
      # operations.append("insert_"+dest[i]+"_"+str(i-dest_length))
    elif i >= dest_length:
      operations.append("delete_"+source[i])
      # operations.append("delete_"+source[i]+"_"+str(i-source_length))
    elif not source[i] == dest[i]:
      operations.append("delete_"+source[i])
      operations.append("insert_"+dest[i])
      # operations.append("delete_"+source[i]+"_"+str(i-source_length))
      # operations.append("insert_"+dest[i]+"_"+str(i-dest_length))

  return(operations)

def init_concept_from_wordpairs(wordpairs):
  concept = Concept()
  for (source, target) in wordpairs:
    if not "*" in source and not "*" in target:
      mutations = iterLCS({'source': source, 'target': target})
      for addition in mutations['added']:
        concept.add_relation("insert_"+addition, source)
      for deletion in mutations['deleted']:
        concept.add_relation("delete_"+deletion, source)
  return(concept)

def init_dataset(i=None):
  concept = Concept()
  if isinstance(i, str):
    # wordpairs = dict((('run','running'), ('fly','flying'), ('sky','skying')))
    wordpairs = read_wordpairs('../daru-dataframe/spec/fixtures/'+i+'-train-high')
    for source in wordpairs:
      target = wordpairs[source]
      if not "*" in source and not "*" in target:
      # if True:
        mutations = iterLCS({'source': source, 'target': target})
        for addition in mutations['added']:
          concept.add_relation("insert_"+addition, source)
        for deletion in mutations['deleted']:
          concept.add_relation("delete_"+deletion, source)
  elif i == 0:
    concept.add_relation('Trollinger', '15C')
    concept.add_relation('Trollinger', '16C')

    concept.add_relation('Beaujolais', '15C')
    concept.add_relation('Beaujolais', '16C')
    concept.add_relation('Beaujolais', '17C')

    concept.add_relation('Burgundy', '15C')
    concept.add_relation('Burgundy', '16C')
    concept.add_relation('Burgundy', '17C')
    concept.add_relation('Burgundy', '18C')

    concept.add_relation('Bordeaux', '15C')
    concept.add_relation('Bordeaux', '16C')
    concept.add_relation('Bordeaux', '17C')
    concept.add_relation('Bordeaux', '18C')
    concept.add_relation('Bordeaux', '19C')

    concept.add_relation('Barolo', '16C')
    concept.add_relation('Barolo', '17C')
    concept.add_relation('Barolo', '18C')
    concept.add_relation('Barolo', '19C')

    concept.add_relation('Barbera', '16C')
    concept.add_relation('Barbera', '17C')
    concept.add_relation('Barbera', '18C')

    concept.add_relation('Brunello', '17C')
    concept.add_relation('Brunello', '18C')
    concept.add_relation('Brunello', '19C')

    concept.add_relation('Negroamaro', '17C')
    concept.add_relation('Negroamaro', '18C')
  elif i == 1:
    relation = []
    relation += [('Air Canada', 'Latin America'), ('Air Canada', 'Europe'),
                ('Air Canada', 'Canada'), ('Air Canada', 'Asia Pacific'),
                ('Air Canada', 'Middle East'), ('Air Canada', 'Africa'),
                ('Air Canada', 'Mexicana'), ('Air Canada', 'Caribbean'),
                ('Air Canada', 'United States')]
    # Air New zealand relation
    relation += [('Air New Zealand', 'Europe'),
                ('Air New Zealand', 'Asia Pacific'),
                ('Air New Zealand', 'United States')]
    # All Nippon Airways relation
    relation += [('All Nippon Airways', 'Europe'),
                ('All Nippon Airways', 'Asia Pacific'),
                ('All Nippon Airways', 'United States')]
    # Ansett Australia relation
    relation += [('Ansett Australia', 'Asia Pacific')]
    # The Australian Airlines Group
    relation += [('The Austrian Airlines Group', 'Europe'),
                ('The Austrian Airlines Group', 'Canada'),
                ('The Austrian Airlines Group', 'Asia Pacific'),
                ('The Austrian Airlines Group', 'Middle East'),
                ('The Austrian Airlines Group', 'Africa'),
                ('The Austrian Airlines Group', 'United States')]
    # British Midland relation
    relation += [('British Midland', 'Europe')]
    # Lufthansa relation
    relation += [('Lufthansa', 'Latin America '), ('Lufthansa', 'Europe'),
                ('Lufthansa', 'Canada'), ('Lufthansa', 'Asia Pacific'),
                ('Lufthansa', 'Middle East'), ('Lufthansa', 'Africa'),
                ('Lufthansa', 'Mexicana'), ('Lufthansa', 'United States')]
    # Mexicana relation
    relation += [('Mexicana', 'Latin America'), ('Mexicana', 'Canada'),
                ('Mexicana', 'Mexicana'), ('Mexicana', 'Caribbean'),
                ('Mexicana', 'United States')]
    # Scandinavian Airlines relation
    relation += [('Scandinavian Airlines', 'Latin America'),
                ('Scandinavian Airlines', 'Europe'),
                ('Scandinavian Airlines', 'Asia Pacific'),
                ('Scandinavian Airlines', 'Africa'),
                ('Scandinavian Airlines', 'United States')]
    # Singapore Airlines relation
    relation += [('Singapore Airlines', 'Europe'),
                ('Singapore Airlines', 'Canada'),
                ('Singapore Airlines', 'Asia Pacific'),
                ('Singapore Airlines', 'Middle East'),
                ('Singapore Airlines', 'Africa'),
                ('Singapore Airlines', 'United States')]
    # Thai Airways International
    relation += [('Thai Airways International', 'Latin America'),
                ('Thai Airways International', 'Europe'),
                ('Thai Airways International', 'Asia Pacific'),
                ('Thai Airways International', 'Caribbean'),
                ('Thai Airways International', 'United States')]
    # United Airlines relation
    relation += [('United Airlines', 'Latin America'),
                ('United Airlines', 'Europe'),
                ('United Airlines', 'Canada'),
                ('United Airlines', 'Asia Pacific'),
                ('United Airlines', 'Mexicana'),
                ('United Airlines', 'Caribbean'),
                ('United Airlines', 'United States')]
    # VARIG relation
    relation += [('VARIG', 'Latin America'), ('VARIG', 'Europe'),
                ('VARIG', 'Asia Pacific'), ('VARIG', 'Africa'),
                ('VARIG', 'Mexicana'), ('VARIG', 'United States')]
    concept.add_relations(relation)
  return(concept)


# [None => dataset, 0 => 'wines', 1 => 'alliance']

# concept = init_dataset()
# print('Initialized concept')

# # print(concept.objects_intent(['sneeze']))

# start1 = time.clock()
# pac = concept.pac_basis(concept.is_member, 0.3, 0.4)
# end1 = time.clock() - start1

# # start2 = time.clock()
# # horn1 = concept.horn1(concept.is_member, concept.is_equivalent_probabilistic)
# # end2 = time.clock() - start2

# # start3 = time.clock()
# # horn2 = concept.horn1(concept.is_member, concept.is_equivalent_deterministic)
# # end3 = time.clock() - start3


# # print("PAC:", pac)
# j=0
# for (antecedent_attrs, consequent_attrs) in pac:
#   j += 1
#   print("PAC Implication", j, ":", len(antecedent_attrs), "attributes:", " ->", len(consequent_attrs), "attributes with", len(concept.attributes_extent(set(consequent_attrs))), "objects")

# print("# of objects:", len(concept.objects()))
# print("# of attributes:", len(concept.attributes()))
# print("# of Implications:", len(pac))
# print(end1)
# # print("Horn probabilistic:", horn1)
# # print(end2)
# # print("Horn Deterministic:", horn2)
# # print(end3)
# # concept.pretty_print()