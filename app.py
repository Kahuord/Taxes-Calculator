#Šeit mēs importējam vairākas bibliotēkas, kas tiks izmantotas mūsu programmas darbībā.
from flask import Flask, render_template, request, flash, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlalchemy
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from taxes import calculate_salary_izv_voz_inv, value_rabotofatela
from flask_bcrypt import Bcrypt
from bcrypt import gensalt, hashpw

#Šeit definējam vairākas konstantes, kuras tiks izmantotas programmas darbībā.
podohod_nalog_salary = 1667
sos_nalog_rabotafatel = 0.2359
poslina_riska_rabotofatela = 0.36

#Šeit tiek definēts SQLAlchemy datubāzes modelis.
Base = sqlalchemy.orm.declarative_base()

#Šeit tiek inicializēts Flask lietotne un definēti tās konfigurācijas iestatījumi.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
app.config['SQLALCHEMY_BINDS'] = {'tax_calculation': 'sqlite:///TaxCalculation.db'}
db = SQLAlchemy(app, model_class=Base)
bcrypt = Bcrypt(app)

#Šeit tiek definēts LoginManager, kas ļaus lietotājiem pierakstīties un izrakstīties no sistēmas.
login_manager = LoginManager()
app.config['SECRET_KEY'] = 'ALKUZJA1200418'
login_manager.init_app(app)
login_manager.login_view = 'login'

#Šeit tiek definēts lietotāju modelis, kas tiks izmantots SQLAlchemy datubāzē.
class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

#Šeit tiek definēts nodokļu aprēķina modelis, kas tiks izmantots SQLAlchemy datubāzē.
class TaxCalculation(db.Model):
    __tablename__ = 'TaxCalculation'
    bind_key = 'tax_calculation'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    salary = db.Column(db.Float)
    num_dependents = db.Column(db.Integer)
    pension_type = db.Column(db.Integer)
    disability_level = db.Column(db.Integer)
    employers_expenses = db.Column(db.Float)
    tax_amount = db.Column(db.Float)
    salary_netto = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)

#Šeit tiek izveidota datubāze, ja tā vēl neeksistē.
with app.app_context():
    db.create_all()

#Šeit tiek definēta funkcija, kas pievieno nodokļu aprēķina datus datubāzei.
def add_tax_calculation(user_id, salary, num_dependents, pension_type, disability_level,
                        employers_expenses, tax_amount, salary_netto):

    new_calculation = TaxCalculation(user_id=user_id, salary=salary, num_dependents=num_dependents,
                                     pension_type=pension_type, disability_level=disability_level,
                                     employers_expenses=employers_expenses, tax_amount=tax_amount,
                                     salary_netto=salary_netto)

    db.session.add(new_calculation)
    db.session.commit()


@app.route('/', methods=['GET', 'POST']) #Pievienojiet funkciju 'salary_calculator' šai adreses trasei
def salary_calculator():
    if request.method == 'POST': #Pārbauda, vai pieprasījuma metode ir POST
        salary = int(request.form.get('salary')) #Saņem ienākošo algu no formas un pārveido to par veselu skaitli


        if request.form.get('disability') == None: #Pārbauda, vai nav invaliditātes izvēlēta no formas, ja tā, tad invaliditāte ir 0
            disability = 0
        else: #Ja invaliditāte ir izvēlēta no formas, saņem to
            disability = int(request.form.get('disability'))


        if request.form.get('pension') == None: #Pārbauda, vai nav pensijas izvēlēta no formas, ja tā, tad pensija ir 0
            pension = 0
        else: #Ja pensija ir izvēlēta no formas, saņem to
            pension = int(request.form.get('pension'))


        if request.form.get('izv') == None or request.form.get('izv') == '': #Pārbauda, vai nav sociālās apdrošināšanas izvēlēta no formas, ja tā, tad izv ir 0
            izv = 0
        else: #Ja sociālā apdrošināšana ir izvēlēta no formas, saņem to
            izv = int(request.form.get('izv'))

        salary_Netto = round(calculate_salary_izv_voz_inv(salary, izv, pension, disability), 2) #Aprēķina algu neto pēc nodokļu nomaksas un sociālās apdrošināšanas iemaksas
        employers_expenses = round(value_rabotofatela(salary, pension), 2) #Aprēķina darba devēja izmaksas
        tax_amount = round(salary - salary_Netto, 2) # Aprēķina nodokļu summu

        # Add the tax calculation to the database
        add_tax_calculation(current_user.id, salary, izv, pension, disability,
                            employers_expenses, tax_amount, salary_Netto) #Saglabā ievadīto algu, nodokļus un sociālās iemaksas lietotāja datu bāzē
        db.session.commit() #Saglabā izmaiņas datu bāzē

        return render_template('result.html', salary=salary, salary_Netto=salary_Netto, tax_amount=tax_amount,
                               employers_expenses=employers_expenses) #Atgriež rezultātu lapu ar aprēķinātajām vērtībām
    else: #Ja pieprasījuma metode ir GET, atgriež sākuma lapu
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST']) #Pievienojiet funkciju 'register' šai adreses trasei
def register():
    if request.method == 'POST': #iegūt datus no lietotāja
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # Pārbaudiet, vai lietotājvārds un e-pasts jau ir reģistrēti
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken', 'error')
            return redirect(url_for('register'))
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        # Ģenerējiet sāli un sajauciet paroli
        salt = gensalt()
        hashed_password = hashpw(password.encode('utf-8'), salt)

        # Pievienojiet jauno lietotāju datu bāzei
        user = User(username=username, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()

        flash('You have successfully registered', 'success')
        return redirect(url_for('login'))
    else: #Ja esat veiksmīgi reģistrējies, jūs tiekat pārsūtīts uz pieteikšanās lapu, pretējā gadījumā reģistrējieties vēlreiz
        return render_template('register.html')

@login_manager.user_loader
def load_user(user_id): #Funkcija meklē lietotāju datu bāzē un atgriež lietotāja objektu.
    return User.query.get(int(user_id))

@login_manager.request_loader
def load_user_from_request(request):
    #lai ielādētu lietotāju, pamatojoties uz datiem no pieprasījuma, sīkfailu
    user_id = request.cookies.get('user_id')
    if user_id:
        return User.query.get(int(user_id))
    return None


#Pieteikšanās lapas izveide
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'] #iegūt datus no lietotāja
        password = request.form['password']
        user = User.query.filter_by(email=email).first()#Lietotāju meklēšana tiek veikta pa pastu

        if user and bcrypt.check_password_hash(user.password, password):#ja datu bāzē ir parole un pieteikšanās, tad lietotājs ir autorizēts, pretējā gadījumā kļūda
            login_user(user)
            return redirect(url_for('salary_calculator'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/history')
@login_required #autentifikācijas nepieciešamība
def history():
    #Iegūstiet visus pašreizējā lietotāja saglabātos aprēķinus
    calculations = TaxCalculation.query.filter_by(user_id=current_user.id).all()
    #Atgriežam HTML veidni, kurā tiks parādīti saglabātie aprēķini
    return render_template('history.html', calculations=calculations)

@app.route('/users')
@login_required #autentifikācijas nepieciešamība
def users(): #html fails, kurā redzams visu lietotāju vārds, e-pasts un ID
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/logout')
@login_required #autentifikācijas nepieciešamība
def logout(): #izrakstieties un atgriezieties pieteikšanās lapā
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) #Flask tīmekļa lietojumprogrammas palaišana atkļūdošanas režīmā, ļaujot izsekot kļūdām un atkļūdošanas informāciju
