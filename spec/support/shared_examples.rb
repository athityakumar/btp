RSpec.shared_examples 'a daru dataframe' do |name: nil, nrows: nil, ncols: nil, **opts|
  it            { is_expected.to be_a(Daru::DataFrame) }

  its(:name)    { is_expected.to eq(name)           } if name
  its(:ncols)   { is_expected.to eq(ncols)          } if ncols
  its(:nrows)   { is_expected.to eq(nrows)          } if nrows

  opts.each { |key, value| its(key.to_sym) { is_expected.to eq(value) } }
end

RSpec.shared_examples 'exact daru dataframe' do |dataframe: nil, data: nil, nrows: nil, ncols: nil, order: nil, index: nil, name: nil, **opts| # rubocop:disable Metrics/LineLength
  it_behaves_like 'a daru dataframe',
    name: name,
    nrows: nrows,
    ncols: ncols,
    **opts

  it            { is_expected.to eq(dataframe)      } if dataframe
  its(:data)    { is_expected.to ordered_data(data) } if data
  its(:index)   { is_expected.to eq(index.to_index) } if index
  its(:vectors) { is_expected.to eq(order.to_index) } if order
end
