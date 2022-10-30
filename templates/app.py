from flask import Flask, render_template, jsonify, request,redirect,flash, Markup,url_for, session
from models import *
from datetime import date, timedelta

folder_name="static"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:yourpass@localhot:5432/libraryDB"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = b'hkahs3720/'
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/logout")
def logout():
    return render_template("index.html")    
    
@app.route("/dashboard", methods=["POST"])
def dashboard():
    unam = request.form.get("username")
    pwd = request.form.get("password")
    ulist = usersList.query.filter_by(userName=unam).first()
    session['userName']= unam
    session['userid']= ulist.userID
    session['utype']= ulist.userType
    if ulist.password==pwd:
        return render_template("dashboard.html")
    else:  
        return render_template("index.html")

#-----Subjects     

@app.route("/saveSubject", methods=["POST"])
def saveSubject():
    sName = request.form.get("subName")
    newSub = Subjects(subName=sName)
    db.session.add(newSub)  
    db.session.commit()
    text=sName+' Saved Successfully'
    return render_template("dashboard.html", text=text)  
 
@app.route("/AddSubject")    
def AddSubject():
    SubList=Subjects.query.all()
    tabl='''<div class="form-group">
            <table class="table table-bordered border-success" ><TR style="text-weight:bold; background-color:#ccffcc;">
            <TD>Subject ID</TD>
            <TD>Subject Name</TD></TR>'''  
    for itm in SubList:
        tabl=tabl+"<TR ><TD>"+str(itm.subID)+"</TD><TD>"+itm.subName+"</TD></TR>"
    tabl=tabl+"</Table></DIV>"    
    strg='''<h5 style="text-align:center">Add a Subject</h5><HR>
    <form action="/saveSubject" method="post">
    <div class="row mb-3">
    <label for="subName" class="col-sm-2 col-form-label">Subject Name</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" name="subName">
    </div>
  </div>
<div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Save Subject</button>
</div>

</FORM>
'''+tabl
    text= Markup(strg)
    return render_template("dashboard.html", text=text)   
#---------------Books------------------------
@app.route("/saveBook", methods=["POST"])
def saveBook():
    aNo = request.form.get("accNumber")
    bNam = request.form.get("bookTitle")
    sID = int(request.form.get("subID"))
    aNam=request.form.get("bookAuthor")
    pNam=request.form.get("PublisherName")
    prc = int(request.form.get("price"))
    pag = int(request.form.get("pages"))
    bookMas = bookMaster(accNumber=aNo, bookTitle=bNam,SubID= sID,authorName=aNam, PublisherName=pNam,pages=pag, price=prc, status='A' )
    db.session.add(bookMas)  
    db.session.commit()
    text=bNam+' book Saved Successfully'
    return render_template("dashboard.html", text=text)

@app.route("/Books")    
def Books():
    bList= bookMaster.query.all()
    tabl='''<div div class="col-md-12">
            <table class="table table-bordered border-success" ><TR style="text-weight:bold; background-color:#ccffcc;">
            <TD>Accession Number ID</TD>
            <TD>Book Title</TD>
            <TD>Subject</TD></TR>'''  
    for itm in bList:
        tabl=tabl+"<TR ><TD>"+itm.accNumber+"</TD><TD>"+itm.bookTitle+"</TD><TD>"+itm.subject.subName+"</TD></TR>"
    tabl=tabl+"</TABLE></DIV>"
    sList= Subjects.query.all()
    dd='''    <div class="form-group">
            <select class="form-control" name="subID">'''
    for itm in sList:
        dd=dd+"<option value=\""+str(itm.subID)+"\">"+itm.subName +"</option>"
    dd=dd+  '''</select>
</div>'''  
    strg='''<h5 style="text-align:center">Add a Book</h5><HR>
    <form class="row g-3" action="/saveBook" method="post">
  <div class="col-md-6">
    <label for="accNumber" class="form-label">Accession Number</label>
    <input type="text" class="form-control" Name="accNumber">
  </div>
  <div class="col-md-6">
    <label for="subID" class="form-label">Subject ID</label>
    '''+dd+'''
  </div>
  <div class="col-md-6">
    <label for="bookTitle" class="form-label">Book Title</label>
    <input type="text" class="form-control" Name="bookTitle">
  </div>
  <div class="col-md-6">
    <label for="bookAuthor" class="form-label">Author Name</label>
    <input type="text" class="form-control" Name="bookAuthor">
  </div>
  <div class="col-md-12">
    <label for="PublisherName" class="form-label">Publisher</label>
    <input type="text" class="form-control" Name="PublisherName">
  </div>
  
  <div class="col-md-6">
    <label for="pages" class="form-label">Pages</label>
    <input type="text" class="form-control" Name="pages">
  </div>
  <div class="col-md-6">
    <label for="price" class="form-label">Price</label>
    <input type="text" class="form-control" Name="price">
  </div>

<div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Save Book</button>
</div>
</FORM>'''+tabl
    
    text=Markup(strg)
    return render_template("dashboard.html", text=text)
#----------------------------User details------------------------------------- 
@app.route("/saveUser", methods=["POST"])
def saveUser():
    uNam = request.form.get("userName")
    pwd = request.form.get("password")
    uTyp = request.form.get("userType")
    uList = usersList(userName=uNam, password=pwd,userType=uTyp )
    db.session.add(uList)  
    db.session.commit()
    text=uNam+' record Saved Successfully'
    return render_template("dashboard.html", text=text) 
    
@app.route("/users")    
def users():
    uList= usersList.query.all()
    tabl='''<div class="form-group">
            <table class="table table-bordered border-success" ><TR style="text-weight:bold; background-color:#ccffcc;">
            <TD>User ID</TD>
            <TD>User Name </TD>
            <TD>User Type</TD></TR>'''  
    for itm in uList:
        tabl=tabl+"<TR ><TD>"+str(itm.userID)+"</TD><TD>"+itm.userName+"</TD><TD>"+itm.userType+"</TD></TR>"
    tabl=tabl+"</table></div>"
    strg='''<h5 style="text-align:center">Add a User</h5><HR>
    <form class="row g-3" method="POST" action="/saveUser">
  <div class="col-md-6">
    <label for="userName" class="form-label">User Name</label>
    <input type="text" class="form-control" Name="userName">
  </div>
  <div class="col-md-6">
    <label for="password" class="form-label">password</label>
    <input type="text" class="form-control" Name="password">
  </div>
  <div class="col-md-6">
    <label for="userType" class="form-label">User Type</label>
    <div class="form-group">
            <select class="form-control" name="userType">
                <option value="Admin">Admin</option>
                <option value="Member">Member</option>
                <option value="Guest">Guest</option>
            </select>
    </div>        
  </div>
 <div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Save User</button>
</div>
</FORM>
'''+tabl
    
    text=Markup(strg)
    return render_template("dashboard.html", text=text)    
#--------------------------- Book Issue---------------------------------------------------    

@app.route("/saveIssue", methods=["POST"])
def saveIssue():
    ano = request.form.get("accNumber")
    uid = int(request.form.get("userID")) 
    idt = date.today()
    exdt = date.today()+timedelta(days=14)
    issDet = IssueReturn(AccNumber=ano, userID=uid,IssueDate=idt , ExpRetDate=exdt)
    bTbl=bookMaster.query.filter_by(accNumber=ano).first()
    st='I'
    bTbl.status=st
    db.session.add(issDet)  
    db.session.commit()
    text=ano+' issued to '+str(uid)+' Successfully'
    return render_template("dashboard.html", text=text) 
    
@app.route("/BookIssue")    
def BookIssue():
    bList=bookMaster.query.filter_by(status='A' ).all()
    bdd='''<div class="form-group">
            <select class="form-control" name="accNumber">'''
    for itm in bList:
        bdd=bdd+"<option value=\""+str(itm.accNumber)+"\">"+itm.bookTitle +"</option>"
    bdd=bdd+  '''</select>
</div>'''  

    uList=usersList.query.all()
    udd='''    <div class="form-group">
            <select class="form-control" name="userID">'''
    for itm in uList:
        udd=udd+"<option value=\""+str(itm.userID)+"\">"+str(itm.userID)+"."+itm.userName +"</option>"
    udd=udd+  '''</select>
</div>'''  
    strg='''<h5 style="text-align:center">Issue a Book</h5><HR>
    <form class="row g-3" action="/saveIssue" method="post">
  <div class="col-md-6">
    <label for="accNumber" class="form-label">Book Title</label>
    '''+bdd+'''
  </div>
  <div class="col-md-6">
    <label for="userID" class="form-label">Issue to</label>
    '''+udd+'''
  </div>
  <div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Issue Book</button>
</div>
</FORM>'''
    
    text=Markup(strg)
    return render_template("dashboard.html", text=text)
    
#-------------------------book return
@app.route("/returnBook/<int:tid>")    
def returnBook(tid):
    issDet=IssueReturn.query.filter_by(transID=tid).first()
    acno=issDet.AccNumber
    delta=date.today()-issDet.ExpRetDate
    dy=delta.days
    issDet.ActRetDate=date.today()
    issDet.OverdueDays=dy
    bTbl=bookMaster.query.filter_by(accNumber=acno).first()
    st='A'
    bTbl.status=st
    db.session.commit()
    text='Return Successfully'
    return render_template("dashboard.html", text=text) 
    
@app.route("/BookReturn")    
def BookReturn():
    iList=IssueReturn.query.filter_by(ActRetDate=None).all()
    bdd='''<div class="form-group">
            <select class="form-control" name="transID">'''
    for itm in iList:
        bdd=bdd+"<option value=\""+str(itm.transID)+"\">"+itm.book.bookTitle +"</option>"
    bdd=bdd+  '''</select>
</div>'''  

     
    strg='''<h5 style="text-align:center">Return a Book</h5><HR>
    <form class="row g-3" action="/showIssue" method="post">
  <div class="col-md-6">
    <label for="accNumber" class="form-label">Book Title</label>
    '''+bdd+'''
  </div>
  <div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Show Details</button>
</div>
</FORM>'''
    
    text=Markup(strg)
    return render_template("dashboard.html", text=text)
    
@app.route("/showIssue", methods=["POST"])    
def showIssue():
    tid=request.form.get("transID")
    idet=IssueReturn.query.filter_by(transID=tid).first()
    iList=IssueReturn.query.filter_by(ActRetDate=None)
    bdd='''<div class="form-group">
            <select class="form-control" name="transID">'''
    for itm in iList:
        bdd=bdd+"<option value=\""+str(itm.transID)+"\">"+itm.book.bookTitle +"</option>"
    bdd=bdd+  '''</select>
</div>'''  

     
    strg='''<h5 style="text-align:center">Return a Book</h5><HR>
    <form class="row g-3" action="/showIssue" method="post">
  <div class="col-md-6">
    <label for="accNumber" class="form-label">Book Title</label>
    '''+bdd+'''
  </div>
  <div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Show Details</button>
</div>
</FORM>
<HR>

  <div class="col-md-6">
    <label for="userName" class="form-label">User Name</label>
    <input type="text" class="form-control" value=\"'''+idet.usr.userName+'''\">
  </div>
  <div class="col-md-6">
    <label for="password" class="form-label">Date of Issue</label>
    <input type="text" class="form-control" value=\"'''+idet.book.bookTitle+'''\">
  </div>
  <div class="col-md-6">
    <label for="userType" class="form-label">Issue Date</label>
    <input type="text" class="form-control" value=\"'''+str(idet.IssueDate)+'''\">        
  </div>
  <div class="col-md-6">
    <label for="userType" class="form-label">Expected Date of Return</label>
    <input type="text" class="form-control" value=\"'''+str(idet.ExpRetDate)+'''\">        
  </div>
  
 <div class="col-12">
    <a href="'''+ url_for('returnBook',tid=itm.transID)+'''"><button class="btn  btn-success mb-3">Return</button></a>
</div>
'''
    
    text=Markup(strg)
    return render_template("dashboard.html", text=text)    

#-----------------User Book List-------------------    

@app.route("/BookList")    
def BookList():
    uid=session['userid']
    dy=None
    uBook= IssueReturn.query.filter_by(userID=uid).all()
    tabl='''<table class="table table-bordered border-success" ><TR style="text-weight:bold; background-color:#ccffcc;">
            <TD>Book Title</TD>
            <TD>Date of Issue</TD>
            <TD>Date of Expected Return</TD>
            <TD>Date of Return</TD>
            <TD>Overdue Days</TD>
            <TD>Fine</TD></TR>'''  
    for itm in uBook:
        if itm.OverdueDays==None:
           fine=0
        else:
           fine=itm.OverdueDays*2
        tabl=tabl+"<TR ><td>"+itm.book.bookTitle+"</TD><TD>"+str(itm.IssueDate)+"</TD><TD>"+str(itm.ExpRetDate)+"</TD><TD>"+str(itm.ActRetDate)+"</TD><TD>"+str(itm.OverdueDays)+"</TD><TD>"+str(fine)+"</TD></TR>"
    tabl=tabl+"</table>"
    strg='''<div class="text-center"><h5>Books of the User</h5></div><hr>'''+tabl
    text=Markup(strg)
    return render_template("dashboard.html", text=text)  
    
    
#-----------------Search and display  Books-------------------    


@app.route("/SearchBooks")    
def SearchBooks(): 
    sList= Subjects.query.all()
    dd='''<select name="subID">'''
    for itm in sList:
        dd=dd+"<option value=\""+str(itm.subID)+"\">"+itm.subName +"</option>"
    dd=dd+  '''</select>''' 
    
    strg='''<h5 style="text-align:center">Search Books</h5><HR>
    <form class="row g-3" action="/display" method="post">
    <div class="col-sm-10">
       <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="sType" id="inlineRadio1" value="T" checked>
          <label class="form-check-label" for="inlineRadio1">Search by Title</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="sType" id="inlineRadio2" value="A">
          <label class="form-check-label" for="inlineRadio2">Search by Author</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="sType" id="inlineRadio3" value="S" >
          <label class="form-check-label" for="inlineRadio3">Search by Subject '''+dd+'''</label>
        </div>
    </div>
    <div class="col-sm-10">
    <label for="KeyWord" class="form-label">Enter your search words</label>
    <input type="text" class="form-control" name="KeyWord">
    </div>
    <BR>
    <div class="row align-items-center">
    <div class="col">
      <button class="btn" style="height:40px; background-color:white; width:200px;box-shadow:5px 5px 10px grey; border-radius: 10px 10px 10px 10px;">Search Now!!</button></a>
    </div>
 </div></FORM>'''
    
    text=text=Markup(strg)
    return render_template("dashboard.html", text=text)  


@app.route("/display", methods=["POST"])    
def display():
    styp=request.form.get("sType")
    skw=request.form.get("KeyWord")
    sid=int(request.form.get("subID"))
    look_for = '%{0}%'.format(skw)
    if styp=="T":
        lBook=db.session.query(bookMaster).filter(bookMaster.bookTitle.ilike(look_for))
    if styp=="A":
        lBook=db.session.query(bookMaster).filter(bookMaster.authorName.ilike(look_for))
    if styp=='S':
        lBook=db.session.query(bookMaster).filter(bookMaster.SubID==sid)
    tabl='''<table class="table table-bordered border-success" ><TR style="text-weight:bold; background-color:#ccffcc;">
            <TD>Accession No.</TD>
            <TD>Title</TD>
            <TD>Author</TD>
            <TD>Publisher</TD>
            <TD>Price</TD>
            <TD>Pages</TD></TR>''' 
    for itm in lBook:
        tabl=tabl+"<TR ><td>"+itm.accNumber+"</TD><TD>"+itm.bookTitle+"</TD><TD>"+itm.authorName+"</TD><TD>"+itm.PublisherName+"</TD><TD>"+str(itm.price)+"</TD><TD>"+str(itm.pages)+"</TD></TR>"
    tabl=tabl+"</table>"
    strg='''<div class="text-center"><h5>Searched Books for "'''+skw+'''"</h5></div><hr>'''+tabl            
    text=text=Markup(strg)
    return render_template("dashboard.html", text=text) 