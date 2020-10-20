from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import datetime, timedelta
import threading
import os

from settings import MAIL, PASSWORD, GECKODRIVER_PATH
from models import *

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', filename='core.log', filemode='w')

driver = None


def init():
	''' Webdriver initialization '''

	logging.info('Starting webdriver initialization')

	global driver
	opt = Options()
	# Start browser in virtual display
	opt.headless = True
	# Block micro and audio
	opt.set_preference("permissions.default.microphone", 2)
	opt.set_preference("permissions.default.camera", 2)
	# binary = FirefoxBinary(FIREFOX_BIN)  # Heroku

	# Init browser webdriver
	# try:
	driver = webdriver.Firefox(options=opt, executable_path=GECKODRIVER_PATH) #Local - '/usr/local/bin/geckodriver'
	# 	logging.info("Webdriver initializated")
	# except:
	# 	logging.critical("Webdriver initialization failed", exc_info=True)


def google_login():
	''' Google authorization '''

	logging.info('Starting Google authorization')

	# Get Google auth page
	driver.get('https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%3Fhs%3D193&&o_ref=https%3A%2F%2Fmeet.google.com%2Fjhg-pbdx-brz%3Fauthuser%3D1&_ga=2.238318663.697307376.1602849973-1269364394.1602849973&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
	logging.info('Get to google authorization page')

	try:
		# Find login field
		driver.find_element_by_id('identifierId').send_keys(MAIL)
		driver.find_element_by_id('identifierNext').click()
		logging.info('Sent mail key')
	except:
		logging.warning('Could not send mail key. Starting authorization again')
		google_login()

	try:
		# Wait form to be loaded
		WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.CLASS_NAME, 'ANuIbb.IdAqtf')))
		# Find password field
		driver.find_element_by_name('password').send_keys(PASSWORD)
		driver.find_element_by_id('passwordNext').click()
		logging.info('Sent password key')
	except:
		logging.warning('Could not send password key. Starting authorization again')
		google_login()

	logging.info("Google authorization success!")


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
		join_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.uArJ5e:nth-child(1)')))
		join_btn.click()
		logging.info(f'Successfully joined {meet}')
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


# start core
init()
google_login()
start_active()
