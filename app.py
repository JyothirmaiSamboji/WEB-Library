from flask import Flask, render_template, request, redirect,session
from lib import run_query
from data import book,student, issue
from flask_session import Session
from functools import wraps

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def admin_login_required(func):
    @wraps(func)
    def inner():
        if session.get('user', 'unknown') == 'unknown':
            return redirect('/admin_login')
        elif session.get('user','unknown') == 'student':
            return redirect('/')
        return func 
    
    return inner

def login_required(func):
    @wraps(func)
    def inner():
        if session.get('user', 'unknown') == 'unknown':
            return redirect('/')
        return func 
    
    return inner

@app.route('/') 
def home():
    
    return render_template('index.html')

@app.route('/student_login', methods = ("GET", "POST"))
def student_login():
    # load add form after inserting or routing
    if request.method=="POST":
        username=request.form.get("uname")
        password=request.form.get("psw")
        status=run_query(f'select count(*) from student where "USER ID"="{username}" and "PASSWORD"="{password}";')[0][0]
        if(status==1):
            session["user"] = "student"
            session["user_id"] = username
            return redirect('/')
    return render_template('student_login.html')

@app.route('/admin_login', methods = ("GET", "POST"))
def admin_login():
    # load add form after inserting or routing
    if request.method=="POST":
        username=request.form.get("uname")
        password=request.form.get("psw")
        status=run_query(f'select count(*) from admin where "USER ID"="{username}" and "PASSWORD"="{password}";')[0][0]
        if(status==1):
            session["user"] = "admin"
            session["user_id"] = username
            return redirect('/')

    return render_template('admin_login.html')

@app.route('/logout')
def logout():
    session['user']=session['user_id']='unknown'
    return redirect('/')

@app.route('/books')
def book_list():
    #to display all the available books
    books=run_query('select * from book;')
    return render_template(
                'booklist.html', 
                books = books,
                fields=book['keys'],
                user_type=session.get('user','unknown')
            )

@app.route('/add_book',methods=['POST','GET'])
@admin_login_required
def add_book():
    #to add a book 
    if request.method=='POST':
        book_id=request.form.get('BOOK CODE')
        book_name=request.form.get('BOOK NAME')
        author_name=request.form.get('AUTHOR NAME')
        edition=request.form.get('EDITION')
        no_of_books=request.form.get('NO OF BOOKS')
        cmd=f"insert into book values({book_id},'{book_name}','{ author_name}',{edition},{no_of_books});"
        
        run_query(cmd)
        return redirect('/books')

    return render_template('addbook.html',fields=book['keys'])

@app.route('/delete_book',methods=['POST','GET'])
@admin_login_required
def delete_book():
    if request.method=="POST":
        book_id=request.form.get('BOOK CODE')
        cmd=f'delete from book where "BOOK CODE"={book_id};'
        #print(cmd)
        run_query(cmd)
        return redirect('/books')

@app.route('/users')
@admin_login_required
def student_list():
    #to display all users
    students=run_query('select * from student;')
    return render_template('userlist.html', students = students,fields=student['keys'])

@app.route('/add_user',methods=['GET','POST'])
@admin_login_required
def add_user():
    #to add user
    if request.method=='POST':
        user_id=request.form.get('USER ID')
        password=request.form.get('PASSWORD')
        full_name=request.form.get('FULL NAME')
        dept=request.form.get('DEPARTMENT')
        mbl=request.form.get('MOBILE NUMBER')
        fine=request.form.get('FINE')
        cmd=f"insert into student values('{user_id}','{password}','{full_name}','{dept}','{mbl}',{fine});"

        run_query(cmd)
        return redirect('/users')
    return render_template('adduser.html',fields=student['keys'])

@app.route('/delete_user',methods=['POST','GET'])
@admin_login_required
def delete_user():

    if request.method=="POST":
        user=request.form.get('USER ID')
        cmd=f'delete from student where "USER ID"="{user}";'
       # print(cmd)
        run_query(cmd)
        return redirect('/users')

@app.route('/issue_book',methods=['GET','POST'])
@admin_login_required
def issue_book():
    # command for listing the books for drop down menu
    cmd=f'select "BOOK CODE" from book where "NO OF BOOKS">0;'
    books=run_query(cmd)
    #print(books)
     # command for listing the users for drop down menu
    cmd=f'select "USER ID" from student;'
    students=run_query(cmd)
    if request.method=="POST":
        user_id=request.form.get('USER ID')
        book_code=request.form.get('BOOK ID')
        issue_date=request.form.get('ISSUE DATE')
        k=run_query(f'select "NO OF BOOKS" from book where "BOOK CODE"={book_code};')[0][0]
        
        #print(k)
        #if k>0:
        cmd=f"insert into issue('USER ID','BOOK ID','ISSUE DATE') values('{user_id}','{book_code}','{issue_date}');"
        #print(cmd)
        run_query(cmd)
        k-=1
        upd=f'update book set "NO OF BOOKS"= {k} where "BOOK CODE"={book_code};'
        print(upd)
        run_query(upd)

        return redirect('/issue_book')
    return render_template('issue.html',books=books,students=students) 

@app.route('/issues')
@admin_login_required
def issue_list():
    #to display all the available books
    issues=run_query('select * from issue;')
    return render_template('issue list.html', issues = issues,fields=issue['keys'])
   
@app.route('/return',methods=['GET','POST'])
@admin_login_required
def return_book():
    if request.method=="POST":
        issue_id=request.form.get('ISSUE ID')
        book_id =run_query(f'select "BOOK ID" from issue where "ISSUE ID"={issue_id}')[0][0]
        
        run_query(f'delete from issue where "ISSUE ID"={issue_id};')
        
        k=run_query(f'select "NO OF BOOKS" from book where "BOOK CODE"={book_id};')[0][0]
        k+=1
        run_query(f'update book set "NO OF BOOKS"={k} where "BOOK CODE"={book_id}')
        
        return redirect('/issues')

if __name__ == "__main__":
    app.run(debug = True)