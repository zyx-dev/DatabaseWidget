# coding:utf8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

from_station = 'CS'
to_station = 'YY'
train_num = 'K966'
train_date = '2019-10-02'

ZYid = 'RW_240000K9671I'  # 通过浏览器找到要查询车票的三个id
ZEid = 'YW_240000K9671I'
WZid = 'YZ_240000K9671I'


def send_email(train_date, train_num, one_num, two_num, wz_num):  # 函数中邮箱信息改为自己的
    email_from = "276908083@qq.com"
    email_to = "276908083@qq.com"
    hostname = "smtp.qq.com"
    login = "276908083@qq.com"
    password = "19632506174+zyx@"
    subject = "train_tickets"
    text = ("日期:%s 车次:%s 软卧:%s 硬卧:%s 硬座:%s " % (train_date, train_num, one_num, two_num, wz_num))

    smtp = SMTP_SSL(hostname)
    smtp.login(login, password)

    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["from"] = email_from
    msg["to"] = email_to

    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.quit()


driver = webdriver.Edge()
driver.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E9%95%BF%E6%B2%99,CSQ&ts=%E7%9B%8A%E9%98%B3,AEQ&date=2019-10-02&flag=N,N,Y')
time.sleep(3)

# driver.find_element_by_id("fromStationText").clear()
# driver.find_element_by_id("fromStationText").send_keys(from_station)
# driver.find_element_by_id("fromStationText").send_keys(Keys.ENTER)
#
# driver.find_element_by_id("toStationText").clear()
# driver.find_element_by_id("toStationText").send_keys(to_station)
# driver.find_element_by_id("toStationText").send_keys(Keys.ENTER)  # 写入终点站
#
# js = "document.getElementById('train_date').removeAttribute('readonly')"  # 去除日期栏只读属性
# driver.execute_script(js)
#
# driver.find_element_by_id("train_date").clear()
# driver.find_element_by_id("train_date").send_keys(train_date)  # 写入乘车日期
# # driver.find_element_by_id("train_date").send_keys(Keys.ENTER)
# driver.find_element_by_class_name("icon icon-huochepiao").click()
#
# driver.find_element_by_class_name("btn btn-primary form-block").click()
# try:
#     driver.find_element_by_xpath('//*[@id="search_one"]').click()
# except Exception:
#     time.sleep(2)

query_times = 0
onetickets_last = 0
twotickets_last = 0
wztickets_last = 0

time.sleep(2)
while (1):
    query_times = query_times + 1
    text = ""
    try:
        driver.find_element_by_id("query_ticket").click()  # 根据查询键是否可以找到，以判断页面显示正确与否
    except Exception:
        driver.refresh()
        time.sleep(5)
        print("bug")
        continue

    print("第%d次查询:" % (query_times))
    time.sleep(5)

    try:
        text = driver.find_element_by_id(ZYid).text
    except Exception:
        driver.refresh()
        time.sleep(5)
        print("bug")
        continue
    if not driver.find_element_by_id(ZYid).text:
        driver.find_element_by_id("query_ticket").click()

    text = driver.find_element_by_id(ZYid).text  # 查询一等座余票
    if text == "有" or text == "无":
        onetickets_now = text
        print("%s 软卧 ： %s" % (train_num, onetickets_now))
        if onetickets_now != onetickets_last:
            onetickets_last = onetickets_now
        # send_email(train_date, train_num, onetickets_last, twotickets_last, wztickets_last)
    else:
        onetickets_now = text
        print("%s 软卧剩余票数 ： %s" % (train_num, onetickets_now))
        if onetickets_now != onetickets_last:
            onetickets_last = onetickets_now
        # send_email(train_date, train_num, onetickets_last, twotickets_last, wztickets_last)

    text = driver.find_element_by_id(ZEid).text  # 查询二等座余票
    if text == "有" or text == "无":
        twotickets_now = text
        print("%s 硬卧 ： %s" % (train_num, twotickets_now))
        if twotickets_now != twotickets_last:
            twotickets_last = twotickets_now
            # send_email(train_date, train_num, onetickets_last, twotickets_last, wztickets_last)
    else:
        twotickets_now = text
        print("%s 硬卧剩余票数 ： %s" % (train_num, twotickets_now))
        if twotickets_now != twotickets_last:
            twotickets_last = twotickets_now
            # send_email(train_date, train_num, onetickets_last, twotickets_last, wztickets_last)

    text = driver.find_element_by_id(WZid).text  # 查询无座余票
    if text == "有" or text == "无":
        wztickets_now = text
        print("%s 硬座 ： %s" % (train_num, wztickets_now))
        if wztickets_now != wztickets_last:
            wztickets_last = wztickets_now
            if wztickets_last != "候补":
                send_email(train_date, train_num, onetickets_last, twotickets_last, wztickets_last)
    else:
        wztickets_now = text
        print("%s 硬座剩余票数 ： %s" % (train_num, wztickets_now))
        if wztickets_now != wztickets_last:
            wztickets_last = wztickets_now
            if wztickets_last != "候补":
                send_email(train_date, train_num, onetickets_last, twotickets_last, wztickets_last)
    print("")
