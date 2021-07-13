from flask import Flask, render_template, request, flash, redirect, url_for
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

# 删除用户 --> 网页中删除-->点击需要发送用户的ID给删除用户的路由 --> 路由需要接受参数
@app.route('/delete_author/<author_id>')
def delete_author(author_id):

    # 1. 查询数据库, 是否有该ID的书, 如果有就删除, 没有提示错误
    author = Author.query.get(author_id)

    # 2. 如果有就删除
    if author:
        try:
            db.session.delete(author)
            db.session.commit()
        except Exception as e:
            print (e)
            flash('删除用户出错')
            db.session.rollback()

    else:
        # 3. 没有提示错误
        flash('用户找不到')

    # redirect: 重定向, 需要传入网络/路由地址
    # url_for('index'): 需要传入视图函数名, 返回改视图函数对应的路由地址
    print (url_for('index'))
    return redirect(url_for('index'))




# 删除书籍 --> 网页中删除-->点击需要发送书籍的ID给删除书籍的路由 --> 路由需要接受参数
@app.route('/delete_book/<book_id>')
def delete_book(book_id):

    # 1. 查询数据库, 是否有该ID的书, 如果有就删除, 没有提示错误
    book = Book.query.get(book_id)

    # 2. 如果有就删除
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
        except Exception as e:
            print (e)
            flash('删除书籍出错')
            db.session.rollback()

    else:
        # 3. 没有提示错误
        flash('书籍找不到')

    # redirect: 重定向, 需要传入网络/路由地址
    # url_for('index'): 需要传入视图函数名, 返回改视图函数对应的路由地址
    print (url_for('index'))
    return redirect(url_for('index'))



@app.route('/', methods=['GET', 'POST'])
def index():
    # return render_template('books.html')
    # 创建自定义的表单类
    book_form = AuthorForm(request.form)
    # 1，调用WTF函数实现表单中输入数据的验证
    # if request.method == 'POST' and book_form.validate():
    if request.method == 'POST':
        # 2. 验证通过获取数据
        author_name = book_form.author.data
        book_name = book_form.book.data
        # 3. 判断作者是否存在
        author = Author.query.filter_by(name=author_name).first()
        if author:
            # 4. 作者存在，判断书籍是否存在, 没有重复书籍就添加数据. 如果重复就提示错误
            book = Book.query.filter_by(name=book_name).first()
            if book:
                # 如果重复就提示错误
                flash('已存在同名书籍')
            else:
                # 没有重复书籍就添加数据
                try:
                    new_book = Book(name=book_name, author_id=author.id)
                    db.session.add(new_book)
                    db.session.commit()
                except Exception as e:
                    print (e)
                    flash('书籍添加失败')
                    db.session.rollback()
        else:
            # 5. 如果作者不存在, 添加作者和书籍
            try:
                new_author = Author(name=author_name)
                db.session.add(new_author)
                db.session.commit()

                new_book = Book(name=book_name, author_id=new_author.id)
                db.session.add(new_book)
                db.session.commit()

            except Exception as e:
                print (e)
                flash('添加失败')
                db.session.rollback()
    # else:
    #     # 6. 验证不通过提示错误
    #     if request.method == 'POST':
    #         flash('参数不完整')

    # 将数据库中作者表中的数据查询出来，传给模板
    authors = Author.query.all()
    return render_template('books.html', authors = authors, form = book_form)



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

