CREATE TABLE datasets (
    id INT PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    status VARCHAR(255),
    gz_path TEXT
);
CREATE TABLE annotated_datasets (
    id INT PRIMARY KEY AUTOINCREMENT,
    dataset_id INT,
    FOREIGN KEY (dataset_id) REFERENCES Datasets(id)
);
CREATE TABLE evaluate_status (
    id INT PRIMARY KEY AUTOINCREMENT,
    annotated_at DATE,
    evaluation_point INT,
    dataset_id INT,
    FOREIGN KEY (dataset_id) REFERENCES Datasets(id)
);
CREATE TABLE users (
    id INT PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_name VARCHAR(255),
    password VARCHAR(255)
);

CREATE TABLE user_counts (
    id INT PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    counts INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE users_evaluated (
    id INT PRIMARY KEY AUTOINCREMENT,
    user_id INT,
    dataset_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (dataset_id) REFERENCES Datasets(id)
);

