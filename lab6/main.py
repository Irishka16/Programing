import numpy as np
import matplotlib.pyplot as plt

# Параметри прямої y = kx + b
true_slope = 2  # коефіцієнт нахилу (k)
true_intercept = 5  # зсув по y (b)

# Генеруємо випадкові дані навколо прямої y = kx + b
num_points = 1000
x_data = np.random.rand(num_points) * 10  # генеруємо випадкові значення x
print(len(x_data))
noise = np.random.randn(num_points) * 2  # генеруємо випадковий шум
y_data = true_slope * x_data + true_intercept + noise


def least_squares_fit(x_values, y_values): #описуємо функцію найменших квадратів

    # Знаходимо середні значення
    x_mean = np.mean(x_values)
    y_mean = np.mean(y_values)

    # Знаходимо наші параметри за цією функцією та повертаємо їх
    k_estimate = np.sum((x_values - x_mean) * (y_values - y_mean)) / np.sum((x_values - x_mean)**2)
    b_estimate = y_mean - k_estimate * x_mean

    return k_estimate, b_estimate
#Виводимо наші параметри 
optimal_slope, optimal_intercept = least_squares_fit(x_data, y_data)
print("Optimal estimate for the slope (k): {}".format(optimal_slope))
print("Optimal estimate for the y-intercept (b): {}".format(optimal_intercept))

def compare_estimates(x, y, true_slope, true_intercept):   #Описуємо функцію порівняння методу мен. кв. та polyfit
    # Least squares method
    optimal_slope, optimal_intercept = least_squares_fit(x, y)

    # np.polyfit
    polyfit_params = np.polyfit(x, y, 1)
    polyfit_slope = polyfit_params[0]
    polyfit_intercept = polyfit_params[1]

    # Початкові параметри
    initial_slope = true_slope
    initial_intercept = true_intercept

    # Виводимо результат
    print("True slope and intercept: {}, {}".format(true_slope, true_intercept))
    print("Optimal estimates (Least Squares): {}, {}".format(optimal_slope, optimal_intercept))
    print("Estimates from np.polyfit: {}, {}".format(polyfit_slope, polyfit_intercept))
    print("Initial parameters: {}, {}".format(initial_slope, initial_intercept))


#2 частина
def gradient_descent(x, y, learning_rate, n_iter): #Описуємо функцію градієнтного спуску 
    '''
Функція gradient_descent реалізує метод градієнтного спуску для лінійної регресії. 
Основна ідея полягає в тому, щоб ітеративно оновлювати параметри моделі (коефіцієнт нахилу та зсув) 
    в напрямку, протилежному градієнту функції втрат. 
Таким чином, ми шукаємо локальний мінімум функції втрат.
    '''
    m = len(y)
    slope = 0
    intercept = 0
    cost_history = []
    for _ in range(n_iter):
        y_pred = slope * x + intercept
        error = y_pred - y
        slope -= (learning_rate / m) * np.sum(error * x)
        intercept -= (learning_rate / m) * np.sum(error)
        cost = np.sum(error**2) / (2 * m)
        cost_history.append(cost)

    return slope, intercept, cost_history # В результаті повертає х, у та функцію втрат

def find_optimal_parameters(x, y, learning_rates, n_iters): #описуємо функцію пошуку оптимальних параметрів
    '''
Функція find_optimal_parameters визначає оптимальну швидкість навчання та кількість ітерацій, 
перебираючи різні комбінації параметрів 
i вибираючи ті, які мінімізують значення функції втрат.
    '''
    min_cost = float('inf')
    optimal_learning_rate = None
    optimal_n_iter = None

    for lr in learning_rates:
        for n_iter in n_iters:
            _, _, cost_history = gradient_descent(x, y, lr, n_iter)
            final_cost = cost_history[-1]
            if final_cost < min_cost:
                min_cost = final_cost
                optimal_learning_rate = lr
                optimal_n_iter = n_iter

    return optimal_learning_rate, optimal_n_iter   #В результаті повертають оптимальну швид. навч. та оптимальну ітерацію
# Порівнюємо оцінки 
compare_estimates(x_data, y_data, true_slope, true_intercept)
#Задаємо потенціальні параметри швид. навч. та ітерації та отриуємо оптимальні значенні lr, iter, завдяки функції find_op_par
learning_rates_to_try = [0.01, 0.1, 0.5]
n_iters_to_try = [100, 500, 1000]
# optimal_lr, optimal_n_iter = find_optimal_parameters(x_data, y_data, learning_rates_to_try, n_iters_to_try)
# print(optimal_lr, optimal_n_iter)

# Знаходимо оптимальні параметри (k,b) за функцією градієнтного спуску
optimal_slope_grad, optimal_intercept_grad, _ = gradient_descent(x_data, y_data, 0.001, 1000000)
# Виводимо дані та будуємо лін. регресії
plt.scatter(x_data, y_data, label='Data')
plt.plot(x_data, optimal_slope * x_data + optimal_intercept, color='red', linewidth=3, label='Least Squares Fit')
plt.plot(x_data, np.polyval(np.polyfit(x_data, y_data, 1), x_data), color='green', linewidth=2, label='np.polyfit')
plt.plot(x_data, true_slope * x_data + true_intercept, '--', color='blue', linewidth=1, label='True Line')
plt.plot(x_data, optimal_slope_grad * x_data + optimal_intercept_grad, color='purple', linewidth=1, label='Gradient Descent Fit')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('Comparison of Regression Lines')
plt.show()