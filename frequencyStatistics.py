# -*- coding: utf-8 -*-
import tkFileDialog, Tkinter, string, os
from tkSimpleDialog import *

# 本程序以I,II...来分解所给的文章，输入n计算n元文法的词频
root = Tkinter.Tk()
root.title('DataAnalysis')

file_opt = options = {}  # 打开文件的基本初始数据等
options['defaultextension'] = '.txt'
options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
options['initialdir'] = os.getcwd()
options['initialfile'] = 'bill_of_rights.txt'
options['parent'] = root
options['title'] = 'This is a title'
bt = []

num = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]  # 需要更多用于分篇章的符号可以在此添加
dict0 = {}
txtdata = []
txtdata.append({})


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # print path+' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        # print path+' 目录已存在'
        return False


# 定义要创建的目录
mkpath = os.path.join(os.getcwd(),"out")
filename = ''
filename0 = os.path.join(os.getcwd(),"out","text.txt")  # used for output


def compareItems((w1, c1), (w2, c2)):  # 比大小函数
    if c1 > c2:
        return - 1
    elif c1 == c2:
        return cmp(w1, w2)
    else:
        return 1


def fenjiecipin(n, tpl):
    global filename0
    global filename
    t = open(filename, "r")
    a = t.read()
    for ch in '!"#$%&()*+,-./:;<=>?@[\\]ˆ_\'{|}˜\n':  # 替换各种符号为空格
        a = string.replace(a, ch, ' ')
    s = a.split(' ')
    tot = 0
    filename0 = os.path.join(os.getcwd(),"dict.txt")
    number = 0
    listn = []
    tpn = ()

    for k in s:
        listn.append(k)
        lenthn = len(listn)
        if lenthn > n:
            listn = listn[lenthn - n:lenthn]
        if len(listn) == n:
            tpn = tuple(listn)
            try:
                dict0[tpn] = dict0[tpn] + 1
            except KeyError:
                dict0[tpn] = 1
            tot = tot + 1
        if k in num:
            del dict0[tpn]
            getlasttxt(tot, k, number, n, tpl)
            number = number + 1
            listn = []

    getlasttxt(tot, num[-1], number, n, tpl)
    t.close()
    Button4 = Tkinter.Button(tpl, text="The Matrix")
    Button4.bind('<Button-1>', lambda event: showmatrix(event, n, s))
    Button4.grid()


def showontext(event, a, name, n):
    ttt = Tkinter.Toplevel()
    lb = Tkinter.Label(ttt, text="DataRates of " + name)
    lb.grid()
    lb0 = Tkinter.Label(ttt, text="Level:" + str(n))
    lb0.grid()
    t = Tkinter.Text(ttt)
    t.insert(1.0, a)
    t.grid()


def showmatrix(event, n, s):  # 输出的矩阵区分大小写,显示每个分割符接下去的文章的n元文法字数统计
    words = []
    maxl = 9
    tp0 = []
    fenge = ''
    for k in s[:-1]:  # s最后1位的终止符号去掉
        if len(tp0) < n:
            tp0.append(k)
            continue
        if n == 1:
            tp0 = []
        else:
            tp0 = tp0[1:]
        tp0.append(k)
        tp = tuple(tp0)
        try:
            txtdata[-1][tp] = txtdata[-1][tp] + 1
        except KeyError:
            txtdata[-1][tp] = 1
        # tot=tot+1
        if not (tp in words):
            words.append(tp)
        if (tp[n - 1] in num):
            del txtdata[-1][tp]
            txtdata.append({})
            del words[-1]
            fenge = tp[n - 1]
            # dict0.clear()
        elif (fenge in tp):
            del txtdata[-1][tp]
            del words[-1]
        if len(str(words[-1])) > maxl:
            maxl = len(str(words[-1]))
    f = open(os.path.join(os.getcwd(),"matrix.txt"), 'w')
    f.write("The Words".ljust(maxl))
    for i in range(1, len(num) + 1):
        f.write(str(i))
        f.write("  ")
    f.write("\n")
    words.sort()
    for k in words:
        if k in txtdata[0]: continue
        f.write(str(k).ljust(maxl))
        for i in range(1, len(num) + 1):
            try:
                f.write(str(txtdata[i][k]).ljust(3))
            except KeyError:
                f.write("0  ")
        f.write("\n")
    ttt = Tkinter.Toplevel()
    te = open(os.path.join(os.getcwd(),"matrix.txt"), "r")
    a = te.read()
    lb = Tkinter.Label(ttt, text="Matrix")
    lb.grid()
    t = Tkinter.Text(ttt, width=maxl + 3 * len(num) + 1)
    t.insert(1.0, a)
    t.grid()


def getlasttxt(tot, k, number, n, tpl):  # 将上一篇记录进来的文章的词频算出来并直接输出，然后清空dict开始下一篇文章词汇的记录
    global filename0
    t0 = open(filename0, "w")
    qq = dict0.items()
    qq.sort(compareItems)  # 排序
    for kk in qq:
        t0.write(str(kk[0]))
        t0.write(':')
        qqq = float(kk[1]) / tot;
        t0.write(str(qqq))
        t0.write('\n')
    dict0.clear()
    tot = 0
    t0.close()
    t0 = open(filename0, "r")
    a = t0.read()
    btname = filename0
    bt.append(Tkinter.Button(tpl, text=filename0 + ":Rates"))
    bt[-1].bind('<Button-1>', lambda event: showontext(event, a, btname, n))
    bt[-1].grid()
    filename0 = os.path.join(os.getcwd(),"dict" + k + ".txt")
    t0.close()


def divideintpiece(event):  # 分解所给的文章
    mkdir(mkpath)  # 创建目录
    global filename
    textn = open(os.path.join(os.getcwd(),"out","text.txt"), 'w')
    if filename == '': sys.exit()
    t = open(filename, 'r')
    while True:  # 输出拆分的文件
        aline = t.readline()
        aline = aline[:-1]
        if aline in num:
            textn.close()
            filename1 = os.path.join(os.getcwd(),"out","text" + aline + ".txt")  # 输出的文档先需要建立一个out文件夹
            textn = open(filename1, 'w')
        elif aline == '':
            break
        else:
            textn.write(aline + '\n')
    textn.close()
    t.close()
    tpl = Tkinter.Toplevel()
    n = askinteger('variant', 'input a integer: ', initialvalue=1, parent=tpl)  # 用户输入“n”表示n元文法
    Button3 = Tkinter.Button(tpl, text=filename + ":RatesAnalysis")
    Button3.bind('<Button-1>', lambda event: showrates(event, n, tpl))
    Button3.grid(row=2)


def showrates(event, n, tpl):
    fenjiecipin(n, tpl)


def showfile(event):  # 显示打开的文件内容
    tt = Tkinter.Toplevel()
    global filename
    opened = open(filename, 'r')
    t = Tkinter.Text(tt)
    t.insert(1.0, opened.read())
    t.grid()


def askopenfile(event):  # 打开文件开始操作
    master = root
    global filename
    filename = tkFileDialog.askopenfilename(**file_opt)
    Button2 = Tkinter.Button(master, text="Divide File: " + filename)
    Button2['command']=lambda button=Button2:divideintpiece(button)
    Button2.grid(row=1)
    Button4 = Tkinter.Button(master, text="Show the opened file")
    Button4['command']=lambda button=Button4:showfile(button)
    Button4.grid(row=1, column=1)


Button1 = Tkinter.Button(root, text="Open a file")
Button1.bind('<Button-1>', askopenfile)
Button1.grid(row=0)

root.mainloop()
