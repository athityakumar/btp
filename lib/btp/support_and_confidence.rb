require 'pp'
require 'json'
require 'jsonpath'
require 'parallel'

class Trainer
  CONFIDENCE = 0.3.freeze

  def initialize(*paths)
    @paths = paths
  end

  def confidence_traverse(match, data=nil, i=0)
    data          ||= JSON.parse(File.read('trie.json'))
    adds            = JsonPath.on(data, '$..add')
    rems            = JsonPath.on(data, '$..rem')
    opts            = adds.map.with_index { |a, i|  {add: a, rem: rems[i]} }
    opts_count      = opts.each_with_object(Hash.new(0)) { |word,counts| counts[word] += 1 }
    count           = opts_count.values.inject(:+).to_f
    opts_prob       = opts_count.map { |k,v| [k, v/count] }.to_h
    opt, confidence = opts_prob.max_by { |k,v| v }

    return [opt, confidence, i] if ((confidence > CONFIDENCE) || match.empty? || (!(data.keys.include?(match[-1]))))
    confidence_traverse(match[0..-2], data[match[-1]], i+1)
  end

  def guess(source, opts)
    pre_add, post_add = opts[:add]
    pre_rem, post_rem = opts[:rem]
    source = source.sub(pre_rem, '') unless pre_rem == ''
    source = source.reverse.sub(post_rem.reverse, '').reverse unless post_rem == ''
    pre_add + source + post_add
  end

  def parse(summa_data)
    @data = Hash.new { |h,k| h[k] = Hash.new(&h.default_proc) }

    if summa_data
      count = summa_data.count
      summa_data.each { |d| train(d.first, d.last) }
    else
      count = 0
      @paths.each do |path|
        data = File
          .read(path)
          .split("\n")
          .map     { |x| x.split("\t")             }
          .keep_if { |x| x[1].include? 'tense=PST' }

        count += data.count

        data.each { |d| train(d.first, d.last) }
      end
    end

    puts "\nTotal training words: #{count}"

    @data
  end

  private

  def train(source, dest)
    # puts "Training word : #{source} -> #{dest}"
    source, dest = source.reverse, dest.reverse
    @data = dredge(
      @data,
      word_to_keys(source.reverse),
      {
        add: add_str(source.reverse, dest.reverse),
        rem: rem_str(source.reverse, dest.reverse)
      }
    )
  end

  def find(match, source=@data)
    return find(match[1..-1], source[match[0]]) if source.keys.include? match[0]
    return [source] if source.keys == %i[add rem]

    source.map do |k,v|
      while v.is_a?(Hash) && v.values.first.is_a?(Hash)
        v = v.values
      end
      v
    end
  end

  def dredge(hash, list, value = nil)
    # Snip off the last element
    *list, tail = list

    # Iterate through the elements in the path...
    final = list.inject(hash) do |h, k|
      # ...and populate with a hash if necessary.
      h[k] ||= {}
    end

    # Add on the final value
    final[tail] = value

    hash
  end

  def word_to_keys(word)
    word.reverse.split('')
  end

  def longest_common_substr(strings)
    shortest = strings.min_by &:length
    maxlen = shortest.length
    maxlen.downto(0) do |len|
      0.upto(maxlen - len) do |start|
        substr = shortest[start,len]
        return substr if strings.all?{|str| str.include? substr }
      end
    end
  end

  def add_str(source, dest)
    common = longest_common_substr([source, dest])
    add = dest.split common

    case add.size
    when 0
      add = ['', '']       
    when 1
      add = (dest.end_with? common) ? [add[0], ''] : ['', add[0]]
    when 2
    else
      raise "Some issue with common sub string between source #{source} & dest #{dest}."
    end

    add
  end

  def rem_str(source, dest)
    common = longest_common_substr([source, dest])
    rem = source.split common

    case rem.size
    when 0
      rem = ['', '']       
    when 1
      rem = (source.end_with? common) ? [rem[0], ''] : ['', rem[0]]
    when 2
    else
      raise "Some issue with common sub string between source #{source} & dest #{dest}."
    end

    rem
  end
end

# words = File.read('fixture/finnish/finnish-task1-test')
#   .split("\n")
#   .keep_if { |x| x.include?('tense=PST') }
#   .map { |x| x.split("\t") }
# summa_data = false

# words = %w[park stalk crack go]
# summa_data = [
#   %w[talk talked],
#   %w[walk walked],
#   %w[cork corking],
#   %w[fork forking],
#   %w[work working],
#   %w[go gone]
# ]

# inst = Trainer.new('fixture/finnish/finnish-task1-train')
# trie = inst.parse(summa_data)

# File.open('trie.json', 'w') { |f| f.write(JSON.pretty_generate(trie)) }

# puts "Total testing words: #{words.count}"

# correct = 0

# output = Parallel.map(words) do |word, type, solution|
#   opts, confidence, context = inst.confidence_traverse(word)
#   dest                      = inst.guess(word, opts)
#   if dest == solution
#     correct += 1
#   else
#     puts "#{dest} doesn't match with #{solution}"
#   end
#   {source: word, dest: dest, confidence: confidence, actual_solution: solution, context: context}
# end

# File.open('testing.json', 'w') { |f| f.write(JSON.pretty_generate(output)) }

# puts "Got #{correct} / #{words.count} testing words correct."
