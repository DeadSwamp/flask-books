# 导入Flask类
from flask import Flask
import config

from flask_sqlalchemy import SQLAlchemy
# 实例化，可视为固定格式
app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

class Role(db.Model):
    # 定义表名
    __tablename__ = 'roles'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    user = db.relationship('User', backref='role')

    #repr()方法显示一个可读字符串
    def __repr__(self):
        return '<Role: %s %s>' % (self.name, self.id)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(32),unique=True)
    password = db.Column(db.String(32))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User: %s %s %s %s>' % (self.name, self.id, self.email, self.password)


# route()方法用于设定路由；类似spring路由配置
@app.route('/')
def hello_world():
    return 'Hello, it!'



if __name__ == '__main__':
    # 删除表
    db.drop_all()
    # 创建表
    db.create_all()

    ro1 = Role(name='admin')
    db.session.add(ro1)
    db.session.commit()
    # 再次插入一条数据
    ro2 = Role(name='user')
    db.session.add(ro2)
    db.session.commit()
    us1 = User(name='zhao', email='zhao@163.com', password='zhao123', role_id=ro1.id)
    us2 = User(name='qian', email='qian@189.com', password='qian123', role_id=ro2.id)
    us3 = User(name='sun', email='sun@126.com', password='sun123', role_id=ro2.id)
    us4 = User(name='li', email='li@163.com', password='li123', role_id=ro1.id)
    us5 = User(name='zhou', email='zhou@itheima.com', password='zhou123', role_id=ro2.id)
    us6 = User(name='wu', email='wu@gmail.com', password='wu123', role_id=ro2.id)
    us7 = User(name='zheng', email='zheng@gmail.com', password='zheng123', role_id=ro1.id)
    us8 = User(name='wang', email='wang@itheima.com', password='wang123', role_id=ro1.id)
    db.session.add_all([us1, us2, us3, us4, us5, us6, us7, us8])
    db.session.commit()


    # app.run(host, port, debug, options)
    # 默认值：host="127.0.0.1", port=5000, debug=False
    app.run(host="0.0.0.0", port=5000)
