from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
import pandas as pd
import csv
from selenium import webdriver
from pandas import DataFrame
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())


def crawlPaperFromNIPS(page):

    browser.get('https://www.facebook.com/')
    browser.find_element_by_id('email').send_keys('0767552079')
    browser.find_element_by_id('pass').send_keys('q121222112300')
    # browser.find_element_by_id('email').send_keys('0903559750')
    # browser.find_element_by_id('pass').send_keys('taokhongbiet123')
    browser.find_element_by_name('login').click()
    time.sleep(5)

    browser.get('https://www.facebook.com/groups/1858836027673096/permalink/3030354247187929/')

    time.sleep(5)
    # browser.execute_script("window.scrollTo(" + str(
    #     browser.execute_script(
    #         'return window.pageYOffset;')) + ", 800);")
    check_all_comment = 0
    while True:
        check = 0

        if check_all_comment == 0:
            check_temp = 0
            post = browser.find_elements_by_xpath(
                "//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9')]")
            time.sleep(0.5)

            for p in post:

                if check_temp == 1:
                    break
                if "Top Comments" in str(p.get_attribute('innerHTML')) or "Top comments" in str(
                        p.get_attribute('innerHTML')):
                    location = p.location
                    pageYOffset = location['y']
                    browser.execute_script("window.scrollTo(0, " + str(pageYOffset - 149) + ");")
                    time.sleep(0.5)
                    p.click()
                    post1 = browser.find_elements_by_xpath(
                        "//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9')]")
                    for pp in post1:
                        if "All comments" in str(pp.get_attribute('innerHTML')) or "All Comments" in str(
                                pp.get_attribute('innerHTML')):
                            # location = pp.location
                            # pageYOffset = location['y']
                            # browser.execute_script("window.scrollTo(0, " + str(pageYOffset - 149) + ");")
                            # time.sleep(0.5)
                            pp.click()
                            time.sleep(2)
                            check_all_comment = 1
                            check_temp = 1
                            break

        post = browser.find_elements_by_xpath(
            "//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j keod5gw0 nxhoafnm aigsh9s9')]")
        time.sleep(0.5)

        for i in range(len(post)):
            if "more comments" in post[len(post) - i - 1].get_attribute('innerHTML'):
                post[len(post) - i - 1].click()
                time.sleep(2)
                check = 1
                break
            if "previous comments" in post[len(post) - i - 1].get_attribute('innerHTML'):
                post[len(post) - i - 1].click()
                time.sleep(2)
                check = 1
                break
        if check == 0:
            break

    while True:
        check_reply_cmt = 0
        post = browser.find_elements_by_xpath(
            "//span[contains(@class,'d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j')]")
        time.sleep(0.5)
        for p in post:
            try:
                if "View" in str(p.get_attribute('innerHTML')):
                    location = p.location
                    pageYOffset = location['y']
                    browser.execute_script("window.scrollTo(0, " + str(pageYOffset - 140) + ");")
                    time.sleep(0.5)
                    check_reply_cmt = 1
                    p.click()
                    time.sleep(1.5)
            except:
                pass
        if check_reply_cmt == 0:
            break

    while True:
        check_see_cmt = 0
        post = browser.find_elements_by_xpath(
            "//div[contains(@class,'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab')]")

        time.sleep(0.4)
        for p in post:
            try:
                if "See more" in str(p.get_attribute('innerHTML')) or "See More" in str(p.get_attribute('innerHTML')):
                    location = p.location
                    pageYOffset = location['y']
                    browser.execute_script("window.scrollTo(0, " + str(pageYOffset - 140) + ");")
                    time.sleep(0.5)
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


try:
    crawlPaperFromNIPS("")
except:
    pass
# finally:
#     browser.close()
#     browser.quit()
