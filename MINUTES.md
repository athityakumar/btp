# Minutes of meetings

- [Jul 25th, 2017 (Tuesday)](#jul-25th-2017-tuesday)
- [Jul 26th, 2017 (Wednesday)](#jul-26th-2017-wednesday)
- [Aug 10th, 2017 (Thursday)](#aug-10th-2017-thursday)
- [Aug 17th, 2017 (Thursday)](#aug-17th-2017-thursday)
- [Aug 24th, 2017 (Thursday)](#aug-24th-2017-thursday)

### Jul 25th, 2017 (Tuesday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Prof Pawan Goyal, Amrith Krishna sir, Gaurav Sahu and myself
- **What**: General discussion on the BTP (Program synthesis)

### Jul 26th, 2017 (Wednesday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**:
  - Clarification on initial approach of guessing inflection from source word by giving importance to suffix
  - Separation of the task between Gaurav and myself

### Aug 10th, 2017 (Thursday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir and myself
- **What**: Support and confidence model, based on the trie data structure tried by me

### Aug 17th, 2017 (Thursday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**: Create a 5000*5000 DataFrame of source charecters and their positions from left and right, to understand how their frequencies can be used to detect any pattern

### Aug 24th, 2017 (Thursday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**: 
  - Perform random walk on the generated source adjacency matrix (DataFrame)
  - Create (unigram) DataFrame df1 with vectors `char`, `left_position`, `right_position` and `count`
  - Create (bigram) DataFrame df2 with vectors `char_1`, `left_1`, `right_1`, `char_2`, `left_2`, `right_2` and `count`
  - Create (substring_removal) DataFrame df3 with vectors `source`, `target` and `removed_substrings`
  - Create (operations_sequence) DataFrame df4 with vectors `source`, `target` and `sequence_of_operations`
  - Create (operations) DataFrame df5 with vectors `operation`, `char`, `left_position`, `right_position` and `count`

  Finally, the idea is to automate the task and perform it for all languages and convert all DataFrames to CSV
