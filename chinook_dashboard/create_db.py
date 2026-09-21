import sqlite3
import urllib.request

url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
sql = urllib.request.urlopen(url).read().decode("utf-8-sig")

con = sqlite3.connect("Chinook_Sqlite.sqlite")
con.executescript(sql)
con.commit()
con.close()
print("Fertig!")