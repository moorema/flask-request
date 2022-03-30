from flask import Flask, render_template, request, redirect, flash
import sqlite3
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import os
from huey import SqliteHuey
from datetime import *

app = Flask(__name__)
huey = SqliteHuey(filename='huey.db')
huey.immediate = True  # 即使模式,测试和开发用
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
db = SQLAlchemy(app)
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_USERNAME'] = '472381899@qq.com'
# app.config['MAIL_PASSWORD'] = 'rzdlhwmecuiebiid'
mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    sshengfen = db.Column(db.String(128), nullable=False)
    sshengfenstr = db.Column(db.String(128), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    # 完整省份代码
    if request.method == "GET":
        users = User.query.all()
        if users:
            return render_template('index.html', users=users)
        else:
            return render_template('index.html')
    else:
        email = request.form.get('email')
        num = request.form.get("num")
        # dingyue = request.form['submit']
        # print(dingyue)
        # 省份数字代码
        sfennum = [

            '11',
            '43',
            '12',
            '44',
            '13',
            '45',
            '14',
            '46',
            '15',
            '50',
            '21',
            '51',
            '22',
            '52',
            '23',
            '53',
            '31',
            '54',
            '32',
            '61',
            '33',
            '62',
            '34',
            '63',
            '35',
            '64',
            '36',
            '65',
            '37',
            '71',
            '41',
            '81',
            '42',
            '82'
        ]
        sfen = {

            '11': '北京市',
            '43': '湖南省',
            '12': '天津市',
            '44': '广东省',
            '13': '河北省',
            '45': '广西壮族自治区',
            '14': '山西省',
            '46': '海南省',
            '15': '内蒙古自治区',
            '50': '重庆市',
            '21': '辽宁省',
            '51': '四川省',
            '22': '吉林省',
            '52': '贵州省',
            '23': '黑龙江省',
            '53': '云南省',
            '31': '上海市',
            '54': '西藏自治区',
            '32': '江苏省',
            '61': '陕西省',
            '33': '浙江省',
            '62': '甘肃省',
            '34': '安徽省',
            '63': '青海省',
            '35': '福建省',
            '64': '宁夏回族自治区',
            '36': '江西省',
            '65': '新疆维吾尔自治区',
            '37': '山东省',
            '71': '台湾省',
            '41': '河南省',
            '81': '香港特别行政区',
            '42': '湖北省',
            '82': '澳门特别行政区'
        }

        cunlist = []
        filename_list = []
        nums = num.split(',')
        # 遍历数据存储文件夹,检查是否有数据存在
        old_path = 'static'
        old_filelist = []
        for root, dirs, files in os.walk(old_path):
            for file in files:
                # print(os.path.join(root,file))
                old_filelist.append(os.path.join(root, file))
        print(old_filelist)
        # 发邮件
        msg = Message(subject="Hello World!",
                      sender="472381899@qq.com",
                      recipients=[email])
        msg.body = "testing"
        for snums in nums:
            # filename_a = "static/" + str(date.today()) + "." + sfen[str(snums)] + ".csv"
            # print(filename_a)
            # print(snums)
            if snums in sfennum:  # 校验前端输入的代码是否符合规定

                # 增删改查
                old_user = User.query.filter_by(email=email).first()
                if old_user:
                    for cl in nums:
                        cunlist.append(sfen[cl])
                    cunstr = ",".join(cunlist)

                    for cs in cunstr.split(","):
                        filename_list.append("static/" + str(date.today()) + "." + cs + ".csv")
                    print(filename_list)

                    old_user.sshengfen = num
                    old_user.sshengfenstr = cunstr
                    db.session.commit()
                    # 发邮件 并检查动态生成的文件是否在遍历的真实存储文件夹内
                    if filename_list in old_filelist:
                        for flist in filename_list:
                            with app.open_resource(flist) as fp:
                                msg.attach(flist, 'text/plain', fp.read())
                    else:  # 后期增加功能
                        pass
                    # flash("数据还未抓取到")

                    # 异步发送数据附件
                    # send_async_email(msg)
                    # mail.send(msg)
                    flash('订阅修改成功')
                    return redirect("/")
                elif email:
                    # print(email)
                    # print(num)
                    for cl in nums:
                        cunlist.append(sfen[cl])
                    cunstr = ",".join(cunlist)
                    for cs in cunstr.split(","):
                        filename_list.append("static/" + str(date.today()) + "." + cs + ".csv")
                    print(filename_list)
                    if filename_list in old_filelist:
                        for flist in filename_list:
                            with app.open_resource(flist) as fp:
                                msg.attach(flist, 'text/plain', fp.read())
                    else:  # 后期增加功能
                        pass
                        # flash("数据还未抓取到")
                    new_user = User()
                    new_user.email = email
                    new_user.sshengfenstr = cunstr
                    new_user.sshengfen = num
                    db.session.add(new_user)
                    db.session.commit()
                    # 发邮件
                    # send_async_email(msg)
                    # mail.send(msg)
                    flash('订阅成功')
                    return redirect("/")
                else:
                    flash('请正确输入email和省份代码')
                return redirect("/")
            else:
                flash('不能为空,请重新输入')
                return redirect("/")
        # 发邮件


# huey邮件处理
@huey.task(retries=3)
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


# 管理定时发送邮件
@app.route("/dingshi_email", methods=['GET', 'POST'])
def ds_email():
    pass


# 查询字符串删除信息
@app.route("/<int:qsid>")
def delid(qsid):
    del_user = User.query.filter_by(id=qsid).first()
    if del_user is not None:
        db.session.delete(del_user)
        db.session.commit()
    flash("删除成功")
    return redirect("/")


if __name__ == '__main__':
    app.run()
