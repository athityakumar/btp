module BTP
  class DataFrames
    def compute_svm_guess
      compute_normalized_matrices unless @norm_adj_mat
      compute_operations unless @operations_hash

      puts 'Started training model with SVM'

      operation_label_names = @operations_hash.keys.map { |k| k.split('_')[0] }
      operation_label_indexes  = operation_label_names.to_set.to_a
      operation_labels = operation_label_names.map { |label_name| operation_label_indexes.index(label_name) }

      char_label_names = @operations_hash.keys.map { |k| k.split('_')[1] }
      char_label_indexes  = char_label_names.to_set.to_a
      char_labels = char_label_names.map { |label_name| char_label_indexes.index(label_name) }

      lpos_label_names = @operations_hash.keys.map { |k| k.split('_')[2] }
      lpos_label_indexes  = lpos_label_names.to_set.to_a
      lpos_labels = lpos_label_names.map { |label_name| lpos_label_indexes.index(label_name) }

      rpos_label_names = @operations_hash.keys.map { |k| k.split('_')[3] }
      rpos_label_indexes  = rpos_label_names.to_set.to_a
      rpos_labels = rpos_label_names.map { |label_name| rpos_label_indexes.index(label_name) }

      features = @operations_hash.keys.map do |label_name|
        _operation, char, lpos, rpos = label_name.split('_')
        if @alphabets.include?("#{char}_#{lpos}_#{rpos}")
          Node.features(*@norm_adj_mat.row["#{char}_#{lpos}_#{rpos}"].to_a)
        elsif @alphabets.include?("#{char}_#{lpos}")
          Node.features(*@norm_adj_mat.row["#{char}_#{lpos}"].to_a)
        elsif @alphabets.include?("#{char}_#{rpos}")
          Node.features(*@norm_adj_mat.row["#{char}_#{rpos}"].to_a)
        elsif @alphabets.include?(char)
          Node.features(*@norm_adj_mat.row[char].to_a)
        else
          n = @norm_adj_mat.ncols
          Node.features([1.0/ n] * n)
        end
      end

      puts 'Training over, creating problem now'
      # Create problem traning set
      operation_problem = Problem.new
      operation_problem.set_examples(operation_labels, features)
        
      char_problem = Problem.new
      char_problem.set_examples(char_labels, features)

      lpos_problem = Problem.new
      lpos_problem.set_examples(lpos_labels, features)

      rpos_problem = Problem.new
      rpos_problem.set_examples(rpos_labels, features)


      parameter = SvmParameter.new
      parameter.cache_size  = 10 # in megabytes
      # parameter.eps         = 0.00001
      # parameter.degree      = 5
      # parameter.gamma       = 0.01
      # parameter.c           = 100

      # Use various kernel types
      # [:LINEAR, :POLY, :RBF, :SIGMOID].each do |type|
      [:LINEAR].each do |type|
        param = parameter
        param.kernel_type = KernelType.const_get(type)

        # Different nfold sizes. It's the number of parts the data is
        # split into.
        [10].each do |nfold|
          operation_result = Model.cross_validation(operation_problem, param, nfold)
          operation_prediction  = operation_result.map { |label| operation_label_indexes[label] }
          operation_correctness = operation_prediction.map.with_index do |p, i|
            # puts "Predicted #{p}, expected #{operation_label_names[i]}"
            p == operation_label_names[i]
          end
          operation_correct = operation_correctness.select { |x| x }
          operation_accuracy = operation_correct.size.to_f / operation_correctness.size
          puts "Accuracy[type = #{type}, nfold = #{nfold}, param = Operation] : #{operation_accuracy}"

          char_result = Model.cross_validation(char_problem, param, nfold)
          char_prediction  = char_result.map { |label| char_label_indexes[label] }
          char_correctness = char_prediction.map.with_index do |p, i|
            # puts "Predicted #{p}, expected #{char_label_names[i]}"
            p == char_label_names[i]
          end
          char_correct = char_correctness.select { |x| x }
          char_accuracy = char_correct.size.to_f / char_correctness.size
          puts "Accuracy[type = #{type}, nfold = #{nfold}, param = Char] : #{char_accuracy}"

          lpos_result = Model.cross_validation(lpos_problem, param, nfold)
          lpos_prediction  = lpos_result.map { |label| lpos_label_indexes[label] }
          lpos_correctness = lpos_prediction.map.with_index do |p, i|
            # puts "Predicted #{p}, expected #{lpos_label_names[i]}"
            p == lpos_label_names[i]
          end
          lpos_correct = lpos_correctness.select { |x| x }
          lpos_accuracy = lpos_correct.size.to_f / lpos_correctness.size
          puts "Accuracy[type = #{type}, nfold = #{nfold}, param = Lpos] : #{lpos_accuracy}"

          rpos_result = Model.cross_validation(rpos_problem, param, nfold)
          rpos_prediction  = rpos_result.map { |label| rpos_label_indexes[label] }
          rpos_correctness = rpos_prediction.map.with_index do |p, i|
            # puts "Predicted #{p}, expected #{rpos_label_names[i]}"
            p == rpos_label_names[i]
          end
          rpos_correct = rpos_correctness.select { |x| x }
          rpos_accuracy = rpos_correct.size.to_f / rpos_correctness.size
          puts "Accuracy[type = #{type}, nfold = #{nfold}, param = Rpos] : #{rpos_accuracy}"
        end
      end
    end
  end
end
