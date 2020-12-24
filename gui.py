#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 20:26:16 2020

@author: yu_hsuantseng
"""
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from rt_mart_category import main as rt
from nh_rt_mart_category import main as nh_rt
from momo import main as momo
from a_mart_category import main as a_mart 
import time


def confirm_callback():
    labelVar.set("選取商家:"+cb.get())
    if cb.get() == "RT_Mart":
        labelVar.set("RT Mart 開始爬取 !!!!")
        time.sleep(5)
        rt()
        labelVar.set("RT Mart 爬取完成")
    elif cb.get() == "RT_Neihu_Mart":
        labelVar.set("RT Neihu Mart 開始爬取 !!!!")
        time.sleep(5)
        nh_rt()
        labelVar.set("RT Neihu Mart 爬取完成")
    elif cb.get() == "A_Mart":
        labelVar.set("A Mart 開始爬取 !!!!")
        time.sleep(5)
        a_mart()
        labelVar.set("A Mart 爬取完成")
    else:
        labelVar.set("MOMO 開始爬取 !!!!")
        time.sleep(5)
        momo()
        labelVar.set("MOMO 爬取完成")
        
    
    
def cancel_callback():
    cb.current(0)
    labelVar.set(var.get())
    
    

window = tk.Tk()
window.title("Web crawler")
window.geometry('400x300')
window.configure(background='white')

h_label = tk.Label(window,text="Carrefour EC - 網站爬取")
h_label.pack()


msg_frame = tk.Frame(window)
msg_frame.pack(side=tk.TOP)
msg_label = tk.Label(msg_frame, text='請選取爬取店家')
msg_label.pack(side=tk.LEFT)


var = StringVar()
cb = Combobox(window,textvariable=var.get())
cb['value'] = ("RT_Mart","RT_Neihu_Mart","A_Mart","MOMO")
cb.current(0)
cb.pack(pady=10)

labelVar = StringVar()
label = Label(window,textvariable=labelVar)
labelVar.set(var.get())
label.pack()

calculate_btn = tk.Button(window, text='確定', command=confirm_callback)
cancel_btn = tk.Button(window, text='取消', command=cancel_callback)
calculate_btn.pack(padx=5,pady=5)
cancel_btn.pack(padx=5,pady=5)

window.mainloop()