import numpy as np
from datetime import time,datetime
from numpy.lib import recfunctions as rfn

# import download_data
# download_data.download_dataset()

# Задаємо стовбці та типи даних
info = {
    'names':('Active','Reactive','Voltage','Intensity','met1', 'met2', 'met3'),
    'formats':('f4','f4','f4','f4','i4','i4','i4')}

# Читаємо дані
power_data = np.genfromtxt("./lab4/data/household_power_consumption.txt", delimiter=';', dtype=info,usecols=range(2,9), skip_header=True, missing_values=['?'])
# Читаємо дані часу
power_datetime = np.loadtxt("./lab4/data/household_power_consumption.txt", delimiter=';', usecols=[0,1], dtype='U', skiprows=1)

# Загружаємо в таблицю даних (data-table)
def to_dt(row):
    date_split = row[0].split('/')[::-1]    
    for i in [1,2]:        
        if len(date_split[i]) < 2:
            date_split[i] = "0" + date_split[i]
    dateISO = "-".join(date_split)
    return np.datetime64(dateISO + "T" + row[1]) 

# співставляємо дані споживання та часові дані
dts = np.apply_along_axis(to_dt, 1, power_datetime)

# Додаємо стовбчик DateTime
power = rfn.append_fields(power_data, 'DateTime', dts, usemask=False)
nan_mask = np.zeros((len(power)), dtype=bool)

# Видаляємо NaN'и
for column in power.dtype.names:
    nan_mask = nan_mask | np.isnan(power[column])

power = power[~nan_mask]
start = datetime.now()
# Task 1
def select_power_cons_more_five(power):
    print("Active > 5")
    print(power[power['Active'] > 5])
    return 0

select_power_cons_more_five(power)
# Task 2
def select_volt_more_235(power):
    print("Voltage > 235")
    print(power[power['Voltage'] > 235])
    return 0
select_volt_more_235(power)

# Task 3
def met2_more_met3_int_19_20(power):
    print("Intensite >= 19 <= 20, met2 > met3")
    print(power[np.logical_and.reduce([ power['Intensity'] >= 19, power['Intensity'] <= 20, power['met2'] > power['met3'] ])])
    return 0
met2_more_met3_int_19_20(power)

# Task 4
def mean_of_50000(power):
    print("Random 50000, mean in met")
    subset = power[np.random.choice(np.arange(0,len(power)), 500000, replace=False)]
    for i in ['met1','met2','met3']:
        mean = subset[i].mean()
        print(f"Mean is {mean} of {i}")
mean_of_50000(power)

# Task 5
def night_cons_more_6kw(power):
    print("Task 5")
    
    def row_time(row):    
        return row[0].time()

    def get_time(arr):        
        dts = arr['DateTime'].astype('object').reshape((len(arr),1))
        return np.apply_along_axis(row_time, 1, dts)
    condition = (get_time(power) >= time(18)) & (power['Active'] > 6)

    power_night = power[condition]
    met1_max_condition = (power_night['met1'] >= power_night['met2']) & (power_night['met1'] >= power_night['met3'])
    met2_max_condition = (power_night['met2'] > power_night['met1']) & (power_night['met2'] >= power_night['met3'])
    met3_max_condition = (power_night['met3'] > power_night['met1']) & (power_night['met3'] > power_night['met2'])

    power_met1 = power_night[met1_max_condition]
    power_met2 = power_night[met2_max_condition]
    power_met3 = power_night[met3_max_condition]
    met1_first, met1_second = np.array_split(power_met1, 2)
    met2_first, met2_second = np.array_split(power_met2, 2)
    met3_first, met3_second = np.array_split(power_met3, 2)
    print(met1_first[::3].shape)
    print(met1_second[::4])

night_cons_more_6kw(power)
end = datetime.now() - start
print(end)