INSERT OR REPLACE INTO stocks (signature, name, exchange, currency, dividend_per_year, dividend_forecast) VALUES
('KOP',     'Kopparbergs',      'STO',      'SEK',  1,  5.90),
('AAPL',    'Apple Inc',        'NASDAQ',   'USD',  4,  0.57),
('BON',     'Bonheur',          'OL',       'NOK',  1,  0.0),
('CAST',    'Castellum',        'STO',      'SEK',  2,  2.5),
('C',       'Citigroup',        'NYSE',     'USD',  4,  0.0),
('CLAS-B',  'Clas Olsson',      'STO',      'SEK',  1,  5.75),
('KO',      'Coca Cola',        'NYSE',     'USD',  4,  0.35),
('DE',      'Deere & Co',       'NYSE',     'USD',  4,  0.6),
('ERIC-B',  'Ericsson',         'STO',      'SEK',  1,  0.0),
('SHB-B',   'Handelsbanken',    'STO',      'SEK',  1,  5.0),
('HM-B',    'Hennes & Mauritz', 'STO',      'SEK',  2,  4.875),
('INDU-C',  'Industrivärden',   'STO',      'SEK',  1,  5.0),
('INVE-B',  'Investor',         'STO',      'SEK',  1,  11.0),
('MCD',     'McDonalds',        'NYSE',     'USD',  4,  0.0),
('PROTCT',  'Protector',        'OL',       'NOK',  1,  0.0),
('SAMAS',   'Sampoo',           'HEL',      'EUR',  1,  2.3),
('SAN',     'Banco Santander',  'NYSE',     'USD',  4,  0.0),
('TELIA',   'Telia',            'STO',      'SEK',  2,  1.0),
('VOLV-B',  'Volvo',            'STO',      'SEK',  1,  3.0),
('WMT',     'Walmarts',         'NYSE',     'USD',  4,  0.0),
('SWED-A',  'Swedbank',         'STO',      'SEK',  1,  13.20),
('SBUX',    'Starbucks',        'NASDAQ',   'USD',  4,  0.25),
('VARDIA',  'Vardia',           'OL',       'NOK',  1,  0.0),
('RATO-B',  'Ratos',            'STO',      'SEK',  1,  3.25),
('NCC-B',   'NCC',              'STO',      'SEK',  1,  0.0),
('SKA-B',   'Skanska',          'STO',      'SEK',  1,  8.25),
('SRNKE-B', 'Serneke',          'STO',      'SEK',  1,  0.0),
('FING-B',  'Fingerprint',      'STO',      'SEK',  1,  0.0),
('NOKIA',   'Nokia',            'HEL',      'EUR',  1,  0.0),
('SIGM-B',  'Sigma',            'STO',      'SEK',  1,  0.0),
('MULQ',    'MultiQ',           'STO',      'SEK',  1,  0.0),
('WM-B',    'WM Data',          'STO',      'SEK',  1,  0.0),
('ORES',    'Öresund',          'STO',      'SEK',  1,  0.0),
('NOVO-B',  'Novo Nordisk',     'CPH',      'DKK',  1,  4.6),
('O',       'Realty Income',    'NYSE',     'USD',  12, 0.211),
('AXFO',    'Axfood',           'STO',      'SEK',  1,  6.0);


INSERT OR REPLACE INTO stock_identifier (stock, identifier) VALUES
('AAPL', 'Apple Inc'),
('KOP', 'Kopparbergs B'),
('VARDIA', 'Vardia Insurance Group'),
('VARDIA', 'Insr Insurance Group'),
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
('WMT', 'Wal-Mart Stores Inc'),
('SWED-A', 'Swedbank A'),
('SBUX', 'Starbucks Corp'),
('RATO-B', 'Ratos B'),
('NCC-B', 'NCC B'),
('SIGM-B', 'SIGM B'),
('MULQ', 'MultiQ International'),
('WM-B', 'WM B'),
('SRNKE-B', 'Serneke Group B'),
('AXFO', 'Axfood'),
('SKA-B', 'Skanska B'),
('ORES', 'Öresund'),
('O', 'Realty Income Corp');

INSERT OR REPLACE INTO split_ratio (stock, ratio) VALUES
('AAPL', 7.0),
('HM-B', 2.0),
('SHB-B', 3.0),
('SBUX', 2.0),
('VOLV-B', 6.0),
('ERIC-B', 0.2);

