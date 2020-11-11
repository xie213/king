import requests
from lxml import etree
import pymysql
import time
from flask import Flask,request,redirect,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
import config
app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

class Grade(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    info = db.Column(db.String(64))
    content = db.Column(db.Text)
    # role_id = db.Column(db.Integer, db.ForeignKey(Grade.id))


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        url = "http://www.xbiquge.la/"
        #
        b = Book()

        html = b.get_url(url)

        detail_vote = b.parse(html)
        for key in detail_vote.keys():
            print(key)
            print(detail_vote[key])
            s1 = Grade(name=key, url=detail_vote[key])
            db.session.add(s1)
            db.session.commit()
        gg = Grade.query.all()
        return render_template('index.html',gg=gg)


@app.route('/show/', methods=['GET','POST'])
def show():
    if request.method == 'GET':
        gg = Grade.query.all()
        ss = Student.query.all()
        return render_template('show.html',gg=gg,ss=ss)

# @app.route('/gain/<id>', methods=['GET','POST'])
# def gain(id):
#     if request.method == 'GET':
#         s1 = Grade.query.filter(Grade.id == id).first()
#         return render_template('gain.html',s1=s1)
#
#         # url = "http://www.xbiquge.la/"
#         # #
#         # b = Book()
#         #
#         # html = b.get_url(url)
#         #
#         # detail_vote = b.parse(html)
#         # for key in detail_vote.keys():
#         #     r = b.get_url(detail_vote[key])
#         #     detail_d = b.detail_parse(r)
#         #     for j in detail_d.keys():
#         #         print('5185112515', j)
#         #         # print("**********",detail_d.get(j))
#         #         detail_url = url + detail_d.get(j)
#         #         print('////////////', detail_url)
#         #         content_html = b.get_url(detail_url)
#         #         content_text = b.read_parse(content_html)
#         #         c1 = Student(name=key, info=j, content=content_text)
#         #         db.session.add(c1)
#         #         db.session.commit()


class Book():
    def get_url(self,url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.56'
        }

        r = requests.get(url,headers=headers)
        # r.encoding = "utf-8"
        r.encoding = r.apparent_encoding
        return r.text

    def parse(self,html):
        # 提取、整理
        r = etree.HTML(html)
        # xpath进行匹配

        # 访问这个网址
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
        }
        vote_name = r.xpath("//div[@class = 'novelslist']//li/a/text()")
        # print("小说名:",vote_name)

        vote_url = r.xpath("//div[@class = 'novelslist']//li/a/@href")
        # print("小说url:", vote_url)

        # 变成字典的数据
        d = dict(zip(vote_name, vote_url))
        # print('寻找到的数据',d)

        return d

    def detail_parse(self,html):
        # 每一个小说详细章节的匹配 提取、整理
        r = etree.HTML(html)
        # xpath进行匹配

        vote_list_name = r.xpath("//div[@id='list']//dd/a/text()")
        vote_list_url = r.xpath("//div[@id='list']//dd/a/@href")
        # print("详细章节的名称：",vote_list_name)
        # print("详细章节的url：",vote_list_url)

        detail_d = dict(zip(vote_list_name, vote_list_url))
        return detail_d

    def read_parse(self,html):
        # 每一个小说详细章节的匹配 提取、整理
        r = etree.HTML(html)
        content = r.xpath("//div[@id='content']//text()")
        ht = ''
        for i in content:
            ht += i
        return ht




if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)
    # 要爬取的网址   获取 ....
    url = "http://www.xbiquge.la/"
    #
    b = Book()

    html = b.get_url(url)

    detail_vote = b.parse(html)
    for key in detail_vote.keys():
        print(key)
        print(detail_vote[key])
        s1 = Grade(name=key, url=detail_vote[key])
        db.session.add(s1)
        db.session.commit()

    detail_vote = {"全球武道进化": "http://www.xbiquge.la/44/44578/"}

    for key in detail_vote.keys():
        r = b.get_url(detail_vote[key])
        detail_d = b.detail_parse(r)
        for j in detail_d.keys():
            print('5185112515', j)
            # print("**********",detail_d.get(j))
            detail_url = url + detail_d.get(j)
            print('////////////', detail_url)
            content_html = b.get_url(detail_url)
            content_text = b.read_parse(content_html)
            c1 = Student(name=key, info=j, content=content_text)
            db.session.add(c1)
            db.session.commit()




