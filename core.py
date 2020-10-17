from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import datetime, timedelta
import threading


opt = Options()
# Start browser in virtual display
opt.headless = True
# Block micro and audio
opt.set_preference("permissions.default.microphone", 2)
opt.set_preference("permissions.default.camera", 2)

# Init browser webdriver
driver = webdriver.Firefox(options=opt, executable_path='/usr/local/bin/geckodriver')


def google_login():
	''' Google authorization '''

	try:
		# Get Google auth page
		driver.get('https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%3Fhs%3D193&&o_ref=https%3A%2F%2Fmeet.google.com%2Fjhg-pbdx-brz%3Fauthuser%3D1&_ga=2.238318663.697307376.1602849973-1269364394.1602849973&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

		# Find login field
		driver.find_element_by_id('identifierId').send_keys('6123647@stud.nau.edu.ua')
		driver.find_element_by_id('identifierNext').click()

		# Wait form to be loaded
		WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.CLASS_NAME, 'ANuIbb.IdAqtf')))
		# Find password field
		driver.find_element_by_name('password').send_keys('d.sh.2001')
		driver.find_element_by_id('passwordNext').click()
	except Exception as e:
		print("google login\n",e)
		google_login()


def join_meet(url):
	''' Function to join meet by link '''

	try:
		# Get Meet Url
		driver.get(url)
		# Wait join button to appear
		join_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.uArJ5e:nth-child(1)')))
		join_btn.click()
	except Exception as e:
		print("join meet\n", e)


def add_meet(url, start, end):
	''' Add Timer by user time to join and leave meet by link '''

	now = datetime.now()

	# Calculate delay from current time and Get delays in seconds
	delay = (start - now).total_seconds()
	end_delay = (end - now).total_seconds()
	
	# Set Timers with calculated delays to join and leave meet
	threading.Timer(delay, join_meet, [url]).start()
	# Leave meet by redirect to any page
	threading.Timer(end_delay, lambda: driver.get("https://google.com")).start()


if __name__ == '__main__':
	# google_login()

	for meet in schedule:
		# add_meet(meet['url'], meet['start'], meet['end'])
