CREATE TABLE IF NOT EXISTS albums (
    album_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(128) NOT NULL,
    release_date DATE NOT NULL,
    url VARCHAR(512),
    UNIQUE KEY (title)
);

CREATE TABLE IF NOT EXISTS songs (
    song_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    album_order INT(11) NOT NULL,
    album_id INT(11) NOT NULL,
    url VARCHAR(512),
    FOREIGN KEY (album_id) REFERENCES albums(album_id),
    UNIQUE KEY (name),
    UNIQUE KEY (album_id, album_order)
);

CREATE TABLE IF NOT EXISTS tours (
    tour_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    UNIQUE KEY (name)
);

CREATE TABLE IF NOT EXISTS venues (
    venue_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    city VARCHAR(128) NOT NULL,
    UNIQUE KEY (name, city)
);

CREATE TABLE IF NOT EXISTS tourdates (
    tourdate_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tour_id INT(11) NOT NULL,
    venue_id INT(11) NOT NULL,
    performance_date DATE NOT NULL,
    FOREIGN KEY (tour_id) REFERENCES tours(tour_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);
