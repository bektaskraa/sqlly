# SQLly

SQLly is a Python package for simplifying and accelerating the use of SQL queries in Python. It has two main functions, `connect()` and `get()`, both of which are designed to make it easier to interact with a SQL database.

## Installation

You can install SQLly using pip:

```bash
pip install SQLly
```
## Usage
To use SQLly, first import it:

```python

from SQLly import SQLly
```

### Connecting to a Database

To connect to a database, use the `connect()` function. This function takes four parameters: `host`, `username`, `password`, and `db` . Here's an example:

```python
db = SQLly.SQL.connect("localhost", "root", "", "game")
```
or

```python
db = SQLly.SQL("localhost", "root", "", "game")
```

### Retrieving Data

To retrieve data from a database, use the `get()` function. This function takes four parameters: `table`, `select`, `sort`, and `limit` . Here's an example:

```python
result = myconnect.get('players', sort=[('level', '1')], limit=10)
```

Returns the top 10 of 'players' with 'level' of '1' from the 'players' table.

