# Scraper information from the website of the German Federal Assembly
Collecting information about members of the German Federal Assembly with saving their contacts in a SQL database.

## Data sources

The information comes from the website of the German Federal Assembly:
- [Members of the German Federal Assembly](https://www.bundestag.de/en/members).

## Requirements

- Python;
- MySQL database.

## Installation

Install requirements:
```bash
pip install -r requiremets
```

Create a database and specify the access parameters in the file:
```bash
config.py
```
Fill in the following fields in file config.py:
```bash
host = "your_host"
user = "user_name"
password = "your_password"
db_name = "your_db_name"

```

## Application launch
After setting the database parameters, run the file: 
```bash
main.py
```