module BTP
  class DataFrames

    attr_reader :norm_adj_mat
    attr_reader :random_walk_nodes

    def compute_normalized_matrices
      compute_adjacency_matrices unless @adj_mat
      @norm_adj_mat = @adj_mat.map do |key, adjacency|
        puts 'Normalizing adjacency matrix'
        alphabets = adjacency.vectors.to_a
        placeholder = 1.0 / (adjacency.ncols ** 2)
        data = adjacency.map_rows do |row|
          zeroes = row.map { |element| element == 0 }
          n_zeroes = zeroes.count(true)
          zero_prob = n_zeroes * placeholder
          non_zero_sum = row.sum.to_f
          row.map do |element|
            if element.zero?
              placeholder
            else
              element*(1-zero_prob)/non_zero_sum
            end
          end
        end
        [
          key,
          Daru::DataFrame.rows(
            data,
            order: alphabets,
            index: alphabets
          )
        ]
      end.to_h
    end

    def perform_random_walk(iterations=5)
      compute_normalized_matrices unless @norm_adj_mat
      @random_walk_nodes = @norm_adj_mat.map do |key, dataframe|
        puts 'Random walking'
        n = dataframe.nrows
        random = Array.new(n) { |i| rand(20) }
        random_sum = random.sum.to_f
        random = random.map { |r| r/(random_sum*random_sum) }
        seed = Daru::DataFrame.new([random])
        topics = dataframe.vectors.to_a
        dataframe_matrix = dataframe.to_matrix
        seed_matrix = seed.to_matrix

        iterations.times do
          seed_matrix = dataframe_matrix * seed_matrix
          # seed_matrix = seed.to_matrix
          # seed = Daru::DataFrame.new([(dataframe_matrix * seed_matrix).to_a.flatten])
        end

        mapping = 
          Daru::DataFrame.new([(dataframe_matrix * seed_matrix).to_a.flatten])
            .map(&:to_a)
            .flatten
            .map
            .with_index { |s, i| [topics[i], s] }
            .to_h

        [
          key,
          Daru::Vector.new(mapping.values, index: mapping.keys)
        ]
      end.to_h
    end
  end
end