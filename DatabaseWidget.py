# _*_ coding:utf-8 _*_
from tkinter import *
import re
import os
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog, StringVar
import copy
import difflib
import pickle
from icon1 import img1
from icon2 import img2
import base64
import winsound
import selenium.webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import xlsxwriter
# import chardet

# 定义打开文件函数
def open_files():
    root.wm_attributes('-topmost', 0)
    global f_name                                                               # 声明全局变量
    global f_name1
    f_name = tkinter.filedialog.askopenfilenames(title='Open Files',            # 打开文件
                                                 filetypes=[('All Files', '*'), ('text file', '*.txt')])
    if len(f_name) == 1:                                                        # 如果第一次只打开一个文件，再执行一次打开文件
        f_name1 = tkinter.filedialog.askopenfilename(title='Open Files',
                                                     filetypes=[('All Files', '*'), ('text file', '*.txt')])
        return f_name, f_name1
    else:
        return f_name


# 定义第二次打开文件函数
def open_second_files():
    global f_name2
    f_name2 = tkinter.filedialog.askopenfilenames(title='Open Files',           # 只用在多文件比较
                                                  filetypes=[('All Files', '*'), ('text file', '*.txt')])
    return f_name2


# 定义弹窗函数
def on_click():
    global x
    winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)    # 弹窗声音
    x = xls_text.get()                                                                      # 获取输入框的值
    string = str("Eid : %s" % x)                                                            # 弹窗确认的字符串
    # print("xls名：%s" % (x))
    war = tk.messagebox.askyesno(title='Confirm?', message=string)                          # 弹窗按钮
    if war:
        save()
    else:
        print("不做处理")
    return x


# 定义用户名密码弹窗
class Pop(tk.Toplevel):                                                                     # 定义顶级窗口类
    var3: StringVar
    var1: StringVar                                                                         # 定义变量
    var2: StringVar

    def __init__(self):                                                                     # 定义子窗口
        super().__init__()
        self.title('Please enter your Username and Password')                               # 子窗口标题
        self.wm_attributes('-topmost', 1)
        self.pop_up_box()

    def pop_up_box(self):
        def close():
            self.destroy()                                                                  # 关闭登录窗口
            self.on_click_1()                                                               # 调用确认弹窗函数

        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        root1 = tk.Frame(self)                                                              # 子窗口框架
        root1.pack(fill="x")
        label4 = tk.Label(root1, text="Sign In to Gerrit Code Review at gerrit.ericsson.se", font=("Arial", 14),
                          bg='#EDEDED')                                                     # 第一行
        label4.pack()
        label2 = tk.Label(root1, text="Username: ", font=("Arial", 12), bg='#EDEDED')       # 第二行
        label2.pack()
        self.var1 = tk.StringVar()                                                          # 输入框中内容
        self.var1.set(name)
        entry1 = tk.Entry(root1, textvariable=self.var1, font=("Arial", 12), bg='#EDEDED', justify="center")
        entry1.pack()                                                                       # 用户名输入框
        label3 = tk.Label(root1, text="Password: ", font=("Arial", 12), bg='#EDEDED')       # 第三行
        label3.pack()
        self.var2 = tk.StringVar()                                                          # 输入框中的内容
        entry2 = tk.Entry(root1, textvariable=self.var2, font=("Arial", 12), bg='#EDEDED', justify="center", show='*')
        entry2.pack()                                                                       # 密码输入框
        label6 = tk.Label(root1, text="Product:  (e.g 6488/8823/4415g3)", font=("Arial", 12), bg='#EDEDED')  # 第四行
        label6.pack()
        self.var3 = tk.StringVar()                                                          # 输入框中的内容
        entry3 = tk.Entry(root1, textvariable=self.var3, font=("Arial", 12), bg='#EDEDED', justify="center")
        entry3.pack()                                                                       # 产品名输入框
        label5 = tk.Label(root1, text="   ", font=("Arial", 12), bg='#EDEDED')              # 空行
        label5.pack()
        button = tk.Button(root1, text='Confirm', font=("Arial", 12), justify="center", command=close)
        button.pack()                                                                       # 确认按钮
        label6 = tk.Label(root1, text="   ", font=("Arial", 12), bg='#EDEDED')              # 空行
        label6.pack()

    def on_click_1(self):
        global v1, v2, v3
        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        v1 = self.var1.get()                                                                # 获取用户名字符串
        v2 = self.var2.get()                                                                # 获取密码字符串
        v3 = self.var3.get()                                                                # 获取产品名称
        string = str("Username：%s \nProject ：%s " % (v1, v3))
        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        tk.messagebox.showinfo(title='Confirm?', message='Please use a wired network connection.')
        war1 = tk.messagebox.askyesno(title='Confirm?', message=string)                     # 弹窗字符串
        if war1:
            download()
        else:
            print("不做处理")


# 定义输入错误行号弹窗
class Pop1(tk.Toplevel):                                                                    # 定义顶级窗口类
    var4: StringVar                                                                         # 定义变量

    def __init__(self):                                                                     # 定义子窗口
        super().__init__()
        self.title('db_syntax_check helper')                                                # 子窗口标题
        self.pop_up_box1()
        self.wm_attributes('-topmost', 1)

    def pop_up_box1(self):
        def close():
            self.destroy()                                                                  # 关闭登录窗口
            self.on_click_11()                                                              # 调用确认弹窗函数

        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        root1 = tk.Frame(self)                                                              # 子窗口框架
        root1.pack(fill="x")
        label2 = tk.Label(root1, text="Please enter the number of error line", font=("Arial", 14),
                          bg='#EDEDED')                                                     # 第一行
        label2.pack()
        label3 = tk.Label(root1, text="Line number: ", font=("Arial", 12), bg='#EDEDED')    # 第二行
        label3.pack()
        self.var4 = tk.StringVar()                                                          # 输入框中内容
        self.var4.set('')
        entry1 = tk.Entry(root1, textvariable=self.var4, font=("Arial", 12), bg='#EDEDED', justify="center")
        entry1.pack()                                                                       # 行数输入框
        label6 = tk.Label(root1, text="   ", font=("Arial", 12), bg='#EDEDED')              # 空行
        label6.pack()
        button = tk.Button(root1, text='Confirm', font=("Arial", 12), justify="center", command=close)
        button.pack()                                                                       # 确认按钮
        label6 = tk.Label(root1, text="   ", font=("Arial", 12), bg='#EDEDED')              # 空行
        label6.pack()

    def on_click_11(self):
        global v4
        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        v4 = self.var4.get()                                                                # 获取行数
        string = str("Line number : %s" % v4)
        war1 = tk.messagebox.askyesno(title='Confirm?', message=string)                     # 弹窗字符串
        v4 = int(v4)
        if war1:
            db_syntax_check()
        else:
            print("不做处理")


# 定义错误行弹窗
class Pop2(tk.Toplevel):                                                                    # 定义顶级窗口类

    def __init__(self):                                                                     # 定义子窗口
        super().__init__()
        self.title('the wrong line')                                                        # 子窗口标题
        self.pop_up_box2()

    def pop_up_box2(self):
        def close():
            self.destroy()                                                                  # 关闭登录窗口

        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        root1 = tk.Frame(self)                                                              # 子窗口框架
        root1.pack(fill="x")
        label2 = tk.Label(root1, text=string5, font=("Arial", 11),
                          bg='#EDEDED')                                                     # 第一行
        label2.pack(anchor=W)
        label3 = tk.Label(root1, text=string6, font=("Arial", 11),
                          bg='#9ACD32')                                                     # 第二行
        label3.pack(anchor=W)
        label4 = tk.Label(root1, text=string7, font=("Arial", 11),
                          bg='#EDEDED')                                                     # 第三行
        label4.pack(anchor=W)
        button = tk.Button(root1, text='Confirm', font=("Arial", 12), justify="center", command=close)
        button.pack()                                                                       # 确认按钮
        label6 = tk.Label(root1, text="   ", font=("Arial", 11), bg='#EDEDED')              # 空行
        label6.pack()


# 检查文件是否重名
def check_filename_available(filename):
    n = [1]

    def check_meta(file_name):
        file_name_new = file_name
        if os.path.isfile(file_name):
            file_name_new = file_name[:file_name.rfind('.')]+'_'+str(n[0])+file_name[file_name.rfind('.'):]
            n[0] += 1
        if os.path.isfile(file_name_new):
            file_name_new = check_meta(file_name)
        return file_name_new
    return_name = check_meta(filename)
    return return_name


# 定义抓取band信息函数
def pv_fv():
    winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
    string = str("You will compare PV/FV with PL")                          # 弹窗确认字符串
    click = tk.messagebox.askyesno(title='Confirm?', message=string)        # 确认按钮

    if click:
        # 读取每个文件名
        for i in f_name:
            global data
            data = []
            data_list = []
            data_list1 = []
            data_list2 = []
            data_list3 = []
            data_list4 = []
            data_list5 = []
            data_list6 = []
            date = time.strftime(" %Y-%m-%d")

            # 读取文件的每一行
            try:
                with open(i, 'r') as log:
                    lines = log.readlines()
            except UnicodeDecodeError:
                with open(i, 'r', encoding='utf-8') as log:
                    lines = log.readlines()
            if '\n' not in lines[len(lines) - 1]:                           # 如果最后一行没有\n，则添加
                lines[len(lines) - 1] += '\n'

            e = 0
            for line in lines:
                line = re.sub('/\*.+\*/', '', line)                         # 删除文件注释
                if 'Â' in line:
                    line = re.sub('Â', ' ', line)
                data_list3.append(line)                                     # 将处理后的原始列表保存在data_list3中
                for _ in range(len(data_list3)):
                    if '\n' in data_list3:
                        data_list3.remove('\n')                             # 删除data_list3中的\n空行
                # 存储带band信息的行
                if line != '\n' and '/Band' in line:                        # 读取非空行而且带band信息的行
                    data_list.append(line)                                  # 将文件存在data_list
                # 存储多行数据
                    pattern = re.compile('^\s+\d+.*')                       # 定义以数字开头的行的规则
                    pattern2 = re.compile('^\s+\[-?\d+.*')                  # 定义以【开头的行的规则
                    pattern3 = re.compile('^\s+"+.*')                       # 定义以"开头的行的规则
                    for b in range(1, 65):                                  # 大约循环65次
                        if e+b < len(lines):
                            value = re.match(pattern, lines[e + b])
                            value2 = re.match(pattern2, lines[e + b])
                            value3 = re.match(pattern3, lines[e + b])
                            if value:
                                data_list.append(lines[e + b])              # 如果下一行符合规则，添加到data_list后面
                            elif value2:
                                if not lines[e + b].endswith('\n'):         # 如果末尾没有换行符，则添加
                                    lines[e + b] += '\n'
                                data_list.append(lines[e + b])
                            elif value3:
                                data_list.append(lines[e + b])
                            else:
                                break
                        else:
                            break
                e = e + 1
            data = copy.deepcopy(data_list)                                 # 将此环节的data_list存入data，避免随后面改动
            for line1 in data_list:
                line1 = re.sub('/Band\d{0,2}[._]?[A-Z]?[a-z]*', '', line1)  # 删除上一步的文件的band信息
                line1 = re.sub('\s.+\n$', '', line1)                        # 删除每行句子空格以后的内容
                data_list1.append(line1)                                    # 将文件存在data_list1
                for _ in data_list1:
                    if '' in data_list1:
                        data_list1.remove('')                               # 删除data_list1里的空行
                for line7 in data_list1:
                    if line7 not in data_list6:
                        data_list6.append(line7)
            d = 0
            # 存储平台信息的行
            for line3 in data_list6:
                for line2 in data_list3:
                    if line3 in line2:                                      # 在data_list3中查找含有data_list1的内容
                        data_list2.append(line2)                            # 将提取的内容存在data_list2的后面
                    # pattern4 = re.compile(r'(('+line3+')$).*')
                    # value4 = re.match(r'(('+line3+')$).*', line2)
                    # if value4:
                    #     data_list2.append(line2)
            # 存储平台的多行数据
                        pattern1 = re.compile('^\s+\d+.*')
                        pattern4 = re.compile('^\s+\[-?\d+.*')
                        pattern5 = re.compile('^\s+"+.*')
                        for c in range(1, 65):
                            if d+c < len(data_list3):
                                value1 = re.match(pattern1, data_list3[d+c])
                                value4 = re.match(pattern4, data_list3[d+c])
                                value5 = re.match(pattern5, data_list3[d+c])
                                if value1:
                                    data_list2.append(data_list3[d+c])
                                elif value4:
                                    data_list2.append(data_list3[d+c])
                                    for e in range(0, len(data_list2), 2):  # 将data_list2进行分组
                                        data_list4.append(data_list2[e:e + 2])
                                elif value5:
                                    data_list2.append(data_list3[d+c])
                                else:
                                    break
                            else:
                                break
                    d = d+1
                d = 0
            # 仅【开头的多行数据使用
            for line4 in data_list4:
                if line4 not in data_list5:                                 # 删除data_list4中重复的
                    data_list5.append(line4)
            for line5 in data_list5:
                for line6 in line5:
                    data_list.append(line6)
            # 其他情况使用
            for line4 in data_list2:
                if '\"' not in line4:
                    if line4 not in data_list:                              # 删除data_list2中重复的
                        data_list.append(line4)
                else:
                    data_list.append(line4)

            path = "C:\\Users\\" + x + "\\Desktop\\db\\PV_FV\\" + date + "\\"
            if not os.path.exists(path):                                    # 新建路径
                os.makedirs(path, 0o755)

            i = re.sub(r'C:.+/', '', i)                                     # 提取文件的文件名
            path = check_filename_available(path + i)
            try:
                with open(path, 'w+', encoding='utf-8') as target:          # 创建结果文件
                    if i == 'gpp3.txt':
                        target.writelines(data)
                    else:
                        target.writelines(data_list)                        # 存储文件
            except UnicodeEncodeError:
                with open(path, 'w+') as target:                            # 创建结果文件
                    if i == 'gpp3.txt':
                        target.writelines(data)
                    else:
                        target.writelines(data_list)                        # 存储文件

        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        string1 = str("The result folder named \'db\' on your desktop.")
        tk.messagebox.showwarning(title='Prompts', message=string1)
    else:
        print('PV/FV')


# diff比较两个文件
def two_products():
    global lin1
    global tit
    linn = []
    linn1 = []
    date = time.strftime(" %Y-%m-%d")

    path = "C:\\Users\\" + x + "\\Desktop\\db\\Two Products\\" + date + "\\"
    if not os.path.exists(path):                                                # 新建路径
        os.makedirs(path, 0o755)

    winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
    string = str("You will compare database with two products")                 # 弹窗确认字符串
    click = tk.messagebox.askyesno(title='Confirm?', message=string)
    table = {ord(gg): ord(tt) for gg, tt in zip(                                # 替换中文字符库
        u"‘’“”，×",
        u"''\"\",*")}

    if click:
        # 如果一次打开两个文件
        # if len(f_name) == 2 and 'f_name2' in locals().keys() is False:      # 第一次打开两个文件，没有第二次打开
        #     with open(f_name[0], 'r', encoding='UTF-8') as log:
        #         lin = log.readlines()
        #         for i in lin:
        #             i = i.translate(table)                                  # 替换中文字符
        #             linn.append(i)
        #     with open(f_name[1], 'r', encoding='UTF-8') as log1:
        #         lin1 = log1.readlines()
        #         for j in lin1:
        #             j = j.translate(table)
        #             linn1.append(j)
        #
        #     title = re.sub(r'C:.+/', '', f_name[0])                         # 提取文件的文件名
        #     title1 = re.sub(r'C:.+/', '', f_name[1])                        # 提取文件的文件名
        #     tit = re.sub('\..*', '', title1)                                # 生成html文件名
        #     html_path = check_filename_available(path + tit + '.html')
        #     with open(html_path, 'w+') as target:                           # 创建html文件
        #         target.write(hd.make_file(linn, linn1, fromdesc=title, todesc=title1, context=False))  # 定义标题，隐藏相同的
        #         target.close()

        # 分两次打开两个文件
        if len(f_name) == 1:
            try:
                with open(f_name[0], 'r') as log:                               # 打开第一个文件
                    lin = log.readlines()
                    for i in lin:
                        i = i.translate(table)
                        linn.append(i)
            except UnicodeDecodeError:
                with open(f_name[0], 'r', encoding='utf-8') as log:             # 打开第一个文件
                    lin = log.readlines()
                    for i in lin:
                        i = i.translate(table)
                        linn.append(i)
            try:
                with open(f_name1, 'r') as log1:                                # 打开第二个文件
                    lin1 = log1.readlines()
                    for j in lin1:
                        j = j.translate(table)
                        linn1.append(j)
            except UnicodeDecodeError:
                with open(f_name1, 'r', encoding='utf-8') as log1:              # 打开第二个文件
                    lin1 = log1.readlines()
                    for j in lin1:
                        j = j.translate(table)
                        linn1.append(j)

            # def get_encoding(file):
            #     with open(file, 'rb') as f:
            #         return chardet.detect(f.read())['encoding']
            # encoding = get_encoding(f_name[0])
            # print(encoding)

            title = re.sub(r'C:.+/', '', f_name[0])                             # 提取文件的文件名
            title1 = re.sub(r'C:.+/', '', f_name1)                              # 提取文件的文件名
            tit = re.sub('\..*', '', title1)
            html_path = check_filename_available(path + tit + '.html')
            try:
                with open(html_path, 'w+', encoding='utf-8') as target:         # 创建html文件
                    target.write(hd.make_file(linn, linn1, fromdesc=title, todesc=title1, context=False))   # 定义标题，不隐藏相同的
                    target.close()
            except UnicodeEncodeError:
                with open(html_path, 'w+') as target:                           # 创建html文件
                    target.write(hd.make_file(linn, linn1, fromdesc=title, todesc=title1, context=False))   # 定义标题，不隐藏相同的
                    target.close()
        # 分两次打开多个文件
        elif len(f_name2) != 0:
            r = -1
            for p in f_name:
                try:
                    with open(p, 'r') as log:                                   # 第一次打开多个文件
                        lin = log.readlines()
                        for i in lin:
                            i = i.translate(table)                              # 替换中文字符
                            linn.append(i)
                except UnicodeDecodeError:
                    with open(p, 'r', encoding='utf-8') as log:                 # 第一次打开多个文件
                        lin = log.readlines()
                        for i in lin:
                            i = i.translate(table)                              # 替换中文字符
                            linn.append(i)
                try:
                    with open(f_name2[r+1], 'r') as log1:                       # 第二次打开多个文件
                        lin1 = log1.readlines()
                        for j in lin1:
                            j = j.translate(table)
                            linn1.append(j)
                except UnicodeDecodeError:
                    with open(f_name2[r+1], 'r', encoding='utf-8') as log1:     # 第二次打开多个文件
                        lin1 = log1.readlines()
                        for j in lin1:
                            j = j.translate(table)
                            linn1.append(j)

                title = re.sub(r'C:.+/', '', p)                                 # 提取文件的文件名
                title1 = re.sub(r'C:.+/', '', f_name2[r+1])                     # 提取文件的文件名
                tit = re.sub('\..*', '', title1)
                html_path = check_filename_available(path + tit + '.html')
                try:
                    with open(html_path, 'w+') as target:                       # 创建html文件
                        target.write(hd.make_file(linn, linn1, fromdesc=title, todesc=title1, context=False))
                        target.close()
                except UnicodeEncodeError:
                    with open(html_path, 'w+', encoding='utf-8') as target:     # 创建html文件
                        target.write(hd.make_file(linn, linn1, fromdesc=title, todesc=title1, context=False))
                        target.close()
                linn = []
                linn1 = []
                r = r+1

        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        string1 = str("The result folder named \'db\' on your desktop.")
        tk.messagebox.showwarning(title='Prompts', message=string1)
    else:
        print('diff')


# 自动下载数据库
def download():
    root.wm_attributes('-topmost', 0)
    driver = selenium.webdriver.Edge()                                          # 调用Edge浏览器
    url = 'https://gerrit.ericsson.se/login/%23%2Fadmin%2Fprojects%2F%3Ffilter%3Dradio%252FxRU%252Fdatabase%252F'
    driver.get(url)
    date = time.strftime(" %Y-%m-%d")                                           # 读取现在日期

    driver.find_element_by_id("f_user").clear()                                 # 清空已填充的用户名
    time.sleep(0.5)
    driver.find_element_by_id("f_user").send_keys(v1)                           # 填写用户名
    driver.find_element_by_id("gerrit_body").click()                            # 点击空白处
    driver.find_element_by_id("f_pass").clear()                                 # 清空已填充的密码
    time.sleep(0.5)
    driver.find_element_by_id("f_pass").send_keys(v2)                           # 填写密码
    driver.find_element_by_id("b_signin").click()                               # 点击登录按钮
    time.sleep(8)

    def download_database():
        total_url = []
        total_url3 = []
        global tag1
        tag1 = []
        global tag2
        tag2 = []
        global db
        db = []
        global dbnames1
        dbnames1 = []
        global dbnames2
        dbnames2 = []

        web = driver.find_elements_by_xpath('//a[1][@class="gwt-Anchor"][@href]')           # 读取database页面所有db路径
        time.sleep(1)
        for gitweb in web:
            total_url.append(gitweb.get_attribute('href'))                                  # 将读取的路径存入total_url
        time.sleep(0.5)
        for gitweb_url in total_url:
            driver.get(gitweb_url)                                                          # 读取每个路径并点开
            print(gitweb_url)
            time.sleep(1.5)
            web6 = driver.find_element_by_xpath('/html/body/div[3]/a[6][@href]').get_attribute('href')   # 点开每个路径的tree
            driver.get(web6)
            time.sleep(1.5)
            if 'eventCtrlConfig' in gitweb_url:
                # driver.find_element_by_xpath('/html/body/div[5]/table/tr[5]/td[4]/a[1]').click()
                driver.get(
                    'https://gerrit.ericsson.se/gitweb?p=radio/xRU/database/eventCtrlConfig.git;a=tree;f=v01;h=034ebc453beef7a628cf66e5455a98da34f3443b;hb=HEAD')
                time.sleep(1)
                web3_1 = driver.find_elements_by_xpath('/html/body/div[6]/table/tr/td[4]/a[2][@href]')     # 读取每个history的路径
                time.sleep(1)
                for history in web3_1:
                    total_url3.append(history.get_attribute('href'))
                driver.get(
                    'https://gerrit.ericsson.se/gitweb?p=radio/xRU/database/eventCtrlConfig.git;a=tree;f=v02/deliv;h=efe90984f4ea0f1b1113f21ae05ce06dc9c25389;hb=HEAD')
                time.sleep(1)
                web3 = driver.find_elements_by_xpath('/html/body/div[6]/table/tr/td[4]/a[2][@href]')
                time.sleep(1)
            else:
                web3 = driver.find_elements_by_xpath('/html/body/div[5]/table/tr/td[4]/a[2][@href]')
                time.sleep(1)
            for history in web3:
                total_url3.append(history.get_attribute('href'))                            # 将读取的history路径存入total_url3
            time.sleep(1)

        for tree_url in total_url3:
            tree_url = re.sub(r'h=.*', '', tree_url)
            if v3 in tree_url:
                driver.get(tree_url)                                                        # 读取每个history路径，如果项目名在路径中，则点开
                time.sleep(1.5)
                # print(tree_url)
                try:
                    tag = driver.find_element_by_xpath('/html/body/table/tr[1]/td[3]/span/span[3]/a').text
                    tag1.append(tag)
                except NoSuchElementException:
                    try:
                        tag = driver.find_element_by_xpath('/html/body/table/tr[1]/td[3]/span/span[2]/a').text
                        if tag == 'master':
                            tag = ''
                        tag1.append(tag)
                    except NoSuchElementException:
                        try:
                            tag = driver.find_element_by_xpath('/html/body/table/tr[1]/td[3]/span/span[1]/a').text
                            if 'CAH' in tag:
                                tag1.append(tag)
                            else:
                                tag1.append('')
                        except NoSuchElementException:
                            tag1.append('')
                web4 = driver.find_element_by_xpath('/html/body/table/tr[1]/td[4]/a[1][@href]').get_attribute('href')
                driver.get(web4)
                time.sleep(1.5)
                if 'eventCtrlConfig' in tree_url:
                    dbname = driver.find_element_by_xpath('/html/body/div[5]/a[3]').text
                    if v3 not in dbname:
                        dbname = driver.find_element_by_xpath('/html/body/div[5]/a[4]').text
                    dbnames1.append(dbname)
                else:
                    dbname = driver.find_element_by_xpath('/html/body/div[5]/a[2]').text    # 读取database名字
                    dbnames1.append(dbname)
                time.sleep(1)
                if 'eventCtrlConfig' in dbname:
                    web2 = driver.find_element_by_xpath('/html/body/div[5]/a[3][@href]').get_attribute('href')
                elif 'evc_' in dbname:
                    web2 = driver.find_element_by_xpath('/html/body/div[5]/a[4][@href]').get_attribute('href')
                else:
                    web2 = driver.find_element_by_xpath('/html/body/div[5]/a[2][@href]').get_attribute('href')
                driver.get(web2)                                                            # 点开database的text页面
                time.sleep(2)
                db = driver.find_element_by_xpath('/html/body/pre').text                    # 将读取的text存在db里
                path = "C:\\Users\\" + x + "\\Desktop\\db\\Download\\" + v3 + date + "\\"
                if not os.path.exists(path):                                                # 新建路径
                    os.makedirs(path, 0o755)
                try:
                    with open(path + dbname, 'w+') as target:                               # 创建database文件
                        target.writelines(db)
                except UnicodeEncodeError:
                    with open(path + dbname, 'w+', encoding='utf-8') as target:             # 创建database文件
                        target.writelines(db)
                time.sleep(1)
                # print(dbname)

            else:
                if v3 == '8823' or v3 == '8836':
                    if 'ltuSwDbRru2212' in tree_url:
                        driver.get(tree_url)
                        time.sleep(1.5)
                        try:
                            tag = driver.find_element_by_xpath('/html/body/table/tr[1]/td[3]/span/span[2]/a').text
                            tag1.append(tag)
                        except NoSuchElementException:
                            try:
                                tag = driver.find_element_by_xpath('/html/body/table/tr[1]/td[3]/span/span[2]/a').text
                                if tag == 'master':
                                    tag = ''
                                tag1.append(tag)
                            except NoSuchElementException:
                                try:
                                    tag = driver.find_element_by_xpath('/html/body/table/tr[1]/td[3]/span/span[1]/a').text
                                    if 'CAH' in tag:
                                        tag1.append(tag)
                                    else:
                                        tag1.append('')
                                except NoSuchElementException:
                                    tag1.append('')
                        web5 = driver.find_element_by_xpath('/html/body/table/tr[1]/td[4]/a[1][@href]').get_attribute('href')
                        driver.get(web5)
                        time.sleep(1.5)
                        dbname = driver.find_element_by_xpath('/html/body/div[5]/a[2]').text
                        dbnames1.append(dbname)
                        web2 = driver.find_element_by_xpath('/html/body/div[5]/a[2][@href]').get_attribute('href')
                        time.sleep(1)
                        driver.get(web2)                                                    # 点开database的text页面
                        time.sleep(2)
                        db = driver.find_element_by_xpath('/html/body/pre').text            # 将读取的text存在db里
                        path = "C:\\Users\\" + x + "\\Desktop\\db\\Download\\" + v3 + date + "\\"
                        if not os.path.exists(path):                                        # 新建路径
                            os.makedirs(path, 0o755)
                        try:
                            with open(path + dbname, 'w+') as target:                       # 创建database文件
                                target.writelines(db)
                        except UnicodeEncodeError:
                            with open(path + dbname, 'w+', encoding='utf-8') as target:     # 创建database文件
                                target.writelines(db)
                        time.sleep(1)
                        # print(dbname)

    try:
        download_database()
    except NoSuchElementException:
        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        tik = tk.messagebox.showinfo(title='Warning', message='The network is poor. Please exit and try again.')
        if tik:
            driver.quit()
            quit()
    tag2 = tag1                                                                     # 将第一次的tag存在tag2里
    dbnames2 = dbnames1                                                             # 将第一次的dbname存在dbnames2里
    url2 = 'https://gerrit.ericsson.se/#/admin/projects/?filter=radio%252FxRU%252Fdatabase%252F,skip=25'
    driver.get(url2)
    time.sleep(3)
    try:
        download_database()
    except NoSuchElementException:
        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        tik = tk.messagebox.showinfo(title='Warning', message='The network is poor. Please exit and try again.')
        if tik:
            driver.quit()
            quit()

    for j in tag1:
        tag2.append(j)                                                              # 将第二次的tag存进tag2
    for jj in dbnames1:
        dbnames2.append(jj)
    path1 = "C:\\Users\\" + x + "\\Desktop\\db\\Download\\" + v3 + date + "\\"
    if not os.path.exists(path1):                                                   # 新建路径
        os.makedirs(path1, 0o755)
    workbook = xlsxwriter.Workbook(path1+'database_tag.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 42)                                                 # 设置行距
    worksheet.set_column('B:B', 21)
    row = -1
    col = 1
    c = 1
    e = 1
    for b in tag2:
        worksheet.write(row + c, col, b)                                            # 向B列写入
        c = c + 1
    for d in dbnames2:
        worksheet.write(row + e, col-1, d)                                          # 向A列写入
        e = e + 1
    workbook.close()
    time.sleep(0.5)

    winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
    string1 = str("The database folder named \'db\' on your desktop.")
    tk.messagebox.showwarning(title='Prompts', message=string1)
    driver.quit()


def db_syntax_check():
    root.wm_attributes('-topmost', 0)
    open_second_files()
    data_list6 = []
    numbers = []
    global string5
    global string6
    global string7

    for i in f_name2:
        # 读取文件的每一行
        with open(i, 'r', encoding='UTF-8') as log:
            lines = log.readlines()
        for line in lines:
            line = re.sub('/\*.+\*/', '', line)                                     # 删除文件注释
            if 'Â' in line:
                line = re.sub('Â', ' ', line)
            data_list6.append(line)                                                 # 将处理后的原始列表保存在data_list6中
        n = 0
        for _ in range(len(data_list6)):
            if data_list6[n] != '\n':
                number = data_list6.index(data_list6[n])
                numbers.append(number + 1)
            n = n + 1
        for _ in range(len(data_list6)):
            if '\n' in data_list6:
                data_list6.remove('\n')                                             # 删除data_list6中的\n空行
    if len(f_name2) != 0:
        string4 = str('There is a high probability of error in the second paragraph!')
        winsound.PlaySound("C:\\Windows\\media\\Windows Background.wav", winsound.SND_ASYNC)
        tk.messagebox.showwarning(title='Prompts', message=string4)
        string5 = str('Line ') + str(numbers[v4 - 3]) + str('：   ') + str(data_list6[v4 - 3])
        string6 = str('Line ') + str(numbers[v4 - 2]) + str('：   ') + str(data_list6[v4 - 2])
        string7 = str('Line ') + str(numbers[v4 - 1]) + str('：   ') + str(data_list6[v4 - 1])
        Pop2()
    else:
        print('不做处理')


# 保存输入值函数
def save():
    eid = xls_text.get()                                                        # 获取输入框的值
    t = open(data_path, 'wb')                                                   # 以二进制写模式打开目标文件
    pickle.dump(eid, t)                                                         # 将变量存储到目标文件中
    t.close()                                                                   # 关闭文件


# 主程序
# GUI界面
hd = difflib.HtmlDiff(wrapcolumn=105)                                           # 105个字符自动换行
root = tk.Tk()

# 左侧说明
bg = tk.Label(root, bg='#F2F2F2', width=69, height=300, font=("Arial", 11), justify=LEFT,
              text='                                         Welcome to use DatabaseWidget\n\n'
                   '                                                            User Guide\n\n'
                   '        1. Enter your Eid (lower case) and click \'Confirm\'.\n'
                   '        2. If you type incorrectly, click \'No\' in the popup window.\n'
                   '            If right, click \'Yes\'.\n\n'
                   '        Feature 1: Compare two products\n'
                   '            ①Open the files you want to compare.\n'
                   '                Please select one file first, open it and then select another.\n'
                   '                Also you can select several files first, then click \'Open Second Files\'\n'
                   '                to select another several files.\n'
                   '            ②Click \'Two Products\' and it will be generated one or more HTML.\n'
                   '            ③You can find the result folder named \'db\' on your desktop.\n\n'
                   '        Feature 2: Compare with platform\n'
                   '            ①Open the files you want to compare.\n'
                   '                You can select one or more files at a time.\n'
                   '            ②Click \'PV_FV\' and it will be generated one or more files with only band information.\n'
                   '            ③You can find the result folder named \'db\' on your desktop.\n\n'
                   '        Feature 3: Download database\n'
                   '            ①Click \'Download Database\', fill username, password and product in the popup window.\n'
                   '            ②Click \'Confirm\'. If right, click \'Yes\'. You can minimize all Windows.\n'
                   '            ③You can find the result folder named \'db\' on your desktop.\n\n'
                   '        Feature 4: db_syntax_check helper\n'
                   '            ①Go to the Jenkins to check db syntax.\n'
                   '            ②Click \'db_syntax_check helper\', fill line number in the popup window.\n'
                   '            ②Click \'Confirm\'. If right, click \'Yes\'.\n'
                   '            ③You can find the result in the popup window.\n\n'
                   '        Note:\n'
                   '            ①Html page display better after narrowing.\n'
                   '            ②If the webpage appears garbled, please switch the page encoding format.\n'
                   '            ③Due to my limited ability, please contact me if you meet any bugs.')
bg.pack(side='left')
bg1 = tk.Label(root, bg='#FFFFFF', width=100, height=300).pack(side='right')            # 窗口右侧背景色

# 定义按钮
btn1 = tk.Button(root, text='Open First Files', font=("Arial", 15),
                 width=15, height=2, command=open_files).place(x=980, y=215)            # 按钮一
btn2 = tk.Button(root, text="Two Products", font=("Arial", 14),
                 command=two_products).place(x=830, y=285, anchor=S)                    # 按钮二
btn3 = tk.Button(root, text="PV / FV", font=("Arial", 14),
                 command=pv_fv).place(x=830, y=365, anchor=S)                           # 按钮三
btn4 = tk.Button(root, text="Confirm", font=("Arial", 12),
                 command=on_click).place(x=830, y=170, anchor=S)                        # 按钮四
btn5 = tk.Button(root, text='Open Second Files', font=("Arial", 15),
                 width=15, height=2, command=open_second_files).place(x=980, y=330)     # 按钮五
btn6 = tk.Button(root, text="Download Database", font=("Arial", 14),
                 command=Pop).place(x=935, y=490, anchor=S)                             # 按钮六
btn7 = tk.Button(root, text="db_syntax_check helper", font=("Arial", 14),
                 command=Pop1).place(x=935, y=560, anchor=S)                            # 按钮七
root.title("DatabaseWidget                                                           Ver 4.1.3")  # 窗口标题
root.resizable(False, False)                                                            # 禁止更改窗口大小
root.geometry("1280x650")
root.wm_attributes('-topmost', 1)
# w, h = root.maxsize()
# root.geometry("{}x{}".format(w, h))
# root.state("zoomed")                                                                    # 窗口最大化

# 输入框
label = tk.Label(root, text="Eid : ", font=("Arial", 12), bg='#FFFFFF')                 # 输入框标题
label.place(x=810, y=60)                                                                # 输入框标题位置
xls_text = tk.StringVar()
xls = tk.Entry(root, textvariable=xls_text, font=("Arial", 12), bg='#EDEDED', justify="center")           # 输入框字体
xls.place(x=740, y=95)                                                                  # 输入框位置
label = tk.Label(root, text="Copyright © EXHZAUY from CBC1 Func.system",                # 底栏标注
                 font=("Arial", 11), fg='#808080', bg='#FFFFFF')
label.place(x=780, y=620)                                                               # 底栏位置

# 显示图片
tmp1 = open('C:\\Users\\Public\\icon1.ico', 'wb')
tmp2 = open('C:\\Users\\Public\\icon2.png', 'wb')                                       # 创建临时图片
tmp1.write(base64.b64decode(img1))
tmp2.write(base64.b64decode(img2))                                                      # 将64位base码编码成图片
tmp1.close()
tmp2.close()
photo2 = PhotoImage(file='C:\\Users\\Public\\icon2.png')                                # 读取编码后图片
eri_button = Label(image=photo2, bg='#FFFFFF').place(x=1130, y=10)                      # 图片位置
# root.iconbitmap('C:\\Users\\Public\\icon1.ico')
root.iconbitmap('C:\\Users\\Public\\icon1.ico')
# os.remove('2.png')


# 存储变量
data_path = 'C:\\Users\\Public\\eid.data'                                               # 存储位置
if os.path.exists(data_path):
    with open(data_path, 'rb') as f:                                                    # 以二进制读模式打开目标文件
        size = os.path.getsize(data_path)                                               # 读取文件大小
        if size == 0:
            name = ''
        else:
            name = pickle.load(f)                                                       # 将文件中的变量加载到当前工作区
else:
    g = open(data_path, 'wb+')
    name = ''
    g.close()
xls_text.set(name)                                                                      # 输出上一次输入的结果

root.mainloop()
