create database scrobble_proxy;

use scrobble_proxy;

create table users (
    id INTEGER primary key auto_increment,
    name TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

create table sessions (
    id VARCHAR(2000) primary key NOT NULL,
    user INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user) REFERENCES users(id)
);

create table tokens (
    token TEXT NOT NULL,
    user INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

create table scrobbles (
    user INTEGER NOT NULL,
    timestamp INTEGER NOT NULL,
    artist TEXT NOT NULL,
    track TEXT NOT NULL,
    album TEXT,
    albumArtist TEXT,
    FOREIGN KEY(user) REFERENCES users(id)
);
