import mysql.connector

class SQL:
    def __init__(self,host,username,password,db):
        self.connect(host, username, password, db)
    def connect(self,host,username,password,db):
        self.connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=db
        )
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            return True
        return False
    def jsonData(self,table,rows):
        query = f"SELECT DISTINCT column_name FROM information_schema.columns WHERE table_name = '{table}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
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
        query = f"SELECT {select} FROM {table}"
        if not sort == None:
            query += " WHERE"
            for i in sort:
                query+= f" {i[0]} = '{i[1]}'"
        if not limit == None:
            if type(limit) == int or type(limit) == str:
                query += f" LIMIT {limit}"
            else:
                if len(list(list([limit])[0])) > 1:
                    query += f" LIMIT {list(list([limit])[0])[0]} , {list(list([limit])[0])[1]}"
                else:
                    query += f" LIMIT {list(list([limit])[0])[0]}"
        self.cursor.execute(query)
        return self.jsonData(table,self.cursor.fetchall())
