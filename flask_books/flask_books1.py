from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, SubmitField, StringField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:flask2021!@localhost:3306/flask_books'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 两种方式设置secret_key
# app.secret_key = 'TPmi4aLWRbyVq8zu9v82dWYW1'
app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
db = SQLAlchemy(app=app)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    books = db.relationship('Book', backref='author')

    def __repr__(self):
        # return '<Author: %s %s>' % (self.name, self.id)
        return 'Author: %s' % self.name

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    def __repr__(self):
        # return 'Book: %s %s' % (self.name, self.author_id)
        return 'Book: %s %s' % (self.name, self.author_id)

# 创建表单类
class AuthorForm(Form):
    author = StringField('作者', [validators.DataRequired()])
    book = StringField('书籍', [validators.DataRequired()])
    submit = SubmitField('提交')

@app.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('books.html')
    # 创建自定义的表单类
    author_form = AuthorForm(request.form)
    # 1，调用WTF函数实现表单中输入数据的验证
    # if request.method == 'POST' and author_form.validate():
    if request.method == 'POST':
        # 2. 验证通过获取数据
        author_name = author_form.author.data
        book_name = author_form.book.data
        print (author_name)
        print (book_name)


    authors = Author.query.all()
    return render_template('books.html', authors = authors, form = author_form)



if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老惠')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()

    app.run(debug=True)
    # app.run(host="0.0.0.0", port=5000)

