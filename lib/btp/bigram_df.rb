module BTP
  class Bigram
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

      @dataframe = Daru::DataFrame.new({}, order: %i[character_1 left_1 right_1 character_2 left_2 right_2 count])
      @words.each { |word| bigram_dataframe(word) }

      @dataframe
    end

    private

    def bigram_dataframe(word)
      i = 0
      word_length = word.length
      puts word
      while i < word_length - 1
        j = i+1
        while j < word_length
          update_bigram(i, i - word_length, word[i], j, j - word_length, word[j])
          update_bigram(j, j - word_length, word[j], i, i - word_length, word[i])
          j += 1
        end
        i += 1
      end
    end

    def update_bigram(left1, right1, char1, left2, right2, char2)
      df = @dataframe
      df = df.where(df[:character_1].eq(char1))
      df = df.where(df[:character_2].eq(char2))
      df = df.where(df[:left_1].eq(left1))
      df = df.where(df[:right_1].eq(right1))
      df = df.where(df[:left_2].eq(left2))
      df = df.where(df[:right_2].eq(right2))

      if df.nrows.zero?
        @dataframe.add_row([char1, left1, right1, char2, left2, right2, 1])
      else
        index = df.index.to_a.first
        @dataframe[:count][index] += 1
      end
    end
  end
end
