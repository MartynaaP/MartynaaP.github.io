import unittest
import json
import requests

from pogoda import konwertuj_do_c
from register import *

class TestPogoda(unittest.TestCase):

    #Moje testy:
    #Metoda testuje działanie metody konwertuj_do_c
    def test_kelvin_celsius(self):
        proper_value = '25.16'
        result = konwertuj_do_c(298.31)
        self.assertEqual(result, proper_value)

    #Sprawdzenie czy jeżeli wpiszę złą nazwę miasta w linku url do API z openweather to czy zwróci błąd o tym, że nie ma takiego miasta
    def test_openweather_result(self):
        dict = {'cod':'404',
              'message':'city not found'}

        r = requests.get('https://api.openweathermap.org/data/2.5/weather?q=error&appid=aca0e7d414772332a3542bbe05aa023b')
        self.assertEqual(r.status_code,404)
        self.assertEqual(r.json(),dict)

    #Testy z zajęć:
    def setUp(self):
        self.weather_json =  json.loads(requests.get(
    'http://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b1b15e88fa797225412429c1c50c122a1').content.strip())
        self.temp = self.weather_json['main']['temp']

    # def sprawdz_temp(self):
    #     self.assertIs(self.weather_json['main']['temp'], 'nie istnieje')


    def test_format_temperatury(self):
        temp = self.temp
        self.assertLess(temp, 1000, "Temp wieksze od 0")

    def test_polaczeni(self):
        r = requests.get('http://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=b1b15e88fa797225412429c1c50c122a1')
        self.assertEqual(r.status_code, 200, 'brak polaczenia')


    # do bazy danych
    def test_dodania_uzytkownika(self):
        session = return_sqlalchemysession()

        username = 'user'
        password = 'password'
        user = User(username, password)
        session.add(user)
        session.commit()

        q = session.query(User).filter(User.username == username)
        self.assertTrue(session.query(q.exists()).scalar(), 'fail')
        session.close()
