
# Определяем функцию для вычисления зарплаты после уплаты налогов
def calculate_salary(salary, disability_percentage, pension_age, minimum_income):
    # Вычисляем налоговую ставку в зависимости от группы инвалидности
    if disability_percentage == 0:
        tax_rate = 0.20
    elif disability_percentage == 3:
        tax_rate = 0.15
    elif disability_percentage == 2:
        tax_rate = 0.10
    elif disability_percentage == 1:
        tax_rate = 0.05
    else:
        raise ValueError("Группа инвалидности должен быть в диапазоне от 0 до 3")

    # Вычисляем налоговую ставку в зависимости от возраста пенсионера
    if pension_age < 0:
        raise ValueError("Возраст должен быть неотрицательным числом")
    elif pension_age < 18:
        tax_rate += 0.05
    elif pension_age >= 18 and pension_age <= 23:
        tax_rate += 0.02
    elif pension_age >= 24 and pension_age <= 55:
        tax_rate += 0.01
    elif pension_age > 55:
        tax_rate += 0.00

    # Вычисляем налоги
    if salary < minimum_income:
        taxed_salary = salary
    else:
        taxed_salary = salary - (salary * tax_rate)
    # Вычисляем зарплату после уплаты налогов
    return taxed_salary

# Получаем входные данные от пользователя
#salary = float(input("Введите вашу зарплату: "))
#disability_percentage = float(input("Введите группу инвалидности (0(нет инвалидности) - 3): "))
#pension_age = int(input("Введите ваш возраст: "))
minimum_income = 620

#taxed_salary = calculate_salary(salary, disability_percentage, pension_age, minimum_income)

# Выводим результат
#print(f"Зарплата после уплаты налогов: {taxed_salary:.2f} евро")
