INSERT OR REPLACE INTO stocks (signature, name, exchange, currency) VALUES
('KOP',     'Kopparbergs',      'STO',      'SEK'),
('AAPL',    'Apple Inc',        'NASDAQ',   'USD'),
('BON',     'Bonheur',          'OL',       'NOK'),
('CAST',    'Castellum',        'STO',      'SEK'),
('C',       'Citigroup',        'NYSE',     'USD'),
('CLAS-B',  'Clas Olsson',      'STO',      'SEK'),
('KO',      'Coca Cola',        'NYSE',     'USD'),
('DE',      'Deere & Co',       'NYSE',     'USD'),
('ERIC-B',  'Ericsson',         'STO',      'SEK'),
('SHB-B',   'Handelsbanken',    'STO',      'SEK'),
('HM-B',    'Hennes & Mauritz', 'STO',      'SEK'),
('INDU-C',  'Industrivärden',   'STO',      'SEK'),
('INVE-B',  'Investor',         'STO',      'SEK'),
('MCD',     'McDonalds',        'NYSE',     'USD'),
('PROTCT',  'Protector',        'OL',       'NOK'),
('SAMAS',   'Sampoo',           'HEL',      'EUR'),
('SAN',     'Banco Santander',  'NYSE',     'USD'),
('TELIA',   'Telia',            'STO',      'SEK'),
('VOLV-B',  'Volvo',            'STO',      'SEK'),
('WMT',     'Walmarts',         'NYSE',     'USD'),
('SWED-A',  'Swedbank',         'STO',      'SEK'),
('SBUX',    'Starbucks',        'NASDAQ',   'USD'),
('VARDIA',  'Vardia',           'OL',       'NOK'),
('RATO-B',  'Ratos',            'STO',      'SEK'),
('NCC-B',   'NCC',              'STO',      'SEK'),
('SKA-B',   'Skanska',          'STO',      'SEK'),
('SRNKE-B', 'Serneke',          'STO',      'SEK'),
('FING-B',  'Fingerprint',      'STO',      'SEK'),
('NOKIA',   'Nokia',            'HEL',      'EUR'),
('SIGM-B',  'Sigma',            'STO',      'SEK'),
('MULQ',    'MultiQ',           'STO',      'SEK'),
('WM-B',    'WM Data',           'STO',      'SEK'),
('NOVO-B',  'Novo Nordisk',     'CPH',      'DKK');

INSERT OR REPLACE INTO stock_identifier (stock, identifier) VALUES
('AAPL', 'Apple Inc'),
('KOP', 'Kopparbergs B'),
('VARDIA', 'Vardia Insurance Group'),
('FING-B', 'FING B'),
('FING-B', 'FING BTB0611'),
('NOKIA', 'NOKI SDB'),
('NOKIA', 'Nokia Oyj'),
('VOLV-B', 'VOLV IL B'),
('VOLV-B', 'Volvo B'),
('VOLV-B', 'Volvo DR B'),
('SAN', 'Banco Santander SA'),
('BON', 'Bonheur'),
('CLAS-B', 'Clas Ohlson B'),
('KO', 'Coca-Cola Co'),
('DE', 'Deere & Co'),
('ERIC-B', 'Ericsson B'),
('SHB-B', 'Handelsbanken'),
('SHB-B', 'Handelsbanken B'),
('SHB-B', 'SHB'),
('SHB-B', 'SHB B OLD'),
('HM-B', 'Hennes & Mauritz B'),
('INDU-C', 'Industrivärden C'),
('INVE-B', 'Investor B'),
('MCD', "McDonald's Corp"),
('PROTCT', 'Protector Forsikring'),
('CAST', 'Castellum'),
('CAST', 'CAST BTA'),
('C', 'Citigroup'),
('C', 'Citigroup Inc'),
('SAMAS', 'Sampo A'),
('TELIA', 'Telia Company'),
('NOVO-B', 'Novo Nordisk B'),
('WMT', 'Walmart'),
('WMT', 'Wal Mart Stores Inc'),
('SWED-A', 'Swedbank A'),
('SBUX', 'Starbucks Corp'),
('RATO-B', 'Ratos B'),
('NCC-B', 'NCC B'),
('SIGM-B', 'SIGM B'),
('MULQ', 'MultiQ International'),
('WM-B', 'WM B'),
('SRNKE-B', 'Serneke Group B'),
('SKA-B', 'Skanska B');

INSERT OR REPLACE INTO split_ratio (stock, ratio) VALUES
('AAPL', 7.0),
('HM-B', 2.0),
('SHB-B', 3.0),
('SBUX', 2.0),
('VOLV-B', 6.0),
('ERIC-B', 0.2);
