from flask import Flask, render_template, request, redirect
from lib import run_query
from data import book,student

app = Flask(__name__)

@app.route('/') 
def home():
    # load the home or index file
    return render_template('index.html')

@app.route('/student_login', methods = ("GET", "POST"))
def student_login():
    # load add form after inserting or routing
    return render_template('student_login.html')

@app.route('/admin_login', methods = ("GET", "POST"))
def admin_login():
    # load add form after inserting or routing
    return render_template('admin_login.html')






@app.route('/books')
def book_list():
    #to display all the available books
    books=run_query('select * from book;')
    return render_template('booklist.html', books = books,fields=book['keys'])

@app.route('/add_book',methods=['POST','GET'])
def add_book():
    #to add a book 
    if request.method=='POST':
        book_id=request.form.get('BOOK CODE')
        book_name=request.form.get('BOOK NAME')
        author_name=request.form.get('AUTHOR_NAME')
        edition=request.form.get('EDITION')
        no_of_books=request.form.get('NO OF BOOKS')
        cmd=f"insert into book values({book_id},'{book_name}','{ author_name}',{edition},{no_of_books});"
        
        run_query(cmd)
        return redirect('/books')

    return render_template('addbook.html',fields=book['keys'])

@app.route('/delete_book',methods=['POST','GET'])
def delete_book():
    if request.method=="POST":
        book_id=request.form.get('BOOK CODE')
        cmd=f'delete from book where "BOOK CODE"={book_id};'
        #print(cmd)
        run_query(cmd)
        return redirect('/books')



@app.route('/users')
def student_list():
    #to display all users
    students=run_query('select * from student;')
    return render_template('booklist.html', students = students,fields=student['keys'])



@app.route('/add_user',methods=['GET','POST'])
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
def delete_user():
    if request.method=="POST":
        user=request.form.get('USERNAME')
        cmd=f'delete from book where "USERNAME"={user};'
        #print(cmd)
        run_query(cmd)
        return redirect('/users')




if __name__ == "__main__":
    app.run(debug = True)