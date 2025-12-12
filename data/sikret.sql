CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    email TEXT UNIQUE(60),
    password_hash VARCHAR(60),
    created_at VARCHAR(60),

)

CREATE TABLE accounts (
    name_company VARCHAR(60),
    
)