import os
import requests
import time
from bs4 import BeautifulSoup

def notify(title, text):
	os.system("""
			  osascript -e 'display notification "{}" with title "{}"'
			  """.format(text, title))

def checkChange(title, text, oldTitle, oldText):
	try:
		oldString = oldTitle + oldText
		newString = title + text
		return oldString != newString
	except:
		return False

startTime = time.time()
oldTitle = None
oldText = None

while True:
	response = requests.get('https://www.thegradcafe.com/survey/index.php?q=computer+science')
	try:
		soup = BeautifulSoup(response.content, 'html.parser')
		records = soup.select("table > tr")
		content = []

		for record in records:
			instContent = record.select("td.tcol1")
			inst = instContent[0].text

			descContent = record.select("td.tcol6 li")
			desc = descContent[1].text

			content.append({
					"inst": inst,
					"desc": desc
				})

		latestPost = content[0]
		changed = checkChange(latestPost["inst"], latestPost["desc"], oldTitle, oldText) 

		if oldTitle is None or changed:
			notify(latestPost["inst"], latestPost["desc"])
			oldTitle = latestPost["inst"]
			oldText = latestPost["desc"]
	except Exception as e:
		print(e)
	time.sleep(60.0 - ((time.time() - startTime) % 60.0))

