#!/usr/bin/env python
#coding:utf-8

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
from icon import img_ico, img_jpg
import base64
import os
import sudoku
import random


class Mygui:

    def __init__(self):
        self.count = 0
        self.coord = []
        self.value = [[0 for i in range(11)] for j in range(11)]
        self.ety = [[0 for i in range(11)] for j in range(11)]
        self.tmp = sudoku.SD(0, 0, 0)
        self.tmp.pmt()

    def bind(self):
        value_ls = self.tmp.creat_pz(self.count)
        infl1 = [0, 1, 2, 4, 5, 6, 8, 9, 10]
        infl2 = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
        rmlist1 = []
        rmlist2 = []
        for i in range(9):
            for j in range(9):
                self.value[infl1[i]][infl1[j]].set(value_ls[i][j])
                self.ety[infl1[i]][infl1[j]]['state'] = 'readonly'
                self.ety[infl1[i]][infl1[j]]['fg'] = 'red'
                rmlist2.append((i,j))
            # 保证每个区至少有两个挖空
            ls = list(range(9))
            coord_a = ls.pop(random.randint(0, 8))
            coord_b = ls.pop(random.randint(0, 7))
            rmlist1.append(tuple(map(lambda x, y: x+y, (int(coord_a/3), coord_a%3), infl2[i])))
            rmlist1.append(tuple(map(lambda x, y: x+y, (int(coord_b/3), coord_b%3), infl2[i])))
        num = random.randint(12, 42)
        rmleft = set(rmlist2)
        rmleft.difference_update(set(rmlist1))
        left = list(rmleft)
        for i in range(num):
            rmlist1.append(left.pop(random.randint(0, len(left)-1)))
        for i in rmlist1:
            self.value[infl1[i[0]]][infl1[i[1]]].set('')
            self.ety[infl1[i[0]]][infl1[i[1]]]['state'] = 'normal'
            self.ety[infl1[i[0]]][infl1[i[1]]]['fg'] = 'black'
            self.ety[infl1[i[0]]][infl1[i[1]]]['bg'] = '#F0F0F0'
        self.count += 1

    def check(self):
        f = [0, 1, 2, 4, 5, 6, 8, 9, 10]
        grid = [[0 for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                grid[i][j] = self.value[f[i]][f[j]].get()
                if grid[i][j] not in list(map(str, list(range(1, 10)))):
                    messagebox.showerror('Result',  'Wrong Answer!')
                    return
                grid[i][j] = {int(grid[i][j])}

        row = []
        col = []
        part = []
        for i in range(9):
            row.append(self.tmp.rowleft(grid[i]))
            col.append(self.tmp.rowleft([rowig[i] for rowig in grid]))
            part.append(self.tmp.rowleft(sudoku.comb(grid, 3*(int(i/3)), 3*(i % 3))))
        if sudoku.isnone(row) and sudoku.isnone(col) and sudoku.isnone(part):
            messagebox.showinfo('Result', 'Perfect!!!')
        else:
            messagebox.showerror('Result', 'Wrong Answer!')

        # 检查填入的数是否合法
        # 检查行、列、区,加入set看len是否为9

    def gui(self):
        root = tk.Tk()
        # 设置窗口宽度与高度不可变
        root.resizable(False, False)
        root.title("Sudoku")
        tmp = open("tmp.ico","wb+")
        tmp.write(base64.b64decode(img_ico))
        tmp.close()
        #im = Image.open("tmp.ico")
        #img = ImageTk.PhotoImage(im)
        #root.tk.call('wm', 'iconphoto', root._w, img)
        root.iconbitmap('tmp.ico')
        os.remove("tmp.ico")
        tmp = open("tmp.jpg","wb+")
        tmp.write(base64.b64decode(img_jpg))
        tmp.close()
        im = Image.open("tmp.jpg")
        photo = ImageTk.PhotoImage(im)
        label = tk.Label(root, image=photo)
        os.remove("tmp.jpg")
        # for i in range(11):
        #     root.rowconfigure(i,weight=1)
        #     root.columnconfigure(i,weight=1)
        # root.rowconfigure(11,weight=1)

        for i in range(11):
            for j in range(11):
                if 3 != i and 7 != i and 3 != j and 7 != j:
                    self.value[i][j] = tk.StringVar()
                    self.ety[i][j] = tk.Entry(root, textvariable=self.value[i][j], width=2, font=90)
                    self.ety[i][j].grid(row=i, column=j, padx=12, pady=12, sticky='NSEW')
        self.bind()

        label.grid(row=0, column=0, rowspan=12, columnspan=11, sticky='NSEW')
        submit_btn = tk.Button(root, text='OK', command=lambda: self.check())
        submit_btn.grid(row=11, column=9, pady=10, ipadx=30, columnspan=2)
        next_btn = tk.Button(root, text='Next>', command=lambda: self.bind())
        next_btn.grid(row=11, column=0, pady=10, ipadx=20, columnspan=2)
        root.mainloop()


def main():
    sudokugui = Mygui()
    sudokugui.gui()


if __name__ == '__main__':
    main()
