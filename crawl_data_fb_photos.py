from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from selenium import webdriver
from pandas import DataFrame
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

browser = webdriver.Chrome(ChromeDriverManager().install())


def crawlPaperFromNIPS(page):

    browser.get('https://www.facebook.com/')
    # write email
    browser.find_element_by_id('email').send_keys('')
    # write password
    browser.find_element_by_id('pass').send_keys('')

    browser.find_element_by_name('login').click()
    time.sleep(5)

    browser.get('https://www.facebook.com/BinhLuanVeDangCongSan/photos/a.395284967296203/1912573778900640')

    time.sleep(5)
    check_break = 0
    post = browser.find_elements_by_xpath(
        "//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9')]")
    time.sleep(0.5)
    for p in post:
        try:
            text = str(p.get_attribute('innerHTML'))
            if check_break == 1:
                break
            if "Top Comments" in text or "Top comments" in text or "Most relevant" in text or "Most Relevant" in text:
                # browser.execute_script("arguments[0].scrollIntoView();", p)
                location = p.location
                pageYOffset = location['y']
                browser.execute_script("window.scrollTo(0, " + str(pageYOffset - 150) + ");")
                time.sleep(2)
                p.click()
                time.sleep(2)
                post1 = browser.find_elements_by_xpath(
                    "//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9')]")
                for pp in post1:
                    text = str(pp.get_attribute('innerHTML'))
                    if "All comments" in text or "All Comments" in text:
                        pp.click()
                        time.sleep(2)
                        check_break = 1
                        break
        except:
            pass

    while True:
        check = 0
        post = browser.find_elements_by_xpath(
            "//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9')]")
        time.sleep(0.5)
        try:
            for p in post:
                text = p.get_attribute('innerHTML')
                if "more comments" in text:
                    browser.execute_script("arguments[0].scrollIntoView();", p)
                    time.sleep(1.5)
                    p.click()
                    time.sleep(1.5)
                    check = 1
                    break
                elif "previous comments" in text:
                    browser.execute_script("arguments[0].scrollIntoView();", p)
                    time.sleep(1.5)
                    p.click()
                    time.sleep(1.5)
                    check = 1
                    break
        except:
            pass
        if check == 0:
            break

    while True:
        check_reply_cmt = 0
        try:
            post = browser.find_elements_by_xpath(
                "//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j')]")
            for p in post:

                text = str(p.get_attribute('innerHTML'))
                if "View" in text or "replies" in text or "reply" in text or "Replies" in text or "reply" in text:
                    if "Hide" not in text or "hide" not in text:
                        check_reply_cmt = 1
                        browser.execute_script("arguments[0].scrollIntoView();", p)
                        time.sleep(1.5)
                        p.click()
                        time.sleep(1.5)
        except:
            pass

        time.sleep(0.5)
        if check_reply_cmt == 0:
            break
        else:
            continue

    while True:
        check_see_cmt = 0
        post = browser.find_elements_by_xpath(
            "//div[contains(@class,'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab')]")

        time.sleep(0.4)
        for p in post:
            try:
                if "See more" in str(p.get_attribute('innerHTML')) or "See More" in str(p.get_attribute('innerHTML')):
                    browser.execute_script("arguments[0].scrollIntoView();", p)
                    time.sleep(1)
                    check_see_cmt = 1
                    p.click()
                    time.sleep(1.5)
            except:
                pass
        if check_see_cmt == 0:
            break

    keys = ['review_text', 'lable']

    list_temp = []
    post = browser.find_elements_by_xpath(
        "//div[@style='text-align: start;']")
    for p in post:

        element = p.find_elements_by_tag_name('a')
        if len(element) > 0:
            browser.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""",
                                   element[0])
        text = re.sub('<[^<]+?>', '', p.get_attribute('innerHTML'))
        message = {"review_text": text, "lable": -1}
        list_temp.append(message)

    df = DataFrame(list_temp, columns=['review_text', 'lable'])
    export_csv = df.to_csv(r'pandaresult.csv', index=None, header=True)
    print("Done!")

try:
    crawlPaperFromNIPS("")
except:
    pass
# finally:
#     browser.close()
#     browser.quit()
