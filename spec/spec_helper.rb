require 'simplecov'
SimpleCov.start do
  add_filter 'spec'
  # minimum_coverage_by_file 95
end

require 'bundler/setup'

require 'rspec'
require 'rspec/its'
require 'webmock/rspec'
require 'saharspec/its/call'

require 'tempfile'
require 'open-uri'

require 'btp'

require_relative 'support/shared_contexts'
require_relative 'support/shared_examples'
require_relative 'support/custom_matchers'

RSpec::Expectations.configuration.warn_about_potential_false_positives = false

RSpec.configure do |config|
  config.example_status_persistence_file_path = '.rspec_status'
  config.disable_monkey_patching!
  config.expect_with :rspec do |c|
    c.syntax = :expect
  end
end

class String
  def unindent
    gsub(/\n\s+?\|/, "\n").gsub(/\|\n/, "\n").gsub(/^\n|\n\s+$/, '')
  end
end
