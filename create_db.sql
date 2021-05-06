CREATE DATABASE survey_db;

CREATE USER survey_user WITH ENCRYPTED PASSWORD 'survey';
GRANT ALL PRIVILEGES ON DATABASE survey_db TO survey_user;

\c survey_db;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "survey_user";

\c postgres;
