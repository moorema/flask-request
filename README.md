# flask_requests

#### 介绍
flask后台管理数据发邮件,爬虫单独部署多线程爬取,flask配合huey异步发邮件,APScheduler管理定时任务,使用sqlite,huey(轻量,不活跃,国内使用较少)根据个人情况可替换redis,celery(新版本windows支持差)
单独输入邮箱提交后发送当天数据,勾选自动订阅按钮再提交发送一次数据,随后按照时间调度进行定时发送,再次提交进行修改,删除会同时删除自动发送.
# 测试运行
运行前生成sqlite数据库文件,加入flask环境变量('SECRET_KEY','MAIL_USERNAME','MAIL_PASSWORD')
flask run 
# 生产环境部署
运行前生成sqlite数据库文件,环境变量
1. from app import db
2. db.create_all()
3. 使用venv环境管理依赖pip install -r requirements.txt
4. nginx gunicorn多进程部署 supervisor管理守护进程
