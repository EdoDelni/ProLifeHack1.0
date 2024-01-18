#packages imported
import time
from datetime import datetime, timedelta
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
import PySimpleGUI as sg
import sys
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# region GUI

# Define the layout of the window
main_layout = [
    [sg.Checkbox('Trasferta', key='Trasferta'), sg.Checkbox('Ufficio', key='Ufficio'), sg.Checkbox('Service', key='Service')],
    [sg.Column([[sg.Button('Settings', size=(10,1))]], justification='center')],
    [sg.Button('Segna le ore di oggi')],
    [sg.Button('Segna le ore di ieri')],
    [sg.Button('Copia il piano di settimana scorsa')],
]

# Create the main window
window = sg.Window('Seleziona il piano', main_layout)
settings_window = None
window_close_byX = True
# Event loop to process events and get button inputs
while True:
    event, values = window.read()
    if event == 'Segna le ore di ieri':
        window_close_byX = False
        window.close()
        segna_ore_ieri = True
        segna_ore_oggi = False
        copia_piano = False
    elif event == 'Segna le ore di oggi':
        window_close_byX = False
        window.close()
        segna_ore_ieri = False
        segna_ore_oggi = True
        copia_piano = False
    elif event == 'Copia il piano di settimana scorsa':
        window_close_byX = False
        window.close()
        segna_ore_ieri = False
        segna_ore_oggi = False
        copia_piano = True
    if event == sg.WINDOW_CLOSED:
        if window_close_byX == True:
            sys.exit()
        if window['Trasferta'].get():
            Location = 'Trasferta'
        elif window['Ufficio'].get():
            Location = "Ufficio"
        elif window['Service'].get():
            Location = 'Service'
        break
    elif event == 'Settings':

        # Settings Layout

        settings_layout = [
            [sg.Text('Username:'), sg.Input(key='user')],
            [sg.Text('Password:'), sg.Input(key='psw')],
            [sg.Text('Orario Inizio Trasferta:'), sg.Input(key='starttrasf')],
            [sg.Text('Orario Fine Trasferta:'), sg.Input(key='finishtrasf')],
            [sg.Text('Orario Inizio Ufficio/Service:'), sg.Input(key='startoff')],
            [sg.Text('Orario Fine Ufficio/Service:'), sg.Input(key='finishoff')],
            [sg.Button('OK'), sg.Button('Cancel')]
        ]
        settings_window = sg.Window('Settings', settings_layout)
        # Event loop for the settings window
        while True:
            event1, values1 = settings_window.read()
            if event1 == sg.WINDOW_CLOSED or event1 == 'Cancel':
                settings_window.close()
                break
            elif event1 == 'OK':
                # Store the entered data into variables
                user = values1['user']
                psw = values1['psw']
                starttrasf = values1['starttrasf']
                finishtrasf = values1['finishtrasf']
                startoff = values1['startoff']
                finishoff = values1['finishoff']
                current_dir = os.getcwd()
                relative_path = 'PROLIFEHACK IMGS/SETTINGS.txt'
                file_path = os.path.join(current_dir, relative_path)
                file_path = os.path.normpath(file_path)
                directory_path = os.path.dirname(file_path)
                if not os.path.exists(directory_path):
                    os.makedirs(directory_path)
                file = open(file_path, 'w')
                file.write(f'Username: {user}\n')
                file.write(f'Password: {psw}\n')
                file.write(f'StartTrasferta: {starttrasf}\n')
                file.write(f'FinishTrasferta: {finishtrasf}\n')
                file.write(f'StartOffice: {startoff}\n')
                file.write(f'FinishOffice: {finishoff}\n')
                file.close()
                settings_window.close()

                # Reopen the main window
                window.un_hide()

# Close the window
    window.close()



#region OPEN BROWSER
#Open the site and adjust the zoom

driver = webdriver.Chrome()
driver.get("https://express.prolifenet.it/#/")
driver.maximize_window()
time.sleep(1)
i=0
while i<3:
    i=i+1
    pyautogui.hotkey('ctrl', '-')
#endregion


# Read data from the file
current_dir = os.getcwd()
relative_path = 'PROLIFEHACK IMGS/SETTINGS.txt'
file_path = os.path.join(current_dir, relative_path)
with open(file_path, 'r') as file:
    lines = file.readlines()

# Extracting the values from the lines
username_text = lines[0].split(': ')[1].strip()
password_text = lines[1].split(': ')[1].strip()

username = driver.find_element(By.ID, "Username")
username.send_keys(username_text)
password = driver.find_element(By.ID, "Password")
password.send_keys(password_text)
accedi = driver.find_element(By.CSS_SELECTOR, '.btn.green.pull-right')
accedi.click()
#endregion

# entra nell'area inserimento ore alla data corrente
today = datetime.today().strftime('%d%m%Y')
yesterday_1 = datetime.today() - timedelta(days=1)
yesterday = yesterday_1.strftime('%d%m%Y')
if segna_ore_ieri == False and segna_ore_oggi == True:
    url = f"https://express.prolifenet.it/#/WorkedHours/{today}"
else:
    url = f"https://express.prolifenet.it/#/WorkedHours/{yesterday}"
driver.get(url)

# chiudi l'hint
timeout = 200  # Wait for a maximum of 20 seconds
wait = WebDriverWait(driver, timeout)
element = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[9]")))
close_hint = driver.find_element(By.XPATH, "/html/body/div[5]/div[9]")
close_hint.click()

#if copia_piano == True:
    #driver.get(https://express.prolifenet.it/#/TaskBoard)
    #
# Region Copia piano

# Go to the previous week and see the Piano

monday_prev_week = today

# find the name and save it in a variable

#else:
#Region Auto compilazione del report
current_dir = os.getcwd()
relative_path = 'PROLIFEHACK IMGS/Progetto.png'
Progetto = os.path.join(current_dir, relative_path)
locate_progetto = pyautogui.locateOnScreen(Progetto, confidence=0.5)
center_progetto = pyautogui.center(locate_progetto)
click_progetto = (center_progetto[0], center_progetto[1] + 25)
pyautogui.click(click_progetto)
if Location == 'Trasferta':
    pyautogui.typewrite('ta230011')
if Location == 'Ufficio':
    pyautogui.typewrite('ta230010')
if Location == 'Service':
    pyautogui.typewrite('ta230006')

current_dir = os.getcwd()
relative_path = 'PROLIFEHACK IMGS/Lente.jpg'
image_path = os.path.join(current_dir, relative_path)
while True:
    image_location = pyautogui.locateOnScreen(image_path, confidence=.7)
    if image_location is not None:
        pyautogui.press('enter')
        break  # Exit the loop if the image is found
    time.sleep(.1)

# Read data from the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Extracting the values from the lines
StartTimeTrasferta = lines[2].split(': ')[1].strip()
FinishTimeTrasferta = lines[3].split(': ')[1].strip()
StartTimeOffice = lines[4].split(': ')[1].strip()
FinishTimeOffice = lines[5].split(': ')[1].strip()

# inserisci le ore

current_dir = os.getcwd()
relative_path = 'PROLIFEHACK IMGS/Inizio.png'
Inizio = os.path.join(current_dir, relative_path)
locate_inizio = pyautogui.locateOnScreen(Inizio, confidence=0.5)
center_inizio= pyautogui.center(locate_inizio)
click_inizio = (center_inizio[0], center_inizio[1] + 25)
pyautogui.click(click_inizio)
if Location == 'Trasferta':
    pyautogui.typewrite(StartTimeTrasferta)
if Location == 'Service' or Location == 'Ufficio':
    pyautogui.typewrite(StartTimeOffice)
pyautogui.press('enter')
pyautogui.press('enter')
pyautogui.press('Tab')
if Location == 'Trasferta':
    pyautogui.typewrite(FinishTimeTrasferta)
if Location == 'Service' or Location == 'Ufficio':
    pyautogui.typewrite(FinishTimeOffice)

pyautogui.press('enter')
pyautogui.press('enter')
pyautogui.press('Tab')
pyautogui.typewrite('1')
pyautogui.press('enter')
pyautogui.press('enter')

current_dir = os.getcwd()
relative_path = 'PROLIFEHACK IMGS/Mansione.PNG'
Mansione = os.path.join(current_dir, relative_path)
locate_mansione = pyautogui.locateOnScreen(Mansione, confidence=0.5)
center_Mansione= pyautogui.center(locate_mansione)
click_mansione = (center_Mansione[0], center_Mansione[1] + 25)
pyautogui.click(click_mansione)
pyautogui.press('down')
pyautogui.press('enter')

current_dir = os.getcwd()
relative_path = 'PROLIFEHACK IMGS/Luogo.PNG'
Luogo = os.path.join(current_dir, relative_path)
locate_luogo = pyautogui.locateOnScreen(Luogo, confidence=0.5)
center_Luogo= pyautogui.center(locate_luogo)
click_luogo = (center_Luogo[0], center_Luogo[1] + 25)
pyautogui.click(click_luogo)
if Location == "Trasferta":
    pyautogui.press('down')
pyautogui.press('down')
pyautogui.press('enter')
if Location == 'Service' or Location == 'Ufficio':
    pyautogui.press('Tab')
    pyautogui.press('Tab')
    pyautogui.typewrite("mensa acn=si".upper())

#endregion

#finish
sys.exit()



