module BTP
  class DataFrames

    # attr_reader :operations_hash

    def compute_operations(source, dest)
      # @operations_mat = Daru::DataFrame.new({}, order: %i[operation char lpos rpos count])
      # @operations_mat = {
      #   chars: Daru::DataFrame.new({}, order: @alphabets, index: ['']+@alphabets),
      #   chars_lpos: Daru::DataFrame.new({}, order: @lpos_fields, index: ['']+@alphabets),
      #   chars_rpos: Daru::DataFrame.new({}, order: @rpos_fields, index: ['']+@alphabets),
      #   chars_lpos_rpos: Daru::DataFrame.new({}, order: @lpos_rpos_fields, index: ['']+@alphabets)
      # }

      # @operations_mat = Daru::DataFrame.new({}, order: @alphabets)

      # @word_pairs.each do |source, dest, _tags|
        source_len   = source.length
        # source_nodes = source.split('').map.with_index do |char, lpos|
        #   rpos = lpos - source_len
        #   [
        #     char,
        #     "#{char}_#{lpos}",
        #     "#{char}_#{rpos}",
        #     "#{char}_#{lpos}_#{rpos}"
        #   ]
        # end.flatten
        # constant_sequence(source, dest).each do |constant|
        #   char, lpos, rpos = constant.split('_')
          # @operations_mat[:chars].update_at(char, char)
          # @operations_mat[:chars_lpos].update_at("#{char}_#{lpos}", char)
          # @operations_mat[:chars_rpos].update_at("#{char}_#{rpos}", char)
          # @operations_mat[:chars_lpos_rpos].update_at("#{char}_#{lpos}_#{rpos}", char)
        # end

        insert_operations = insertion_sequence(source, dest).map do |insert|
          char, lpos, rpos = insert.split('_')
          "insert_#{insert}"
          # source_nodes.each do |node|
          #   @operations_mat.update_at(node, "insert_#{insert}")
          # end
          # @operations_mat[:chars].update_at(alpha, char)
          # @operations_mat[:chars_lpos].update_at("#{alpha}_#{lpos}", char)
          # @operations_mat[:chars_rpos].update_at("#{alpha}_#{rpos}", char)
          # @operations_mat[:chars_lpos_rpos].update_at("#{alpha}_#{lpos}_#{rpos}", char)
        end

        delete_operations = deletion_sequence(source, dest).each do |delete|
          char, lpos, rpos = delete.split('_')
          "delete_#{delete}"
          # source_nodes.each do |node|
          #   @operations_mat.update_at(node, "delete_#{delete}")
          # end
          # @operations_mat[:chars].update_at(char, '')
          # @operations_mat[:chars_lpos].update_at("#{char}_#{lpos}", '')
          # @operations_mat[:chars_rpos].update_at("#{char}_#{rpos}", '')
          # @operations_mat[:chars_lpos_rpos].update_at("#{char}_#{lpos}_#{rpos}", '')
        end

        word_operations = insert_operations + delete_operations
        word_operations.each do |operation|
          @operations.push(operation) unless @operations.include?(operation)
        end
        word_operations

        # @operations_mat = Daru::DataFrame.rows(
        #   @operations_hash.map { |key, count| [key.split('_'), count].flatten },
        #   order: %i[operation char lpos rpos count]
        # )
      # end

      # @operations_mat = @operations_mat.map do |key, dataframe|
      #   [
      #     key,
      #     dataframe.replace_values(nil, 0)
      #   ]
      # end.to_h

      # @norm_operations_mat = @operations_mat.map do |key, adjacency|
      #   puts 'Normalizing operations matrix'
      #   alphabets = adjacency.vectors.to_a
      #   operations = adjacency.index.to_a
      #   placeholder = 1.0 / (adjacency.ncols * adjacency.nrows)
      #   data = adjacency.map_vectors.with_index do |row, i|
      #     zeroes = row.map { |element| element == 0 }
      #     n_zeroes = zeroes.count(true)
      #     zero_prob = n_zeroes * placeholder
      #     non_zero_sum = row.sum.to_f
      #     row.map.with_index do |element|
      #       if element.zero?
      #         placeholder
      #       else
      #         element*(1-zero_prob)/non_zero_sum
      #       end
      #     end
      #   end
      #   [
      #     key,
      #     Daru::DataFrame.new(
      #       data,
      #       order: alphabets,
      #       index: operations
      #     )
      #   ]
      # end.to_h
    end

    private

    def constant_sequence(source, dest)
      i = 0
      ind = 0
      common = []
      com = ''
      while i < source.length
        if source[i] == dest[i]
          com += source[i]
        else
          common.push([com, ind]) if com.length > 1
          com = ''
          ind = i
        end
        i += 1
      end

      common.push([com, ind]) if com.length > 1

      common.map do |comm, lpos|
        comm.split('').map.with_index do |c, index|
          # "#{c}_#{index+lpos}_#{index+lpos-source.length}"
          "#{c}_#{index+lpos}_#{index+lpos-source.length}"
        end
      end.flatten
    end

    def deletion_sequence(source, dest)
      i = 0
      ind = 0
      common = []
      com = ''
      while i < source.length
        if source[i] != dest[i]
          com += source[i]
        else
          common.push([com, ind]) if com.length > 1
          com = ''
          ind = i
        end
        i += 1
      end

      common.push([com, ind]) if com.length > 1

      common.map do |comm, lpos|
        comm.split('').map.with_index do |c, index|
          # "#{c}_#{index+lpos}_#{index+lpos-source.length}"
          "#{c}_#{index+lpos}_#{index+lpos-source.length}"
        end
      end.flatten
    end

    def insertion_sequence(source, dest)
      i = 0
      ind = i
      insertion = []
      add = ''
      while i < dest.length
        ind = i if dest[i] != source[i] && source[i] && dest[i]
        add += dest[i] if dest[i] != source[i] || add.length == 1
        if add.length > 1
          insertion.push([add, ind])
          add = ''
        end
        i += 1
      end

      insertion.push([add, ind]) if add.length >= 1

      insertion.map do |del, lpos|
        del.split('').map.with_index do |d, index|
          "#{d}_#{lpos+index}_#{index+lpos-source.length}"
        end
      end.flatten
    end
  end
end
