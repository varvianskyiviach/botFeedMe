CREATE TABLE feeding (
	id INTEGER PRIMARY KEY,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	volume FLOAT NOT NULL,
	chat_id INTEGER DEFAULT 1
);

