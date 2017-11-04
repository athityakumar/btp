module BTP
  class DataFrames

    attr_reader :operations
    attr_reader :decision_trees

    def compute_decision_tree
      create_source_fasttext_file unless @fast_text_vectors
      @operations = []
      @decision_trees = {}

      @word_pairs[:training].each { |source, dest, _tags| compute_operations(source, dest) }


      features = @word_pairs[:training][1..500].map do |source, dest, tags|
        begin
          [source, @fast_text_vectors[:training][source] + @all_tags.map { |tag| tags.include?(tag) ? 1 : 0 } ]
        rescue
          nil
        end
      end.reject { |x| x.nil? }.to_h

      attributes = (1..@fast_text_vectors[:training].values.first.count).map { |i| "word_#{i}" } + (1..@all_tags.count).map { |i| "tag_#{i}" }

      type = attributes.map do |attr|
        if attr.start_with?("word")
          [attr.to_sym, :continuous]
        else
          [attr.to_sym, :discrete]
        end
      end.to_h

      # operation_0 = @operations[0]
      # puts operation_0
      @operations.each do |operation|
        training = @word_pairs[:training][1..500].map do |source, dest, tags|
          if features[source]
            label = compute_operations(source, dest).include?(operation) ? 1 : 0
            features[source] + [label]
          else
            nil
          end
        end.reject { |t| t.nil? }

        dec_tree = DecisionTree::ID3Tree.new(attributes, training, 0, type)

        puts "Training decision tree for #{operation} model..."
        dec_tree.train

        correct_predictions = { yes: 0, no: 0 }
        false_positive = 0
        true_negative = 0
        total_predictions = 0

        @word_pairs[:testing].each do |source, dest, tags|
          if @fast_text_vectors[:testing][source]
            features = @fast_text_vectors[:testing][source] + @all_tags.map { |tag| tags.include?(tag) ? 1 : 0 }
            prediction = dec_tree.predict(features)
            operations = compute_operations(source, dest)

            if operations.include?(operation) && prediction == 1
              correct_predictions[:yes] += 1
            elsif !operations.include?(operation) && prediction == 0
              correct_predictions[:no] += 1
            elsif operations.include?(operation) && prediction == 0
              true_negative += 1
            else
              false_positive += 1
            end
            total_predictions += 1
          end
        end

        puts "operation #{operation}"
        puts "Total predictions : #{total_predictions}"
        puts "correct_predictions: #{correct_predictions}"
        puts "false_positive: #{false_positive}"
        puts "true_negative: #{true_negative}"

        sleep 10

      end
    end
  end
end