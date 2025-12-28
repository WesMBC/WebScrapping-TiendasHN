from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def extracProductos(pageSources):
    """Extracion de fuente"""
    soup = BeautifulSoup(pageSources, "html.parser")
    prodInfo = []

    productos = soup.select("div.product-card-vertical")

    for producto in productos:
        try:
            titulo = (
                producto.select("h3.product-card__title")[0]
                .text.lstrip()
                .rstrip()
                .replace(",", "")
            )
            precio = (
                producto.select("span.sf-price__regular")[0]
                .text.lstrip()
                .rstrip()
                .replace(",", "")
            )
            prodInfo.append([titulo, precio])
        except Exception as e:
            print(f"Error en la extraccion de productos:\nerror{e}")

    return prodInfo


def extracNumPages(pageSource):
    paginaFinal = 0
    soup = BeautifulSoup(pageSource, "html.parser")

    numerador = soup.select("nav.custom-pagination")
    paginaFinal = numerador[-1].select("span.inactivePage")[-1].text
    print(f"La categoria tiene un numero de {paginaFinal} Paginas")

    return paginaFinal


def createCsvFile(lista):
    file = open("Resultado.csv", "w")
    file.write(f"Producto,Precio\n")
    for fila in lista:
        file.write(f"{fila[0]},{fila[1]}\n")
    file.close()


urls = [
    "https://www.pricesmart.com/es-hn/categoria/Alimentos-G10D03/G10D03",
    "https://www.pricesmart.com/es-hn/categoria/Productos-de-temporada-S10D45/S10D45",
    "https://www.pricesmart.com/es-hn/categoria/Hogar-H30D22/H30D22",
    "https://www.pricesmart.com/es-hn/categoria/Salud-y-belleza-H20D09/H20D09",
    "https://www.pricesmart.com/es-hn/categoria/Licor-cerveza-y-vino-G10D08014/G10D08014",
    "https://www.pricesmart.com/es-hn/categoria/Mascotas-P10D51/P10D51",
    "https://www.pricesmart.com/es-hn/categoria/Bebe-B10D27/B10D27",
    "https://www.pricesmart.com/es-hn/categoria/Ferreteria-y-mejoras-al-hogar-H10D21/H10D21",
    "https://www.pricesmart.com/es-hn/categoria/Deportes-y-fitness-S30D26/S30D26",
    "https://www.pricesmart.com/es-hn/categoria/Exteriores-O20D30/O20D30",
    "https://www.pricesmart.com/es-hn/categoria/Exteriores-O20D30/O20D30",
    "https://www.pricesmart.com/es-hn/categoria/Electronicos-E10D24/E10D24",
    "https://www.pricesmart.com/es-hn/categoria/Electrodomesticos-S20D23/S20D23",
    "https://www.pricesmart.com/es-hn/categoria/Computadoras-tablets-y-accesorios-C10D29/C10D29",
    "https://www.pricesmart.com/es-hn/categoria/Linea-blanca-M10D43/M10D43",
    "https://www.pricesmart.com/es-hn/categoria/Moda-y-accesorios-F10D40/F10D40",
    "https://www.pricesmart.com/es-hn/categoria/Muebles-F20D27/F20D27",
    "https://www.pricesmart.com/es-hn/categoria/Oficina-O10D25/O10D25",
    "https://www.pricesmart.com/es-hn/categoria/Suministros-para-restaurantes-R10D22/R10D22",
    "https://www.pricesmart.com/es-hn/categoria/Automotriz-A10D20/A10D20",
    "https://www.pricesmart.com/es-hn/categoria/Juguetes-y-juegos-T10D46/T10D46",
    "https://www.pricesmart.com/es-hn/categoria/Equipaje-L10D22/L10D22",
    "https://www.pricesmart.com/es-hn/categoria/Optica-U10D72/U10D72",
    "https://www.pricesmart.com/es-hn/categoria/Audiologia-U11D13/U11D13",
    "https://www.pricesmart.com/es-hn/categoria/Peliculas-musica-y-libros-T20D42/T20D42",
    "https://www.pricesmart.com/es-hn/categoria/Tarjetas-de-Regalo-V10D79/V10D79",
    "https://www.pricesmart.com/es-hn/categoria/Joyeria-y-relojes-J10D44/J10D44",
]
paginador = "?page="


pricesInfo = []

# Llamado de la pagina para que cargue completamente con Selenium
driver = webdriver.Chrome()
for url in urls:
    print(f"Esta entrando a direccion: {url}")
    driver.get(f"{url}")
    driver.maximize_window()
    print("En espera de carga de objetos")
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card__title"))
        )
        html = driver.page_source
        numPaginas = extracNumPages(html)
    except Exception as e:
        print(f'Hubo algun error en la pagina {e}')
        continue


    for i in range(1, int(numPaginas)):
        print(f"Esta entrando a direccion: {url}{paginador}{i}")
        driver.get(f"{url}{paginador}{i}")
        print("En espera de carga de objetos")
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-card__title"))
        )
        html = driver.page_source
        pricesInfo.extend(extracProductos(html))


createCsvFile(pricesInfo)

driver.quit()
