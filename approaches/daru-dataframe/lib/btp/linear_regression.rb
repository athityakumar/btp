module BTP
  class DataFrames
    def compute_linear_regression_guess
      compute_normalized_matrices unless @norm_adj_mat
      compute_operations unless @operations_hash

      puts 'Started training model with linear regression'

      features = @operations_hash.keys.map do |label_name|
        _operation, char, lpos, rpos = label_name.split('_')
        if @alphabets.include?("#{char}_#{lpos}_#{rpos}")
          @norm_adj_mat.row["#{char}_#{lpos}_#{rpos}"].to_a
        elsif @alphabets.include?("#{char}_#{lpos}")
          @norm_adj_mat.row["#{char}_#{lpos}"].to_a
        elsif @alphabets.include?("#{char}_#{rpos}")
          @norm_adj_mat.row["#{char}_#{rpos}"].to_a
        elsif @alphabets.include?(char)
          @norm_adj_mat.row[char].to_a
        else
          n = @norm_adj_mat.ncols
          [1.0/ n] * n
        end
      end

      # n = @norm_adj_mat.ncols
      # feature = [1.0/ n] * n
      # features = @operations_hash.keys.map do |label_name|
      #   feature
      # end
      puts 'Finished computing features'

      regress(features, 0, 'operations')
      regress(features, 1, 'chars')
      regress(features, 2, 'lpos')
      regress(features, 3, 'rpos')
    end

    private

    def regress(features, i, type)
      puts "Started prediction for #{type}"

      label_names = @operations_hash.keys.map { |k| k.split('_')[i] }
      label_indexes  = label_names.to_set.to_a
      labels = label_names.map { |label_name| label_indexes.index(label_name) }

      linear_regression = RubyLinearRegression.new
      linear_regression.load_training_data([[0.1]*labels.count]*labels.count, labels)
      linear_regression.train_normal_equation
      predicted_labels = features.map { |feature| linear_regression.predict(feature) }

      correct = 0
      total = labels.count.to_f
      predicted_labels.each_with_index do |prediction, i|
        correct += 1 if prediction == labels[i]
      end
      accuracy = correct/total

      puts "Finished prediction for #{type} with accuracy = #{accuracy}"
    end
  end
end
