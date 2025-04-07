from flask import Flask,render_template,redirect,url_for,request,flash
from models import db,User,Book
from flask_login import login_user,logout_user,LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iyke'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book_library.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash("Username and password are required")
            return redirect(url_for('register'))

        new_user = User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have been successfully registered, now login!!')
        return redirect(url_for('login'))
    return redirect('register.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for('home'))

@app.route('/add', methods = ['GET','POST'])
def add_book():
    if request.method == 'POST':
        name = request.form['name']
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        if not name or not title or not author or not year:
            flash("All fields are required")
            return redirect(url_for('add_book'))

        new_book = Book(name = name,title = title,author = author,year = year)
        db.session.add(new_book)
        db.session.commit()
        flash('New book has been added!')
        return redirect(url_for('home'))
    return render_template('add_book.html')

@app.route('/edit<int:book_id>',methods=['GET','POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.name = request.form['name']
        book.title = request.form ['title']
        book.author = request.form['title']
        book.year = request.form['year']
        db.session.commit()
        flash('book has been added!')
        return redirect(url_for('home'))
    return render_template('edit_book.html')


@app.route('/delete<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book has been deleted!!')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
    # if not os.path.exists('book_library.db'):
    #          os.remove('book_library.db')
    #         with app.app_context():
    #             db.create_all()
    #     app.run(debug=True)