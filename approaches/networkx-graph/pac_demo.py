from pac_library import *

concept = init_dataset('english')
print('Initialized concept')

start1 = time.clock()
pac = concept.pac_basis(concept.is_member, 0.3, 0.4)
end1 = time.clock() - start1

j=0
for (antecedent_attrs, consequent_attrs) in pac:
  j += 1
  print("PAC Implication", j, ":", len(antecedent_attrs), "attributes:", " ->", len(consequent_attrs), "attributes with", len(concept.attributes_extent(set(consequent_attrs))), "objects : ", concept.attributes_extent(set(consequent_attrs)))

print("# of objects:", len(concept.objects()))
print("# of attributes:", len(concept.attributes()))
print("# of Implications:", len(pac))
print(end1)


