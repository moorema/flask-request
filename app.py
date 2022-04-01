import datetime
import os
from datetime import *
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Flask, render_template, request, redirect, flash
from flask_apscheduler import APScheduler
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from huey import SqliteHuey

app = Flask(__name__)


class SchedulerConfig(object):
    # 持久化配置，数据持久化至MongoDB
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobstores.db')}
    # 线程池配置，最大20个线程
    SCHEDULER_EXECUTORS = {'default': ThreadPoolExecutor(20)}
    # 调度开关开启
    SCHEDULER_API_ENABLED = True
    # 设置容错时间为 1小时
    SCHEDULER_JOB_DEFAULTS = {'misfire_grace_time': 3600}
    # 配置时区
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'


app.config.from_object(SchedulerConfig())
scheduler = APScheduler()
scheduler.init_app(app)

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
    isActive = db.Column(db.Boolean(), nullable=False, default=False)


filename_list010 = {
    '11': "static/" + str(date.today()) + ".北京市" + ".csv",
    '43': "static/" + str(date.today()) + ".湖南省" + ".csv",
    '12': "static/" + str(date.today()) + ".天津市" + ".csv",
    '44': "static/" + str(date.today()) + ".广东省" + ".csv",
    '13': "static/" + str(date.today()) + ".河北省" + ".csv",
    '45': "static/" + str(date.today()) + ".广西壮族自治区" + ".csv",
    '14': "static/" + str(date.today()) + ".山西省" + ".csv",
    '46': "static/" + str(date.today()) + ".海南省" + ".csv",
    '15': "static/" + str(date.today()) + ".内蒙古自治区" + ".csv",
    '50': "static/" + str(date.today()) + ".重庆市" + ".csv",
    '21': "static/" + str(date.today()) + ".辽宁省" + ".csv",
    '51': "static/" + str(date.today()) + ".四川省" + ".csv",
    '22': "static/" + str(date.today()) + ".吉林省" + ".csv",
    '52': "static/" + str(date.today()) + ".贵州省" + ".csv",
    '23': "static/" + str(date.today()) + ".黑龙江省" + ".csv",
    '53': "static/" + str(date.today()) + ".云南省" + ".csv",
    '31': "static/" + str(date.today()) + ".上海市" + ".csv",
    '54': "static/" + str(date.today()) + ".西藏自治区" + ".csv",
    '32': "static/" + str(date.today()) + ".江苏省" + ".csv",
    '61': "static/" + str(date.today()) + ".陕西省" + ".csv",
    '33': "static/" + str(date.today()) + ".浙江省" + ".csv",
    '62': "static/" + str(date.today()) + ".甘肃省" + ".csv",
    '34': "static/" + str(date.today()) + ".安徽省" + ".csv",
    '63': "static/" + str(date.today()) + ".青海省" + ".csv",
    '35': "static/" + str(date.today()) + ".福建省" + ".csv",
    '64': "static/" + str(date.today()) + ".宁夏回族自治区" + ".csv",
    '36': "static/" + str(date.today()) + ".江西省" + ".csv",
    '65': "static/" + str(date.today()) + ".新疆维吾尔自治区" + ".csv",
    '37': "static/" + str(date.today()) + ".山东省" + ".csv",
    '71': "static/" + str(date.today()) + ".台湾省" + ".csv",
    '41': "static/" + str(date.today()) + ".河南省" + ".csv",
    '81': "static/" + str(date.today()) + ".香港特别行政区" + ".csv",
    '42': "static/" + str(date.today()) + ".湖北省" + ".csv",
    '82': "static/" + str(date.today()) + ".澳门特别行政区" + ".csv"
}


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
        # 接收前端数据
        email = request.form.get('email')
        num = request.form.get("num")
        checkme = request.form.get("check")
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

        nums = num.split(',')
        # 真实数据文件列表
        zs_filelist = []

        def numtostr(n):  # 把提交来的省份代码转成省份
            cunlist = []
            for cl in n:
                cunlist.append(sfen[cl])
            cunstr = ",".join(cunlist)
            return cunstr

        def is_ok_send_email(zslist):  # 判断附件是否存在并发邮件
            if zslist:
                for flist in zslist:
                    with app.open_resource(flist) as fp:
                        msg.attach(flist, 'text/plain', fp.read())
                send_async_email(msg)
                flash('订阅成功并发送邮件')
                return redirect("/")
            else:
                flash("已记录,没有数据请稍后再试")
                return redirect("/")

        # 邮件内容
        msg = Message(subject="Hello World!",
                      sender="472381899@qq.com",
                      recipients=[email])
        msg.body = "testing"
        # 查询
        old_user = User.query.filter_by(email=email).first()
        # 插入数据
        for snums in nums:
            if snums in sfennum:  # 校验前端输入的代码是否符合规定
                # 判断路径是否真实,存储到zs_filelist中
                if os.path.exists(filename_list010[snums]):
                    zs_filelist.append(filename_list010[snums])
                # 老用户修改
                if old_user:
                    old_user.sshengfen = num
                    old_user.sshengfenstr = numtostr(n=nums)
                    if checkme == 'on':
                        old_user.isActive = True
                    else:
                        old_user.isActive = False
                    db.session.commit()
                    is_ok_send_email(zs_filelist)
                # 新用户
                elif email:
                    # 准备提交数据
                    new_user = User()
                    new_user.email = email
                    new_user.sshengfenstr = numtostr(n=nums)
                    new_user.sshengfen = num
                    # 判断前端传来的数据是否自动订阅
                    if checkme:
                        new_user.isActive = True
                    else:
                        new_user.isActive = False
                    # 提交到数据库中
                    db.session.add(new_user)
                    db.session.commit()
                    # 判断并发邮件
                    is_ok_send_email(zs_filelist)
                else:
                    flash('请正确输入email和省份代码')
                return redirect("/")
            else:
                flash('不能为空,请重新输入')
                return redirect("/")


# huey邮件处理
@huey.task()
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


# @scheduler.task('cron', id='auto_send', day_of_week='0,2', hour='9')
@scheduler.task('interval', id='auto_send', seconds=10)
def job1():
    msg = Message(subject="自动订阅数据请查收",
                  sender="472381899@qq.com",
                  recipients=[])
    msg.body = "附件数据请查收"
    auto_email = User.query.filter_by(isActive=True).all()
    if auto_email:
        for user in auto_email:
            print(f"邮箱: {user.email} 订阅省份: {user.sshengfenstr} ")
            usershengfen_list = str(user.sshengfen)
            for flist in usershengfen_list.split(','):
                if os.path.exists(filename_list010[flist]):
                    print(filename_list010[flist])
                    with app.open_resource(filename_list010[flist]) as fp:
                        msg.attach(filename_list010[flist], 'text/plain', fp.read())
                else:
                    msg.body = "数据爬取中稍后自动重发"
            msg.recipients = [user.email]
            send_async_email(msg)


# 查询字符串删除信息
@app.route("/<int:qsid>")
def delid(qsid):
    del_user = User.query.filter_by(id=qsid).first()
    if del_user is not None:
        db.session.delete(del_user)
        db.session.commit()
    flash("删除成功")
    return redirect("/")


# scheduler.start()

if __name__ == '__main__':
    app.run()
