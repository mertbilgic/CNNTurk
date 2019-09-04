from flask import Flask,render_template,url_for,escape,request,redirect,flash,session,logging
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from sqlalchemy import Table, Column, Integer, String, MetaData,desc, ForeignKey
from sqlalchemy.orm import relationship
from wtforms import Form, BooleanField, StringField, PasswordField, validators,IntegerField
from flask_ckeditor import CKEditor
from slugify import slugify, Slugify, UniqueSlugify
import datetime
from datetime import date

app = Flask(__name__)
#secret_keyi client tarafında oturumları güvenli tutmak için kullanıyoruz
app.secret_key="cnnturk"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@127.0.0.1/Cnn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ckeditor = CKEditor()
ckeditor.init_app(app)







#Kullanıcı login olmadığında erişmemesi gerek yerleri engelliyoruz
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "login" in session:
            return f(*args, **kwargs)
        else:
            flash("Lütfen Kullanıcı girişi yapınız","danger")
            return redirect(url_for('login'))
    return decorated_function

#WTforms sayesinde input kontrollerinin yapıldığı ver ekranda olmasını istediğimiz input anlanlarını belirlediğim kısım
class RegistrationForm(Form):
    try:
        #id = StringField('id', [validators.Length(min=4, max=25)])
        name = StringField('Name', [validators.Length(min=4, max=25)])
        username = StringField('Username', [validators.Length(min=4, max=25)])
        email = StringField('Email Address', [validators.Length(min=6, max=35)])
        password = PasswordField('New Password', [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords must match')
        ])
        confirm = PasswordField('Repeat Password')
    except:
        print("Kayıt formunda problem var")

class UpdateForm(Form):
    try:
        id = StringField("id")
        title = StringField("Title")
        title2 =StringField("Title2")
        text = StringField("Text")
        hrimage=StringField("Hrimage")
        sqimage=StringField("Sqimage")
        category=StringField("Category")
    except:
        print("Update formunda problem var")
class DeleteForm(Form):
    try:
        id = StringField("id")
        title = StringField("Title")
    except:
        print("Delete formunda problem var")

class NewsAddForm(Form):
    try:
        title = StringField("Title",[validators.Length(min=4)])
        title2 =StringField("Title2",[validators.Length(min=4)])
        text = StringField("Text")
        hrimage=StringField("Hrimage")
        sqimage=StringField("Sqimage")
        category_id=IntegerField("Category")
        
    except:
        print("Haber formunda problem var")

 
class LoginForm(Form):
    username = StringField('username', [validators.Length(min=4, max=25)])
    password = PasswordField('password', [
        validators.DataRequired(message="Lütfen parolanızı giriniz!!!")
    ])
#Databasedeki şemaların görünümleri

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=True)
    title2 = db.Column(db.String(200), unique=False, nullable=True)
    text = db.Column(db.String(200), unique=False, nullable=True)
    hrimage = db.Column(db.String(200), unique=False, nullable=True)
    sqimage = db.Column(db.String(200), unique=False, nullable=True)
    addtime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updattime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=True)
    news = db.relationship('News', backref='category', lazy=True)
    

class users(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(80),unique=True ,nullable=False)
    email =db.Column(db.String(120),unique=True,nullable=False)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password =db.Column(db.String(80),unique=True,nullable=False)

#Anasayfanın yüklenmesi için gerekli sorguların return edildiği kısım
@app.route('/')
def cnn():
    topMansetNews = News.query.order_by(News.id.desc()).limit(7).all()
    tripleNews = News.query.order_by(News.id.desc()).limit(3).offset(7).all()
    midMansetNews = News.query.order_by(News.id.desc()).limit(7).offset(11).all()
    titleMansetNews = News.query.order_by(News.id.desc()).limit(4).offset(18).all()
    oneNews = News.query.order_by(News.id.desc()).limit(1).offset(22).all()
    tripleNews2 = News.query.order_by(News.id.desc()).limit(3).offset(23).all()
    lastMansetNews = News.query.order_by(News.id.desc()).limit(5).offset(26).all()
    lastNews = News.query.order_by(News.id.desc()).limit(1).offset(31).all()
    return render_template("mainpage.html", topMansetNews=topMansetNews,tripleNews=tripleNews,midMansetNews=midMansetNews,
    titleMansetNews=titleMansetNews,oneNews=oneNews,tripleNews2=tripleNews2,lastMansetNews=lastMansetNews,lastNews=lastNews,
    slugify=slugify)

#Kullanıcının login işleminin gerçekleştirildiği kısım
@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm(request.form)

    if request.method =="POST" and form.validate():

        username=form.username.data
        password=form.password.data
        
        result=users.query.filter_by(username=username).all()

        for record in result:
            
            if record.password==password:
                flash("Giriş başarılı","success")

                session["login"]=True
                session["username"]=username
                return redirect(url_for("cnn"))
            else:
                flash("Kullanıcı veya parola yanlış","danger")
                return redirect(url_for("login"))
        
    return render_template("loginpage.html",form=form)

#Kayıt sayfası
@app.route("/register",methods=["GET","POST"])
#@login_required
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        user =users(name=form.name.data,email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
         
    return render_template('register.html', form=form)

#Kullanıcı paneli   
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

#Haber ekleme sayfası
@app.route("/newsadd",methods=["GET","POST"])
@login_required
def newsAdd():
    form = NewsAddForm(request.form)

    if request.method =="POST" and form.validate():
        news = News(title=form.title.data,title2=form.title2.data,text=form.text.data,hrimage=form.hrimage.data,sqimage=form.sqimage.data,
        category_id=form.category_id.data)
        db.session.add(news)
        db.session.commit()

        return redirect(url_for("dashboard"))
    
    return render_template("newsadd.html",form=form)

#Kayıtlı verilerin güncelendiği kısım
@app.route("/updatenews",methods=["GET","POST"])
@login_required
def uppdatenews():
    form = UpdateForm(request.form)
    
    if request.method =="POST" and form.validate():
        
        allNews = News.query.filter_by(id=form.id.data).all()
        #Koşullar formların boş kısımlarının kayıtlı sütünlarında veri kaybını engellemek için kullanıldı
        if(form.title.data!=""):
            allNews[0].title=form.title.data

        if(form.title2.data!=""):
            allNews[0].title2=form.title2.data

        if(form.text.data!=""):
            allNews[0].text=form.text.data

        if(form.hrimage.data!=""):
            allNews[0].hrimage=form.hrimage.data

        if(form.sqimage.data!=""):
            allNews[0].sqimage=form.sqimage.data
            
        if(form.category.data!=""):
            allNews[0].category=form.category.data

        allNews[0].updattime=datetime.datetime.now()
        db.session.commit()
        return redirect(url_for("dashboard"))
        
    
    return render_template("updatenews.html",form=form)

#Kayıtlı verinlerin silindiği kısım
@app.route("/deletenews", methods=['GET', 'POST'])
@login_required
def deletnews():
    form = DeleteForm(request.form)
    if request.method=="POST":
        if form.id.data !="" and form.title.data!="":
            News.query.filter_by(id=form.id.data,title=form.title.data).delete()
        elif form.id.data !="":
            News.query.filter_by(id=form.id.data).delete()
        else:
            News.query.filter_by(title=form.title.data).delete()
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("deletenews.html",form=form)
        

#Sistemdeki kayıtlı haberlerin listelendiği kısım
@app.route("/registerednews",methods=["GET","POST"])
@login_required
def registerednews():
    
    allNews = News.query.order_by(News.id.desc()).all()

    return render_template("registerednews.html",allNews=allNews)

@app.route("/newscategory")
@app.route("/<categoryname>")
def newscategory(categoryname="turkiye"):
    
    #Ana sayfa yüklenirken category.id ye erişirken nonetype hatası verdiği için bu hatadan kaçış için bu koşulu kulladım
    category= Category.query.filter_by(name=categoryname).first()
    if category:
        categoryyNews = News.query.filter_by(category_id=category.id).order_by(News.id.desc()).limit(7).all()
        return render_template("newscategory.html",categoryyNews=categoryyNews,slugify=slugify)
    else:
        categoryyNews = News.query.order_by(News.id.desc()).limit(7).all()
        return render_template("newscategory.html",categoryyNews=categoryyNews,slugify=slugify)

#haberler tıklandığında geçişin sağlandığı kısım
@app.route("/haberdetay/")
@app.route('/<category>/<name>-<int:post_id>')
def newsDetail(category="haberdetay",name="deneme",post_id=47):
    detail = News.query.filter_by(id=post_id)    
    if (name==(slugify(detail[0].title).lower())) and (post_id==detail[0].id):
        return render_template('haberdetay.html',catergory=category,name=name,post_id=post_id,detail=detail)
    else:
        return "404"
        
#debug=true modunda hata çalıştırıldığında hata ile karşılaşabilirsiniz
if __name__=="__main__":
    app.run()







