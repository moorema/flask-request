from flask import Flask, render_template, request, redirect, flash
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'FSDFSDFSDFSD4564313'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    sshengfen = db.Column(db.String(128), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    # 完整省份代码
    global dss2
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
    if request.method == "GET":

        users = User.query.all()
        if users:
            for user in users:
                ss = user.sshengfen
                ss = ss.split(',')
                dss = []
                for s in ss:
                    dss.append(sfen[s])
                dss2 = ','.join(dss)
            return render_template('index.html', users=users, dss2=dss2)
        else:
            return render_template('index.html')
    else:
        email = request.form.get('email')
        num = request.form.get("num")
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
        nums = num.split(',')
        for snums in nums:
            if snums in sfennum:  # 校验前端输入的代码是否符合规定
                # 增删改查
                old_user = User.query.filter_by(email=email).first()
                if old_user:
                    old_user.sshengfen = num
                    db.session.commit()
                    # return render_template("index.html", ne=ne, nn=nn, qsid=qsid)
                    # return "订阅成功"
                    flash('订阅修改成功')
                    return redirect("/")
                elif email:
                    print(email)
                    print(num)
                    new_user = User()
                    new_user.email = email
                    new_user.sshengfen = num
                    db.session.add(new_user)
                    db.session.commit()
                    # return render_template("index.html", ne=ne, nn=nn, qsid=qsid)
                    flash('订阅成功')
                    return redirect("/")
                else:
                    flash('请正确输入email和省份代码')
                    # print("请正确输入email和省份代码")
                return redirect("/")
            else:
                flash('省份代码不对,请重新输入')
                return redirect("/")
                # return "省份代码不对,请重新输入"


# 个木查询字符串删除信息
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
