# Importación de las bibliotecas necesarias
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np

# Listas para almacenar datos
hrefs = []  # Enlaces a las páginas de los equipos
playerList = []  # Información detallada de los jugadores

# Configuración de las opciones del navegador
options = Options()
options.add_argument("start-maximized")  # Maximizar ventana al iniciar
options.add_argument("disable-infobars")  # Deshabilitar mensajes informativos del navegador
options.add_argument("--disable-extensions")  # Deshabilitar extensiones
options.add_argument("--disable-gpu")  # Deshabilitar aceleración por GPU
options.add_argument("--no-sandbox")  # Deshabilitar el sandbox
# options.add_argument("--headless")  # Ejecutar navegador en modo headless (sin interfaz gráfica)
options.add_argument("--disable-crash-reporter")  # Deshabilitar reportes de fallos
options.add_argument("--disable-popup-blocking")  # Deshabilitar bloqueo de ventanas emergentes

# Inicializar navegador con opciones configuradas
driver = uc.Chrome(options=options)

# Abrir página principal de estadísticas de equipos en HLTV
driver.get('https://www.hltv.org/stats/teams?startDate=2023-11-27&endDate=2024-11-27')

# Guardar el identificador de la ventana actual
windows_teamList = driver.current_window_handle

# Esperar a que los elementos del selector de equipos sean visibles
elements = WebDriverWait(driver, 20).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "td.teamCol-teams-overview>a"))
)
time.sleep(3)  # Pausa adicional para garantizar que los elementos estén cargados

# Función para extraer valores de estadísticas mediante XPATH
def unpack(xpath):
    stat_value = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    ).text
    return stat_value

# Recopilar enlaces de los equipos
for element in elements:
    hrefs.append(element.get_attribute("href"))

# Recorrer cada equipo para obtener detalles
for href in hrefs[25:55]: # Añade [:número] para eligir hasta el equipo que quieres que scrapee
    driver.execute_script("window.open('" + href + "');")  # Abrir enlace en una nueva pestaña
    windows_after = driver.window_handles
    window_Team = [x for x in windows_after if x != windows_teamList][1]  # Identificar nueva pestaña
    driver.switch_to.window(window_Team)  # Cambiar a la pestaña del equipo

    # Hacer clic en la pestaña "Lineups"
    lineups = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Lineups')]"))
    ).click()

    # Scraping de datos de alineaciones
    bs = BeautifulSoup(driver.page_source, "lxml")
    lineupContainers = bs.find_all("div", class_="lineup-container")  # Contenedores de alineaciones
    teamName = (bs.find("span", class_="context-item-name")).text  # Nombre del equipo

    for lineupContainer in lineupContainers:
        lineupYear = ((lineupContainer.find("div", class_="lineup-year")).text).replace('Replace context with lineup', '')
        mapsPlusWinrate = lineupContainer.find_all("div", class_="large-strong")
        mapsPlayed = int(mapsPlusWinrate[0].text)  # Mapas jugados
        winrate = round(int(mapsPlusWinrate[1].text.split()[0]) / mapsPlayed, 2)  # Winrate

        # Scraping de jugadores en la alineación
        lineupMembers = WebDriverWait(driver, 23).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.teammate-info>a"))
        )
        newhrefs = [member.get_attribute("href") for member in lineupMembers]
        playerPrelimNames = [member.find_element(By.CSS_SELECTOR, "div.text-ellipsis").text for member in lineupMembers]

        # Recopilar estadísticas de cada jugador
        for j, newhref in enumerate(newhrefs):
            playerPrelimName = playerPrelimNames[j]

            # Procesar solo si el jugador aún no está en la lista
            if not any(d['playerName'] == playerPrelimName for d in playerList):
                valueToFill = True
                driver.execute_script("window.open('" + newhref + "');")  # Abrir página del jugador
                windows_after = driver.window_handles
                window_Player = [x for x in windows_after if x != window_Team][2]  # Identificar pestaña del jugador
                driver.switch_to.window(window_Player)  # Cambiar a la pestaña del jugador

                # Scraping de estadísticas del jugador
                pbs = BeautifulSoup(driver.page_source, "lxml")
                playerName = pbs.find("h1", class_="summaryNickname").text
                stats = pbs.find_all("div", class_="stats-row")
                statTopPanel = pbs.find_all("div", class_="summaryStatBreakdownDataValue")
                statImpact = statTopPanel[3].text
                statKAST = (statTopPanel[2].text).strip("%")

                statList = {}
                for stat in stats:
                    statPair = stat.find_all("span")
                    actualStat = (statPair[1].text).strip("%") if valueToFill else 'NA'
                    statList = {**statList, **dict({f"{statPair[0].text}": actualStat})}

                if valueToFill:
                    # Obtener estadísticas adicionales individuales
                    WebDriverWait(driver, 23).until(
                        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Individual')]"))
                    ).click()

                    statOKratio = unpack('/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[1]/div[5]/div[3]/span[2]')
                    statOK = unpack('/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[1]/div[5]/div[1]/span[2]')
                    statRifleKills = unpack("/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[2]/div[5]/div[1]/span[2]")
                    statSniperKills = unpack("/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[2]/div[5]/div[2]/span[2]")
                    statSmgKills = unpack("/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[2]/div[5]/div[3]/span[2]")
                    statPistolKills = unpack("/html/body/div[2]/div[8]/div[2]/div[1]/div/div[6]/div/div[2]/div[5]/div[4]/span[2]")

                # Añadir estadísticas a la lista
                playerList.append({
                    "playerName": playerName,
                    "teamName": f"{teamName} {lineupYear}",
                    "mapsPlayed": mapsPlayed,
                    "winrate": winrate,
                    "hltvImpact": statImpact,
                    "KAST": statKAST,
                    "openingKills": statOK,
                    "OKratio": statOKratio,
                    "rifleKills": statRifleKills,
                    "sniperKills": statSniperKills,
                    "smgKills": statSmgKills,
                    "pistolKills": statPistolKills,
                    **statList
                })

                driver.close()  # Cerrar pestaña del jugador
            driver.switch_to.window(window_Team)  # Volver a la pestaña del equipo
    driver.close()  # Cerrar pestaña del equipo
    driver.switch_to.window(windows_teamList)  # Volver a la pestaña principal

driver.quit()  # Cerrar el navegador

# Guardar los datos en un archivo CSV
df = pd.DataFrame(playerList)
df.replace('NA', np.nan, regex=True, inplace=True)  # Reemplazar 'NA' con valores nulos
df.sort_values(by='playerName', inplace=True)  # Ordenar por nombre del jugador
df.to_csv("stats-2024-before-major_2.csv", index=False)  # Guardar datos en un archivo CSV
