module BTP
  class DataFrames

    attr_reader :adj_mat
    attr_reader :alphabets

    def compute_adjacency_matrices(summa_data=nil)
      compute_counters(@words)
      @alphabets = @words.map { |word| word.split('') }.flatten.uniq.sort

      @lpos_fields = @alphabets.map { |alphabet| (0..@left_most-1).map { |i| "#{alphabet}_#{i}" } }.flatten
      @rpos_fields = @alphabets.map { |alphabet| (@right_most+1..-1).map { |j| "#{alphabet}_#{j}" } }.flatten
      @lpos_rpos_fields = @alphabets.map do |alphabet|
        [
          (0..@left_most-1).map do |i|
            (@right_most+1..-1).map do |j|
              "#{alphabet}_#{i}_#{j}"
            end
          end
        ]
      end.flatten

      @fields = @alphabets + @lpos_fields + @rpos_fields + @lpos_rpos_fields

      puts "Unique alphabets: #{@alphabets}"
      puts "Unique alphabets count: #{@alphabets.count}"
      puts "Words count: #{@words.count}"

      @adj_mat = Daru::DataFrame.new({}, order: @fields, index: @fields)
      # @adjacency_matrix = @adj_mat

      @words.each do |word|
        chars  = word.split('')
        uniq_chars = chars.uniq
        word_length = word.length
        char_dist = chars.map do |x|
          [
            x,
            (0...word_length).to_a.find_all { |i| chars[i] == x }
          ]
        end.to_h

        uniq_chars.each do |char1|
          char_dist[char1].each do |left1|
            right1 = left1 - word_length
            char_dist.each do |char2, dist|
              dist.each do |left2|
                right2 = left2 - word_length

                @adj_mat.update_at(char1, char2)
                @adj_mat.update_at(char1, "#{char2}_#{left2}") if left2 < @left_most
                @adj_mat.update_at(char1, "#{char2}_#{right2}") if right2 > @right_most
                @adj_mat.update_at(char1, "#{char2}_#{left2}_#{right2}") if left2 < @left_most && right2 > @right_most

                @adj_mat.update_at("#{char1}_#{left1}", char2) if left1 < @left_most
                @adj_mat.update_at("#{char1}_#{left1}", "#{char2}_#{left2}") if left1 < @left_most && left2 < @left_most
                @adj_mat.update_at("#{char1}_#{left1}", "#{char2}_#{right2}") if left1 < @left_most && right2 > @right_most
                @adj_mat.update_at("#{char1}_#{left1}", "#{char2}_#{left2}_#{right2}") if left1 < @left_most && left2 < @left_most && right2 > @right_most

                @adj_mat.update_at("#{char1}_#{right1}", char2) if right1 > @right_most
                @adj_mat.update_at("#{char1}_#{right1}", "#{char2}_#{left2}") if left2 < @left_most && right1 > @right_most
                @adj_mat.update_at("#{char1}_#{right1}", "#{char2}_#{right2}") if left2 < @left_most && right2 > @right_most
                @adj_mat.update_at("#{char1}_#{right1}", "#{char2}_#{left2}_#{right2}") if left2 < @left_most && right1 > @right_most && right2 > @right_most

                @adj_mat.update_at("#{char1}_#{left1}_#{right1}", char2) if left1 < @left_most && right1 > @right_most
                @adj_mat.update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{left2}") if left1 < @left_most && left2 < @left_most && right1 > @right_most
                @adj_mat.update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{right2}") if left1 < @left_most && right1 > @right_most && right2 > @right_most
                @adj_mat.update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{left2}_#{right2}") if left1 < @left_most && left2 < @left_most && right1 > @right_most && right2 > @right_most
              end
            end
          end
        end
      end

      @adj_mat = @adj_mat.replace_values(nil, 0)
      # @adj_mat = {
      #   chars: chars,
      #   chars_lpos: chars_lpos,
      #   chars_rpos: chars_rpos,
      #   chars_lpos_rpos: chars_lpos_rpos
      # }
    end

    # def chars
    #   @fields = @alphabets
    #   puts "DataFrame size: #{@fields.count}"

    #   @adjacency_matrix = Daru::DataFrame.new({}, order: @fields, index: @fields)
    #   @words.each do |word|
    #     chars  = word.split('')
    #     uniq_chars = chars.uniq
    #     word_length = word.length
    #     char_dist = chars.map do |x|
    #       [
    #         x,
    #         (0...word_length).to_a.count { |i| chars[i] == x }
    #       ]
    #     end.to_h

    #     uniq_chars.each do |char1|
    #       char_dist.each do |char2, count|
    #         update_at(char1, char2, count)
    #       end
    #     end
    #   end

    #   @adjacency_matrix.replace_values(nil, 0)
    #   @adjacency_matrix
    # end

    # def chars_lpos
    #   @lpos_fields = @alphabets.map { |alphabet| (0..@left_most-1).map { |i| "#{alphabet}_#{i}" } }.flatten

    #   puts "DataFrame size: #{@lpos_fields.count} = "\
    #        "#{@alphabets.count}*#{@left_most}"

    #   @adjacency_matrix = Daru::DataFrame.new({}, order: @lpos_fields, index: @lpos_fields)
    #   @words.each do |word|
    #     chars  = word.split('')
    #     uniq_chars = chars.uniq
    #     word_length = word.length
    #     char_dist = chars.map do |x|
    #       [
    #         x,
    #         (0...word_length).to_a.find_all { |i| chars[i] == x }
    #       ]
    #     end.to_h

    #     uniq_chars.each do |char1|
    #       char_dist[char1].each do |left1|
    #         char_dist.each do |char2, dist|
    #           dist.each do |left2|
    #             update_at("#{char1}_#{left1}", "#{char2}_#{left2}") if left1 < @left_most && left2 < @left_most
    #           end
    #         end
    #       end
    #     end
    #   end

    #   @adjacency_matrix.replace_values(nil, 0)
    #   @adjacency_matrix
    # end

    # def chars_rpos
    #   @rpos_fields = @alphabets.map { |alphabet| (@right_most+1..-1).map { |j| "#{alphabet}_#{j}" } }.flatten

    #   puts "DataFrame size: #{@rpos_fields.count} = "\
    #        "#{@alphabets.count}*#{@left_most}"

    #   @adjacency_matrix = Daru::DataFrame.new({}, order: @rpos_fields, index: @rpos_fields)
    #   @words.each do |word|
    #     chars  = word.split('')
    #     uniq_chars = chars.uniq
    #     word_length = word.length
    #     char_dist = chars.map do |x|
    #       [
    #         x,
    #         (0...word_length).to_a.find_all { |i| chars[i] == x }
    #       ]
    #     end.to_h

    #     uniq_chars.each do |char1|
    #       char_dist[char1].each do |left1|
    #         right1 = left1 - word_length
    #         char_dist.each do |char2, dist|
    #           dist.each do |left2|
    #             right2 = left2 - word_length
    #             update_at("#{char1}_#{right1}", "#{char2}_#{right2}") if right1 > @right_most && right2 > @right_most
    #           end
    #         end
    #       end
    #     end
    #   end

    #   @adjacency_matrix.replace_values(nil, 0)
    #   @adjacency_matrix
    # end

    # def chars_lpos_rpos
    #   @lpos_rpos_fields = @alphabets.map do |alphabet|
    #     [
    #       (0..@left_most-1).map do |i|
    #         (@right_most+1..-1).map do |j|
    #           "#{alphabet}_#{i}_#{j}"
    #         end
    #       end
    #     ]
    #   end.flatten

    #   puts "DataFrame size: #{@lpos_rpos_fields.count} = "\
    #        "#{@alphabets.count}*#{@left_most}*#{@left_most}"

    #   @adjacency_matrix = Daru::DataFrame.new({}, order: @lpos_rpos_fields, index: @lpos_rpos_fields)
    #   @words.each do |word|
    #     chars  = word.split('')
    #     uniq_chars = chars.uniq
    #     word_length = word.length
    #     char_dist = chars.map do |x|
    #       [
    #         x,
    #         (0...word_length).to_a.find_all { |i| chars[i] == x }
    #       ]
    #     end.to_h

    #     uniq_chars.each do |char1|
    #       char_dist[char1].each do |left1|
    #         right1 = left1 - word_length
    #         char_dist.each do |char2, dist|
    #           dist.each do |left2|
    #             right2 = left2 - word_length
    #             update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{left2}_#{right2}") if left1 < @left_most && left2 < @left_most && right1 > @right_most && right2 > @right_most
    #           end
    #         end
    #       end
    #     end
    #   end

    #   @adjacency_matrix.replace_values(nil, 0)
    #   @adjacency_matrix
    # end

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

      @left_most  = (length_frequency.find { |_k, v| v > 0.7 }.first).freeze
      @right_most = (-1 * @left_most - 1).freeze

      puts "Left most: #{@left_most}"
    end


    # def update_at(key1, key2, count=1)
    #   @adjacency_matrix.update_at(key1, key2, count)
    # end
  end
end