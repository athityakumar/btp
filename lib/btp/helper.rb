module BTP
  class Helper
    def self.read_input(summa_data, path, source: true, dest: false)
      if summa_data
        summa_data
      else
        file = File.read(path).split("\n").map { |line| line.split("\t") }
        if path.end_with?('task1-train')
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
        elsif path.end_with?('task2-train')
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
          end
        end
      end.uniq
  end
end
