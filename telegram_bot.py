import requests
import json
from datetime import datetime


class TelegramBot:

    def __init__(self):
        self.token = 'INSERT_BOT_TOKEN_HERE'
        self.covid_19_info_url = 'https://data.covid19.go.id/public/api/update.json'
        self.base_url = 'https://api.telegram.org/bot{}/'.format(self.token)

    def check_message(self, offset=None):
        url = self.base_url+'getUpdates?timeout=100'
        if offset:
            url = url + '&offset={}'.format(offset + 1)
        response = requests.get(url)
        return json.loads(response.content)

    def send_message(self, msg, sender_id):
        url = self.base_url + \
            'sendMessage?chat_id={}&text={}'.format(sender_id, msg['text'])
        if msg.get('reply_markup'):
            url = url + '&reply_markup={}'.format(msg['reply_markup'])
        req = requests.get(url)

    def get_covid_info(self):
        res = requests.get(self.covid_19_info_url)
        data = json.loads(res.content)
        return {
            "tanggal": datetime.today().strftime('%d-%m-%Y'),
            "positif": data['update']['total']['jumlah_positif'],
            "sembuh": data['update']['total']['jumlah_sembuh'],
            "dirawat": data['update']['total']['jumlah_dirawat'],
            "meninggal": data['update']['total']['jumlah_meninggal'],
        }

    def get_covid_info_day(self):
        res = requests.get(self.covid_19_info_url)
        data = json.loads(res.content)
        return {
            "tanggal": datetime.strptime(data['update']['penambahan']['tanggal'], '%Y-%m-%d'),
            "positif": data['update']['penambahan']['jumlah_positif'],
            "sembuh": data['update']['penambahan']['jumlah_sembuh'],
            "dirawat": data['update']['penambahan']['jumlah_dirawat'],
            "meninggal": data['update']['penambahan']['jumlah_meninggal'],
        }

    def make_reply(self, msg):
        reply_markup = {
            "keyboard": [
                ["Cek Informasi Keseluruhan", "Cek Informasi Hari Ini"]
            ],
            "one_time_keyboard": True,
            "resize_keyboard": True
        }
        if msg == '/start':
            return {"text": "Selamat Datang Di Informasi Covid-19 Indonesia, \n\nSilahkan Pilih Salah Satu Menu.",
                    "reply_markup": json.dumps(reply_markup)}
        elif msg == '/help':
            return {"text": "Silahkan Pilih Salah Satu Menu.",
                    "reply_markup": json.dumps(reply_markup)}
        elif msg == 'Cek Informasi Keseluruhan':
            data = self.get_covid_info()
            message = f"Informasi Covid-19 Di Indonesia Secara Keseluruhan per tanggal {data['tanggal']}\n\nJumlah Pasien Positif : {data['positif']}\nJumlah Pasien Sembuh : {data['sembuh']}\nJumlah Pasien Dirawat : {data['dirawat']}\nJumlah Pasien Meninggal : {data['meninggal']}\n\nData Ini Langsung Di Ambil dari Informasi API Pemerintah Indonesia.\n\n%23Stay_Safe %23DiRumah_Saja"
            return {"text": message, "reply_markup": json.dumps(reply_markup)}
        elif msg == 'Cek Informasi Hari Ini':
            data = self.get_covid_info_day()
            message = f"Informasi Penambahan Pasien Covid-19 di Indonesia Pada Tanggal {data['tanggal'].strftime('%d-%m-%Y')}\n\nPenambahan Pasien Positif : {data['positif']}\nPasien Sembuh Hari Ini : {data['sembuh']}\nPasien Dirawat : {data['dirawat']}\nJumlah Pasien Meninggal : {data['meninggal']}\n\nData Ini Langsung Di Ambil dari Informasi API Pemerintah Indonesia.\n\n%23Stay_Safe %23DiRumah_Saja"
            return {"text": message, "reply_markup": json.dumps(reply_markup)}
        else:
            return {"text": 'Command Salah, Ketik "/help" untuk cek Menu.'}


