import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json



big_json = {}


driver = webdriver.Chrome()
driver.get("https://www.nytimes.com/crosswords/game/mini")

start_button = driver.find_element_by_class_name("buttons-modalButton--1REsR")
start_button.click()

cell_container = driver.find_element_by_css_selector('[data-group="cells"]')
cells = cell_container.find_elements_by_tag_name("g")

x = 1
y = 1
cell_objs = []
for cell in cells:
    temp = {'x': x, 'y': y, 'color': cell.find_element_by_tag_name("rect").get_attribute("fill"), 'key': ""}

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
    temp = {'x': x, 'y': y,
            'color': cell.find_element_by_tag_name("rect").get_attribute("fill"), 'key': "", 'solution': ""}

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
big_json['date'] = str(datetime.date.today())


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


append_to_json(big_json, "Data/data.json")

driver.delete_all_cookies()
driver.close()
