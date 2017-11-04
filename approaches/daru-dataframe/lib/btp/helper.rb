module BTP
  class DataFrames
    attr_reader :train_path
    attr_reader :test_path
    attr_reader :summa_data
    attr_reader :words
    attr_reader :word_pairs
    attr_reader :dests
    attr_reader :tags
    attr_reader :all_tags

    def initialize(summa_data=nil, train: 'spec/fixtures/polish/polish-train-high', test: 'spec/fixtures/polish/polish-uncovered-test')
      @summa_data = summa_data
      @train_path = train
      @test_path = test
      @language = train.split("/")[2]
 
      @words = {
        training: read_input(@train_path),
        testing: read_input(@test_path)
      }

      @tags = {
        training: read_input(@train_path, source: false, tags: true),
        testing: read_input(@test_path, source: false, tags: true)
      }

      @all_tags = @tags[:training] + @tags[:testing]

      # @dests = {
      #   training: read_input(@train_path, source: false, dest: true),
      #   testing: read_input(@test_path, source: false, dest: true)
      # }

      @word_pairs = {
        training: read_input(@train_path, dest: true, tags: true),
        testing: read_input(@test_path, dest: true, tags: true)
      }
    end

    def read_input(path, source: true, dest: false, tags: false)
      @path = path

      if @summa_data
        @summa_data
      else
        file = File.read(@path).split("\n").map { |line| line.split("\t") }

        if source and not dest and not tags
          file.map(&:first)
        elsif source and dest and not tags
          file.map { |line| line[0..1] }
        elsif tags and not source and not dest
          file.map { |line| line.last.split(';') }.flatten
        elsif source and not dest and tags
          file.map { |line| [line[0], line.last.split(';')] }
        elsif source and dest and tags
          file.map { |line| [line[0], line[1], line.last.split(';')] }         
        end
      end.uniq
    end


    # def read_input(path, source: true, dest: false)
    #   @path = path

    #   if @summa_data
    #     @summa_data
    #   else
    #     file = File.read(@path).split("\n").map { |line| line.split("\t") }
    #     if @path.end_with?('task1-train')
    #       if source and not dest
    #         file
    #           .keep_if { |line| line[1].include?('pos=N') }
    #           .map(&:first)
    #       elsif dest and not source
    #         file
    #           .keep_if { |line| line[1].include?('pos=N') }
    #           .map(&:last)
    #       else
    #         file
    #           .keep_if { |line| line[1].include?('pos=N') }
    #           .map     { |line| [line.first, line.last]   }
    #       end
    #     elsif @path.end_with?('task2-train')
    #       if source and not dest
    #         file
    #           .keep_if { |line| line[0].include?('pos=N') }
    #           .map { |line| line[1] }
    #       elsif dest and not source
    #         file
    #           .keep_if { |line| line[0].include?('pos=N') }
    #           .map(&:last)
    #       else
    #         file
    #           .keep_if { |line| line[0].include?('pos=N') }
    #           .map     { |line| [line[1], line.last]      }
    #       end
    #     else
    #       if source and not dest
    #         file
    #           .keep_if { |line| line.last.start_with?('N;') }
    #           .map(&:first)
    #       elsif source and dest
    #         file
    #           .keep_if { |line| line.last.start_with?('N;') }
    #           .map     { |line| line[0..1] }           
    #       end
    #     end
    #   end.uniq
    # end
  end
end
