import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json

big_json = {}

driver = webdriver.Chrome()

#Adds the current link's puzzle to data.json
def getCrossword(puzzleLink):
	driver.get(puzzleLink)
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

	##driver.delete_all_cookies()
	return

#Iterating through days
def calendarForward(day,month,year):
	day += 1
	#Incrementing the month and resetting day in beginning of a month
	if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12: # 31 day months
		if day == 32:
			month += 1
			day = 1
	elif month == 4 or month == 6 or month == 9 or month == 11: # 30 day months 
		if day == 31:
			month += 1
			day = 1
	elif month == 2: # February
		if year % 4 == 0: # 29 day 
			if day == 30:
				month += 1
				day = 1
		else: # 28 day 
			if day == 29:
				month += 1
				day = 1
	#Incrementing the year and resetting month in beginning of a year
	if month == 13:
		year += 1
		month = 1
	return day,month,year

#Login into account
driver.get("https://myaccount.nytimes.com/auth/login?URI=")
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
username.send_keys("erkutalakus@gmail.com")
password.send_keys("ea22461016")
driver.find_element_by_id("submitButton").click()

#This is for the green ad, it disappears after some time so this loops wait it to disappear
########## CHANGE HERE !!! ###############
i = 0
while i < 150000000:
	i = i + 1
print("I'm ready")
##########################################

#Starting date
year = 2014
month = 8
day = 21
count = 5 #Day count, its initially thursday

#Calculating todays day in integer format to determine the boundary
todayDate = datetime.date.today().year * 10000 + (datetime.date.today().month * 100) + datetime.date.today().day

#Iterate though history
while (year *10000 + month * 100 + day) <= todayDate:

	#If current day is Saturday
	if count % 7 == 0: # Skip Saturdays
		day,month,year = calendarForward(day,month,year)
		count += 1

	#Build the current date as a string
	puzzleDate = "" + str(year) + "/"
	if month < 10:
		puzzleDate += "0"
	puzzleDate += "" + str(month) + "/" 
	if day < 10:
		puzzleDate += "0"
	puzzleDate += "" + str(day) + "/" 

	#Concatinate date with link
	puzzleLink = "https://www.nytimes.com/crosswords/game/mini/"
	puzzleLink += puzzleDate
	getCrossword(puzzleLink)

	#Increment date and day count
	count += 1
	day,month,year = calendarForward(day,month,year)

#Exit
driver.delete_all_cookies()
driver.close()

