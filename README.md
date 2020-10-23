<h2 align="center">easyMeet</h2>
<p align="center"><b>Join's Google Meet links for you 😴</b></p>

#### Bot for scheduling and entering Google Meet sessions automatically.

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
On home page you can add your subject table for easy usage.
Also, you can add timers on your meets. Set start time and end time - add whatever number of meets you want!

#### Google Login
On Google Login page you can start authorization if it failed on boot (check logs).
Also, application core provide functionality to "recover" your account by phone number or if captcha appeared!
To check success of authorization - click "Check" and go to `Test` tab to see screenshot of myaccount.google.com

### Requirements
- [Node.js](https://nodejs.org/en/download/) should be installed
- [Google Chrome](https://www.google.com/intl/en_in/chrome/) with version 70+
- Works only on windows (see [Issue #2](https://github.com/AmanRaj1608/Google-Meet-Scheduler/issues/8) for more info)

### If you want to see the whole process
On line `16` of `server.js` file you can see a variable name head=false;

If you want to see bot automatically opening the page and filling login values and joining meet link then you can set the headless as flase.

But while for deployment we need headless as true.


### Deployment

If you want to deploy your instance of app you need it to set it up properly.
The main problem on deployment is that after deployment it will be hosted on different IP and when bot tries to sign in Google will ask to login again with `one time password`. 

More details here [Issue #1](https://github.com/AmanRaj1608/Google-Meet-Scheduler/issues/1)

The option of deployment limits for apps like Heroku and Glitch. 


### Todo

You can however deploy it by creating an API that will ask for OTP and while sign-in you give that info to the server.
This can be implemented as a new branch especially for deployment purpose

### How it works
Project is made using [Puppeteer](https://developers.google.com/web/tools/puppeteer) which is a Node library which provides a high-level API to control headless Chrome or Chromium. We open a chromium app on server where we can add create open tabs see browser versions and everything.

So here we are using `puppeteer-extra` and `puppeteer-extra-plugin-stealth` which helps in creating an instance of chrome where google don't able to detect that it is created by puppeteer. So using this plugin we can login into google without filling capcha.
