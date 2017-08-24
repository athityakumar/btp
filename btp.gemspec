# coding: utf-8

lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'btp/version'

BTP::DESCRIPTION = "This is Athitya Kumar's BTech project, done under "\
                   "Research Scholar Amrith Krishna and Prof. Pawan Goyal "\
                   "from the Department of Computer Science, IIT Kharagpur."
                   .freeze

Gem::Specification.new do |spec|
  spec.name          = 'btp'
  spec.version       = BTP::VERSION
  spec.authors       = ['Athitya Kumar']
  spec.email         = ['athityakumar@gmail.com']
  spec.summary       = BTP::DESCRIPTION
  spec.description   = BTP::DESCRIPTION
  spec.homepage      = 'https://github.com/athityakumar/btp'
  spec.license       = 'MIT'
  spec.files         = `git ls-files -z`.split("\x0").reject { |f| f.match(%r{^(test|spec|features)/}) }
  spec.bindir        = 'bin'
  spec.executables   = spec.files.grep(%r{^bin/}) { |f| File.basename(f) }
  spec.require_paths = ['lib']

  spec.add_runtime_dependency 'daru', '~> 0.1.5'

  spec.add_development_dependency 'bundler', '~> 1.15'
  spec.add_development_dependency 'rake', '~> 10.0'
  spec.add_development_dependency 'redcarpet'
  spec.add_development_dependency 'rspec', '~> 3.0'
  spec.add_development_dependency 'rspec-its'
  spec.add_development_dependency 'rubocop', '>= 0.40.0'
  spec.add_development_dependency 'rubocop-rspec'
  spec.add_development_dependency 'simplecov'
  spec.add_development_dependency 'webmock'
  spec.add_development_dependency 'yard'
  spec.add_development_dependency 'guard-rspec' if RUBY_VERSION >= '2.2.5'
end
