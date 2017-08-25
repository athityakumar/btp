module BTP
  class SourceDest
    def initialize(path)
      @path      = path
      @words     = []
    end

    def parse(summa_data=nil)
      @word_pairs = if summa_data
                      summa_data
                    else
                      File
                        .read(@path)
                        .split("\n")
                        .map { |line| line.split("\t") }
                        .keep_if { |line| line[1].include?('pos=N') }
                        .map { |line| [line.first, line.last] }
                    end

      @dataframe = Daru::DataFrame.new({}, order: %i[source destination removal insertion])
      @word_pairs.each do |source, dest|
        delete = deletion_sequence(source, dest)
        insert = insertion_sequence(source, dest)
        @dataframe.add_row([source, dest, delete, insert])
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
