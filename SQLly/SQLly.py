import mysql.connector
import psycopg2
import sqlite3
from colorama import Fore, Back, Style

SHOW_ERROR = False
SHOW_EVENT = False

def __error(e):
    if SHOW_ERROR: print(Fore.RED + Style.BRIGHT + "SQLly Error: " + Style.RESET_ALL + Fore.RED + e + Style.RESET_ALL)
def __event(e):
    if SHOW_EVENT: print(Fore.BLUE + Style.BRIGHT + "SQLly Event: " + Style.RESET_ALL + Fore.BLUE + e + Style.RESET_ALL)
def show_error():
    SHOW_ERROR = True
def hide_error():
    SHOW_ERROR = False

class SQL:
    def __error(self,e):
        if SHOW_ERROR: print(Fore.RED + Style.BRIGHT + "SQL Error: " + Style.RESET_ALL + Fore.RED + e + Style.RESET_ALL)
    def __event(self,e):
        if SHOW_EVENT: print(Fore.BLUE + Style.BRIGHT + "SQL Event: " + Style.RESET_ALL + Fore.BLUE + e + Style.RESET_ALL)
    def __init__(self,host,username,password,db,driver="mysql"):
        self.host = host
        self.db = db
        self.driver = driver
        self.connect(host, username, password, db,driver)
    def connect(self,host, username, password, db, driver="mysql"):
        if driver == "mysql":
            try:
                try:
                    self.connection = mysql.connector.connect(host=host, user=username, password=password, database=db)
                except mysql.connector.errors.ProgrammingError as e:
                    self.__error(f"Unknown database '{db}'")
                    return False
                self.__event(f"Connected to MySQL database '{db}'")
            except mysql.connector.Error as e:
                self.__error(f"Error connecting to MySQL database: {e}")
                return False
        elif driver == "postgresql":
            try:
                self.connection = psycopg2.connect(host=host, user=username, password=password, dbname=db)
                self.__event(f"Connected to PostgreSQL database '{db}'")
            except psycopg2.Error as e:
                self.__error(f"Error connecting to PostgreSQL database: {e}")
                return None, None
        elif driver == "sqlite":
            try:
                self.connection = sqlite3.connect(db)
                self.__event(f"Connected to SQLite database '{db}'")
            except sqlite3.Error as e:
                self.__error(f"Error connecting to SQLite database: {e}")
        else:
            self.__error(f"Unknown database driver: {driver}")
            return False
        self.cursor = self.connection.cursor()
        return True

    def __jsonData(self,table,rows,header=True):
        if header == True:
            query = f"SELECT DISTINCT column_name FROM information_schema.columns WHERE table_name = '{table}'"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        else:
            result = header
        clearData = []
        for row in list(rows):
            index = 0
            data = {}
            for column_name in result:
                data[column_name[0]] = list(row)[index]
                if len(result) - 1 > index:
                    index += 1
            clearData.append(data)
        return clearData

    def get(self,table,select="*",sort=None,limit=None,clear=True):

        if not select == '*' and not isinstance(select,str):
            slct = ""
            index = 0
            for i in select:
                slct += i
                if not index == len(select)-1:
                    slct+=", "
                index += 1
            select = slct
        query = f"SELECT {select} FROM {table}"
        if not sort == None:
            query += " WHERE"
            index = 0
            for i in sort:
                if index > 0 and not index == len(sort):
                    if type(i) == tuple:
                        query += " AND"
                    if type(i) == list:
                        query += " OR"
                if len(i) == 3:
                    if str(i[2]).upper() == 'BETWEEN':
                        query += f" {i[0]} {i[2]} {i[1][0]} AND {i[1][1]}"
                    else:
                        query += f" {i[0]} {i[2]} {i[1]}"
                elif len(i) == 2:
                    query+= f" {i[0]} = {i[1]}"
                else:
                    pass
                index += 1
        if not limit == None:
            if type(limit) == int or type(limit) == str:
                query += f" LIMIT {limit}"
            else:
                if len(list(list([limit])[0])) > 1:
                    query += f" LIMIT {list(list([limit])[0])[0]} , {list(list([limit])[0])[1]}"
                else:
                    query += f" LIMIT {list(list([limit])[0])[0]}"
        self.__event(query)
        self.cursor.execute(query)
        if not select == "*":
            if isinstance(select,list):
                header = select
                result = []
                for i in header:
                    arg = (i,)
                    result.append(arg)
                select = result
            if isinstance(select,str):
                select = select.split(',')
                header = select
                result = []
                for i in header:
                    arg = (i,)
                    result.append(arg)
                select = result
            if isinstance(select,str):
                arg = (select,)
                select = list(select)
                select.clear()
                select.append(arg)
            return self.__jsonData(table,self.cursor.fetchall(),select)
        else:
            return self.__jsonData(table,self.cursor.fetchall())

    def insert(self,table,data:dict):
        for i in data:
            if isinstance(data[i],str):data[i] = f"'{data[i]}'"
            if data[i] == None:data[i] = f"NULL"
        query = f"INSERT INTO {table} ("
        index = 0
        for i in data.keys():
            query += f"{i}"
            if index < len(data.keys())-1:
                query += ","
            index +=1
        query += ") VALUES ("
        index = 0
        for i in data:
            query += f"{data[i]}"
            if index < len(data)-1:
                query += ","
            index +=1
        query += ")"
        self.__event(query)
        self.cursor.execute(query)
        self.connection.commit()

    def update(self,table,select:dict,data:dict):
        for i in data:
            if isinstance(data[i],str):data[i] = f"'{data[i]}'"
        for i in select:
            if isinstance(select[i], str): select[i] = f"'{select[i]}'"
        query = f"UPDATE {table} SET "
        index = 0
        for i in data:
            query += f"{i} = {data[i]}"
            if index < len(data)-1:
                query += ","
            index +=1
        query += " WHERE "
        index = 0
        for i in select:
            query += f"{i} = {select[i]}"
            if index < len(select)-1:
                query += ","
            index +=1
        self.__event(query)
        self.cursor.execute(query)
        self.connection.commit()

    def remove(self,table,select:dict):
        for i in select:
            if isinstance(select[i], str): select[i] = f"'{select[i]}'"
        query = f"DELETE FROM {table} WHERE "
        index = 0
        for i in select:
            query += f"{i} = {select[i]}"
            if index < len(select) - 1:
                query += ","
            index += 1
        self.__event(query)
        self.cursor.execute(query)
        self.connection.commit()

    def duplicate(self,table,select,to:str,avoidColumn=None,replaceColumn=None):
        data = self.get(table,sort=select)
        if len(data) <= 0:
            self.__error("Selected data to duplicate could not be found!")
        else:
            self.__event(f"Data '{str(data[0])}' selected to duplicate to table '{to}'")
            print(replaceColumn)
            if not avoidColumn == None:
                for i in data[0]:
                    for x in avoidColumn:
                        if i == x:
                            data[0][i] = None
            if not replaceColumn == None:
                for i in data[0]:
                    for x in replaceColumn:
                        for y in x:
                            if i == y:
                                data[0][i] = x[y]
            self.insert(to,data[0])

    def addRows(self,table,datas:list):
        for i in datas:
            self.insert(table,i)

    def removeRows(self,table,datas:list):
        for i in datas:
            self.remove(table,i)

    def existTable(self,table):
        if self.driver.lower() in ['mysql','postgresql']:
            query = f"SHOW TABLES LIKE '{table}'"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.__event(query)
            if result:
                self.__event(f"There is table '{table}'")
                return True
            else:
                self.__event(f"Cannot find table '{table}'")
                return False
        else:
            self.__error(f'{self.driver} not supported existTable() function!')

    def createTable(self,table, cols ):
        query = f"CREATE TABLE {table}("
        index = 0
        for col in cols:
            if len(col) >= 3:
                if str(col[2]).lower() == "auto" or str(col[2]).lower() == "key":
                    query += f"{col[0]} {col[1]} AUTO_INCREMENT PRIMARY KEY"
                else:
                    query += f"{col[0]} {col[1]} {col[3]}"
            else:
                query += f"{col[0]} {col[1]}"
            if index < len(cols) - 1:
                query += ","
            index += 1
        query+=");"
        self.__event(query)
        try:
            self.cursor.execute(query)
            self.__event(f"Table '{table}' has been successfully created in database '{self.db}'!")
        except mysql.connector.errors.ProgrammingError as error:
            if error.errno == 1050:
                self.__error(f"Table creation denied. There is already a table named '{table}'!")
            else:
                self.__error(f"{error}")
        return table

class Table:
    def __init__(self,connect,table):
        self.table = table
        self.connect = connect
    def get(self,select="*",sort=None,limit=None,clear=True):
        return self.connect.get(self.table,select,sort,limit,clear)
    def remove(self,select:dict):
        return self.connect.remove(self.table,select)
    def insert(self,data:dict):
        return self.connect.insert(self.table,data)
    def update(self,select:dict,data:dict):
        return self.connect.update(self.table,select,data)
    def duplicate(self,select,to:str,avoidColumn=None,replaceColumn=None):
        return self.connect.duplicate(self.table,select,to,avoidColumn,replaceColumn)
    def addRows(self,datas:list):
        return self.connect.addRows(self.table,datas)
    def removeRows(self,datas:list):
        return self.connect.removeRows(self.table, datas)
def sort(col,value,process='=',valType=str,AndOr='AND'):
    if isinstance(valType, str) and isinstance(value, tuple) and process.upper() == "IN": valType = tuple
    if isinstance(value, str):
        if isinstance(value, list) or isinstance(value, tuple):
            value = list(value)
            index = 0
            for i in value:
                if isinstance(i, str):
                    value[index] = f"'{i}'"
                index+=1
        else:
            value = f"'{value}'"
    if AndOr.upper() == 'AND':
        return (col,value,process)
    if AndOr.upper() == 'OR':
        return [col,value,process]
