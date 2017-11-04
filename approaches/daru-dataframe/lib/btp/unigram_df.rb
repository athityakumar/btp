module BTP
  class Unigram
    def initialize(path)
      @path      = path
      @words     = []
    end

    def parse(summa_data=nil)
      @words = Helper.read_input(summa_data, @path)
      @dataframe = Daru::DataFrame.new({}, order: %i[word_index character left_position right_position count])
      @words.each_with_index { |word, i| unigram_dataframe(word, i) }

      @dataframe
    end

    private

    def unigram_dataframe(word, i)
      word_length = word.length

      word.split('').each_with_index do |char, left|
        df = @dataframe
        bool_array = df[:character].eq(char) & df[:left_position].eq(left) & df[:right_position].eq(left - word_length)
        df = df.where(bool_array)

        if df.nrows.zero?
          @dataframe.add_row([i, char, left, left - word_length, 1])
        else
          index = df.index.to_a.first
          @dataframe[:count][index] += 1
        end
      end
    end
  end
end
