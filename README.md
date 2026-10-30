# web-scraping-vivienda-85120261prac1

##Español

El siguiente _scraper_ extrae la oferta de viviendas de lujo alrededor de España de la inmobiliaria [Lucasfox](https://www.lucasfox.es/).

Para ejecutar el script es necesario instalar la siguientes bibliotecas:
```
pip install pandas
pip install numpy
pip install curl_cffi
pip install beautifulsoup4
```

Una vez instaladas, se puede lanzar:
```
python scraper.py 
```
Los registros se almacenan en un archivo de tipo .CSV, con el formato lucasfox_scraped_YYYYMMDD_HHMMSS.csv, donde YYYY representa el año, MM el mes, DD el día y HHMMSS la hora, minuto y segundo en el que se empezó a ejecutar el script.

El script extrae los siguientes campos de cada listado:
- Ubicación
- Precio
- Superficies (construida, de parcela, y terraza)
- Número de dormitorios
- Número de baños
- Fecha de finalización (si sigue en construcción)
- Si se trata de oferta de compra o alquiler
- Una pequeña descripción que resume todo lo anterior en un _string_


## English

The following webscraper extracts the data of multiple listings on luxury real estate throughout Spain from the realtor [Lucasfox](https://www.lucasfox.es/).

It is necessary to install the following libraries to be able to run the script:
```
pip install pandas
pip install numpy
pip install curl_cffi
pip install beautifulsoup4
```

Once installed, run:
```
python scraper.py
```

All the listings are stored in a .CSV file, in the format lucasfox_scraped_YYYYMMDD_HHMMSS.csv, being YYYYMMDD the year, month and date, and HHMMSS the exact hour, minute and second when the script started running.

The script currently extracts the following data:
- Location
- Price
- Surface area (built, parcel size, and terrace/balcony)
- Number of bedrooms
- Amount of bathrooms
- End of construction date (if still being built)
- Whether is on sale or for rent
- A little description summing up the whole data in a string
