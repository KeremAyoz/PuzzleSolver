from datetime import date, timedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import threading

THREAD_COUNT = 4
HEADLESS = True
VERBOSE = False
START_DATE = date(2018, 2, 1)
END_DATE = date.today()
USERNAME = "erkutalakus@gmail.com"
PASSWORD = "ea22461016"

CURRENT_DATE = START_DATE
FILE_LOCK = threading.Lock()
DATE_LOCK = threading.Lock()

#webdriver options
OPTIONS = webdriver.ChromeOptions()
if HEADLESS:
    OPTIONS.add_argument('--headless')
if not VERBOSE:    
    OPTIONS.add_argument('--log-level=3')

print(str(END_DATE))

def getCrossword(driver, puzzleDate):
    #start to get puzzle
    big_json = {}

    driver.get("https://www.nytimes.com/crosswords/game/mini/" + puzzleDate.strftime("%Y/%m/%d"))

    try:
        start_button = driver.find_element_by_class_name("buttons-modalButton--1REsR")
        start_button.click()
    except NoSuchElementException:
        driver.find_element_by_class_name("Toolbar-resetButton--1bkIx").find_element_by_tag_name("button").click()

    cell_container = driver.find_element_by_css_selector('[data-group="cells"]')
    cells = cell_container.find_elements_by_tag_name("g")

    x = 1
    y = 1
    cell_objs = []
    for cell in cells:
        rect = cell.find_element_by_tag_name("rect")
        temp = {'x': x, 'y': y, 'color': rect.get_attribute("fill") is None if rect.get_attribute("fill") else ("black" if rect.value_of_css_property("fill") == "rgb(0, 0, 0)" else "none" ), 'key': ""}    #color fix for erkut's stupid env

        try:
            text = cell.find_element_by_tag_name("text").text
            temp['key'] = text
        except NoSuchElementException:
            pass

        if x % 5 == 0:
            y += 1
            x = 0
        x += 1

        cell_objs.append(temp)

    big_json['cells'] = cell_objs

    clue_container = driver.find_element_by_class_name("Layout-clueLists--10_Xl")

    lists = clue_container.find_elements_by_tag_name("div")

    processed_clues = {"Down": [], "Across": []}
    for clue_list in lists:

        header = clue_list.find_element_by_tag_name("h3").text
        clues = clue_list.find_elements_by_tag_name("li")

        l = []
        for clue in clues:
            clue_contents = clue.find_elements_by_tag_name("span")
            clue_dict = {"key": clue_contents[0].text, "hint": clue_contents[1].text}
            l.append(clue_dict)
        if header == "ACROSS":
            processed_clues["Across"] = l
        elif header == "DOWN":
            processed_clues["Down"] = l
        else:
            print("Header not recognized: " + header)


    big_json['clues'] = processed_clues

    solution_button = driver.find_element_by_css_selector(".Toolbar-expandedMenu--2s4M4").find_elements_by_css_selector(".Tool-button--39W4J.Tool-tool--Fiz94.Tool-texty--2w4Br")[1]
    solution_button.click()
    reveal_button = solution_button.find_elements_by_css_selector(".HelpMenu-item--1xl0_")[2]
    reveal_button.click()

    modal = driver.find_element_by_css_selector(".ModalWrapper-overlay--3D0UT.ModalWrapper-stretch--19Bif")
    button = driver.find_element_by_css_selector(".buttons-modalButtonContainer--35RTh").find_elements_by_css_selector(".buttons-modalButton--1REsR")[1]
    button.click()


    close_button = driver.find_element_by_css_selector(".ModalBody-closeX--2Fmp7")
    close_button.click()


    cell_container = driver.find_element_by_css_selector('[data-group="cells"]')
    cells = cell_container.find_elements_by_tag_name("g")

    x = 1
    y = 1
    cell_objs = []
    for cell in cells:
        rect = cell.find_element_by_tag_name("rect")
        temp = {'x': x, 'y': y, 'color': rect.get_attribute("fill") is None if rect.get_attribute("fill") else ("black" if rect.value_of_css_property("fill") == "rgb(0, 0, 0)" else "none" ), 'key': "", 'solution': ""}    #color fix for erkut's stupid env
        try:
            texts = cell.find_elements_by_tag_name('text')
            if len(texts) == 1:
                temp['solution'] = texts[0].text
            if len(texts) == 2:
                temp['key'] = texts[0].text
                temp['solution'] = texts[1].text

        except NoSuchElementException:
            pass

        if x % 5 == 0:
            y += 1
            x = 0
        x += 1

        cell_objs.append(temp)


    big_json['solution_cells'] = cell_objs

    #print(json.dumps(big_json, indent=4))

    solutions = {"Down": {}, "Across": {}}

    y = 1
    x = 1

    while y < 6:
        text = ""
        key = -1
        first = True
        x = 1
        while x < 6:
            cell = cell_objs[5 * (y - 1) + (x - 1)]
            if cell['color'] != 'black':
                if cell['key'] != '':
                    if first:
                        key = cell['key']
                        first = False
                text = text + cell['solution']
            x += 1
            if x == 6:
                y += 1
        solutions["Across"][key] = text

    x = 1
    y = 1

    while x < 6:
        text = ""
        key = -1
        first = True
        y = 1
        while y < 6:
            cell = cell_objs[5 * (y - 1) + (x - 1)]
            if cell['color'] != 'black':
                if cell['key'] != '':
                    if first:
                        key = cell['key']
                        first = False
                text = text + cell['solution']
            y += 1
            if y == 6:
                x += 1
        solutions["Down"][key] = text


    big_json['solutions'] = solutions
    big_json['date'] = str(date.today())

    return big_json

def append_to_json(_dict, path):
    with open(path, 'ab+') as f:
        f.seek(0, 2)  # Go to the end of file
        if f.tell() == 0:  # Check if file is empty
            f.write(str.encode(json.dumps([_dict], indent=2)))  # If empty, write an array
        else:
            f.seek(-1, 2)
            f.truncate()  # Remove the last character, open the array
            f.write(str.encode(' , '))  # Write the separator
            f.write(str.encode(json.dumps(_dict, indent=2)))  # Dump the dictionary
            f.write(str.encode(']'))  # Close the array

def driverLoop(index):
    global CURRENT_DATE, DATE_LOCK, FILE_LOCK, OPTIONS, USERNAME, PASSWORD
    driverFailed = True
    while driverFailed:
        try:
            driver = webdriver.Chrome(chrome_options = OPTIONS)
            driverFailed = False
        except:
            print("Driver " + str(index+1) + " failed to initialize. Retrying...")
            pass

    wait = WebDriverWait(driver, 100)
    print("Driver " + str(index+1) + " initialized.")

    #Login into account
    driver.get("https://myaccount.nytimes.com/auth/login?URI=")
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    driver.find_element_by_id("submitButton").click()
    time.sleep(20)

    print("Thread " + str(index+1) + " successfully logged in.")

    while CURRENT_DATE < END_DATE:
        DATE_LOCK.acquire()
        CURRENT_DATE = CURRENT_DATE + timedelta(days=1)
        assigned_date = CURRENT_DATE
        if (assigned_date.weekday() == 5): #if it is saturday, pass
            DATE_LOCK.release()
            print("Puzzle " + assigned_date.strftime("%x") + " passed because it is SATURDAY")
            continue
        DATE_LOCK.release()
        print("Started to fetch: " + assigned_date.strftime("%x"))

        json = getCrossword(driver, assigned_date)

        FILE_LOCK.acquire()
        append_to_json(json, "Data/data.json")
        FILE_LOCK.release()
        print("Puzzle " + assigned_date.strftime("%x") + " written to file.")

    driver.delete_all_cookies()
    driver.close()
    print("Driver " + str(index+1) + " closed.")

    print("Thread " + str(index+1) + " finished.")

threads = []
#start threads here
for x in range(0,THREAD_COUNT):
    threads.append(threading.Thread(target=driverLoop, args=(x,)))
    threads[x].start()
    print("Thread " + str(x+1) + " started.")
    time.sleep(1)

#wait for threads to finish their job
for x in range(0,THREAD_COUNT):
    threads[x].join()
