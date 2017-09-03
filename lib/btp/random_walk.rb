module BTP
  class RandomWalk
    def initialize(path)
      @path      = path
      @words     = []
      @alphabets = []
    end

    def parse(summa_data=nil)
      @adjacency = AdjacencyMatrix.new(@path).parse(summa_data)
      @normalized = normalize_matrix(@adjacency)
      puts 'Adj mat normalized'
      random_walk(@normalized)
    end

    private

    def normalize_matrix(adjacency)
      # def normalize_mat(matrix):
      #     def normalize(row):
      #         zeros = sum(row == 0)
      #         if zeros == 0:
      #             return(row.apply(lambda x: x/sum(row)))
      #         elif zeros == len(row):
      #             return(row.apply(lambda x: x + 1/len(row)))
      #         zero_prob = zeros/len(row)
      #         zero_smoothing = zero_prob/zeros
      #         non_zero_smoothing = zero_prob/(len(row) - zeros)
      #         return(row.apply(lambda x: float(x + zero_smoothing)/sum(row) if x == 0 else float(x - non_zero_smoothing)/sum(row)))
      #     return(matrix.apply(normalize, axis=1))      

      puts 'Normalizing adjacency matrix'
      alphabets = adjacency.vectors.to_a

      placeholder = 1.0 / (adjacency.ncols ** 2)
      # adjacency.replace_values(0, placeholder)
      data = adjacency.map_rows.with_index do |row, i|
        zeroes = row.map { |element| element == 0 }
        n_zeroes = zeroes.count(true)
        zero_prob = n_zeroes * placeholder
        non_zero_sum = row.sum.to_f
        row.map.with_index do |element|
          if element.zero?
            placeholder
          else
            element*(1-zero_prob)/non_zero_sum
          end
        end
      end
      puts 'Vectors normalized'
      normalized = Daru::DataFrame.rows(
        data,
        order: alphabets,
        index: alphabets
      )
      normalized
    end

    def random_walk(dataframe)
      # def random_walk(trans_mat):
      #     num_iters = 5
      #     n = trans_mat.shape[0]
      #     seed = np.array([float(1/n)]*n)

      #     for i in range(num_iters):
      #         seed = np.matmul(seed, trans_mat)
      #     mapping = zip(trans_mat.columns, seed, range(n))
      #     return(sorted(mapping, key=operator.itemgetter(1), reverse=True))
      puts 'Random walking'
      iterations = 20
      n = dataframe.nrows
      seed = Daru::DataFrame.new([[1.0, [0.0]*(n-1)].flatten])
      topics = dataframe.vectors.to_a
      dataframe_matrix = dataframe.to_matrix

      iterations.times do
        seed_matrix = seed.to_matrix
        seed = Daru::DataFrame.new([(dataframe_matrix * seed_matrix).to_a.flatten])
      end

      seed = seed.map(&:to_a).flatten
      mapping = seed.map.with_index { |s, i| [topics[i], s] }

      Daru::DataFrame
        .rows(mapping, order: %i[character seed_weight])
        .sort([:seed_weight], ascending: false)
    end
  end
end