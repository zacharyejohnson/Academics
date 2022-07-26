/* 1. this logical design for the youth sports league is logically incorrect.
The player object should have a teamID foreign key, not vice versa. This is because
players has a one-to-one relationship to team(one player can only have one team),
but team can have many players. So, the player object should have a teamID FK to
identify the SINGLE team that the player can belong to. Also, player name shoudl be fname, lname
and does not need to be unique as players couls have the same name. */

-- 2.
CREATE TABLE IF NOT EXISTS Team(
	teamID int PRIMARY KEY,
	name varchar( 255 ) UNIQUE NOT NULL,
	color varchar( 50 ) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Player(
  playerID serial PRIMARY KEY,
  fname varchar( 255 ) NOT NULL,
  lname varchar( 255 ) NOT NULL,
  birthdate date NOT NULL,
  team_ID int, 
  FOREIGN KEY (team_ID) REFERENCES Team(teamid)
);

-- 3.
INSERT INTO Team( teamID, name, color )
  VALUES ( 1, 'Eagles', 'white'), ( 2, 'Tigers', 'yellow');
INSERT INTO Player(fname, lname, birthdate, team_ID)
  VALUES ('John', 'Doe', '2012-1-01', 1), ('Jake', 'Johnson', '2012-3-01', 1),  -- team 1 players
          ('Josh', 'Monroe', '2001-4-01', 2), ('Isaac', 'Huber', '2000-4-16', 2), ('Jacob', 'Rodin', '2006-10-10', 2);  -- team 2 players;


/* 4.  This logical design will work. The two types of book- Printted and E-Book are disjoint in this bookstore so books are sold as either
an E-book or a paperback book. Hence, I will make two seperate tables and not even make a "Book" table. This
is logically valid. */

CREATE TABLE IF NOT EXISTS PrintedBook(
  bookID serial PRIMARY KEY,
  title varchar( 255 ) NOT NULL,
  height float,
  depth float,
  width float,
  weight float,
  number_of_pages int NOT NULL
);

CREATE TABLE IF NOT EXISTS Ebook(
  ebookID serial PRIMARY KEY,
  title VARCHAR( 255 ),
  download_size int,
  support_platform VARCHAR( 50 )
);

-- 5.

CREATE TABLE support_platform(
  platformID serial PRIMARY KEY,
  platform_description VARCHAR( 50 ),
  ebookID int,
  FOREIGN KEY (ebookID) REFERENCES ebook(ebookID)
);


ALTER TABLE Ebook DROP COLUMN support_platform;
-- 6.

INSERT INTO PrintedBook(title, height, depth, width, weight, number_of_pages)
VALUES('To Kill a Mockingbird', 8, 2, 5, 1.3, 506), ('War and Peace', 11, 4, 6, 2.8, 1109);

INSERT INTO Ebook(title, download_size)
VALUES('Harry Potter', 19.6), ('Lord of The Rings', 20.8); 

INSERT INTO support_platform(platform_description, ebookID)
VALUES('kindle', 1),('pdf', 1),('kindle', 2),('pdf', 2),('html', 2);
