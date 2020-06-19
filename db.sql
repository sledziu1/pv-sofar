CREATE TABLE `pv` (
  `id` int(11) NOT NULL,
  `uploaded` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `measured` datetime NOT NULL,
  `power` int(11) NOT NULL,
  `energyDay` decimal(5,2) NOT NULL,
  `energyTotal` decimal(16,1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin2;