<h2 align="center">easyMeet</h2>
<p align="center"><b>Join's Google Meet links for you 😴</b></p>

#### Bot for scheduling and entering Google Meet sessions automatically.

### How it works
Project is made using `Selenium` (which is a web testing library for Robot Framework that utilizes the Selenium tool internally) and `Flask` (Python backend library). We open a chromium app on server where we can add, create, open tabs and set browser operations and everything.
Using `Flask` as interface to create our schedule subjects and timers (meets) make it easy to use and understand.

### Installation guide for local usage and development
1. Open terminal on your PC
2. Clone the repo `https://github.com/DSH01/easyMeet.git`
3. Go inside the project directory
4. Create file `.env` file and add these lines:
```
MAIL=(your Google account email)
PASSWORD=(your Google account password)
DB_URI=(whatever db you are comfortable with)
APP_SECRET_KEY=(create your Flask secret key)
GOOGLE_CHROME_BIN=(path to your chrome binary. in my case - /usr/bin/google-chrome)
CHROMEDRIVER_PATH=(path to your chrome webdriver. in my case - /usr/local/bin/chromedriver)
```
As you can see, you should install Chrome binary and webdriver for selenium library - [installation guide](https://chromedriver.chromium.org/getting-started)

5. Install dependencies `pip3 install -r requirements.txt`
6. Start the application `gunicorn app:app -t 1200`

Now the project has started on `localhost:8000`


### Usage Guide
Now when you visit the page you will see 4 tabs in navbar 
- Home
- Google Login
- Logs
- Test

#### Home
On the home page you can add your subject table for easy usage.
Also, you can add timers on your meets. Set start time and end time - add whatever number of meets you want!

#### Google Login
On the Google Login page you can start authorization if it failed on boot (check logs).
Also, application core provide functionality to "recover" your account by phone number or if captcha appeared!
To check success of authorization - click "Check" and go to `Test` tab to see screenshot of myaccount.google.com

#### Logs
Pretty self-explanatory.

#### Test
On this tab you will see all operations of application core. **Check this tab to see Google login recover code!**


### Requirements
- [Python 3](https://www.python.org/downloads/) should be installed
- [Google Chrome](https://www.google.com/intl/en_in/chrome/) with version 70+


### If you want to see the whole process
On line `30` of `core.py` file you can see line `chrome_options.add_argument("--headless")`

If you want to see bot automatically opening the page and filling login values and joining meet link then you can comment that line.


### Deployment

If you want to deploy your instance of app you need it to set it up properly.
The main problem on deployment is that after deployment it will be hosted on different IP and when bot tries to sign in Google will ask to login again with `one time password`.
But application's core provide functionality to solve this problem. Check `Test` tab to see what excatly Google wants from you (phone code/captcha/number confiramtion) and set it in `Google Login` tab.

For example, here's a guide on [how to set up a project with Nginx + Gunicorn](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04#create-a-gunicorn-systemd-service-file) on AWS or similar services.
