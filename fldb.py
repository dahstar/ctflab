import sqlite3
from sqlite3 import Error

class Key:
    def __init__(self, key,content,info, database_path):
     if database_path!="":
      try:
        self.key = key
        self.database_path =database_path 

        if not self.check_key_exists():
          if len(self.get_all__key(key))==0:
           if key!="":
            self.create_key(key,content,info)
        else:
            self.update_key(key,content,info)
      except Error as e:
          print(e)
          
    def check_key_exists(self):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM os WHERE key like '%'+?+'%'", (self.key,))
        exists = cursor.fetchone()

        conn.close()

        if exists is None:
            return False
        else:
            return True
    def get_all__key(self, key):
     a=[]
     if self.database_path!="":
      conn = sqlite3.connect(self.database_path)
      if key!="":
       cur = conn.cursor()
       cur.execute("SELECT * FROM os", () )

       rows = cur.fetchall()

       for row in rows:
        #print("s",row[1])
        if key in row[1]:
         a.append(row[1])
      return a
     return a;
    def find_key_content(self, key):
     conn = sqlite3.connect(self.database_path)
     a=[]
     if key!='':
      cur = conn.cursor()
      cur.execute("SELECT * FROM os WHERE key=?", (key,) )
      rows = cur.fetchall()
      for row in rows:
        #print("s",row[2])
        return row[2]
        if key in row[2]:
         a.append(row[2])
     return a 
    def delete_key(self,key):
        try:
         conn = sqlite3.connect(self.database_path)
         cursor = conn.cursor()

         cursor.execute("DELETE FROM os WHERE key=?", (key,))

         conn.commit()
         conn.close()       
        except Error as e:
         print(e)
    def create_key(self,key,content,info):
      try:
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        print(str(len(self.get_all__key(key))))
        if len(self.get_all__key(key))==0:
         cursor.execute("INSERT INTO os (key,content,info) VALUES (?,?,?)", (key,content,info))

        conn.commit()
        conn.close()       
      except Error as e:
        print(e)
            
    def update_key(self,key,content,info):
      try:
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE os SET content=?,info=? WHERE key=?", (content,info,key))
        conn.commit()
        conn.close()
      except Error as e:
        print(e)

    def get_key(self):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()

        cursor.execute("SELECT key FROM os WHERE key=?", (self.key,))

