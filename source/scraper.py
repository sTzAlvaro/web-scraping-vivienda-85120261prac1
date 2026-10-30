from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import time
import random
import re

NOW = datetime.datetime.now()
PURCHASE_URL = 'https://www.lucasfox.es/comprar-vivienda/espana.html'
RENT_URL = 'https://www.lucasfox.es/alquilar-vivienda/espana.html'
CSV_FILENAME = f'lucasfox_scraped_{NOW.strftime('%Y%m%d')}_{NOW.strftime('%H%M%S')}.csv'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

total_properties_df = pd.DataFrame()

def scrape_lucasfox(rent=False):
    properties_df = pd.DataFrame()
    base_url = RENT_URL if rent else PURCHASE_URL
    response = requests.get(base_url, timeout=15, impersonate='chrome120')
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(type(str(soup.find('span', class_='listing-pagination__status'))))
    paging = list(map(int, re.findall(r'\d+', str(soup.find('span', class_='listing-pagination__status')))))
    max_pages = max(paging)
    print(f' ********** A screapear: {base_url} ********** ')
    print(f'Total de páginas de búsqueda: {max_pages}')


    for page in range(1, max_pages + 1):
        print(f'Página {page}...')

        if page == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page}"

        # 1. Hasta que encuentre un fallo en la página (o trate de scrapear más páginas de las que hay)
        #    el bot sigue.
        while True:
            try:
                # Con esta librería, impersonate se encarga del header. No muy buena práctica, pero pregunté a Gemini si
                # había alguna forma de saltarse las restricciones y me la recomendó (no funciona, pero te olvidas de
                # gestionar el header!
                response = requests.get(url, timeout=15, impersonate='chrome120')

                # Intentando hacer scraping de algunas páginas tipo Idealista, Fotocasa, Thinkspain...
                # me encontré con varios de estos códigos.
                if response.status_code == 429:
                    print(f'Error 429: Scraping demasiado rápido... Delay de un minuto.')
                    time.sleep(60 + random.uniform(0.1, 30.5))
                    continue

                if response.status_code == 403:
                    print('Error 403: Bloqueo de firewall...')
                    return

                if response.status_code == 404:
                    print(f"Error 404, clásico. Fin del scraping.")
                    break

                # Cualquier otro error lleva a excepción, si está ok, rompe el bucle y sigue
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                print(f"Error en página {page}: {e}")
                break


        # 2 Parseo HTML: búsqueda de las características de cada casa
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)

        listings = soup.find_all('div', class_="property-card__body")
        #print(listings) ### Sólo para testeo
        if not listings:
            print("La página de búsqueda está vacía. Fin del scraping.")
            break

        page_properties = []

        for listing in listings:
            property_data = {}
            # Ubicación
            location_tag = listing.find('span', class_='property-card__meta')
            property_data['ubicacion'] = location_tag.text.strip() if location_tag else np.nan

            # Precio (en Euros)
            price_tag = listing.find('span', class_='property-card__price')
            property_data['precio'] = price_tag.text.strip() if price_tag else np.nan

            # Características
            features = listing.find_all('li', class_='key-facts__item')
            for feature in features:
                key = feature.find('span', class_='key-facts__key')
                value = feature.find('span', class_='key-facts__value')
                if key:
                    property_data[f'{key.text.strip().lower()}'] = value.text.strip() if value else np.nan

            # Descripción
            description_tag = listing.find('p', class_='property-card__title')
            property_data['descripcion'] = description_tag.text.strip() if description_tag else np.nan

            property_data['tipo_transaccion'] = 'alquiler' if rent else 'compra'

            if property_data:
                property_data_df = pd.DataFrame([property_data])
                properties_df = pd.concat([properties_df, property_data_df], ignore_index=True)

        print(f"Extraídas {len(properties_df)} propiedades tras completar página {page}.")

        # El random para que no todos los delays sean exactamente iguales y prevenir detección
        # Puede que dos segundos sea igual demasiado rápido?
        delay = 10 + random.uniform(-1.5, 1.5)
        print(f"Delay de ~{delay:.2f} segundos...\n")
        time.sleep(delay)

    return properties_df

def data_output(data:pd.DataFrame):
    data.to_csv(CSV_FILENAME, index=False, encoding='utf-8-sig')
    print(f"Scraping completado, datos disponibles en: {CSV_FILENAME}.")

if __name__ == "__main__":
    purchase_prop_df = scrape_lucasfox()
    total_properties_df = pd.concat([total_properties_df, purchase_prop_df], ignore_index=True)
    rent_prop_df = scrape_lucasfox(True)
    total_properties_df = pd.concat([total_properties_df, rent_prop_df], ignore_index=True)
    data_output(total_properties_df)
