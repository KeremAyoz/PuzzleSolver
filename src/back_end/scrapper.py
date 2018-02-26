from datetime import date, timedelta, time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json, time, threading, os

# settings
THREAD_COUNT = 6
MAX_RETRY = 3
HEADLESS = True
VERBOSE = False
START_DATE = date(2014, 8, 21)      # included
END_DATE = date.today()             # included
USERNAME = "erkutalakus@gmail.com"
PASSWORD = "ea22461016"

# shared
CURRENT_DATE = None
FAILED_ONES = []
FILE_LOCK = threading.Lock()
DATE_LOCK = threading.Lock()
JSON_DATA = []
OPTIONS = None


def getCrossword(driver, puzzleDate, retry=0):
    # start to get puzzle
    big_json = {}

    driver.get("https://www.nytimes.com/crosswords/game/mini/" + puzzleDate.strftime("%Y/%m/%d"))

    try:
        start_button = driver.find_element_by_class_name("buttons-modalButton--1REsR")
        start_button.click()
    except NoSuchElementException:
        try:
            driver.find_element_by_class_name("Toolbar-resetButton--1bkIx").find_element_by_tag_name("button").click()
        except:
            global MAX_RETRY
            if retry < MAX_RETRY:
                print(str(puzzleDate) + " --- Unable to fetch puzzle. Retrying...(%s)" % (retry + 1))
                return getCrossword(driver, puzzleDate, retry=retry + 1)
            else:
                print(str(puzzleDate) + " --- Unable to fetch puzzle. Retry limit exceeded, skipping.")
                DATE_LOCK.acquire()
                FAILED_ONES.append(puzzleDate)
                DATE_LOCK.release()
                return None

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
    big_json['date'] = str(puzzleDate)

    return big_json


def append_to_json(_dict, path):
    if _dict is None:
        return
    with open(path, 'ab+') as f:
        f.seek(0, 2)  # Go to the end of file
        if f.tell() == 0:  # Check if file is empty
            f.write(str.encode(json.dumps([_dict], separators=(',', ':'))))  # If empty, write an array
        else:
            f.seek(-1, 2)
            f.truncate()  # Remove the last character, open the array
            f.write(str.encode(' , '))  # Write the separator
            f.write(str.encode(json.dumps(_dict, separators=(',', ':'))))  # Dump the dictionary
            f.write(str.encode(']'))  # Close the array


def is_in_list(puzzleDate):
    # "2016-09-26"; this puzzle has different shape
    if str(puzzleDate) == "2016-09-26":
        return True

    if len(JSON_DATA) > 0:
        for puzzle in JSON_DATA:
            if puzzle['date'] == str(puzzleDate):
                return True
        return False
    else:
        return False


def driverLoop(index, file_path, retry=0):
    global CURRENT_DATE, DATE_LOCK, FILE_LOCK, OPTIONS, USERNAME, PASSWORD
    driverFailed = True

    while driverFailed:
        try:
            driver = webdriver.Chrome(chrome_options=OPTIONS)
            driverFailed = False
        except:
            if retry < MAX_RETRY:
                print("Driver " + str(index + 1) + " failed to initialize. Retrying...(%s)" % (retry + 1))
                return driverLoop(index, retry + 1)
            else:
                print("Driver " + str(index + 1) + " failed to initialize. Discarding.")
                return

    print("Driver " + str(index + 1) + " initialized.")

    # Login into account
    driver.get("https://myaccount.nytimes.com/auth/login?URI=")
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)
    driver.find_element_by_id("submitButton").click()
    time.sleep(10)  # wait some to login

    print("Thread " + str(index + 1) + " successfully logged in.")

    while True:
        DATE_LOCK.acquire()

        # loop check
        if CURRENT_DATE > END_DATE:
            if len(FAILED_ONES) > 0:
                assigned_date = FAILED_ONES.pop()
                DATE_LOCK.release()
            else:                   # end loop
                DATE_LOCK.release()
                break
        else:
            assigned_date = CURRENT_DATE
            CURRENT_DATE = CURRENT_DATE + timedelta(days=1)
            if assigned_date.weekday() == 5:  # if it is saturday, pass
                DATE_LOCK.release()
                print("Puzzle " + assigned_date.strftime("%x") + " passed because it is SATURDAY")
                continue
            DATE_LOCK.release()

        # check the date if it is already fetched
        if is_in_list(assigned_date):
            print("Puzzle " + assigned_date.strftime("%x") + " passed because it is already in the list")
            continue

        print("Started to fetch: " + assigned_date.strftime("%x"))
        day_json = getCrossword(driver, assigned_date)

        # detect zombie driver
        if day_json is None:
            driver.delete_all_cookies()
            driver.close()
            print("Driver " + str(index + 1) + " closed.")
            print("Thread " + str(index + 1) + " restarting...")
            driverLoop(index)   # restart it
            break

        FILE_LOCK.acquire()
        append_to_json(day_json, file_path)
        FILE_LOCK.release()
        print("Puzzle " + assigned_date.strftime("%x") + " written to file.")

    try:
        driver.delete_all_cookies()
        driver.close()
        print("Driver " + str(index + 1) + " closed.")
        print("Thread " + str(index + 1) + " finished.")
    except:
        pass    # driver already closed


def minify(file_path):
    file = open(file_path, "r", 1)
    file_data = file.read()  # store file info in variable
    json_data = json.loads(file_data)  # store in json structure
    json_string = json.dumps(json_data, separators=(',', ":"))  # Compact JSON structure
    file.close()
    open(file_path, "w", 1).write(json_string)  # write json_string to file


def start(file_path):
    global JSON_DATA, OPTIONS, CURRENT_DATE, START_DATE

    CURRENT_DATE = START_DATE

    try:
        JSON_DATA = json.load(open(file_path))
    except:
        pass    # json file not here

    # webdriver options
    OPTIONS = webdriver.ChromeOptions()
    if HEADLESS:
        OPTIONS.set_headless(headless=True)
    if not VERBOSE:
        OPTIONS.add_argument('--log-level=3')
    OPTIONS.add_argument("--mute-audio")

    start_time = time.time()
    threads = []

    # start threads here
    for x in range(0, THREAD_COUNT):
        threads.append(threading.Thread(target=driverLoop, args=(x, file_path,)))
        threads[x].start()
        print("Thread " + str(x + 1) + " started.")
        time.sleep(1)

    # wait for threads to finish their job
    for x in range(0, THREAD_COUNT):
        threads[x].join()

    # minify the resulting json file
    # minify()
    # print("JSON file minified.")

    print("---- Scrapper ran for %s seconds ----" % (time.time() - start_time))
