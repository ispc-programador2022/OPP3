import time 
from datetime import datetime
from requests import get, post
import bs4 as bs
import pytz

#Primero definimos función y variables para el envío de mensajes del bot de  la app de mensajería Telegram
# se completa con los valores pertinentes, por razones de privacidad no lo expodremos pero sí lo haremos en la presentación

bot_token = #""
chat_id = # COMPLETAR


def send_msg(msg, chat_id, bot_token):
    resp = post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage?"
        f"chat_id={chat_id}&parse_mode=Markdown&text={msg}"
    )
    return resp.json()

#Luego declaramos las listas vacías

lista_fechas = []

lista_dolar= []

#el scraper se ejecutará continuamente, tomando cada una hora el valor del dolar informal, enviará ese valor por Telegram 
# y adicionará a una lista el valor y la fecha y hora

while True:

  # Descargo el codigo HTML
  result = get("https://www.cronista.com/MercadosOnline/moneda.html?id=ARSB")

  # Hago que la computadora lo vea y lo interprete para luego poder navegarlo facilmente
  soup = bs.BeautifulSoup(result.content,'html.parser')

  # Extraigo los valores que me interesan
  values = soup.find_all("div",{"class":"sell-value"})

  # Extraigo el texto de cada elemento
  dolar = [value.text for value in values]

  print(dolar)

  tz_argentina = pytz.timezone("America/Buenos_Aires")

  fecha_argentina = datetime.now(tz_argentina)

  current_time = fecha_argentina.strftime("%d-%m-%Y %H:%M:%S")

  print("The current date and time is", current_time)

  lista_fechas.append(current_time)

  lista_dolar.append(dolar)

  # Envio los shows encontrados
  send_msg(dolar, chat_id, bot_token)

  time.sleep(1*60*60)


#con las listas armamos un dataframe para poder analizarlo; para esto utilizaremos la librería Pandas

import pandas as pd
import numpy as np


df_dolar = pd.DataFrame(list(zip(lista_fechas, lista_dolar)), columns = ['fecha_hora','valor_dolar_informal'])
#opcion
#df_dolar = pd.DataFrame({ 'fecha_hora' : lista_fechas , 'valor_dolar_informal' : lista_dolar })

print(df_dolar)


# Visualización en serie de tiempo

df_dolar.plot( 'lista_fechas' , 'lista_dolar' )

