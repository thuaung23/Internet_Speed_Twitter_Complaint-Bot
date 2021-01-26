from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

"""
By using selenium, automate to check the internet speed and 
  tweet automatically by tagging the internet service provider if results are lower than promised speed. 
Time.sleep is used to delay to cover page loading and speed testing. 
Chrome driver can be downloaded from https://chromedriver.chromium.org/.
P.S. Check your chrome version before starting to download.
"""

chrome_driver_path = "Your_Chrome_Driver_Path"
TWT_EMAIL = "Your_Username/Email"
TWT_PASSWORD = "Your_Password"
PROMISED_DOWN = "Your_Download_Speed_From_Provider"
PROMISED_UP = "Your_Upload_Speed_From_Provider"


class InternetSpeedTwitterBot:

    def __init__(self, executable_path):
        self.driver = webdriver.Chrome(executable_path)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        # Go to speedtest website.
        self.driver.get("https://www.speedtest.net/")
        # Get hold of go button.
        go_button = self.driver.find_element_by_class_name("start-text")
        # Page loading takes time so click the button after 5 seconds.
        time.sleep(5)
        go_button.click()
        # Speed testing takes times so wait 40s before accessing results.
        time.sleep(40)
        # Get hold of download speed by using xpath.
        self.down = self.driver.find_element_by_xpath("/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]"
                                                        "/div/div[3]/div/div/div[2]/div[1]"
                                                        "/div[2]/div/div[2]/span").text
        # Get hold of upload speed.
        self.up = self.driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]'
                                                      '/div/div[3]/div/div/div[2]/div[1]/div[3]/div'
                                                      '/div[2]/span').text
        # Compare if results are lower than promised speed.
        if float(self.down) < PROMISED_DOWN and float(self.up) < PROMISED_UP:
            # If yes, call function to tweet.
            self.tweet_at_provider(TWT_EMAIL, TWT_PASSWORD)
        # If not, simply return the results without calling tweet function.
        else:
            print(f"Your internet speed is as the contract.\n{self.down}down/{self.up}up.")
            return self.down, self.up

    def tweet_at_provider(self, username, password):
        # Go to twitter login webpage.
        self.driver.get("https://twitter.com/login")
        # Wait for page loading.
        time.sleep(3)
        # Get hold of username box and automatically type in the username/email.
        email_box = self.driver.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]"
                                                      "/form/div/div[1]/label/div/div[2]/div/input")
        email_box.send_keys(username)
        # Get hold of password box and automatically type in the password.
        pass_box = self.driver.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]"
                                                      "/form/div/div[2]/label/div/div[2]/div/input")
        pass_box.send_keys(password)
        # Wait for typing to finish.
        time.sleep(3)
        # Press enter.
        pass_box.send_keys(Keys.ENTER)
        # Wait for page loading.
        time.sleep(5)
        # Get hold of tweet box.
        tweet_box = self.driver.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]"
                                                       "/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div"
                                                       "/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div"
                                                       "/div/div")
        # Type in the message.
        tweet_box.send_keys(f"Hey @comcast, why is my internet speed {self.down}down/{self.up}up when I am paying "
                            f"for {PROMISED_DOWN}down/{PROMISED_UP}up?")
        time.sleep(2)
        # Get hold of tweet button.
        twt_button = self.driver.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]"
                                                       "/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div"
                                                       "/div[2]/div/div/span/span")
        # Click on it.
        twt_button.click()
        # Wait for page to load.
        time.sleep(2)
        # Quit automatically.
        self.driver.quit()


# Create the object.
bot = InternetSpeedTwitterBot(chrome_driver_path)
# Trigger the function.
bot.get_internet_speed()


