from flask import Flask, render_template, request
from taxes import calculate_salary_izv_voz_inv, value_rabotofatela
podohod_nalog_salary = 1667
sos_nalog_rabotafatel = 0.2359
poslina_riska_rabotofatela = 0.36
app = Flask(__name__)


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

        return render_template('result.html', salary=salary, salary_Netto=salary_Netto, tax_amount=tax_amount,
                               employers_expenses=employers_expenses)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
