CREATE TABLE datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    status VARCHAR(255),
    gz_path TEXT
);
CREATE TABLE annotated_datasets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dataset_id INT,
    FOREIGN KEY (dataset_id) REFERENCES Datasets(id)
);
CREATE TABLE evaluate_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    annotated_at DATE,
    evaluated_point INT,
    dataset_id INT,
    evaluated_text_category TEXT,
    FOREIGN KEY (dataset_id) REFERENCES Datasets(id)
);
CREATE TABLE user_counts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    counts INT,
    annotated_at DATE
);

CREATE TABLE users
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT,
    password  TEXT
);