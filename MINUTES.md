# Minutes of meetings

- [Jul 25th, 2017 (Tuesday)](#jul-25th-2017-tuesday)
- [Jul 26th, 2017 (Wednesday)](#jul-26th-2017-wednesday)
- [Aug 10th, 2017 (Thursday)](#aug-10th-2017-thursday)
- [Aug 17th, 2017 (Thursday)](#aug-17th-2017-thursday)
- [Aug 24th, 2017 (Thursday)](#aug-24th-2017-thursday)
- [Sep 3rd, 2017 (Sunday)](#sep-3rd-2017-sunday)
- [Oct 10th, 2017 (Tuesday)](#oct-10th-2017-tuesday)
- [Oct 12th, 2017 (Thursday)](#oct-12th-2017-thursday)
- [Oct 19th, 2017 (Thursday)](#oct-19th-2017-thursday)
- [Oct 24th, 2017 (Tuesday)](#oct-24th-2017-tuesday)
- [Nov 3rd, 2017 (Friday)](#nov-3rd-2017-friday)
- [Nov 4th, 2017 (Saturday)](#nov-4th-2017-saturday)
- [Nov 9th, 2017 (Thursday)](#nov-9th-2017-thursday)

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
- **What**: 
  - [x] Support and confidence model, based on the trie data structure tried by me

### Aug 17th, 2017 (Thursday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**: 
  - [x] Create a 5000*5000 DataFrame of source charecters and their positions from left and right, to understand how their frequencies can be used to detect any pattern

### Aug 24th, 2017 (Thursday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**: 
  - [ ] Perform random walk on the generated source adjacency matrix (DataFrame)
  - [x] Create (unigram) DataFrame df1 with vectors `char`, `left_position`, `right_position` and `count`
  - [x] Create (bigram) DataFrame df2 with vectors `char_1`, `left_1`, `right_1`, `char_2`, `left_2`, `right_2` and `count`
  - [x] Create (substring_removal) DataFrame df3 with vectors `source`, `target` and `removed_substrings`
  - [x] Create (operations_sequence) DataFrame df4 with vectors `source`, `target` and `sequence_of_operations`
  - [x] Create (operations) DataFrame df5 with vectors `operation`, `char`, `left_position`, `right_position` and `count`

  Finally, the idea is to automate the task and perform it for all languages and convert all DataFrames to CSV

### Sep 3rd, 2017 (Sunday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**: 
  - [ ] Design traceable structures
  - [ ] Fix adjacency matrix and faster bigram with rgl gem
  - [ ] Apply random walk, random search and logistic regression


### Oct 10th, 2017 (Tuesday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Prof Pawan Goyal, Gaurav Sahu and myself
- **What**: 
  - [ ] Explaining progress till mid-term evaluations
  - [ ] Discussion about choosing better labels and features

### Oct 12th 2017 (Thursday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**: 
  - [ ] Explaining progress till mid-term evaluations
  - [ ] Discussion about choosing better labels and features
  - [ ] I'm given the task of fasttext

### Oct 19th 2017 (Thursday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**: 
  - [ ] According to the set metric, adj_mat seems better than fasttext
  - [ ] Given the task of generating the graph of source words

### Oct 24th, 2017 (Tuesday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir and myself
- **What**: 
  - [ ] Modified LDist to be used to get 10 closest words to a given word
  - [ ] By comparing closest words to the word, chunks of characters can be formed as nodes

### Nov 3rd, 2017 (Friday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir and myself
- **What**: 
  - [ ] Think about adding visualization with JS libraries
  - [ ] Use Giphe to get network data like Diameter, Average Degree, etc.

### Nov 4th, 2017 (Saturday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**: 
  - [ ] Add visualization with JS libraries, by next Thursday
  - [ ] Send Giphe network data today and discuss tomorrow
  
### Nov 9th, 2017 (Thursday)

[(Back to top)](#minutes-of-meetings)

- **Who**: Amrith Krishna sir, Gaurav Sahu and myself
- **What**: 
  - [ ] Preparation for BTP-1 presentation
