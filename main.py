# Импортирование модулей
from selenium import webdriver as wb
from time import sleep
from bs4 import BeautifulSoup as bs
from os import system
from typing import Any
import sqlite3, requests, sys
from os.path import exists as ex

class BOT:
    # Блок с переменными
    URL = 'https://youla.ru/cities'
    baseURL = 'https://youla.ru'
    BASE = "./phantomjs.exe"
    browser = ''
    kolwvo = 0; point=0
    countPage = 0

    # Блок методов
    def __init__(self, emptyDB):
        if emptyDB == False:
            print('\tНе удалось найти базу городов!\n\nСейчас будет произведена создание и заполнение Б/Д\n\n'+str('*****')*5+'\n\n')
            conn = sqlite3.connect("parser.db")
            cursor = conn.cursor()
            html = requests.get(self.URL).text
            html = bs(html, 'html.parser')
            # Список доступных городов
            listCity = html.find_all('div', {'class': 'cities_list'})
            for i in range(len(listCity)):
                # Получаем букву алфавита
                simbol = listCity[i].find('li', {'cities_list__item'}).getText()
                sql = "CREATE TABLE "+str(simbol)+" (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, city VARCHAR(100) NOT NULL, url VARCHAR (1000) NOT NULL)"
                print('\nCоздание таблицы '+str(simbol)+' : Успешно!\n\n'+str('*****')*5+'\n')
                cursor.execute(sql)
                # Создаем словарь тип {Буква алфивита: [город1, город2, ...]}
                subCity = listCity[i].find_all('li', {'cities_list__item'})
                side = 1
                for i in range(len(subCity)):
                    if str(simbol) == str(subCity[i].getText()):
                        continue
                    subCityHref = subCity[i].find('a').get('href')
                    sql = "INSERT INTO "+str(simbol)+" (city, url) VALUES (\'"+subCity[i].getText()+"\'"+",\'"+subCityHref+"\')"
                    cursor.execute(sql)
                    conn.commit()
                    print('\r'+'Заполнено {bow} данных из {total} [ {proc} % ]'.format(bow = side, total = len(subCity)-1, proc =  round( (side*100)/len(subCity),1)), end='')
                    side += 1
                system('cls')
        else:
            return

    def _del(self):
        print('\nДанные успешно получены.')
        input('\nНажмите любую кнопку чтобы выйти...')
    
    def refactorPhone(self, phone):
        try:
            phone = phone[0] + phone[1] + \
                ' (' + phone[2] + phone[3] + phone[4] + ') ' + \
                phone[5] + phone[6] + phone[7] + '-' + \
                phone[8] + phone[9] + '-' + \
                phone[10] + phone[11]
            return  phone
        except:
            return
        
    def checkDuplicat(self, phone, name, numbers):
        conn = sqlite3.connect("parser.db")
        cursor = conn.cursor()
        sql = "SELECT * FROM phone_"+self.SelectCity.title()+' WHERE phone="'+phone+'"'
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) == 0:
            kj  = 'Совпадений нет\n'
            print( ('\nПроверка {nomer} на наличие в БД: '+kj).format(nomer=phone))
            conn = sqlite3.connect("parser.db")
            cursor = conn.cursor()
            sql = "INSERT INTO phone_"+self.SelectCity.title()+" (name, phone) VALUES (\'"+name+"\',\'"+phone+"\' )"
            cursor.execute(sql)
            conn.commit()
            conn.close()
            print('Получено {now} данных из {total} !'.format(now=self.kolwvo+1, total=numbers))
            self.kolwvo+=1
            return
        else:
            kj  = 'Совпадение есть\n'
            print( ('\nПроверка {nomer} на наличие в БД: '+kj).format(nomer=phone))
            print('Был получен дубликат.\nПереход к следующему\n')
            return


    def pars_page(self, url, numbers):
        self.br.get(url)
        html = self.br.page_source
        html = bs(html, 'html.parser')
        phone = str(html)[str(html).find('tel:'):str(html).find('tel:')+16]
        phone = self.refactorPhone(phone[phone.find(':')+1:])
        name = str(html)[str(html).find('/user/')+2:];	name=name[name.find('/user'):]; name=name[name.find('">'):name.find('</')]
        name = name[2:len(name)-1];	name=name[:name.find('(')]
        system('cls')
        self.checkDuplicat(phone, name, numbers)
        
            
    def pars_main_page(self, numbers, checkDB=1):
        conn = sqlite3.connect("parser.db")
        cursor = conn.cursor()
        if checkDB == 1:
            sql = "SELECT COUNT(*) FROM phone_"+self.SelectCity.title()
            try:
                cursor.execute(sql)
                conn.commit()
                conn.close()
            except:
                sql = "CREATE TABLE phone_"+self.SelectCity.title()+" (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name VARCHAR(100) NOT NULL, phone VARCHAR (50) NOT NULL) "
                cursor.execute(sql)
                conn.commit()
                conn.close()
                self.pars_main_page(numbers,0)
        req = requests.get(self.URL)
        html = bs(req.text, 'html.parser')
        items = html.find_all('li',{'class':'product_item'})
        self.br = wb.PhantomJS(self.BASE)
        for i in range(len(items)):
            if i+1%60 == 0:
                self.br.close()
                self.pars_main_page(numbers,0)
            if self.kolwvo==numbers:
                self.br.close()
                return
            url = self.baseURL+items[i].find('a').get('href')
            self.pars_page(url, numbers)
           
            
    def checkIN(self):
        conn = sqlite3.connect("parser.db")
        cursor = conn.cursor()
        simbol = (self.SelectCity[0]).upper()
        sql = "SELECT city, url FROM "+simbol+ " WHERE city = \'"+self.SelectCity.title()+"\'"
        cursor.execute(sql)
        res = cursor.fetchall()
        conn.commit()
        conn.close()
        if len(res) == 0:
            print('\r\nК сожалению, города с таким названием не удалось найти в Б/Д. Проверьте название на наличие ошибок и попробуйте снова')
            sys.exit(0)
        else:
            self.URL = res[0][1]
            
			
    def selectCity(self, name):
        self.SelectCity = name
        self.checkIN()
	
	
def main():
    emptyDB = ex('./parser.db')
    a = BOT(emptyDB)
    city = input('Введите название города: ')
    a.selectCity(city)
    numbers = int(input('\nСколько объявлений спарсить ? '))
    a.pars_main_page(numbers)
    a._del()



main()

