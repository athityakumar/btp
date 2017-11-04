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
