import tkinter as tk

import urllib as url
import  urllib.request as ur
from bs4 import BeautifulSoup
import requests
import _thread as td
import os

class Frame(tk.Frame):
    def __init__(self, bg='black', width=100, height=100):
        super().__init__(master, bg='black', width=100, height=100)
        self.pack(ipadx=310, ipady=250)
        self.canvas =   tk.Canvas(self)
        self.start_btn  =   tk.Button(self.canvas, font=('黑体', 20, 'bold'), width=10, height=2, bg='#12FF12')

        self.canvas.create_text(240, 60, text='E-hentai-Spider', font=('宋体', 45, 'bold'))
        self.canvas.create_text(130, 110, text='Hentai位置:', font=('宋体', 30), fill='#FF12A1')
        self.canvas.create_text(130, 160, text='Hentai数量:', font=('宋体', 30), fill='#FF12A1')
        self.canvas.create_text(130, 220, text='开始序号:', font=('宋体', 30), fill='#FF12A1')

        self.start_area =   tk.Text(self.canvas, font=('黑体', 11), width=17, height=2, bg='gray', fg='#0000FF')     
        self.food   =   tk.Text(self.canvas, font=('黑体', 11), width=17, heigh=2, bg='gray', fg='#0000FF')   
        self.firnum = tk.Text(self.canvas, font=('黑体', 11), width=17, heigh=2, bg='gray', fg='#0000FF')
        self.path = tk.Text(self.canvas, font=('黑体', 7), width=15, heigh=3, bg='gray', fg='#0000FF') 
        self.reply  =   tk.Text(self.canvas, font=('黑体', 13), width=40, heigh=7, bg='gray', fg='#0000FF')
        
        self.canvas.pack(ipadx='200', ipady='345', fill='both')

        self.start_btn['command']   =   self.StartCommand                  
        self.start_btn['text']  =   'Start!'
        self.start_btn.pack(side='bottom')
        self.start_btn.place(x=200, y=400)
    
        self.start_area.pack()
        self.start_area.place(x=240, y=100)
        self.food.pack()
        self.food.place(x=240, y=150)
        self.firnum.pack()
        self.firnum.place(x=240, y=210)
        self.path.pack()
        self.path.place(x=400, y=180)
        self.reply.pack()
        self.reply.place(x=70, y=260)

    def StartCommand(self):
        try:
            td.start_new_thread( StartCommand_t, (self.start_area, self.food, self.firnum, self.path, self.reply,))
        except Exception:
            PutReply(self.reply, "多线程错误！")
            
def StartCommand_t(self_area, self_food, self_firnum, self_path, self_reply):
    path = str(self_path.get('1.0', '1.end'))
    os.mkdir(path)
    count = int(str(self_firnum.get('1.0', 'end')))
    num = path + "/" + str(count) + ".jpg"
    area = str(self_area.get('1.0', 'end'))
    food_info   =   str(self_food.get('1.0', 'end'))
    count_hentai = int(food_info)
    sum_c = count_hentai 
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/51.0.2704.63 Safari/537.36'}
    while count_hentai != 0:
        PutReply(self_reply, "解析地址:" + area)
        PutReply(self_reply, "当前将要处理:" + num + "     还剩:" + str(count_hentai))
        res  =   ur.Request(url=area, headers=headers)
        try:
            response = ur.urlopen(res, data=None, timeout = 3).read()
        except:
            PutReply(self_reply, "连接超时,重试..........")
            continue
        PutReply(self_reply, "地址解析完成.............")
        PutReply(self_reply, "正在下载图片.................................")
        soup = BeautifulSoup(response)
        tags_a = soup.find_all(id="next")
        area = tags_a[0].get('href')
        tags_img = soup.find_all(id="img")
        src = tags_img[0].get('src')
        img_r = requests.get(src, stream=True)
        PutReply(self_reply, "下载完成")
        PutReply(self_reply, "开始本地写入图片.........................")
        with open(num, 'ab') as fd:
            for chunk in img_r.iter_content():
                fd.write(chunk)
        count = count + 1
        PutReply(self_reply, "已写入" + num + "..................")
        num = path + "/" + str(count) + ".jpg"
        count_hentai = count_hentai - 1
        if count_hentai == 0:
            PutReply(self_reply, "完成任务!!!")
        else:
            PutReply(self_reply, "跳转下一页................................")

def PutReply(obj, reply_str):
    obj.config(state='normal')
    obj.insert('end', reply_str + '\n')
    obj.see('10000.0')
    obj.config(state='disabled')
            
            
            
root_frame    =   tk.Tk()
frame   =   Frame(master=root_frame)
frame.pack()
root_frame.title("hentai-spider")
root_frame.geometry("500x500+250+30")
root_frame.maxsize('500', '500')
root_frame.minsize('500', '500')
frame.mainloop()
