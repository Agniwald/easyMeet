from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import datetime, timedelta
import threading
import os

from settings import MAIL, PASSWORD, GOOGLE_CHROME_BIN, CHROMEDRIVER_PATH
from models import *

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', filename='core.log', filemode='w')

driver = None


def init():
	''' Webdriver initialization '''

	logging.info('Starting webdriver initialization')

	global driver

	chrome_options = webdriver.ChromeOptions()
	chrome_options.binary_location = GOOGLE_CHROME_BIN
	# Start browser in virtual display
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_options.add_argument("--no-sandbox")
	# Block micro, audio, geolocation and notifications
	chrome_options.add_experimental_option("prefs", { \
		"profile.default_content_setting_values.media_stream_mic": 2, 
		"profile.default_content_setting_values.media_stream_camera": 2,
		"profile.default_content_setting_values.geolocation": 2, 
		"profile.default_content_setting_values.notifications": 2 
  	})

	# Init browser webdriver
	try:
		driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
		logging.info("Webdriver initializated")
	except:
		logging.critical("Webdriver initialization failed", exc_info=True)


def send_mail():
	''' Send mail key in google login form '''

	driver.find_element_by_name('Email').send_keys(MAIL)

	driver.save_screenshot("static/img/2.png")

	# If capthcha appeared - return False
	if 'identifier-captcha-input' in driver.page_source:
		logging.info('Captcha appeared')
		return False
	driver.find_element_by_id('next').click()
	logging.info('Sent mail key')
	return True


def send_captcha(text):
	''' If captcha appeared - send captcha key in google login form '''

	driver.find_element_by_id('identifier-captcha-input').send_keys(text)

	driver.save_screenshot("static/img/3.png")
	
	driver.find_element_by_id('submit').click()
	logging.info('Sent phone code key')



def send_phone_code(code):
	''' If recovery menu apeared - send phone code key in google login form '''

	logging.info("phone code" + code + driver.page_source)

	driver.find_element_by_id('idvPreregisteredPhonePin').send_keys(code)

	driver.save_screenshot("static/img/12.png")
	
	driver.find_element_by_xpath('//*[@id="submit"]').click()
	logging.info('Sent captcha and mail key')

	time.sleep(2)
	driver.save_screenshot("static/img/15.png")


def send_password():
	''' Send password key in google login form '''

	driver.save_screenshot("static/img/4.png")
	WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'Passwd')))

	driver.find_element_by_name('Passwd').send_keys(PASSWORD)
	driver.find_element_by_id('submit').click()
	logging.info('Sent password key')


def check_login():
	''' Check if google login was successful '''

	driver.save_screenshot("static/img/5.png")
	logging.info("here" + driver.page_source)

	if 'mSMaIe' in driver.page_source:
		driver.save_screenshot("static/img/6.png")
		driver.find_elements_by_class_name('mSMaIe')[1].click()
		driver.save_screenshot('static/img/11.png')
		return False

	driver.save_screenshot("static/img/8.png")
	return True


def google_login():
	''' Google authorization '''

	logging.info('Starting Google authorization')

	# Get Google auth page
	driver.get('https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%3Fhs%3D193&&o_ref=https%3A%2F%2Fmeet.google.com%2Fjhg-pbdx-brz%3Fauthuser%3D1&_ga=2.238318663.697307376.1602849973-1269364394.1602849973&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
	logging.info('Get to google authorization page')
	driver.save_screenshot("static/img/1.png")


def start_active():
	''' Re-start active timers '''

	logging.info('Re-start active timers')

	meets = db.session.query(ActiveTimer).all()
	now = datetime.now()

	for meet in meets:
		# If end of the meet is still in the future
		if meet.end > now:
			add_meet(meet)
			logging.info(f'Adding active meet {meet}')
		else:
			logging.info(f'{meet} is off time. Skipping.')


def join_meet(meet):
	''' Function to join meet by link '''

	logging.info(f'Joining the meet {meet}')

	needed_subject = Subject.query.filter_by(name=meet.name).first()
	try:
		# Get Meet Url
		driver.get(needed_subject.url)
		# Wait join button to appear 

		driver.save_screenshot("static/img/5.png")

		join_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.uArJ5e:nth-child(1)')))
		driver.save_screenshot("static/img/6.png")
		time.sleep(7)
		driver.save_screenshot("static/img/7.png")
		join_btn.click()
		driver.save_screenshot("static/img/8.png")
		logging.info(f'Successfully joined {meet}')
		time.sleep(5)
		driver.save_screenshot("static/img/9.png")
	except:
		logging.warning('Joining meet failed. Trying again.')
		join_meet(meet)


def leave_meet(meet):
	''' Leave meet and delete from the database'''

	driver.get("https://google.com") #TODO: Leave meet by clickling "End call" button
	
	local_meet_obj = db.session.merge(meet) # Handling diffrent session object issue
	db.session.delete(local_meet_obj)
	db.session.commit()
	logging.info(f'Left the meet ({meet}) and deleted from the database.')


def add_meet(meet):
	''' Add Timer by user time to join and leave meet by link '''

	now = datetime.now()

	# Calculate delay from current time and Get delays in seconds
	delay = (meet.start - now).total_seconds()
	end_delay = (meet.end - now).total_seconds()
	
	# Set Timers with calculated delays to join and leave meet
	start_thread = threading.Timer(delay, join_meet, [meet])
	start_thread.setName(str(meet.id))
	start_thread.start()

	end_thread = threading.Timer(end_delay, leave_meet, [meet])
	end_thread.setName(f"{meet.id} end")
	end_thread.start()

	logging.info(f'Adding meet {meet} to:')
	for t in threading.enumerate():
		logging.info(t)


def cancel_meet(thread_id):
	''' Cancel Timer object by name '''

	for t in threading.enumerate():
		if t.name == thread_id:
			t.cancel()
			logging.info(f'Canceling thread {thread_id}')
		elif t.name == f'{thread_id} end':
			t.cancel()
			logging.info(f'Canceling thread {thread_id} end')
		else:
			logging.warning(f'Did not find thread with id {thread_id}')
