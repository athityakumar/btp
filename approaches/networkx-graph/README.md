# Approach with Graphs

A set of Pythons scripts that tries to represent the given dataset of words and operations into graphs, and then mapping them. This part uses networkx library for graphs, and Gephi for visualization.

### source_pairs.py

This script forms the Graph based on only source words, deciding nodes based on 10 least-modified-LDist values for each word. it supports various parameters :

- Language (set to polish currently, should be added support for CLI ARGV)
- Quality (set to high currently, should be added support for CLI ARGV)
- Mode : 
  - export : Reads from conll data and dumps to csv file
  - import : Reads from dumped csv file (rather than re-build) for quick graph operations