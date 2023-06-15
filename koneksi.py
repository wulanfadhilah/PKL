db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="db_gizi"
)

cursor = db.cursor()
sql = "INSERT INTO `tbl_balita`(`Nama`, `JK`, `Alamat`, `Usia`, `Berat`, `Tinggi`, `prediction`) VALUES ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]','[value-6]','[value-7]')"
cursor.execute(sql)

db.commit()
