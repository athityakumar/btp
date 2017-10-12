module BTP
  class DataFrames
    attr_reader :train_path
    attr_reader :test_path
    attr_reader :summa_data
    attr_reader :words
    attr_reader :word_pairs
    attr_reader :word_pairs_test

    def initialize(summa_data=nil, train: 'spec/fixtures/finnish/finnish-train-high', test: 'spec/fixtures/finnish/finnish-uncovered-test')
      @summa_data = summa_data
      @train_path = train
      @test_path = test
      @words = read_input(@train_path)
      @word_pairs = read_input(@train_path, dest: true)
      @word_pairs_test = read_input(@test_path, dest: true)
    end

    def read_input(path, source: true, dest: false)
      @path = path

      if @summa_data
        @summa_data
      else
        file = File.read(@path).split("\n").map { |line| line.split("\t") }
        if @path.end_with?('task1-train')
          if source and not dest
            file
              .keep_if { |line| line[1].include?('pos=N') }
              .map(&:first)
          elsif dest and not source
            file
              .keep_if { |line| line[1].include?('pos=N') }
              .map(&:last)
          else
            file
              .keep_if { |line| line[1].include?('pos=N') }
              .map     { |line| [line.first, line.last]   }
          end
        elsif @path.end_with?('task2-train')
          if source and not dest
            file
              .keep_if { |line| line[0].include?('pos=N') }
              .map { |line| line[1] }
          elsif dest and not source
            file
              .keep_if { |line| line[0].include?('pos=N') }
              .map(&:last)
          else
            file
              .keep_if { |line| line[0].include?('pos=N') }
              .map     { |line| [line[1], line.last]      }
          end
        else
          if source and not dest
            file
              .keep_if { |line| line.last.start_with?('N;') }
              .map(&:first)
          elsif source and dest
            file
              .keep_if { |line| line.last.start_with?('N;') }
              .map     { |line| line[0..1] }           
          end
        end
      end.uniq
    end
  end
end

module Daru
  class DataFrame
    def update_at(key1, key2, count=1)
      unless self.vectors.include? key1
        self.add_vector(key1, [nil]*self.nrows)
      end

      unless self.index.include? key2
        self.add_row([nil]*self.ncols)
        self.index = self.index.to_a[0..-2] + [key2]
      end

      if self[key1][key2]
        self[key1][key2] += count
      else
        self[key1][key2] = count
      end
    end
  end
end

class Hash
  def update_at(key, count=1)
    if self.keys.include?(key)
      self[key] += count
    else
      self[key] = count
    end
  end
end
