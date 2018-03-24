def read_words(filepath)
  File.read(filepath).split("\n").map { |line| line.split("\t")[0..1] }.to_h
end

training_words = read_words('../daru-dataframe/spec/fixtures/english-train-high')
testing_words  = read_words('../daru-dataframe/spec/fixtures/english-dev')
common_words   = testing_words.keys.map { |t| training_words[t] ? t : nil }.compact
same_words     = common_words.map { |w| training_words[w] == testing_words[w] ? w : nil }.compact


common_words.each_with_index do |w, i|
  puts "#{i+1}: #{w}, trained as #{training_words[w]}, tested as #{testing_words[w]}"
end

same_words.each_with_index do |w, i|
  puts "#{i+1}: #{w}, trained as #{training_words[w]}, tested as #{testing_words[w]}"
end
