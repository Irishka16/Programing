#імпортуємо модулі
import pandas as pd
import requests
import glob
import os
from datetime import datetime
echo 0
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

# df = load_data_to_df('./lab2-3/data',NOAAIndex) 

def vhi_by_province(df, province): # вибір всіх даних за областю
    return df[df['area'] == float(province)]

def extreme_by_year(df,year,province): # шукаємо мін і макс для конкретногої обсті та року

    area_data = df
    area_data = df[(df['area'] == province) & ((df['year'] == year))]
    min_vhi = area_data['VHI'].min()
    max_vhi = area_data['VHI'].max()
    return (min_vhi, max_vhi)
# extreme = extreme_by_year(df,2010,1)
# print("Extreme drought in {year}, in province {province}, is {min}, max {max}".format(year=2010,province=1,min=extreme[0],max=extreme[1]))

def extreme_by_areas(df): # знаходимо роки та регіони де була екстремальна посуха

    for i in range(1, 28):
        extreme_drought = df[(df['area'] == i) & (df['VHI'] <= 15)]['year']
        province = NOAAIndex.get(i)
        print(f"Province: {province}")
        print(f"Year: {set(extreme_drought)}")
# extreme_by_areas(df)

class StockExample(server.App):
    title = 'NOAA data vizualization'

    inputs = [ 
        {
            "type": 'dropdown',
            "label": 'Param1',
            "options": [{'label': "VCI", "value": 'VCI'},
                        {'label': "TCI", "value": 'TCI'},
                        {'label': "VHI", "value": 'VHI'}],
            "key": 'param1',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Param2',
            "options": [{'label': "-", "value": '0'},
                        {'label': "VCI", "value": 'VCI'},
                        {'label': "TCI", "value": 'TCI'},
                        {'label': "VHI", "value": 'VHI'}],
            "key": 'param2',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'province',
            "options": [
                {"label": "Вінницька", "value": 1},
                {"label": "Волинська", "value": 2},
                {"label": "Дніпропетровська", "value": 3},
                {"label": "Донецька", "value": 4},
                {"label": "Житомирська", "value": 5},
                {"label": "Закарпатська", "value": 6},
                {"label": "Запорізька", "value": 7},
                {"label": "Івано-Франківська", "value": 8},
                {"label": "Київська", "value": 9},
                {"label": "Кіровоградська", "value": 10},
                {"label": "Луганська", "value": 11},
                {"label": "Львівська", "value": 12},
                {"label": "Миколаївська", "value": 13},
                {"label": "Одеська", "value": 14},
                {"label": "Полтавська", "value": 15},
                {"label": "Рівенська", "value": 16},
                {"label": "Сумська", "value": 17},
                {"label": "Тернопільська", "value": 18},
                {"label": "Харківська", "value": 19},
                {"label": "Херсонська", "value": 20},
                {"label": "Хмельницька", "value": 21},
                {"label": "Черкаська", "value": 22},
                {"label": "Чернівецька", "value": 23},
                {"label": "Чернігівська", "value": 24},
                {"label": "AP Крим", "value": 25},                
                {"label": "Київ", "value": 26},
                {"label": "Севастополь", "value": 27}],
            "value": 26,
            "key": 'province',
            "action_id": "update_data"
        },
        {
            "type": 'text',            
            "label": 'From(Year)',
            "value": '1991',
            "key": 'start_year',
            "action_id": "update_data"
        },
        {
            "type": 'text',            
            "label": 'From(week)',
            "value": '1',
            "key": 'start_week',
            "action_id": "update_data"
        },
        {
            "type": 'text',            
            "label": 'To(Year)',
            "value": datetime.now().strftime('%Y'),
            "key": 'end_year',
            "action_id": "update_data"
        },
        {
            "type": 'text',            
            "label": 'To(Week)',
            "value": 52,
            "key": 'end_week',
            "action_id": "update_data"
        },
         {
            "type": 'text',
            "label": "step",
            "value": "27",
            "key": "step",
            "action_id": "update_data"
        },

    ]
    controls = [
        {
            "type": "button",
            "id": "update_data",
            "label": "Show data"
        }]
    tabs = ["Table", "Plot"]
    outputs = [{"type": "table",
                "id": "data1",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True},
              {"type": "plot",
                "id": "plot",
                "control_id": "update_data",
                "tab": "Plot"}
               ]

    def data1(self, params):
        param1 = params['param1']
        param2 = params['param2']
        province = params['province']

        start_year = params['start_year']
        end_year = params['end_year']
        start_week = params['start_week']
        end_week = params['end_week']

        df = load_data_to_df("./lab2-3/data",NOAAIndex)    #загружаємо
        df = vhi_by_province(df,province)           #
        df = df[(df['year'] >= int(start_year)) & (df['year'] <= int(end_year)) & (df['week'] >= int(start_week)) &
            (df['week'] <= int(end_week))]

        exported_list = ['year',
                         'week',
                          str(param1)]

        if param2 != '0':
            if param2 != param1:
                exported_list.append(str(param2))
        df = df[exported_list]
        return df


    def plot(self, params):
        df = self.data1(params)
        df['year:week'] = df['year'].astype(str) + ':' + df['week'].astype(str)
        plt.figure(figsize=(16, 6))
        img = sns.lineplot(data=df, x='year:week', y=f'{params["param1"]}',
                           label=f'{params["param1"]+str(NOAAIndex[int(params["province"])])}',
                           marker="*", markersize=10,markerfacecolor="r")

        if str(params["param2"]) != "0":
            sns.lineplot(data=df, x='year:week', y=f'{params["param2"]}',
                         label=f'{params["param2"]+str(NOAAIndex[int(params["province"])])}', marker="*", markersize=10, ax=img,markerfacecolor="r")
        plt.xlabel('Year:Week')  
        plt.ylabel('Value') 
        plt.xticks(range(0, len(df), int(params['step'])))
        plt.xticks(rotation=70)
        plt.legend()
        plt.grid()
        return img

app = StockExample()
app.launch(port=9105)
