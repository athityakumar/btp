require 'pp'
require 'daru'

class Trainer
  LEFT_MOST  = 12
  RIGHT_MOST = -12

  def initialize(*paths)
    @paths     = paths
    @sources   = Hash.new { |h,k| h[k] = Hash.new(&h.default_proc) }
    @alphabets = []
  end

  def parse(summa_data=nil)
    if summa_data
      summa_data.each { |word| source_matrix(word) }
    else
      @paths.each do |path|
        File.foreach(path) do |line|
          line = line.split("\t")
          next unless line[1].include?('pos=N')
          word = line.first
          source_matrix(word)
          # @alphabets = @alphabets.push(word).reduce(:+).split('').uniq
        # .read(path)
        # .split("\n")
        # .map { |x| x.split("\t") }      
        # .keep_if { |x| x[1].include?('pos=N') }
        # .map(&:first)
        # .each { |word| source_matrix(word) }
        end
      end
    end
    @alphabets   = (@sources.keys + @sources.values.map(&:keys).flatten).uniq
    @sources.each do |k, v|
      source_keys = v.keys
      (@alphabets - source_keys).each { |s| @sources[k][s] = 0 }
    end
    source_keys = @sources.keys
    (@alphabets - source_keys).each do |key|
      @alphabets.each do |alpha|
        @sources[key][alpha] = 0
        @sources[alpha][key] = 0
        @sources[key][key] = 0
        @sources[alpha][alpha] = 0
      end
    end
    @sources.sort_by { |k,v| k }.to_h
  end

  private

  def source_matrix(word)
    puts "Training word: #{word}"
    i, j = 0, 0
    word_length = word.length

    while i < word_length - 1 do
      j = i+1
      while j < word_length do
        update_source_matrix(i, i - word_length, word[i], j, j - word_length, word[j])
        update_source_matrix(j, j - word_length, word[j], i, i - word_length, word[i])
        j += 1
      end
      i += 1
    end
  end

  def update_source_matrix(left1, right1, char1, left2, right2, char2)
    update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{left2}_#{right2}") if left1 < LEFT_MOST && left2 < LEFT_MOST && right1 > RIGHT_MOST && right2 > RIGHT_MOST
    update_at("#{char1}_#{right1}", "#{char2}_#{left2}_#{right2}") if left2 < LEFT_MOST && right1 > RIGHT_MOST && right2 > RIGHT_MOST
    update_at("#{char1}_#{left1}", "#{char2}_#{left2}_#{right2}") if left1 < LEFT_MOST && left2 < LEFT_MOST && right2 > RIGHT_MOST
    update_at(char1, "#{char2}_#{left2}_#{right2}") if left2 < LEFT_MOST && right2 > RIGHT_MOST

    update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{right2}") if left1 < LEFT_MOST && right1 > RIGHT_MOST && right2 > RIGHT_MOST
    update_at("#{char1}_#{right1}", "#{char2}_#{right2}") if right1 > RIGHT_MOST && right2 > RIGHT_MOST
    update_at("#{char1}_#{left1}", "#{char2}_#{right2}") if left1 < LEFT_MOST && right2 > RIGHT_MOST
    update_at(char1, "#{char2}_#{right2}") if right2 > RIGHT_MOST

    update_at("#{char1}_#{left1}_#{right1}", "#{char2}_#{left2}") if left1 < LEFT_MOST && left2 < LEFT_MOST && right1 > RIGHT_MOST
    update_at("#{char1}_#{right1}", "#{char2}_#{left2}") if left2 < LEFT_MOST && right1 > RIGHT_MOST
    update_at("#{char1}_#{left1}", "#{char2}_#{left2}") if left1 < LEFT_MOST && left2 < LEFT_MOST
    update_at(char1, "#{char2}_#{left2}") if left2 < LEFT_MOST

    update_at("#{char1}_#{left1}_#{right1}", char2) if left1 < LEFT_MOST && right1 > RIGHT_MOST
    update_at("#{char1}_#{right1}", char2) if right1 > RIGHT_MOST
    update_at("#{char1}_#{left1}", char2) if left1 < LEFT_MOST
    update_at(char1, char2)
  end

  def update_at(key1, key2)
    if @sources.keys.include?(key1) && @sources[key1].keys.include?(key2)
      @sources[key1][key2] += 1
    else
      @sources[key1][key2] = 1
    end
  end
end

summa_data = nil

# summa_data = %w[walk talk]

# inst    = Trainer.new('fixture/finnish/finnish-task1-train')
# source = inst.parse(summa_data)
# File.open('source_matrix4.json', 'w') { |f| f.write(JSON.pretty_generate(source)) }
# df = Daru::DataFrame.new(source, index: source.keys)
# pp df