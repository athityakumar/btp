module BTP
  class DataFrames

    attr_reader :fast_text_vectors

    def create_source_fasttext_file(summa_data=nil)
      @fast_text_vectors = { training: {}, testing: {} }

      File.open("#{@language}-train.txt", 'w') { |f| f.write(@words[:training].join("\n")) }
      `../fastText/fasttext skipgram -input #{@language}-train.txt -output #{@language}-train -minCount 1`
      `rm -rf #{@language}-train.txt`

      File.read("#{@language}-train.vec")
        .split("\n")[1..-1]
        .each do |line|
          word, *vectors = line.split(' ')
          @fast_text_vectors[:training][word] = vectors.map(&:to_f)
        end

      # pp @fast_text_vectors[:training]["najprzytulniejszy"]

      File.open("#{@language}-test.txt", 'w') { |f| f.write(@words[:testing].join("\n")) }
      `../fastText/fasttext print-word-vectors #{@language}-train.bin < #{@language}-test.txt`
        .split("\n")
        .each do |line|
          word, *vectors = line.split(' ')
          @fast_text_vectors[:testing][word] = vectors.map(&:to_f)
        end
      `rm -rf #{@language}-test.txt`
    end
  end
end