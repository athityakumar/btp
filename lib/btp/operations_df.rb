module BTP
  class DataFrames

    attr_reader :operations_mat

    def compute_operations
      @operations_mat = {
        chars: Daru::DataFrame.new({}, order: @alphabets, index: ['']+@alphabets),
        chars_lpos: Daru::DataFrame.new({}, order: @lpos_fields, index: ['']+@alphabets),
        chars_rpos: Daru::DataFrame.new({}, order: @rpos_fields, index: ['']+@alphabets),
        chars_lpos_rpos: Daru::DataFrame.new({}, order: @lpos_rpos_fields, index: ['']+@alphabets)
      }

      @word_pairs.each do |source, dest|
        constant_sequence(source, dest).each do |constant|
          char, lpos, rpos = constant.split('_')
          @operations_mat[:chars].update_at(char, char)
          @operations_mat[:chars_lpos].update_at("#{char}_#{lpos}", char)
          @operations_mat[:chars_rpos].update_at("#{char}_#{rpos}", char)
          @operations_mat[:chars_lpos_rpos].update_at("#{char}_#{lpos}_#{rpos}", char)
        end

        insertion_sequence(source, dest).each do |source_char, insert|
          alpha, lpos, rpos = source_char.split('_')
          char = insert.map { |i| i.split('_').first }.join
          @operations_mat[:chars].update_at(alpha, char)
          @operations_mat[:chars_lpos].update_at("#{alpha}_#{lpos}", char)
          @operations_mat[:chars_rpos].update_at("#{alpha}_#{rpos}", char)
          @operations_mat[:chars_lpos_rpos].update_at("#{alpha}_#{lpos}_#{rpos}", char)
        end

        deletion_sequence(source, dest).each do |delete|
          char, lpos, rpos = delete.split('_')
          @operations_mat[:chars].update_at(char, '')
          @operations_mat[:chars_lpos].update_at("#{char}_#{lpos}", '')
          @operations_mat[:chars_rpos].update_at("#{char}_#{rpos}", '')
          @operations_mat[:chars_lpos_rpos].update_at("#{char}_#{lpos}_#{rpos}", '')
        end
      end

      @operations_mat = @operations_mat.map do |key, dataframe|
        [
          key,
          dataframe.replace_values(nil, 0)
        ]
      end.to_h

      @norm_operations_mat = @operations_mat.map do |key, adjacency|
        puts 'Normalizing operations matrix'
        alphabets = adjacency.vectors.to_a
        operations = adjacency.index.to_a
        placeholder = 1.0 / (adjacency.ncols * adjacency.nrows)
        data = adjacency.map_vectors.with_index do |row, i|
          zeroes = row.map { |element| element == 0 }
          n_zeroes = zeroes.count(true)
          zero_prob = n_zeroes * placeholder
          non_zero_sum = row.sum.to_f
          row.map.with_index do |element|
            if element.zero?
              placeholder
            else
              element*(1-zero_prob)/non_zero_sum
            end
          end
        end
        [
          key,
          Daru::DataFrame.new(
            data,
            order: alphabets,
            index: operations
          )
        ]
      end.to_h
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
        [
          "#{source[del]}_#{lpos}_#{lpos-source.length}",
          del.split('').map.with_index do |d, index|
            "#{d}_#{lpos+index}_#{index+lpos-source.length}"
          end
        ]
      end.to_h
    end
  end
end
