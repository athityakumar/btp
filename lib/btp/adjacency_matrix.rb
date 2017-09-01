module BTP
  class AdjacencyMatrix
    def initialize(path)
      @path      = path
      @words     = []
      @alphabets = []
    end

    def parse(summa_data=nil)
      @words = Helper.read_input(summa_data, @path)
      compute_counters(@words)
      @alphabets = @words.map { |word| word.split('') }.flatten.uniq.sort

      puts "Unique alphabets: #{@alphabets}"
      puts "Unique alphabets count: #{@alphabets.count}"
      puts "Words count: #{@words.count}"
    
      @fields = @alphabets.map do |alphabet|
        [
          alphabet,
          (0..@left_most-1).map { |i| "#{alphabet}_#{i}" },
          (@right_most+1..-1).map { |j| "#{alphabet}_#{j}" },
          (0..@left_most-1).map do |i|
            (@right_most+1..-1).map do |j|
              "#{alphabet}_#{i}_#{j}"
            end
          end
        ]
      end.flatten

      puts "DataFrame size: #{@fields.count} = "\
           "#{@alphabets.count}*#{@left_most}*#{@left_most} + "\
           "#{@alphabets.count}*#{@left_most}*2 + #{@alphabets.count}"

      @dataframe = Daru::DataFrame.new({}, order: @fields, index: @fields)
      @words.each { |word| adjacency_matrix(word) }
      @dataframe.replace_values(nil, 0)

      @dataframe
    end

    private

    def compute_counters(words)
      total = 0.0
      length_frequency = Hash
                         .new(0)
                         .tap { |h| words.map(&:size).each { |word| h[word] += 1 } }
                         .sort_by { |k, _v| k }
                         .map { |k, v| [k, (total+=v)] }
                         .map { |k, v| [k, v/total] }
                         .to_h

      @left_most  = (length_frequency.find { |_k, v| v > 0.7 }.first - 1).freeze
      @right_most = (-1 * @left_most - 1).freeze

      puts "Left most: #{@left_most}"
    end

    def adjacency_matrix(word)
      i = 0
      word_length = word.length

      while i < word_length
        j = i+1
        while j < word_length
          update_adjacency_matrix(i, i - word_length, word[i], j, j - word_length, word[j])
          update_adjacency_matrix(j, j - word_length, word[j], i, i - word_length, word[i])
          j += 1
        end
        i += 1
      end
    end

    def update_adjacency_matrix(left1, right1, char1, left2, right2, char2)
      update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{left2}_#{right2}") if left1 < @left_most && left2 < @left_most && right1 > @right_most && right2 > @right_most
      update_at("#{char1}_#{right1}", "#{char2}_#{left2}_#{right2}") if left2 < @left_most && right1 > @right_most && right2 > @right_most
      update_at("#{char1}_#{left1}", "#{char2}_#{left2}_#{right2}") if left1 < @left_most && left2 < @left_most && right2 > @right_most
      update_at(char1, "#{char2}_#{left2}_#{right2}") if left2 < @left_most && right2 > @right_most

      update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{right2}") if left1 < @left_most && right1 > @right_most && right2 > @right_most
      update_at("#{char1}_#{right1}", "#{char2}_#{right2}") if right1 > @right_most && right2 > @right_most
      update_at("#{char1}_#{left1}", "#{char2}_#{right2}") if left1 < @left_most && right2 > @right_most
      update_at(char1, "#{char2}_#{right2}") if right2 > @right_most

      update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{left2}") if left1 < @left_most && left2 < @left_most && right1 > @right_most
      update_at("#{char1}_#{right1}", "#{char2}_#{left2}") if left2 < @left_most && right1 > @right_most
      update_at("#{char1}_#{left1}", "#{char2}_#{left2}") if left1 < @left_most && left2 < @left_most
      update_at(char1, "#{char2}_#{left2}") if left2 < @left_most

      update_at("#{char1}_#{left1}_#{right1}", char2) if left1 < @left_most && right1 > @right_most
      update_at("#{char1}_#{right1}", char2) if right1 > @right_most
      update_at("#{char1}_#{left1}", char2) if left1 < @left_most
      update_at(char1, char2)
    end


    def update_at(key1, key2)
      if @dataframe[key1][key2]
        @dataframe[key1][key2] += 1
      else
        @dataframe[key1][key2] = 1
      end
    end
  end
end