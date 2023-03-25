from flask import Flask, render_template, request, jsonify, url_for, redirect,make_response,Response
from socket import gethostname,gethostbyname
import mysql.connector
from datetime import datetime,date
app=Flask(__name__)

class dataBase:
    __mydb=mysql.connector.connect(host="localhost",user="root",password="1234",database="turf")
    __mycursor = __mydb.cursor()
    
    def ver_id_exists(self,email,mobile,user):
        query="select * from "+user+" where mail= %s && mobile=%s"
        value=(email,mobile,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        if result==[]:
            return False
        else:
            return True

    def ver_login(self,email,pas,user):
        query="select * from "+user+" where mail= %s && pass=%s"
        value=(email,pas,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        if result==[]:
            return "not match"
        else:
            return result

    def ver_turf(self,tname,tgame,taddress,mail,mobile):
        query="select * from "+tname+" where turf_name=%s && related_game=%s && owner_mail= %s && owner_mobile=%s && address=%s"
        value=(tname,tgame,mail,mobile,taddress,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        if result==[]:
            return False
        else:
            return True

    def save_new_owner(self,name,mailid,mobile,upass,gpay,phonepe,paytm,ifsc,account):
        print("save owner")
        query="insert into owner values (%s, %s, %s, %s,%s,%s,%s,%s,%s)"
        value=(name,mailid,mobile,upass,gpay,phonepe,paytm,ifsc,account)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()

    def save_new_user(self,name,mailid,mobile,upass):
        print("save user")
        query="insert into users values (%s, %s, %s, %s)"
        value=(name,mailid,mobile,upass)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()

    def save_turf(self,tname,tgame,mail,mobile,Area,street,city,rate,img):
        #print("save user")
        query="insert into turf_data values (%s, %s, %s, %s,%s,%s,%s,%s,%s)"
        value=(tname,tgame,mail,mobile,Area,street,city,rate,img)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        
    def get_turfs(self,mail,mobile):
        query="select turf_name,related_game,owner_mail,owner_mobile,Area,street,city,rate from turf_data where owner_mail= %s && owner_mobile=%s"
        value=(mail,mobile,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        return result

    def get_requests(self,mail):
        query="select * from requested where owner_mail= %s"
        value=(mail,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        return result

    def get_myOrders(self,mail):
        query="select * from requested where user_mail= %s"
        value=(mail,)
        self.__mycursor.execute(query,value)
        requested=self.__mycursor.fetchall()
        query="select * from booked where user_mail= %s"
        value=(mail,)
        self.__mycursor.execute(query,value)
        booked=self.__mycursor.fetchall()
        query="select * from rejected where user_mail= %s"
        value=(mail,)
        self.__mycursor.execute(query,value)
        rejected=self.__mycursor.fetchall()
        return {"req":requested,"booked":booked,"rej":rejected}
    
    
    def del_turf(self,tname,tgame,omail,omobile,tcity):
        
        #query="delete from turf_data where turf_name=%s AND related_game=%s AND owner_mail=%s AND owner_mobile=%s AND city=%s"
        query="delete from turf_data where turf_name=%s"
        value=(tname,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        print("turf deleted")
        print(self.__mycursor.rowcount, "record(s) deleted")
        return "done"

    def update_turf(self,tname,tgame,omail,omobile,tcity,rate):
        query="update turf_data set rate = '"+rate+"' where turf_name=%s"
        print(query)
        value=(tname,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        return "done"

    def update_owner(self,mail,udata):
        query="update owner set name=%s,mail=%s,mobile=%s,pass=%s,gpay=%s,phonepe=%s,paytm=%s where mail=%s"
        value=(udata[0],udata[1],udata[2],udata[3],udata[4],udata[5],udata[6],mail,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        print("owner updated")

        query="update turf_data set owner_mail=%s,owner_mobile=%s where owner_mail=%s"
        print(query)
        value=(udata[1],udata[2],mail,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        print("turf_data updated")

        query="update booked set owner_mail=%s where owner_mail=%s"
        print(query)
        value=(udata[1],mail,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        print("booked updated")

        query="update requested set owner_mail=%s where owner_mail=%s"
        print(query)
        value=(udata[1],mail,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        print("requested updated")
        
        return "done"
    
    def search_turfs(self,turf):
        query="select * from turf_data where related_game=%s"
        value=(turf,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        return result
    def get_payment_details(self,mail):
        query="select gpay,phonepe,paytm from owner where mail=%s"
        value=(mail,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        return result

    def apply_for_turf(self,tname,game,omail,umail,city,rate,year,month,day,stime,etime,tpname):
        #select * from requested where turf_name="Paul Football club" && related_game="Football" && year="2023" && month="02" && day="26" && stime="10:20" && etime="11:21";
        query="select stime,etime from requested where turf_name=%s && related_game=%s && year=%s && month=%s && day=%s"
        value=(tname,game,year,month,day,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        print("booked time: ",result)
        if result==[]:
            query="insert into requested values (%s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s,%s,%s)"
            value=(tname,game,omail,umail,city,rate,year,month,day,stime,etime,tpname)
            print(query)
            self.__mycursor.execute(query,value)
            self.__mydb.commit()
            return "done"
        else:
            valu=True
            for data in result:
                print(data)
                dstime=datetime.strptime(data[0], '%H:%M').time()
                detime=datetime.strptime(data[1], '%H:%M').time()
                ustime=datetime.strptime(stime, '%H:%M').time()
                uetime=datetime.strptime(etime, '%H:%M').time()
                print(dstime<ustime<detime)
                print(dstime<uetime<detime)
                if(dstime<=ustime<=detime):
                    valu=False
                elif(dstime<=uetime<=detime):
                    valu=False
            print(valu)
            if valu:
                query="insert into requested values (%s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s,%s,%s)"
                value=(tname,game,omail,umail,city,rate,year,month,day,stime,etime,tpname)
                print(query)
                self.__mycursor.execute(query,value)
                self.__mydb.commit()
                return "done"
            return "exists"
    
    def accept(self,tname,game,omail,umail,city,rate,year,month,day,stime,etime):
        query="insert into booked values (%s, %s, %s, %s ,%s ,%s ,%s ,%s ,%s ,%s,%s,%s)"
        today=str(date.today())
        value=(tname,game,omail,umail,city,rate,year,month,day,stime,etime,today)
        print(query)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        ret=self.delete_from_requested(tname,game,omail,umail,city,rate,year,month,day,stime,etime)
        return ret
    
    def reject(self,tname,game,omail,umail,city,rate,year,month,day,stime,etime):
        query="delete from requested where turf_name=%s && related_game=%s && owner_mail=%s && user_mail=%s && city=%s && rate=%s && year=%s && month=%s && day=%s && stime=%s && etime=%s"
        value=(tname,game,omail,umail,city,rate,year,month,day,stime,etime,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        query="insert into rejected values (%s, %s, %s, %s ,%s ,%s)"
        value=(tname,game,umail,year,month,day)
        print(query)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()

        return "done"

    def delete_from_requested(self,tname,game,omail,umail,city,rate,year,month,day,stime,etime):
        query="delete from requested where turf_name=%s && related_game=%s && owner_mail=%s && user_mail=%s && city=%s && rate=%s && year=%s && month=%s && day=%s && stime=%s && etime=%s"
        value=(tname,game,omail,umail,city,rate,year,month,day,stime,etime,)
        self.__mycursor.execute(query,value)
        self.__mydb.commit()
        return "done"

    def getOwnerData(self,mail):
        query="select * from owner where mail=%s"
        value=(mail,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        return result
    
    def get_income_data(self,mail):
        query="select rate,date,turf_name,related_game from booked where owner_mail=%s"
        value=(mail,)
        self.__mycursor.execute(query,value)
        result=self.__mycursor.fetchall()
        return result

        



"""
@app.route("/save_turf/",methods=['POST'])
def save_turf():
    req = request.get_json()
    print(req)
    tname=req["turf_name"]
    tgame,=req["game"]
    tarea=req["area"]
    tstreet=req["street"]
    tcity=req["city"]
    user_data=req['user']
    mail=user_data["mail"]
    mobile=user_data["mobile"]
    taddress=tarea+","+tstreet+","+tcity
    db=dataBase()
    ret=db.ver_turf(tname,tgame,taddress,mail,mobile)
    print(ret)
    return ret
"""

@app.route("/")
def start():
    return render_template("main.html")
#return render_template("User_panel.html")

@app.route("/loginPage")
def loginPage():
    return render_template("Login.html")

@app.route("/searchPage")
def searchPage():
    return render_template("search_panel.html")

@app.route("/bookingPage")
def bookingPage():
    return render_template("bokking_panel.html")


@app.route("/get_booking")
def get_booking():
    return render_template("booking_details.html")

@app.route("/user")
def user():
    return render_template("User_panel.html")

@app.route("/sign_owner")
def sign_owner():
    return render_template("signup.html")

@app.route("/owner_page/")
def owner_page():
    return render_template("owner_dashboard.html")

@app.route("/add_turf_page/")
def add_turf_page():
    return render_template("add_turf_page.html")

@app.route("/bank_details/")
def bank_details():
    return render_template("bank_details.html")

@app.route("/myTurfs/")
def muturfs():
    return render_template("myTurfs.html")

@app.route("/myOrders/")
def orders():
    return render_template("orders.html")

@app.route("/income_show/")
def income_show():
    return render_template("dashboard.html")

@app.route("/myRequests/")
def myRequests():
    return render_template("requests.html")

@app.route("/owner_setting/")
def owner_setting():
    return render_template("owner_settings.html")



@app.route("/signup/",methods=["POST"])
def signup():
    req = request.get_json()
    db=dataBase()
    ret=db.ver_id_exists(req["mail"],req["mobile"],req["user"])
    if(ret==False):
        if(req['user']=="owner"):
            db.save_new_owner(req["name"],req["mail"],req["mobile"],req["pass"])
        else:
            db.save_new_user(req["name"],req["mail"],req["mobile"],req["pass"])
        return req['user']+" saved done"
    return "exists"

@app.route("/signup_owner/",methods=["POST"])
def signup_owner():
    req = request.get_json()
    print(req)
    db=dataBase()
    db.save_new_owner(req["name"],req["email"],req["mobile"],req["pass"],req["gpay"],req["phonepe"],req["paytm"],req["ifsc"],req["account"])
    return "0"

@app.route("/login/",methods=['POST'])
def login():
    req = request.get_json()
    db=dataBase()
    ret=db.ver_login(req["mail"],req["pass"],req["user"])
    return {"ret":ret}

@app.route("/saveTurf",methods=["POST"])
def save_turf():
    req = request.get_json()
    db=dataBase()
    #db.save_turf()
    return "done"

@app.route("/admin/",methods=['POST'])
def admin():
    req = request.get_json()
    #print(req)
    db=dataBase()
    tname=req["turf_name"]
    tgame=req["game"]
    tarea=req["area"]
    tstreet=req["street"]
    tcity=req["city"]
    trate=req["rate"]
    user_data=req["user"]
    #print(user_data)
    user=user_data["name"]
    img=req["img"]
    mobile=user_data["mobile"]
    mail=user_data["mail"]
    #print(())
    ret=db.save_turf(tname,tgame,mail,mobile,tarea,tstreet,tcity,trate,img)
    return "done"

@app.route("/get_turf/",methods=['POST'])
def get_turf():
    req=request.get_json()
    print(req)
    db=dataBase()
    mail=req["mail"]
    mobile=req["mobile"]
    ret={"ret":db.get_turfs(mail,mobile)}
    return ret

@app.route("/get_income_data/",methods=['POST'])
def get_income_data():
    req=request.get_json()
    print(req)
    db=dataBase()
    mail=req["mail"]
    ret={"ret":db.get_income_data(mail)}
    return ret


@app.route("/getOwnerData/",methods=['POST'])
def getOwnerData():
    req=request.get_json()
    print(req)
    db=dataBase()
    mail=req["mail"]
    ret={"ret":db.getOwnerData(mail)}
    return ret


@app.route("/get_requests/",methods=['POST'])
def get_requests():
    req=request.get_json()
    print(req)
    db=dataBase()
    mail=req["mail"]
    ret={"ret":db.get_requests(mail)}
    return ret

@app.route("/get_myOrders/",methods=['POST'])
def get_myOrders():
    req=request.get_json()
    print(req)
    db=dataBase()
    mail=req["user"]
    ret=db.get_myOrders(mail)
    print(ret)
    return ret


@app.route("/get_payment_details/",methods=['POST'])
def get_payment_details():
    req=request.get_json()
    db=dataBase()
    ret=db.get_payment_details(req["mail"])
    return {"ret":ret}

@app.route("/del_turf/",methods=['POST'])
def del_turf():
    req=request.get_json()
    print(req)
    data=req["ret"]
    tname=data[0]
    tgame=data[1]
    omail=data[2]
    omobile=data[3]
    tcity=data[5]
    db=dataBase()
    return db.del_turf(tname,tgame,omail,omobile,tcity)

@app.route("/update_turf/",methods=['POST'])
def update_turf():
    req=request.get_json()
    print(req)
    data=req["ret"]
    tname=data[0]
    tgame=data[1]
    omail=data[2]
    omobile=data[3]
    tcity=data[5]
    rate=req["rate"]
    db=dataBase()
    return db.update_turf(tname,tgame,omail,omobile,tcity,rate)

@app.route("/Search_turf/",methods=['POST'])
def s_turf():
    req=request.get_json()
    print(req)
    db=dataBase()
    ret={"ret":db.search_turfs(req["turf"])}
    return ret

@app.route("/apply_for_turf/",methods=['POST'])
def apply_for_turf():
    req=request.get_json()
    print(req)
    db=dataBase()
    return db.apply_for_turf(req["tname"],req["game"],req["omail"],req["umail"],req["city"],req["rate"],req["year"],req["month"],req["day"],req["stime"],req["etime"],req["tpname"])

@app.route("/book/",methods=['POST'])
def book():
    req=request.get_json()
    print(req)
    db=dataBase()
    ret={"ret":db.book(req["tdata"],req["udata"])}
    return ret

@app.route("/accept/",methods=['POST'])
def accept():
    req=request.get_json()
    print(req)
    db=dataBase()
    ret=db.accept(req["tname"],req["tgame"],req["omail"],req["umail"],req["city"],req["rate"],req["year"],req["month"],req["day"],req["stime"],req["etime"])    
    return ret

@app.route("/reject/",methods=['POST'])
def reject():
    req=request.get_json()
    print(req)
    db=dataBase()
    ret=db.reject(req["tname"],req["tgame"],req["omail"],req["umail"],req["city"],req["rate"],req["year"],req["month"],req["day"],req["stime"],req["etime"])    
    return ret


@app.route("/update_owner/",methods=['POST'])
def update_owner():
    req=request.get_json()
    print(req)
    db=dataBase()
    db.update_owner(req["mail"],req["udata"])
    return db.update_owner(req["mail"],req["udata"])


app.run(host=gethostbyname(gethostname()),port="5000")
