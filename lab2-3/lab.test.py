#імпортуємо модулі
import pandas as pd
import requests
import glob
import os
from datetime import datetime

from spyre import server
import matplotlib.pyplot as plt
import seaborn as sns

NOAAIndex = { # індекси для кожної області
        1:24,
        2:25,
        3:5,
        4:6,
        5:27,
        6:23,
        7:26,
        8:7,
        9:11,
        10:13,
        11:14,
        12:15,
        13:16,
        14:17,
        15:18,
        16:19,
        17:21,
        18:22,
        19:8,
        20:9,
        21:10,
        22:1,
        23:3,
        24:2,
        25:4, 
        26:12, #Київ
        27:20 #Севастополь
}

def clear_dir(directory): # проста функція для очищення даних
    for file in glob.glob(os.path.join(directory, "obl*.csv")):
        os.remove(file) # видаляємо всі попередні файли
    
def download_data(directory, index, minYear=1991, maxYear=2023):     #завантаження даних
   
    url='https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2023&type=Mean'.format(index)
    response = requests.get(url) #завантажити веб сторінку
    text = response.content.decode() 
    clean_text = text.replace("b'", "")  # очищуємо дані
    clean_text = clean_text.replace("'", "")
    clean_text = clean_text.replace(",  from 1982 to 2023,", "  from 1982 to 2023")
    clean_text = clean_text.replace(",\n", "\n")
    clean_text = clean_text.replace("</pre></tt>", "")
    clean_text = clean_text.replace("<tt><pre>1982", "1982")
    clean_text = clean_text.replace("<br>", "")
    clean_text = clean_text.replace("weeklyfor", "weekly for")
    clean_text = clean_text.replace(", SMN", ",SMN")
    clean_text = clean_text.replace(", VHI", ",VHI")
    clean_text = clean_text.encode()
    now = datetime.now()
    with open(directory+'/obl_{}_{}.csv'.  #створюємо таблиці за шаблоном і записуємо у файл
              format(index,datetime.now().strftime("%d-%m-%Y_%H-%M")) , 'wb') as file: 
        file.write(clean_text)
    
# clear_dir("./lab2-3/data") # очистка папки зі старими даними, дп функ

# for i in range(1,28): # запуск завантаження для кожної області
#     download_data("./lab2-3/data", i)
#     print("Province {} is downloaded".format(i))

def load_data_to_df(directory,NOAAIndex):  # завантажуємо дані у датафрейм
    data = pd.DataFrame(columns=['SMN', 'SMT', 'VCI', 'TCI', 'VHI']) # створюємо пустий датафрейм


    for file in glob.glob(os.path.join(directory,"obl_*.csv")):  # Для кожного файлу зчитуємо дані та завантж до загального датафрейму
        df = pd.read_csv(file, index_col=None, header=1)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        province_id = int(file.split('_')[1])
        df.insert(0, 'area', province_id)
        data = pd.concat([data, df], ignore_index=True)

    data["area"].replace(NOAAIndex, inplace=True)   # алфавітний порядок
    data.sort_values(by=['area', 'year', 'week'], ascending=True, inplace=True)
    return data

df = load_data_to_df('./lab2-3/data',NOAAIndex) 

def vhi_by_province(df, province): # вибір всіх даних за областю
    return df[df['area'] == float(province)]

def extreme_by_year(df,year,province): # шукаємо мін і макс для конкретногої обсті та року

    min_vhi = df['VHI'].min()
    max_vhi = df['VHI'].max()
    area_data = df[(df['VHI'] == min_vhi)|(df['VHI'] == max_vhi)]
    return area_data[['VHI','area','week','year']]
extreme = extreme_by_year(df,2010,1)
print(extreme)
# print("Extreme drought in {year}, in province {province}, is {min}, max {max}".format(year=2010,province=1,min=extreme[0],max=extreme[1]))

def extreme_by_areas(df): # знаходимо роки та регіони де була екстремальна посуха

    for i in range(1, 28):
        extreme_drought = df[(df['area'] == i) & (df['VHI'] <= 15)]['year']
        province = NOAAIndex.get(i)
        print(f"Province: {province}")
        print(f"Year: {set(extreme_drought)}")
# extreme_by_areas(df)
