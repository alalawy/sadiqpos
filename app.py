from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
from datetime import datetime
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sadiqpos'
mysql = MySQL(app)

#View & Read
@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/login')
def login():
    return render_template('app/login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('app/dashboard.html')

@app.route('/data/barang')
def databarang():
    def formatrupiah(uang):
        y = str(uang)
        if len(y) <= 3 :
            return 'Rp. ' + y     
        else :
            p = y[-3:]
            q = y[:-3]
            return   formatrupiah(q) + '.' + p

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM barang")
    rv = cur.fetchall()
    cur.close()
    cur2 = mysql.connection.cursor()
    cur2.execute("SELECT * FROM satuan")
    rv2 = cur2.fetchall()
    cur2.close()
    cur3 = mysql.connection.cursor()
    cur3.execute("SELECT * FROM supplier")
    rv3 = cur3.fetchall()
    cur3.close()
    return render_template('app/dataBarang.html', barang=rv, satuan=rv2, supplier=rv3, rupiah=formatrupiah)

@app.route('/data/supplier')
def datasupplier():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM supplier")
    rv = cur.fetchall()
    cur.close()
    return render_template('app/dataSupplier.html', supplier=rv)

#Create Data
@app.route('/add/barang', methods=["POST"])
def addbarang():
    kodeBarang = request.form['kodeBarang'] or ""
    namaBarang = request.form['namaBarang'] or ""
    supplier = request.form['supplier'] or ""
    satuan = request.form['satuan'] or ""
    hargaBeli = re.sub(r'\D', "", request.form['hargaBeli'] or "")
    hargaJual = re.sub(r'\D', "", request.form['hargaJual'] or "")
    stokMinimal = request.form['stokMinimal'] or ""
    timestamp = str(datetime.now())
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO barang (kode,nama,supplier,satuan,harga_beli,harga_jual,stokmin,hpp,kode_toko,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (kodeBarang,namaBarang,supplier,satuan,hargaBeli,hargaJual,stokMinimal,hargaBeli,'1',timestamp,))
    mysql.connection.commit()
    return redirect(url_for('databarang'))


@app.route('/add/supplier', methods=["POST"])
def addsupplier():
    kodeSupplier = request.form['kodeSupplier'] or ""
    namaSupplier = request.form['namaSupplier'] or ""
    alamat = request.form['alamat'] or ""
    kontak = request.form['kontak'] or ""
    keterangan = request.form['keterangan'] or ""
    timestamp = str(datetime.now())
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO supplier (kode,nama,alamat,kontak,keterangan,timestamp) VALUES (%s,%s,%s,%s,%s,%s)", (kodeSupplier,namaSupplier,alamat,kontak,keterangan,timestamp,))
    mysql.connection.commit()
    return redirect(url_for('datasupplier'))

#Delete Data
@app.route('/hapus/barang/<string:id_data>', methods=["GET"])
def hapusbarang(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM barang WHERE id LIKE %s", (id_data,))
    cur.connection.commit()
    return redirect(url_for('databarang'))
    
@app.route('/hapus/supplier/<string:id_data>', methods=["GET"])
def hapussupplier(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM supplier WHERE id LIKE %s", (id_data,))
    cur.connection.commit()
    return redirect(url_for('datasupplier'))

if __name__ == "__main__":
    app.run(debug=True)