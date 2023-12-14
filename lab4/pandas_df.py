import numpy as np
import pandas as pd
from datetime import datetime


# import download_data
# download_data.download_dataset()
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time} seconds to execute.")
        return result
    return wrapper

def extract_to_df():
    power = pd.read_csv("./lab4/data/household_power_consumption.txt", delimiter=';') # читаємо датафрейм
    # встановлюємо колонки
    power.columns = ['Date', 'Time', 'Active', 'Reactive', 'Voltage', 'Intensity', 'met1', 'met2', 'met3']
    # поєднуємо дату та час в одну колонку DateTime
    power['DateTime'] = pd.to_datetime(power['Date'] + power['Time'], format="%d/%m/%Y%H:%M:%S")

    # Вбираємо колонки Date, Time, індексуємо DateTime
    power.drop(columns = ['Date', 'Time'], inplace=True)
    power.set_index('DateTime', inplace=True)

    # Вбираємо рядки з N/A даними
    power.dropna(inplace=True)

    # Встановлюємо усім даним тип float32 для уніфікації взаємодії
    for column in power.columns:
        power[column] = power[column].astype('float32')
    return power

power = extract_to_df()

# Task 1
@timing_decorator
def select_power_cons_more_five(df):
    print("Active > 5")
    print(df[df['Active'] > 5])
    return 0

# Task 2
@timing_decorator
def select_volt_more_235(df):
    print("Voltage > 235")
    print(df[df['Voltage'] > 235])
    return 0

# Task 3
@timing_decorator
def met2_more_met3_int_19_20(df):
    print("Intensite >= 19 <= 20, met2 > met3")
    subset = df[(df['Intensity'] >= 19) & (df['Intensity'] <= 20)]
    print(subset[subset['met2'] > subset['met3']])
    return 0

# Task 4
@timing_decorator
def mean_of_50000(df):
    print("Random 5000, mean in each met1")
    subset = df.sample(50000)
    for i in ['met1','met2','met3']:
        mean = subset[i].mean()
        print(f"Mean is {mean} of {i}")
    return 0

# Task 5
@timing_decorator
def night_cons_more_6kw(df):
    print("Task5")

    # Обираємо рядки, де час використання більше 18
    subset = df[df.index.hour >= 18]
    subset = subset.resample('Min').sum()

    # Обираємо рядки, де використання більше 6Kw
    nigth_gt6_subset = subset[subset['Active'] > 6]

    # Розподіляємо на класи
    indexer = lambda row: np.argmax([row['met1'], row['met2'], row['met3']]) + 1
    classes = nigth_gt6_subset.apply(indexer, axis = 1)

    # Допоміжна функція  для вибору групи з розподілу
    def get_split_group(df : pd.DataFrame, n: int, classes):
        return df.loc[classes[classes == n].index]

    # Розподіляємо по групах
    met1_subset = get_split_group(nigth_gt6_subset, 1, classes)
    met2_subset = get_split_group(nigth_gt6_subset, 2, classes)
    met3_subset = get_split_group(nigth_gt6_subset, 3, classes)

    # Допоміжна функція вибору
    def nth(df, n, start, end):
        indexes = np.arange(start, end, n)      
        return df.iloc[indexes]
    # Допоміжна функція задання параметрів для вибору: кожен третій з першої половини
    def third_first_part(df):
        start = 0
        end = np.ceil(len(df) / 2)
        return nth(df, 3, start, end)

    # Допоміжна функція задання параметрів для вибору: кожен четвертий з другої половини
    def fourth_second_part(df):
        start = np.floor(len(df) / 2)
        end = len(df)
        return nth(df, 4, start, end)

    print(third_first_part(met1_subset))
    print(fourth_second_part(met1_subset))


select_power_cons_more_five(power)
select_volt_more_235(power)
met2_more_met3_int_19_20(power)
mean_of_50000(power)
night_cons_more_6kw(power)
