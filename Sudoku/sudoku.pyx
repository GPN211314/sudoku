#!/usr/bin/env python
# coding:utf-8

import sys
import numpy as np
import time
from perm import all_perm


class SD:

    def __init__(self, flag, arg):
        # sudoku.txt文件句柄
        self.sudoku = open('sudoku.txt', 'w+')
        # 待解数独文件路径或待生成终局数
        self.arg = arg
        # -c -s 参数
        self.flag = flag
        # 第一行的初始状态
        self.first_row = list(range(1, 10))
        self.first_row.remove(8)
        self.tmp_row = [8]+self.first_row
        #
        self.cur = 1
        # 第一行右转数
        self.order = []
        # 第一行的全排列
        # self.perm = perm.all_perm
        # 标记空位
        self.mark = []
        # 记录在行方向各个数值的占用情况
        self.row = []
        # 记录在列方向各个数值的占用情况
        self.col = []
        # 记录在各区中各个数值的占用情况
        self.part = []
        # 用来保存单个数独题目
        self.a_plz = []

    # 将生成的每一种终局，写入文件
    def write2file(self, grid, i):
        if i != 0:
            self.sudoku.write("\n")
        for k in range(9):
            for j in range(9):
                if j != 0:
                    self.sudoku.write(" ")
                self.sudoku.write(str(grid[k][j]))
            self.sudoku.write("\n")

    # 对一种终局，交换其中一些行，衍生出其它终局
    def create_pz(self, n, perm):
        k = n % 40320
        tmp = int(n/40320)
        i = int(tmp/6)
        j = tmp % 6
        self.order = [0, 3, 6, 1, 4, 7, 2, 5, 8]
        grid345 = self.order[3:6]
        grid678 = self.order[6:]
        order_a = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
        self.order = self.order[:3] + \
            [grid345[order_a[i][0]], grid345[order_a[i][1]], grid345[order_a[i][2]]] + \
            [grid678[order_a[j][0]], grid678[order_a[j][1]], grid678[order_a[j][2]]]
        return self.create_grid(perm[k])

    # 对第一行不同的排列，生成不同的局面
    def create_grid(self, row):
        grid = []
        for slice_x in self.order:
            grid.append(row[-slice_x:]+row[:-slice_x])
        return grid

    '''
    # 生成第一行的全排列
    def permutation(self, a_row):
        if not a_row:
            self.perm.append(list(self.tmp_row))
            return
        for i in a_row:
            self.tmp_row[self.cur] = i
            self.cur += 1
            tmp_ls = list(a_row)
            tmp_ls.remove(i)
            self.permutation(tmp_ls)
            self.cur -= 1
        return

    def pmt(self):
        self.permutation(self.first_row)
    '''

    def create(self):
        number = int(self.arg)
        # self.pmt()
        perm = all_perm
        for i in range(number):
            self.write2file(self.create_pz(i, perm), i)
        self.sudoku.close()

    def find_next(self, row_n, col_n, head):
        part_n = find_part(row_n, col_n)
        for i in range(head, 10):
            if self.row[row_n][i] and self.col[col_n][i] and self.part[part_n][i]:
                return i
        return 0

    def rule(self, row_n, col_n, med):
        value = self.a_plz[row_n][col_n]
        part_n = find_part(row_n, col_n)
        self.row[row_n][value] = med
        self.col[col_n][value] = med
        self.part[part_n][value] = med

    def create_mark(self):
        for i in range(9):
            for j in range(9):
                if self.a_plz[i][j] == 0:
                    # 所有的空格标为True
                    self.mark[i][j] = True
                else:
                    # 非空的将其三个约束列表置False
                    self.rule(i, j, False)

    def solve(self, row_n, col_n):
        # 如果当前列超出总列数则进入下一行第一列
        if col_n == 9:
            row_n += 1
            col_n = 0
        # 直到找到一个空格
        while True:
            # 若遍历完仍没有空，说明已完成填空，返回
            if row_n > 8:
                return True
            if self.mark[row_n][col_n]:
                break
            col_n += 1
            if col_n == 9:
                row_n += 1
                col_n = 0
        while True:
            self.a_plz[row_n][col_n] = self.find_next(row_n, col_n, self.a_plz[row_n][col_n] + 1)
            if self.a_plz[row_n][col_n] == 0:
                break
            self.rule(row_n, col_n, False)
            tmp_flag = self.solve(row_n, col_n+1)
            if tmp_flag:
                return True
            self.rule(row_n, col_n, True)
        return False

    def core(self):
        # 初始化列表
        self.mark = np.zeros([10, 10], bool)
        self.row = np.ones([10, 10], bool)
        self.col = np.ones([10, 10], bool)
        self.part = np.ones([10, 10], bool)
        # 将所有未填的空标为True
        self.create_mark()
        if not self.solve(0, 0):
            print("文件中存在无解数独")
            sys.exit(0)

    # 解当前的问题，并写入解文件
    def solve_part(self):
        self.core()
        for i in range(9):
            for j in range(9):
                if j != 0:
                    self.sudoku.write(" ")
                self.sudoku.write(str(self.a_plz[i][j]))
            self.sudoku.write("\n")

    # 每次从文件中读取一个问题并将终局写入解文件
    def detach(self):
        puzzle_file = open(self.arg)
        k = 0
        for line in puzzle_file:
            if k == 9:
                k = 0
                # 求解:
                self.solve_part()
                self.sudoku.write("\n")
                self.a_plz = []
            else:
                self.a_plz.append(list(map(int, line.split())))
                k += 1
        self.solve_part()
        puzzle_file.close()
        self.sudoku.close()

    def main(self):
        time_start = time.time()
        if self.flag == '-c':
            self.create()
        elif self.flag == '-s':
            self.detach()
        time_end = time.time()
        print("总时长：", time_end - time_start, "s")


def find_part(row_n, col_n):
    return 3*int(row_n/3)+int(col_n/3)
