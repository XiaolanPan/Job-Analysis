from flask import Flask,render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    dataList = []
    conn = sqlite3.connect("job.db")
    cur = conn.cursor()
    sql = "select link,jname,cname,job_address,job_year,job_ins,job_num,job_salary,job_allowance,job_kind,job_info from  job_analyse"
    data = cur.execute(sql)
    for item in data:
        dataList.append(item)
    cur.close()
    # conn.close()
    con = sqlite3.connect("job.db")
    cu = con.cursor()
    sql = "select count(1) from job_analyse"
    num = cu.execute(sql)
    for it in num:
        print(type(it))
        value = it[0]
    # print(value)
    cur.close()

    con.close()

    javaSalary = []
    javaNum = []
    uiSalary = []
    uiNum = []

    sql1 = "select job_salary,count(job_salary) from job_analyse where jname like '%java%' and job_salary like '%万/月' group by  job_salary"
    sql2 = "select job_salary,count(job_salary) from job_analyse where jname like '%UI%' and job_salary like '%万/月' group by  job_salary"

    conn = sqlite3.connect("job.db")
    cu = conn.cursor()
    data1 = cu.execute(sql1)

    for ite in data1:
        javaSalary.append(ite[0])
        javaNum.append(ite[1])
    cu.close()
    # con.close()

    con = sqlite3.connect("job.db")
    c = con.cursor()
    data2 = c.execute(sql2)
    for item in data2:
        uiSalary.append(item[0])
        uiNum.append(item[1])
    c.close()
    con.close()

    return render_template('index.html', jobs=dataList, num=value, javaSalary=javaSalary, javaNum=javaNum,
                           uiSalary=uiSalary, uiNum=uiNum)


@app.route('/index')
def home():
    dataList = []
    conn = sqlite3.connect("job.db")
    cur = conn.cursor()
    sql = "select link,jname,cname,job_address,job_year,job_ins,job_num,job_salary,job_allowance,job_kind,job_info from  job_analyse"
    data = cur.execute(sql)
    for item in data:
        dataList.append(item)
    cur.close()
    # conn.close()
    con = sqlite3.connect("job.db")
    cu = con.cursor()
    sql = "select count(1) from job_analyse"
    num = cu.execute(sql)
    for it in num:
        print(type(it))
        value = it[0]
    # print(value)
    cur.close()

    con.close()

    javaSalary = []
    javaNum = []
    uiSalary = []
    uiNum = []

    sql1 = "select job_salary,count(job_salary) from job_analyse where jname like '%java%' and job_salary like '%万/月' group by  job_salary"
    sql2 = "select job_salary,count(job_salary) from job_analyse where jname like '%UI%' and job_salary like '%万/月' group by  job_salary"

    conn = sqlite3.connect("job.db")
    cu = conn.cursor()
    data1 = cu.execute(sql1)

    for ite in data1:
        javaSalary.append(ite[0])
        javaNum.append(ite[1])
    cu.close()
    # con.close()

    con = sqlite3.connect("job.db")
    c = con.cursor()
    data2 = c.execute(sql2)
    for item in data2:
        uiSalary.append(item[0])
        uiNum.append(item[1])
    c.close()
    con.close()

    return render_template('index.html',jobs=dataList,num = value,javaSalary = javaSalary,javaNum = javaNum,uiSalary=uiSalary,uiNum=uiNum)

@app.route('/table')
def table():
    dataList = []
    conn = sqlite3.connect("job.db")
    cur = conn.cursor()
    sql = "select link,jname,cname,job_address,job_year,job_ins,job_num,job_salary,job_allowance,job_kind,job_info from  job_analyse"
    data = cur.execute(sql)
    for item in data:
        dataList.append(item)
    cur.close()
    conn.close()

    return render_template('tables.html',jobs=dataList)


@app.route('/salary')
def salary():
    pySalary = []
    pyNum = []
    javaSalary = []
    javaNum = []
    uiSalary = []
    uiNum = []

    con = sqlite3.connect("job.db")
    cur = con.cursor()
    sql = "select job_salary,count(job_salary) from job_analyse where jname like '%python%' and job_salary like '%万/月' group by  job_salary"
    sql1 = "select job_salary,count(job_salary) from job_analyse where jname like '%java%' and job_salary like '%万/月' group by  job_salary"
    sql2 = "select job_salary,count(job_salary) from job_analyse where jname like '%UI%' and job_salary like '%万/月' group by  job_salary"
    # print(sql1)
    data = cur.execute(sql)
    for item in data:
        pySalary.append(item[0])
        # print(item[0])
        pyNum.append(item[1])
    cur.close()
    con.close()


    conn = sqlite3.connect("job.db")
    cu = conn.cursor()
    data1 = cu.execute(sql1)

    for ite in data1:
        javaSalary.append(ite[0])
        javaNum.append(ite[1])
    cu.close()
    con.close()

    con = sqlite3.connect("job.db")
    c = con.cursor()
    data2 = c.execute(sql2)
    for item in data2:
        uiSalary.append(item[0])
        uiNum.append(item[1])
    c.close()
    con.close()

    return render_template('charts/salary.html',pythonSalary=pySalary,pythonNum=pyNum,javaSalary=javaSalary,javaNum=javaNum,uiSalary=uiSalary,uiNum=uiNum)

@app.route('/address')
def address():
    maps = {}
    name = {}
    value = {}
    dataList = []
    conn = sqlite3.connect("job.db")
    cur = conn.cursor()
    sql = "select job_address,count(*) from job_analyse group by job_address"
    print(".......................")
    data = cur.execute(sql)
    for item in data:
        # maps["value"]=item[1]
        # maps["name"]=item[0]
        dataList.append({"value":item[1],"name":item[0]})

    print("..................")
    print(dataList)
    cur.close()
    conn.close()


    return render_template("charts/address.html",dataList = dataList)

@app.route('/professor')
def jobInfo():
    return render_template("wordCloud/jobInfo.html")
@app.route('/allowance')
def allowanceInfo():
    return render_template("wordCloud/joballowance.html")

if __name__ == '__main__':
    app.run()
