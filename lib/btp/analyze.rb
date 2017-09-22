module BTP
  class DataFrames

    attr_reader :char_analysis
    attr_reader :matching_words

    @@coefficients = [
      [0.989, 0.005, 0.005, 0.001],
      [0.979, 0.01, 0.01, 0.001],
      [0.89, 0.05, 0.05, 0.01],
      [0.85, 0.07, 0.07, 0.01],
      [0.79, 0.1, 0.1, 0.01],
      [0.75, 0.12, 0.12, 0.01],
      [0.7, 0.14, 0.14, 0.02],
      [0.65, 0.16, 0.16, 0.03],
      [0.6, 0.18, 0.18, 0.04],
      [0.5, 0.21, 0.21, 0.08]
    ].freeze

    def compute_guess_analysis
      perform_random_walk unless @random_walk_nodes
      compute_operations unless @operations_mat

      @norm_operations_mat = @norm_operations_mat.map do |key, operations|
        @random_walk_nodes[key].to_h.each do |node, weight|
          operations[node] = operations[node] * weight
        end
        [
          key,
          operations
        ]
      end.to_h

      @@coefficients.each do |alpha_1, alpha_2, alpha_3, alpha_4|
        @@alpha_1 = alpha_1
        @@alpha_2 = alpha_2
        @@alpha_3 = alpha_3
        @@alpha_4 = alpha_4

        puts "Setting of alphas (1,2,3,4) : (#{@@alpha_1}, #{@@alpha_2}, #{@@alpha_3}, #{@@alpha_4})"
        @char_analysis = { matching: 0, false_positives: 0, total: 0 }
        @matching_words = 0

        @word_pairs_test.each do |source, expected_dest|
          obtained_dest = guess(source)
          # puts "Testing for source #{source}, expected #{expected_dest} and got #{obtained_dest}"
          analyze(obtained_dest, expected_dest)
        end

        @char_analysis[:total] = @char_analysis[:matching] + @char_analysis[:false_positives]
        puts "#{@matching_words} / #{@word_pairs_test.length} words have a PERFECT match"
        puts "#{@char_analysis[:matching]} / #{@char_analysis[:total]} matching character tranformations"
        puts "#{@char_analysis[:false_positives]} / #{@char_analysis[:total]} false positives in character tranformations"
      end
    end

    private

    def guess(source)
      source_arr = source.split('')
      source_len = source.length
      source_arr.map.with_index do |char, lpos|
        rpos = lpos - source_len
        guessed_map = @operations_mat.map do |key, dataframe|
          [
            key,
            pairs(key, dataframe, char, lpos, rpos)
          ]
        end.to_h.reject { |_k, v| v.nil? }
        if guessed_map.nil?
          dv = guessed_map.values.reduce(:+)[char]
          dv.index_of_max
          # max_guess = guessed_map.max_by { |_k,v| v[1] }
          # max_guess[1] ? max_guess[1][0] : char
        else
          char
        end
      end.join
    end

    def analyze(obtained_dest, expected_dest)
      @matching_words += 1 if obtained_dest == expected_dest

      max_length = obtained_dest.length > expected_dest.length ? obtained_dest.length : expected_dest.length
      i = 0

      while i < max_length
        if obtained_dest[i] == expected_dest[i]
          @char_analysis[:matching] += 1
        else
          @char_analysis[:false_positives] += 1
        end
        i += 1
      end
    end

    private

    def pairs(key, dataframe, char, lpos, rpos)
      dv = 
        case key
        when :chars then dataframe[char]
        when :chars_lpos then dataframe["#{char}_#{lpos}"]
        when :chars_rpos then dataframe["#{char}_#{rpos}"]
        when :chars_lpos_rpos then dataframe["#{char}_#{lpos}_#{rpos}"]
        end

      max =
        case key
        when :chars then @@alpha_4
        when :chars_lpos then @@alpha_3
        when :chars_rpos then @@alpha_2
        when :chars_lpos_rpos then @@alpha_1
        end

      idx, m = roulette_wheel(dv)
      [idx, max*m]
    rescue
    end

    def roulette_wheel(vector)
      array = vector.to_h.map { |k,v| [k]*v }.flatten
      random = rand(array.length)
      value = array[random]
      # puts "Random index : #{random}, value : #{value}, actual max : #{dv.max}"
      [random, value]
    end
  end
end
