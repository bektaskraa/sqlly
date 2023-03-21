# SQLly

SQLly is a python library. It supports many database servers. Its purpose is to help perform database operations quickly and easily. The goal in future releases is to support using both SQL and noSQL databases simultaneously. It also aims to minimize manual usage by adding many functions.

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
myconnect = SQLly.SQL.connect("localhost", "root", "", "game")
```
or

```python
myconnect = SQLly.SQL("localhost", "root", "", "game")
```
This code **automatically** searches for a **'mySQL'** server. **you can change** the **'driver'** parameter and use **'postgresql'** or **'sqlite'**
```python
myconnect = SQLly.SQL("localhost", "root", "", "game","postgresql")
```
```python
myconnect = SQLly.SQL("localhost", "root", "", "game","sqlite")
```
### Retrieving Data

To **retrieve data** from a **database**, use the `get()` function. This function **takes four parameters**: `table`, `select`, `sort`, and `limit` . Here's an example:
#### Basic
```python
result = myconnect.get('players')
# SELECT * FROM players
```
This code is the **simplest use** of the **get() function**. In this code the data in the **'players'** table is returned. The returned data is **returned in list type**. There is **dictionary type data for each row**. For example:
```
[
 {
  'id':1,
  'name':'Tom',
  'username':'_tom'
 }
]
```
#### Select
With select you can get only the columns you want
```python
myconnect.get('players','name')
# SELECT name FROM players
```
```python
myconnect.get('players','name,username')
# SELECT name,username FROM players
```
```python
myconnect.get('players',('name','username'))
# SELECT name,username FROM players
```
#### Data Sort & Limit
```python
result = myconnect.get('players', sort=[('level', 1)], limit=10)
# SELECT * FROM players WHERE level = 1 LIMIT 10
```

Returns the top 10 of 'players' with 'level' of '1' from the 'players' table.  **This usage can create error some times** so it is better to use as below.
```python
myconnect.get('players', sort=[SQLly.sort('level',1)], limit=10)
# SELECT * FROM players WHERE level = 1 LIMIT 10
```
Using the **SQLly.sort()** function eliminates these errors.
