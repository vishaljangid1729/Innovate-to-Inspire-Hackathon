from flask import Flask, render_template, request
import sqlite3 as sql 
from random import randint
import io 
import base64 
import matplotlib.pyplot as plt 
import numpy as np 
import pandas as pd 
import csv
from flask_mail import Mail, Message


conn = sql.connect('database.db')
cur = conn.cursor()
# cur.execute("CREATE TABLE complaint (name text, email text, address text, subject text, complain)e")
# conn.commit()
# cur.execute("DROP TABLE complaint")
# conn.commit()

# cur.execute("CREATE TABLE complaint (name text, email text, address text, subject text, complain text, id text)")
# conn.commit()
# cur.execute("CREATE TABLE power_loss (power number, date text)")
# conn.commit()
# cur.execute("DELETE FROM complaint")
# conn.commit()



app = Flask('__main__')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jangidvishal1999@gmail.com'
app.config['MAIL_PASSWORD'] = 'vishal@1729'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin', methods = ['POST', 'GET'])
def admin():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        if id == 'user' and password == 'user':
            return render_template('admin.html')

    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')
    


@app.route('/complaint', methods = ['POST', 'GET'])
def complaint():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        subject = request.form['subject']
        complain = request.form['subject']
        id = randint(1000000000, 9999999999)

        conn = sql.connect('database.db')
        cur = conn.cursor()
        cur.execute(''' INSERT INTO complaint VALUES (?, ?, ?, ?, ?, ?) ''', [name, email, address, subject, complain, id])
        conn.commit()
        cur.execute("SELECT * FROM complaint")
        print(cur.fetchall())
        msg = Message(subject, sender='jangidvishal1999@gmail.com', recipients=[email])
        head_msg = Message(subject=subject, sender= 'jangidvishal1999@gmail.com', recipients=['nprosofficial@gmail.com'] )
        head_msg.body = complain + "\n" + "Address: " + "\n" + address + "\nEmail: " + email
        mail.send(head_msg)
        msg.body = "Your complaint register successfully. Your complain ID: " + str(id)
        mail.send(msg)

    return render_template('index.html')

@app.route('/raw')
def raw():

    return render_template('rawdata.html')
@app.route('/comp')
def comp():
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM complaint")
    data = cur.fetchall()
    
    
    return render_template('complaints.html', data = data)

@app.route('/current')
def current():
    with open('fault.csv', 'r') as f:
        reader = csv.reader(f)
        fault_data = list(reader)
        # print(fault_data)
        # print(fault_data[5][1][11:13])
        # print(float(fault_data[4][2]))
        fault_count = np.zeros((1, 24), dtype=int)
        for i in range(len(fault_data)):
            if i != 0:
                time = float(fault_data[i][1][11:13])
                time = int(time)
                # print(time)

                if ((time >= 0 and time <= 6) or (time > 19 and time <= 23)) and (float(fault_data[i][2]) < 3):
                    # print(float(fault_data[i][2]))
                    # print(time)
                    fault_count[0][time] = fault_count[0][time] + 1
        # print(fault_count)
        total = 0 
        for i in range(24):
            total = total + fault_count[0][i]
        

    return render_template('currentstats.html', total = total)

@app.route('/timestamp')
def timestamp():
    #power loss vs date
    with open('DailyConsumption1.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        # print(your_list)
        # print(len(your_list))
        # print(your_list[3][1][:10])
        # print(your_list[4][2])
        # print(your_list[4][3])
        # print(float(your_list[4][3]) - float(your_list[4][2]))
        date = []
        power_loss = []

        for i in range(len(your_list) - 1):
            if i != 0:
                date.append(your_list[i][1][:10])
                loss = float(your_list[i][3]) - float(your_list[i][2])
                loss = abs(loss * 100)
                if loss > 100:
                    msg = Message(subject = "High Power Loss", sender='jangidvishal1999@gmail.com', recipients=['nprosofficial@gmail.com'])
                    msg.body = "Power loss is high in SMR03-0219-0252.\n " + "Power loss: " + str(loss/100) + "Kwh."
                    mail.send(msg)
                power_loss.append(loss)
    #fault rate vs time 

    with open('fault.csv', 'r') as f:
        reader = csv.reader(f)
        fault_data = list(reader)
        print(fault_data)
        print(fault_data[5][1][11:13])
        print(float(fault_data[4][2]))
        fault_count = np.zeros((1, 24), dtype= int)
        for i in range(len(fault_data)):
            if i != 0:
                time = float(fault_data[i][1][11:13])
                time = int(time)
                # print(time)
                
                if ((time >=0 and time <= 6) or (time > 19 and time <= 23)) and (float(fault_data[i][2]) < 3):
                    print(float(fault_data[i][2]))
                    print(time)
                    fault_count[0][time] = fault_count[0][time] + 1


        print(fault_count[0])
        x = []
        for i in range(24):
            x.append(i)
        graph_fault = fault(x, fault_count[0])

    with open('Instant.csv', 'r') as f:
        reader = csv.reader(f)
        instant_data = list(reader)
        # print(instant_data)
        x = []
        y = []
        for i in range(30):
            if i != 0:
                time = instant_data[i][1][-8:]
                # print(time)
                loss = float(instant_data[i][3]) - float(instant_data[i][2])
                loss = loss * 100
                # print(loss)
                

                x.append(time)
                y.append(loss)
        graph3 = draw_instant(x, y)
        


    graph_url = draw_graph(date, power_loss) 

    return render_template('timestamp.html', graph1 = graph_url, graph2 = graph_fault, graph3 = graph3)
        



    # return render_template('timestamp.html')
def fault(x, y):
    img = io.BytesIO()
    plt.bar(x, y)
    plt.xlabel('Time')
    plt.ylabel('Number of fault')
    # plt.xticks(xValues)
    plt.xticks(x)
    plt.yticks(y)
    plt.title('Fault rate vs time')
    # plt.tight_layout()
    # plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

def draw_graph(x, y):
    img = io.BytesIO()
    plt.plot(x, y)
    plt.xlabel('Date')
    plt.ylabel('Power Loss')
    plt.xticks(rotation = 90)
    plt.title('Power loss vs Date')
    plt.tight_layout()
    # plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

def draw_instant(x, y):
    img = io.BytesIO()
    plt.plot(x, y)
    plt.xlabel('Time')
    plt.ylabel('Power Loss')
    plt.xticks(rotation=90)
    plt.title('Power loss vs Time')
    plt.tight_layout()
    # plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)



if __name__ == '__main__':
    app.run(debug = True)
