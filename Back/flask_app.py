from flask import Flask
from flask_cors import CORS
import connect_to_mysql_DB as my_db


my_db.fill_the_table()
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    db = my_db.connect_to_mysql()
    # df = pd.read_csv("output.csv",encoding = 'utf-8-sig', engine='python', sep='\t')
    # result = df.to_json(orient="values")
    cur = db.cursor()
    res2= []

    cur.execute("SELECT * FROM attendance_total")
    # print all the first cell of all the rows
    for row in cur.fetchall():
        r=[]
        line_str = str(row[0])+","+str(row[1])+","+str(row[2])+","+str(row[3])+","+str(row[4])
        r.append(line_str)
        # print(row)
        res2.append(r)
    cur.close()
    db.close()
    return res2  #result

@app.route('/read')
def readFromFile():
    my_db.fill_the_table()



app.run(host='0.0.0.0', port=5000)

# if __name__ == "__main__":
#     from waitress import serve
#     serve(app, host="0.0.0.0", port=5000)

