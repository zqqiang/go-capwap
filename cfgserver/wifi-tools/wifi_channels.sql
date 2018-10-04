
DROP TABLE IF EXISTS 'wifi_channels';

CREATE TABLE 'wifi_channels' (
  'country' int(11) NOT NULL COMMENT 'country numeric code',
  'platform' int(11) NOT NULL COMMENT 'platform oid',
  'radio' smallint(5) DEFAULT NULL COMMENT 'radio-1: 1, radio-2: 2',
  'band' int(11) NOT NULL COMMENT 'band oid',
  'bonding' smallint(5) DEFAULT NULL COMMENT 'high-throughput band-wide mode(0:20MHz,1:40MHz,2:80MHz)',
  'darrp' tinyint(1) DEFAULT NULL COMMENT 'if darrp has been choose.',
  'channels' varchar(128) NOT NULL COMMENT 'channel list, eg. 1,2,3,4,...'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES 'wifi_channels' WRITE;

INSERT INTO 'wifi_channels' VALUES 
(1, 0, 0, 3, 1, 0, '1,2,3,4,5,6,7'),
(1, 0, 0, 3, 1, 1, '1,2,3,4,5,6,7'),
(1, 0, 0, 3, 0, 0, '1,2,3,4,5,6,7,8,9,10,11'),
(1, 0, 0, 3, 0, 1, '1,2,3,4,5,6,7,8,9,10,11'),
(1, 0, 0, 4, 1, 0, '36,44,149,157'),
(1, 0, 0, 4, 1, 1, '36,40,44,48,149,153,157,161'),
(1, 0, 0, 4, 0, 0, '36,40,44,48,149,153,157,161,165'),
(1, 0, 0, 4, 0, 1, '36,40,44,48,149,153,157,161,165'),
(1, 0, 0, 5, 1, 0, '1,2,3,4,5,6,7'),
(1, 0, 0, 5, 1, 1, '1,2,3,4,5,6,7'),
(1, 0, 0, 5, 0, 0, '1,2,3,4,5,6,7,8,9,10,11'),
(1, 0, 0, 5, 0, 1, '1,2,3,4,5,6,7,8,9,10,11'),
(1, 0, 0, 7, 1, 0, '1,2,3,4,5,6,7'),
(1, 0, 0, 7, 1, 1, '1,2,3,4,5,6,7'),
(1, 0, 0, 7, 0, 0, '1,2,3,4,5,6,7,8,9,10,11'),
(0, 0, 0, 0, 0, 0, '');

UNLOCK TABLES;