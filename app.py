from flask import Flask, render_template, request
from nologi import calculate_salary, minimum_income

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def salary_calculator():
    if request.method == 'POST':
        age = int(request.form.get('age'))
        salary = int(request.form.get('salary'))
        disability = int(request.form.get('disability'))

        net_salary = calculate_salary(salary, disability, age, minimum_income)
        tax_amount = salary - net_salary

        return render_template('result.html', salary=salary, net_salary=net_salary, tax_amount=tax_amount)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
