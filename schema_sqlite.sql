CREATE TABLE `securities` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `ticker` VARCHAR(255),
  `name` VARCHAR(255),
  `current_price` REAL
);

CREATE TABLE `portfolio` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `ticker` VARCHAR(255),
  `shares` INTEGER,
  `average_price` REAL
);

CREATE TABLE `transactions` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `ticker` VARCHAR(255),
  `shares` INTEGER,
  `trade` VARCHAR(255),
  `created_at` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);