import math

# Функция для сложения двух чисел
def add(x, y):
   return x + y

# Функция для вычитания двух чисел
def subtract(x, y):
   return x - y

# Функция для умножения двух чисел
def multiply(x, y):
   return x * y

# Функция для деления двух чисел
def divide(x, y):
   return round(x / y, 3)

def dis(a, b, c):
    return b**2 - 4*a*c

# Основная функция калькулятора
def calculator():
    print("Выберите операцию.")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. Нахождение корней в примере по типу 'аx^2+bx+c=0' ")
    print("6. Нахождение косинуса угла")
    print("7. Нахождение синуса угла")
    print("8. Нахождение тангенса угла")
    var1 = ""
    answer = ""
    # Запросить у пользователя выбор операции
    choice = input("Введите номер операции (1/2/3/4/5/6/7/8): ")
    if choice > '8' or choice < '1':
        print("Неверный ввод")

    elif choice < '5' and choice > '0':
        # Запросить у пользователя два числа для выполнения операции
        num1 = float(input("Введите первое число: "))
        num2 = float(input("Введите второе число: "))

        # Выбор операции на основе пользовательского выбора
        if choice == '1':
            var1 = "+"
            answer = add(num1, num2)

        elif choice == '2':
            var1 = "-"
            answer = subtract(num1, num2)

        elif choice == '3':
            var1 = "*"
            answer = multiply(num1, num2)

        elif choice == '4':
            var1 = "/"
            answer = divide(num1, num2)

        print(num1, var1, num2, "=", answer)
    elif choice == '5':
        # Запросить у пользователя два числа для выполнения операции
        a = float(input("Введите a: "))
        b = float(input("Введите b: "))
        c = float(input("Введите c: "))
        D = dis(a, b, c)

        if D > 0:
            x1 = (-b + math.sqrt(D)) / (2 * a)
            x2 = (-b - math.sqrt(D)) / (2 * a)
            print("Уравнение имеет два корня: x1 = {0}, x2 = {1}".format(x1, x2))
        elif D == 0:
            x = -b / (2 * a)
            print("Уравнение имеет один корень: x = {0}".format(x))
        else:
            print("Уравнение не имеет действительных корней.")
    elif choice < '9' and choice > '5':
        # Ввод угла в градусах
        angle_degrees = float(input("Введите угол в градусах: "))

        # Перевод угла в радианы
        angle_radians = math.radians(angle_degrees)

        if choice == '6':
            # Вычисление значений тригонометрических функций
            cos_value = math.cos(angle_radians)
            # Вывод результатов
            print("Косинус угла {0} равен {1}".format(angle_degrees, cos_value))
        elif choice == '7':
            sin_value = math.sin(angle_radians)
            print("Косинус угла {0} равен {1}".format(angle_degrees, sin_value))
        elif choice == '8':
            tan_value = math.tan(angle_radians)
            print("Косинус угла {0} равен {1}".format(angle_degrees, tan_value))



# Вызов функции калькулятора
calculator()
