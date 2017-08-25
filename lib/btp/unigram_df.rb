module BTP
  class Unigram
    def initialize(path)
      @path      = path
      @words     = []
    end

    def parse(summa_data=nil)
      @words = if summa_data
                 summa_data
               else
                 File
                   .read(@path)
                   .split("\n")
                   .map { |line| line.split("\t") }
                   .keep_if { |line| line[1].include?('pos=N') }
                   .map(&:first)
               end

      @dataframe = Daru::DataFrame.new({}, order: %i[character left_position right_position count])
      @words.each { |word| unigram_dataframe(word) }

      @dataframe
    end

    private

    def unigram_dataframe(word)
      word_length = word.length

      word.split('').each_with_index do |char, left|
        df = @dataframe
        df = df.where(df[:character].eq(char))
        df = df.where(df[:left_position].eq(left))
        df = df.where(df[:right_position].eq(left - word_length))

        if df.nrows.zero?
          @dataframe.add_row([char, left, left - word_length, 1])
        else
          index = df.index.to_a.first
          @dataframe[:count][index] += 1
        end
      end
    end
  end
end
