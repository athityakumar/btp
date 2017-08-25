RSpec.describe BTP::Matrix do
  subject { described_class.new(path).parse }

  context 'for finnish language dataset' do
    let(:path) { 'spec/fixtures/finnish/finnish-task1-train' }

    it { is_expected.to be_a(Daru::DataFrame) }
  end
end
