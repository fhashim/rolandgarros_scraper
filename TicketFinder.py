import os
import requests
import time
from random import *

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

status_file = open('STATUS.txt', 'w')

delayTime = 3
audioToTextDelay = 10
filename = '1.mp3'
byPassUrl = "https://tickets.rolandgarros.com/sign-in"
googleIBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'
MAX_RETRIES = 5

username = ""
password = ""

option = webdriver.ChromeOptions()
option.add_argument('--disable-notifications')
option.add_argument("--mute-audio")
option.add_argument("--enable-javascript")
option.add_argument("--start-fullscreen")
option.add_argument(
    "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1")


def audioToText(mp3Path):
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(googleIBMLink)
    delayTime = 10
    time.sleep(1)
    root = driver.find_element_by_id(
        'root').find_elements_by_class_name(
        'dropzone _container _container_large')
    btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    btn.send_keys(r'D:\Rolando\audio\1.mp3')
    time.sleep(delayTime)
    time.sleep(audioToTextDelay)
    text = driver.find_element(By.XPATH,
                               '//*[@id="root"]/div/div[7]/div/div/div').find_elements_by_tag_name(
        'span')
    result = " ".join([each.text for each in text])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return result


def saveFile(content, filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)


def handle_captcha():
    driver.switch_to.default_content()
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)

    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    iframe1 = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe1)
    time.sleep(delayTime)

    try:
        googleClass = driver.find_elements_by_class_name('g-recaptcha')[
            0]
        time.sleep(delayTime)
    except:
        return

    iframe2 = googleClass.find_element_by_tag_name('iframe')
    time.sleep(2)
    iframe2.click()
    time.sleep(2)
    allIframesLen = driver.find_elements_by_tag_name('iframe')
    time.sleep(delayTime)
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(allIframesLen)):
        iframe_1 = driver.find_elements_by_tag_name('iframe')[index]
        driver.switch_to.frame(iframe_1)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element_by_id(
                'recaptcha-audio-button')
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            driver.switch_to.parent_frame()
            pass

    if audioBtnFound:
        breaker = 0
        while True:
            if breaker >= MAX_RETRIES:
                break
            try:
                href = driver.find_element_by_id(
                    'audio-source').get_attribute('src')
                response = requests.get(href, stream=True)
                saveFile(response, filename)
                response = audioToText(os.getcwd() + '/' + filename)
                time.sleep(delayTime)

                driver.switch_to.default_content()
                iframe_1 = driver.find_elements_by_tag_name('iframe')[0]
                driver.switch_to.frame(iframe_1)

                breaker += 1
                googleClass = \
                driver.find_elements_by_class_name('g-recaptcha')[0]
                time.sleep(delayTime)

                iframe_2 = driver.find_elements_by_tag_name('iframe')[
                    audioBtnIndex]
                driver.switch_to.frame(iframe_2)
                driver.implicitly_wait(delayTime)

                inputbtn = driver.find_element_by_id('audio-response')
                inputbtn.send_keys(response)
                inputbtn.send_keys(Keys.ENTER)
                try:
                    errorMsg = driver.find_elements_by_class_name(
                        'rc-audiochallenge-error-message')[0]
                    if errorMsg.text == "" or errorMsg.value_of_css_property(
                            'display') == 'none':
                        print("Success")
                        break
                except NoSuchElementException:
                    print("rc-audiochallenge-error-message not found!")
                    break

            except Exception as e:
                print(e)
                print('Caught. Need to change proxy now')
                return
    else:
        print('Button not found. This should not happen.')
        return


# ----------------------------------------------------------

while True:
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(),
                                  options=option)
        driver.get(byPassUrl)
        errors = driver.find_elements_by_class_name('cmsg')
        if len(errors) > 0:
            driver.close()
            driver.quit()
            time.sleep(60)
            continue
        else:
            break

    except:
        driver.quit()
        print('try after 15 minutes.')
        time.sleep(1500)
        driver = webdriver.Chrome(ChromeDriverManager().install(),
                                  options=option)
        driver.get(byPassUrl)

breaker = 0
while True:
    if breaker >= MAX_RETRIES:
        break
    try:

        login_elements = driver.find_elements_by_id("login")
        if len(login_elements) > 0:
            driver.find_element_by_id(username).send_keys(
                "hfurqan")
            driver.find_element_by_id("password").send_keys(password)

        time.sleep(delayTime)

        handle_captcha()
        time.sleep(10)

        driver.switch_to.default_content()
        driver.find_element_by_id("login").send_keys(username)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_id("submit-button").click()

        time.sleep(randrange(2, 6))
        driver.find_element_by_xpath(
            '//a[normalize-space(text())="Book now"]').click()
        time.sleep(10)

        breaker += 1

    except:
        continue
    finally:
        break

breaker = 0
while True:
    if breaker >= MAX_RETRIES:
        break
    try:
        driver.switch_to.default_content()
        time.sleep(5)
        iframe_test = driver.find_elements_by_tag_name('iframe')
        if len(iframe_test) > 0:
            handle_captcha()

        breaker += 1

        finals_box = driver.find_elements_by_class_name('round')
        latest_date = 'SAM June 4'
        if len(finals_box) > 0:
            latest_date = \
            finals_box[-1].find_elements_by_class_name('txt-date')[
                -1].get_attribute('innerHTML')

        iframe_test = driver.find_elements_by_tag_name('iframe')
        if len(iframe_test) > 0:
            handle_captcha()
            continue

        btn = driver.find_element_by_xpath(
            "//*[contains(text(), \'" + latest_date + "\')]")

        iframe_test = driver.find_elements_by_tag_name('iframe')
        if len(iframe_test) > 0:
            print('here')
            handle_captcha()

        driver.switch_to.default_content()
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(10)

        driver.switch_to.default_content()
        btn = driver.find_element_by_xpath(
            "//*[contains(text(), \'" + latest_date + "\')]")
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(5)

        iframe_test = driver.find_elements_by_tag_name('iframe')
        if len(iframe_test) > 0:
            handle_captcha()
        driver.switch_to.default_content()
        ticket_list = driver.find_element_by_class_name(
            'collection-list-2')
        ticket_cards_available = ticket_list.find_elements_by_xpath(
            "//*[contains(text(), 'From €')]")
        ticket_cards_sold = ticket_list.find_elements_by_xpath(
            "//div[contains(text(), 'Sold out')]")

        status = ''' 
        Date: {} 
        Total tickets: {} 
        \t Tickets Available: {}
        \t Tickets Sold : {}
        '''.format(latest_date,
                   len(ticket_cards_available) + len(ticket_cards_sold),
                   len(ticket_cards_available), len(ticket_cards_sold))

        print(status)
        status_file.write(status)
        break
    except NoSuchElementException:
        break
