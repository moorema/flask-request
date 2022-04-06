# flask_requests

#### 介绍
flask后台管理数据发邮件,爬虫单独部署多线程爬取,flask配合huey异步发邮件,APScheduler管理定时任务,测试使用sqlite部署可替换redis

# 生产环境部署
运行前生成sqlite数据库文件
1. from app import db
2. db.create_all()
3. 使用venv环境管理依赖pip install -r requirements.txt
4. nginx gunicorn多进程运行 supervisor管理守护进程
