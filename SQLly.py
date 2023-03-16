import mysql.connector
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
    def __init__(self,host,username,password,db):
        self.connect(host, username, password, db)
    def connect(self,host,username,password,db):
        try:
            self.connection = mysql.connector.connect(host=host,user=username,password=password,database=db)
        except mysql.connector.errors.ProgrammingError as e:
            self.__error(f"Unknown database '{db}'")
            return False
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            self.__event(f"Connection to '{db}' is successful.")
            return True
        else:
            self.__error('Could not connect to database!')
        return False
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

class Table:
    def __init__(self,connect,table):
        self.table = table
        self.connect = connect
    def get(self,select="*",sort=None,limit=None,clear=True):
        return self.connect.get(self.table,select,sort,limit,clear)

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

