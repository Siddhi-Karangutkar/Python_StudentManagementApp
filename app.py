from bottle import * 
from sqlite3 import *


def db_setup():
    con = None
    try:
        con = connect("sms.db")
        sql= "create table if not exists student(rno int primary key, name text, marks1 int,marks2 int, marks3 int)"
        cursor = con.cursor()
        cursor.execute(sql)
        con.commit()
    except Exception as e:
        print("Issue: "+str(e))
        con.rollback()
    finally:
        if con is not None:
            con.close()
    
db_setup()

application = Bottle()

@application.route("/",method=["GET","POST"])
def home():
    con = None
    try:
        con = connect("sms.db")
        sql= "select * from student"
        cursor = con.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return template("home", msg = data)
    except Exception as e:
        print("Issue: "+str(e))
    finally:
        if con is not None:
            con.close()    


@application.route("/create",method=["GET","POST"])
def create():
    if request.method == "POST":
        rno = int(request.forms.get("rno"))
        name = request.forms.get("name")
        marks1 = int(request.forms.get("marks1"))
        marks2 = int(request.forms.get("marks2"))
        marks3 = int(request.forms.get("marks3"))
        con = None
        try:
            con = connect("sms.db")
            sql= "insert into student values(?,?,?,?,?)"
            cursor = con.cursor()
            cursor.execute(sql,(rno,name,marks1,marks2,marks3))
            con.commit()
            msg = "Saved"
            return template("create",msg = msg)
        except Exception as e:
            con.rollback()
            msg = "Issue: "+str(e)
            return template("create", msg=msg)
        finally:
            if con is not None:
                con.close() 
    else:
        return template("create", msg = "")
    

@application.get("/delete/<r:int>")
def delete(r):
    con = None
    try:
        con = connect("sms.db")
        sql= "delete from student where rno = ?"
        cursor = con.cursor()
        cursor.execute(sql,(r, ))
        con.commit()
    except Exception as e:
        con.rollback()
        print("Issue: "+str(e))
    finally:
        if con is not None:
            con.close() 
    redirect("/")


@application.get("/edit/<r:int>",method=["GET","POST"])
def edit(r):
    if request.method == "POST":
        rno = int(request.forms.get("rno"))
        name = request.forms.get("name")
        marks1 = int(request.forms.get("marks1"))
        marks2 = int(request.forms.get("marks2"))
        marks3 = int(request.forms.get("marks3"))
        con = None
        try:
            con = connect("sms.db")
            sql= "update student set name = ?, marks1 = ?, marks2 = ?, marks3 = ? where rno = ?"
            cursor = con.cursor()
            cursor.execute(sql,(name,marks1,marks2,marks3,rno))
            con.commit()
        except Exception as e:
            con.rollback()
        finally:
            if con is not None:
                con.close() 
        redirect("/")
    else:
        con = None
        try:
            con = connect("sms.db")
            sql= "select * from student where rno = ?"
            cursor = con.cursor()
            cursor.execute(sql,(r, ))
            data = cursor.fetchone()
            return template("edit", msg = data)
        except Exception as e:
            print("Issue: "+str(e))
        finally:
            if con is not None:
                con.close()    

run(application,reloader=True, debug=True,port=9000)