insert OR REPLACE INTO stocks(signature, name, currency, dividend_per_year, dividend_forecast)
VALUES ('KOP', 'Kopparbergs', 'SEK', 1, 5.90),
('AAPL', 'Apple Inc', 'USD', 4, 0.57),
('BON', 'Bonheur', 'NOK', 1, 0.0),
('CAST', 'Castellum', 'SEK', 2, 3.05),
('C', 'Citigroup', 'USD', 4, 0.0),
('CLAS-B', 'Clas Olsson', 'SEK', 1, 6.25),
('KO', 'Coca Cola', 'USD', 4, 0.37),
('DE', 'Deere & Co', 'USD', 4, 0.6),
('ERIC-B', 'Ericsson', 'SEK', 1, 0.0),
('SHB-B', 'Handelsbanken B', 'SEK', 1, 7.5),
('SHB-A', 'Handelsbanken A', 'SEK', 1, 7.5),
('HM-B', 'Hennes & Mauritz', 'SEK', 2, 4.875),
('INDU-C', 'Industrivärden', 'SEK', 1, 5.75),
('INVE-B', 'Investor', 'SEK', 1, 13.0),
('MCD', 'McDonalds', 'USD', 4, 0.0),
('PROTCT', 'Protector', 'NOK', 1, 0.0),
('SAMPO', 'Sampoo', 'EUR', 1, 2.85),
('NDA', 'Nordea', 'EUR', 1, 0.69),
('SAN', 'Banco Santander', 'USD', 4, 0.0),
('TELIA', 'Telia', 'SEK', 2, 1.18),
('VOLV-B', 'Volvo', 'SEK', 1, 3.0),
('WMT', 'Walmarts', 'USD', 4, 0.0),
('SWED-A', 'Swedbank', 'SEK', 1, 14.2),
('SBUX', 'Starbucks', 'USD', 4, 0.3),
('VARDIA', 'Vardia', 'NOK', 1, 0.0),
('RATO-B', 'Ratos', 'SEK', 1, 3.25),
('NCC-B', 'NCC', 'SEK', 1, 0.0),
('SKA-B', 'Skanska', 'SEK', 1, 6.00),
('SRNKE-B', 'Serneke', 'SEK', 1, 0.0),
('FING-B', 'Fingerprint', 'SEK', 1, 0.0),
('NOKIA', 'Nokia', 'EUR', 1, 0.0),
('SIGM-B', 'Sigma', 'SEK', 1, 0.0),
('MULQ', 'MultiQ', 'SEK', 1, 0.0),
('WM-B', 'WM Data', 'SEK', 1, 0.0),
('ORES', 'Öresund', 'SEK', 1, 5.5),
('NOVO-B', 'Novo Nordisk', 'DKK', 1, 8.31),
('SKIS-B', 'Skistar', 'SEK', 1, 5.5),
('O', 'Realty Income', 'USD', 12, 0.219),
('JNJ', 'Johnson & Johnson', 'USD', 4, 0.9),
('AXFO', 'Axfood', 'SEK', 1, 7.0),
('KINV-B', 'Kinnevik', 'SEK', 1, 8.25),
('BILIA-A', 'Bilia', 'SEK', 1, 0),
('MQ', 'MQ', 'SEK', 1, 0),
('MTG', 'MTG', 'SEK', 1, 0),
('TIGO', 'Millicom', 'SEK', 1, 1.32),
('BALD-B', 'Balder', 'SEK', 1, 0),
('SBB-B', 'SBB i Norden', 'SEK', 1, 0),
('LUND-B', 'Lundbergföretagen', 'SEK', 1, 0),
('AVZ-GLO', 'Avanza Global', 'SEK', 1, 0),
('AVZ-ZRO', 'Avanza Zero', 'SEK', 1, 0),
('XACTHDIV', 'XACT Högutdelande', 'SEK', 1, 0),
('LATO-B', 'Latour', 'SEK', 1, 2.5);

insert OR REPLACE INTO stock_avanza (stock, stock_id, stock_name, is_stock) VALUES ('AVZ-GLO', 878733, 'avanza-global',
0),
('AVZ-ZRO', 41567, 'avanza-zero', 0),
('XACTHDIV', 742236, 'xact-hogutdelande', 2),
('LUND-B', 5375, 'lundbergforetagen-b', 1),
('SBB-B', 517316, 'samhallsbyggnadsbo--i-norden-b', 1),
('KOP', 13477, 'kopparbergs-b', 1),
('AXFO', 5465, 'axfood', 1),
('SKA-B', 5257, 'skanska-b', 1),
('CAST', 5353, 'castellum', 1),
('CLAS-B', 5457, 'clas-ohlson-b', 1),
('HM-B', 5364, 'hennes---mauritz-b', 1),
('INDU-C', 5245, 'industrivarden-c', 1),
('INVE-B', 5247, 'investor-b', 1),
('JNJ', 3666, 'johnson---johnson', 1),
('KINV-B', 5369, 'kinnevik-b', 1),
('LATO-B', 5321, 'latour-b', 1),
('NOVO-B', 52300, 'novo-nordisk-b', 1),
('O', 147048, 'realty-income-corp', 1),
('PROTCT', 81848, 'protector-forsikring', 1),
('SAMPO', 52810, 'sampo-oyj-a', 1),
('RATO-B', 5397, 'ratos-b', 1),
('NDA', 888677, 'nordea-bank-abp', 1),
('SWED-A', 5241, 'swedbank-a', 1),
('TELIA', 5479, 'telia-company', 1),
('TIGO', 6048, 'millicom-int--cellular-sdb', 1),
('ORES', 5302, 'oresund', 1),
('MCD', 4375, 'mcdonalds-corp', 1),
('FING-B', 5468, 'fingerprint-cards-b', 1),
('AAPL', 3323, 'apple-inc', 1),
('BON', 52498, 'bonheur', 1),
('KO', 3803, 'coca-cola-co', 1),
('C', 3655, 'citigroup-inc', 1),
('DE', 4160, 'deere---co', 1),
('BALD-B', 5459, 'fast--balder-b', 1),
('SKIS-B', 5339, 'skistar-b', 1),
('WMT', 4008, 'walmart-inc', 1),
('SBUX', 4456, 'starbucks-corp', 1),
('SRNKE-B', 707959, 'serneke-group-b', 1),
('NOKIA', 52784, 'nokia-oyj', 1),
('VOLV-B', 5269, 'volvo-b', 1),
('NCC-B', 5294, 'ncc-b', 1),
('SHB-A', 5264, 'handelsbanken-a', 1),
('SHB-B', 5265, 'handelsbanken-b', 1),
('MULQ', 5464, 'multiq-international', 1),
('MTG', 5438, 'modern-times-group-b', 1),
('BILIA-A', 5276, 'bilia-a', 1),
('SAN', 35067, 'banco-santander-sa', 1),
('ERIC-B', 5240, 'ericsson-b', 1);

insert OR REPLACE INTO stock_bloomberg (stock, bloomberg_signature) VALUES
('KOP',     'KOBRMTFB:SS'),
('AXFO',    'AXFO:SS'),
('BILIA-A', 'BILIA:SS'),
('MQ',      'MQ:SS'),
('MTG',     'MTGB:SS'),
('SKA-B',   'SKAB:SS'),
('TIGO',    'TIGO:SS'),
('ORES',    'ORES:SS'),
('TELIA',   'TELIA:SS'),
('LATO-B',  'LATOB:SS'),
('KINV-B',  'KINVB:SS'),
('SKIS-B',  'SKISB:SS'),
('HM-B',    'HMB:SS'),
('CAST',    'CAST:SS'),
('CLAS-B',  'CLASB:SS'),
('SHB-A', 'SHBA:SS'),
('SWED-A', 'SWEDA:SS'),
('INDU-C', 'INDUC:SS'),
('INVE-B', 'INVEB:SS'),
('SAMPO', 'SAMPO:FH'),
('NDA', 'NDA:FH'),
('NOVO-B', 'NOVOB:DC'),
('KO', 'KO:US'),
('JNJ', 'JNJ:US'),
('O', 'O:US'),
('AVZ-GLO', 'avanza-global'),
('AVZ-ZRO', 'avanza-zero-den-avgiftsfria-fonden');

insert OR REPLACE INTO stock_identifier(stock, identifier)
VALUES ('XACTHDIV', 'XACT Högutdelande'),
('SBB-B', 'Samhällsbyggnadsbo. i Norden B'),
('LUND-B', 'Lundbergföretagen B'),
('AAPL', 'Apple Inc'),
('SKIS-B', 'SkiStar B'),
('SKIS-B', 'SKIS B'),
('BALD-B', 'Fast. Balder B'),
('MTG', 'Modern Times Group B'),
('MTG', 'MTG B DR'),
('BILIA-A', 'Bilia A'),
('BILIA-A', 'BILI A DR'),
('MQ', 'MQ Holding'),
('MQ', 'MQ DR'),
('KOP', 'Kopparbergs B'),
('VARDIA', 'Vardia Insurance Group'),
('VARDIA', 'Insr Insurance Group'),
('VARDIA', 'VARDIA BTA15'),
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
('TIGO', 'Millicom Int. Cellular SDB'),
('DE', 'Deere & Co'),
('ERIC-B', 'Ericsson B'),
('SHB-B', 'Handelsbanken'),
('SHB-B', 'Handelsbanken B'),
('SHB-A', 'Handelsbanken A'),
('SHB-B', 'SHB'),
('SHB-B', 'SHB B OLD'),
('HM-B', 'Hennes & Mauritz B'),
('INDU-C', 'Industrivärden C'),
('INVE-B', 'Investor B'),
('MCD', "Mcdonald's Corp"),
('PROTCT', 'Protector Forsikring'),
('CAST', 'Castellum'),
('CAST', 'CAST BTA'),
('C', 'Citigroup'),
('C', 'Citigroup Inc'),
('JNJ', 'Johnson & Johnson'),
('SAMPO', 'Sampo A'),
('SAMPO', 'Sampo Oyj A'),
('TELIA', 'Telia Company'),
('NOVO-B', 'Novo Nordisk B'),
('WMT', 'Walmart Inc'),
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
('SKIS-B', 'SkiStar B'),
('ORES', 'Öresund'),
('O', 'Realty Income Corp'),
('LATO-B', 'Latour B'),
('NDA', 'Nordea Bank Abp'),
('AVZ-GLO', 'Avanza Global'),
('AVZ-ZRO', 'Avanza Zero'),
('KINV-B', 'Kinnevik B');

insert OR REPLACE INTO split_ratio (stock, ratio) VALUES
('AAPL', 7.0),
('HM-B', 2.0),
('SHB-B', 3.0),
('SBUX', 2.0),
('VOLV-B', 6.0),
('ERIC-B', 0.2);
