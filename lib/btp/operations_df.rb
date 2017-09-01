module BTP
  class Operations
    def initialize(path)
      @path       = path
      @word_pairs = []
    end

    def parse(summa_data=nil)
      @word_pairs = Helper.read_input(summa_data, @path, dest: true)
      @dataframe  = Daru::DataFrame.new({}, order: %i[operation character count])

      @word_pairs.each do |source, dest|
        delete = deletion_sequence(source, dest)
        insert = insertion_sequence(source, dest)
        
        delete.each do |d|
          df = @dataframe
          df = df.where(df[:operation].eq(:delete))
          df = df.where(df[:character].eq(d))

          if df.nrows.zero?
            @dataframe.add_row([:delete, d, 1])
          else
            index = df.index.to_a.first
            @dataframe[:count][index] += 1
          end
        end

        insert.each do |i|
          df = @dataframe
          df = df.where(df[:operation].eq(:insert))
          df = df.where(df[:character].eq(i))

          if df.nrows.zero?
            @dataframe.add_row([:insert, i, 1])
          else
            index = df.index.to_a.first
            @dataframe[:count][index] += 1
          end
        end
      end

      @dataframe
    end

    private

    def deletion_sequence(source, dest)
      i = 0
      ind = 0
      deletion = []
      rem = ''
      while i < source.length
        if source[i] == dest[i]
          rem += source[i]
        else
          deletion.push([rem, ind]) if rem.length > 1
          rem = ''
          ind = i
        end

        i += 1
      end

      deletion.push([rem, ind]) if rem.length > 1

      deletion.map do |del, lpos|
        del.split('').map.with_index do |d, index|
          "#{d}_#{index+lpos}_#{index+lpos-source.length}"
        end
      end.flatten
    end

    def insertion_sequence(source, dest)
      i = 0
      ind = i
      insertion = []
      add = ''
      while i < dest.length
        if dest[i] != source[i]
          add += dest[i]
        else
          insertion.push([add, ind]) if add.length > 1
          add = ''
          ind = i
        end

        i += 1
      end

      insertion.push([add, ind]) if add.length > 1

      insertion.map do |del, lpos|
        del.split('').map.with_index do |d, index|
          "#{d}_#{lpos+index}_#{index+lpos-source.length}"
        end
      end.flatten
    end
  end
end
