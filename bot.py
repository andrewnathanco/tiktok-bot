from selenium.webdriver import ActionChains
import os
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium import webdriver
import time

# ask user for display name (not user name) (ditoo speaker vs ditoospeaker)
# display_name = str(input("Display Name for comment: "))
display_name = "Centric Media"

# ask user for tiktok url
#tiktok_url = str(input("Enter tiktok url: "))

# open chrom

options = webdriver.ChromeOptions()
options.add_argument('--log-level=3')
options.add_argument(f"--user-data-dir={os.getcwd()}\\profile")
mobile_emulation = {
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
bot = webdriver.Chrome(options=options, executable_path=CM().install())
a = ActionChains(bot)

bot.set_window_position(0, 0)
bot.set_window_size(414, 936)

url_file = open('urls.txt', "r")
urls = url_file.readlines()

for url in urls:
    print('--Liking comments for this post: ' + url)

    bot.get(url)

# pop up
print("waiting for popup")
time.sleep(5)
try:
    print("trying to disable popup")
    bot.find_element_by_xpath(
        f".//button[contains(@class, 'ButtonRefuseOpen')]").click()
finally:
    print("no pop up, skipping")

# click on comments
print("clicking on comments")
time.sleep(3)
bot.find_element_by_xpath(
    f".//div[contains(@class, 'DivComment')]").click()

found_comment = False
while not found_comment:
    # search for comment
    print("looking for comments")
    time.sleep(3)
    try:
        comment = bot.find_element_by_xpath(
            f".//*[text() = '{display_name}']")
        if (comment != None):
            print("found comment")
            found_comment = True
            comment_button = bot.find_element_by_xpath(
                f".//*[text() = '{display_name}']/../../../*/*[contains(@class, 'DivLikeWrapper')]")
            # like the comment
            time.sleep(3)
            comment_button.click()
            print("comment liked")
            break
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        comment = None
    finally:
        print("couldn't find comment, need to scroll")
        print("find last comment")
        # find last comment
        time.sleep(3)
        last_comment = bot.find_element_by_xpath(
            f".//div[contains(@class, 'DivCommentListContainer')][last()]")

        print("scroll to it")
        # scroll to it
        time.sleep(3)
        a.move_to_element(last_comment)
