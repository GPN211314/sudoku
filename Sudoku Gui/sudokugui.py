#!/usr/bin/env python
# coding:utf-8

import tkinter as tk
import base64
import os
import random
from tkinter import messagebox
from PIL import Image, ImageTk
import sudoku_calc
import sudoku
from icon import JPG_IMG, ICO_IMG


class Mygui:

    def __init__(self):
        # 记录当前已生成的题目个数
        self.count = 0
        self.coord = []
        self.value = [[0 for i in range(11)] for j in range(11)]
        self.ety = [[0 for i in range(11)] for j in range(11)]
        self.tmp = sudoku_calc.SD()
        self.tmp.pmt()

    def bind(self):
        value_ls = self.tmp.create_puzzle(self.count)
        infl1 = [0, 1, 2, 4, 5, 6, 8, 9, 10]
        infl2 = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
        rmlist1 = []
        rmlist2 = []
        for i in range(9):
            for j in range(9):
                self.value[infl1[i]][infl1[j]].set(value_ls[i][j])
                self.ety[infl1[i]][infl1[j]]['state'] = 'readonly'
                self.ety[infl1[i]][infl1[j]]['fg'] = 'red'
                rmlist2.append((i, j))

            # 保证每个区至少有两个挖空
            tmp_ls = list(range(9))
            coord_a = tmp_ls.pop(random.randint(0, 8))
            coord_b = tmp_ls.pop(random.randint(0, 7))
            rmlist1.append(tuple(map(lambda x, y: x+y, (int(coord_a/3), coord_a%3), infl2[i])))
            rmlist1.append(tuple(map(lambda x, y: x+y, (int(coord_b/3), coord_b%3), infl2[i])))

        # 随机生成18+num个空
        num = random.randint(12, 42)
        rmleft = set(rmlist2)
        rmleft.difference_update(set(rmlist1))

        # rmleft为除去那18个空外还剩余的位置
        left = list(rmleft)
        for i in range(num):

            # 再随机选择num个空添加到rmlist1,此时rmlist1有30-60对坐标
            rmlist1.append(left.pop(random.randint(0, len(left)-1)))
        for i in rmlist1:

            # 将rmlist1中坐标的点的值都置空
            self.value[infl1[i[0]]][infl1[i[1]]].set('')
            self.ety[infl1[i[0]]][infl1[i[1]]]['state'] = 'normal'
            self.ety[infl1[i[0]]][infl1[i[1]]]['fg'] = 'black'
            self.ety[infl1[i[0]]][infl1[i[1]]]['bg'] = '#F0F0F0'

        # 题目计数+1
        self.count += 1

    def check(self):
        hash_ls = [0, 1, 2, 4, 5, 6, 8, 9, 10]
        grid = [[0 for i in range(9)] for j in range(9)]

        # 输入不合法时报错
        for i in range(9):
            for j in range(9):
                grid[i][j] = self.value[hash_ls[i]][hash_ls[j]].get()
                if grid[i][j] not in list(map(str, list(range(1, 10)))):
                    messagebox.showerror('Result', 'Wrong Answer!')
                    return
                grid[i][j] = {int(grid[i][j])}

        row = []
        col = []
        part = []
        for i in range(9):
            row.append(sudoku.row_left(grid[i]))
            col.append(sudoku.row_left([rowig[i] for rowig in grid]))
            part.append(sudoku.row_left(sudoku.comb(grid, 3*(int(i/3)), 3*(i % 3))))
        if sudoku.isnone(row) and sudoku.isnone(col) and sudoku.isnone(part):
            messagebox.showinfo('Result', 'Perfect!')
        else:
            messagebox.showerror('Result', 'Wrong Answer!')


    def gui(self):
        root = tk.Tk()
        # 设置窗口宽度与高度不可变
        root.resizable(False, False)
        root.title("Sudoku")

        # 从文件中读取并解码生成临时图标，用完后立马删除
        tmp = open("tmp.ico", "wb+")
        tmp.write(base64.b64decode(ICO_IMG))
        tmp.close()
        #im = Image.open("tmp.ico")
        #img = ImageTk.PhotoImage(im)
        #root.tk.call('wm', 'iconphoto', root._w, img)
        root.iconbitmap('tmp.ico')
        os.remove("tmp.ico")
        tmp = open("tmp.jpg", "wb+")
        tmp.write(base64.b64decode(JPG_IMG))
        tmp.close()
        tmp_image = Image.open("tmp.jpg")
        photo = ImageTk.PhotoImage(tmp_image)
        label = tk.Label(root, image=photo)
        os.remove("tmp.jpg")
        # for i in range(11):
        #     root.rowconfigure(i,weight=1)
        #     root.columnconfigure(i,weight=1)
        # root.rowconfigure(11,weight=1)

        # 生成空格
        for i in range(11):
            for j in range(11):
                if i != 3 and i != 7 and j != 3 and j != 7:
                    self.value[i][j] = tk.StringVar()
                    self.ety[i][j] = tk.Entry(root, textvariable=self.value[i][j], width=2, font=90)
                    self.ety[i][j].grid(row=i, column=j, padx=12, pady=12, sticky='NSEW')

        # 生成第一个题目并显示
        self.bind()

        label.grid(row=0, column=0, rowspan=12, columnspan=11, sticky='NSEW')

        # 确定按钮
        submit_btn = tk.Button(root, text='OK', command=lambda:self.check())
        submit_btn.grid(row=11, column=9, pady=10, ipadx=30, columnspan=2)

        # next按钮
        next_btn = tk.Button(root, text='Next>', command=lambda:self.bind())
        next_btn.grid(row=11, column=0, pady=10, ipadx=20, columnspan=2)

        root.mainloop()


def main():
    sudokugui = Mygui()
    sudokugui.gui()


if __name__ == '__main__':
    main()
