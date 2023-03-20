from flask import Flask, render_template, request, flash, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlalchemy
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from taxes import calculate_salary_izv_voz_inv, value_rabotofatela
from flask_bcrypt import Bcrypt
from bcrypt import gensalt, hashpw

podohod_nalog_salary = 1667
sos_nalog_rabotafatel = 0.2359
poslina_riska_rabotofatela = 0.36


Base = sqlalchemy.orm.declarative_base()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TaxCalculation.db'
db = SQLAlchemy(app, model_class=Base)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
app.config['SECRET_KEY'] = 'ALKUZJA1200418' # установить секретный ключ
login_manager.init_app(app) # инициализировать LoginManager
login_manager.login_view = 'login' # указать название вьюхи для логина



# Создаем модель пользователя
class User(UserMixin, db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class TaxCalculation(db.Model):
    __tablename__ = 'TaxCalculation'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    salary = Column(Float)
    num_dependents = Column(Integer)
    pension_type = Column(Integer)
    disability_level = Column(Integer)
    employers_expenses = Column(Float)
    tax_amount = Column(Float)
    salary_netto = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

def add_tax_calculation(user_id, salary, num_dependents, pension_type, disability_level,
                        employers_expenses, tax_amount, salary_netto):
    new_calculation = TaxCalculation(user_id=user_id, salary=salary, num_dependents=num_dependents,
                                     pension_type=pension_type, disability_level=disability_level,
                                     employers_expenses=employers_expenses, tax_amount=tax_amount,
                                     salary_netto=salary_netto)
    db.session.add(new_calculation)
    db.session.commit()




@app.route('/', methods=['GET', 'POST'])
def salary_calculator():
    if request.method == 'POST':
        pension = int(request.form.get('pension'))
        salary = int(request.form.get('salary'))
        disability = int(request.form.get('disability'))
        izv = int(request.form.get('izv'))

        salary_Netto = round(calculate_salary_izv_voz_inv(salary, izv, pension, disability), 2)
        employers_expenses = round(value_rabotofatela(salary, pension), 2)
        tax_amount = round(salary - salary_Netto, 2)

        # Add the tax calculation to the database
        add_tax_calculation(current_user.id, salary, izv, pension, disability,
                            employers_expenses, tax_amount, salary_Netto)
        db.session.commit()

        return render_template('result.html', salary=salary, salary_Netto=salary_Netto, tax_amount=tax_amount,
                               employers_expenses=employers_expenses)
    else:
        return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # Check if the username and email are already registered
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken', 'error')
            return redirect(url_for('register'))
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered', 'error')
            return redirect(url_for('register'))

        # Generate a salt and hash the password
        salt = gensalt()
        hashed_password = hashpw(password.encode('utf-8'), salt)

        # Add the new user to the database
        user = User(username=username, password=hashed_password, email=email)
        db.session.add(user)
        db.session.commit()

        flash('You have successfully registered', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.request_loader
def load_user_from_request(request):
    # Получить данные пользователя из запроса, например, из cookie или заголовка
    user_id = request.cookies.get('user_id')
    if user_id:
        return User.query.get(int(user_id))
    return None


# Создаем страницы для авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('salary_calculator'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/history')
@login_required
def history():
    # Получаем все сохраненные вычисления для текущего пользователя
    calculations = TaxCalculation.query.filter_by(user_id=current_user.id).all()

    # Возвращаем HTML-шаблон, где будут отображаться сохраненные вычисления
    return render_template('history.html', calculations=calculations)

@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
