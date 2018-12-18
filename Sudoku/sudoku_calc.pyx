#!/usr/bin/env python
# coding:utf-8

import sys
import time
from libc.stdio cimport FILE, fopen, fclose, fputs, fgets, feof, fputc

cdef class SD:
    cdef FILE* sudoku
    cdef list first_row, tmp_row, order, a_plz, perm, uncertain_ls#, mark, row, col, part
    cdef str flag, arg
    cdef int cur
    cdef int count, length
    cdef char string[1000200]
    cdef bint mark[11][11], row[11][11], col[11][11], part[11][11]

    def __init__(self, flag="", arg=""):
        # sudoku.txt文件句柄
        self.sudoku = fopen('sudoku.txt', 'w+')
        if self.sudoku == NULL:
            print("打开文件失败")
            sys.exit(0)
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
        self.perm = []
        # 标记空位
        # self.mark = []
        # 记录在行方向各个数值的占用情况
        # self.row = []
        # 记录在列方向各个数值的占用情况
        # self.col = []
        # 记录在各区中各个数值的占用情况
        # self.part = []

        # 用来保存单个数独题目
        self.a_plz = []
        # 写文件时计数
        self.count = 0
        # 记录空位，并把空位按可能解个数从小到大排序
        self.uncertain_ls = []


    # 将生成的每一种终局，写入文件
    cdef void write2file(self, list grid,int i):
        cdef int k
        cdef int j
        if i != 0:
            self.string[self.count] = ord('\n')
            self.count += 1
            # fputs("\n", self.sudoku)
        for k in range(9):
            for j in range(9):
                if j != 0:
                    self.string[self.count] = ord(' ')
                    self.count += 1
                    # fputs(" ", self.sudoku)
                self.string[self.count] = grid[k][j] + 48
                self.count += 1
                # fputc(grid[k][j] + 48, self.sudoku)
            self.string[self.count] = ord('\n')
            self.count += 1
        #self.string[self.count] = ord('\0')
        #fputs(self.string, self.sudoku)
        # fputs("\n", self.sudoku)

    def create_puzzle(self, n):
        return self.create_pz(n)
    # 对一种终局，交换其中一些行，衍生出其它终局
    cdef list create_pz(self, int n):
        cdef int k = n % 40320
        cdef int tmp = n//40320
        cdef i = tmp//6
        cdef j = tmp % 6
        self.order = [0, 3, 6, 1, 4, 7, 2, 5, 8]
        cdef list grid345 = self.order[3:6]
        cdef list grid678 = self.order[6:]
        cdef list order_a = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
        self.order = self.order[:3] + \
            [grid345[order_a[i][0]], grid345[order_a[i][1]], grid345[order_a[i][2]]] + \
            [grid678[order_a[j][0]], grid678[order_a[j][1]], grid678[order_a[j][2]]]
        return self.create_grid(self.perm[k])

    # 对第一行不同的排列，生成不同的局面
    cdef list create_grid(self,list row):
        cdef list grid = []
        for slice_x in self.order:
            grid.append(row[-slice_x:]+row[:-slice_x])
        return grid

    # 生成第一行的全排列
    cdef void permutation(self,list a_row):
        cdef list tmp_ls
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

    def  pmt(self):
        self.permutation(self.first_row)

    cdef void create(self):
        cdef int number = int(self.arg) - 1 
        cdef int i
        self.pmt()
        for i in range(number):
            self.write2file(self.create_pz(i), i)
            if self.count > 1000000:
                self.string[self.count] = ord('\0')
                fputs(self.string, self.sudoku)
                self.count = 0
        self.write2file(self.create_pz(number), number)
        self.string[self.count] = ord('\0')
        fputs(self.string, self.sudoku)
        fclose(self.sudoku)

    cdef int find_next(self, int row_n, int col_n, int head):
        cdef int part_n
        cdef int i
        for i in range(head, 10):
            if self.row[row_n][i] and self.col[col_n][i]:
                part_n = find_part(row_n, col_n)
                if self.part[part_n][i]:
                    return i
        return 0

    cdef void rule(self, int row_n, int col_n, bint med):
        cdef int value = self.a_plz[row_n][col_n]
        cdef int part_n = find_part(row_n, col_n)
        self.row[row_n][value] = med
        self.col[col_n][value] = med
        self.part[part_n][value] = med

    cdef void create_mark(self):
        cdef int i
        cdef int j
        for i in range(9):
            for j in range(9):
                if self.a_plz[i][j] == 0:
                    # 所有的空格标为True
                    self.mark[i][j] = True
                else:
                    # 非空的将其三个约束列表置False
                    self.rule(i, j, False)

    cdef void uncertain(self):
        cdef dict uncertain_dict={}
        cdef int part_n
        cdef int row_n, col_n, i
        for row_n in range(9):
            for col_n in range(9):
                if self.mark[row_n][col_n]:
                    for i in range(1,10):
                        if self.row[row_n][i] and self.col[col_n][i]:
                            part_n = find_part(row_n, col_n)
                            if self.part[part_n][i]:
                                if uncertain_dict.has_key((row_n, col_n)):
                                    uncertain_dict[row_n, col_n] += 1
                                else:
                                    uncertain_dict[row_n, col_n] = 0
        self.uncertain_ls = list(map(lambda xs:xs[0], sorted(uncertain_dict.items(), key=lambda item:item[1])))



    cdef bint solve(self,int sid):
        '''
        # 如果当前列超出总列数则进入下一行第一列
        #if col_n == 9:
        #    row_n += 1
        #    col_n = 0
        # 直到找到一个空格
        while True:
            # 若遍历完仍没有空，说明已完成填空，返回
            #if row_n > 8:
            if sid >= self.length:
                return True
            if self.mark[row_n][col_n]:
                break
            col_n += 1
            if col_n == 9:
                row_n += 1
                col_n = 0
        '''
        cdef int row_n, col_n
        if sid >= self.length:
            return True
        row_n, col_n = self.uncertain_ls[sid]
        while True:
            self.a_plz[row_n][col_n] = self.find_next(row_n, col_n, self.a_plz[row_n][col_n] + 1)
            if self.a_plz[row_n][col_n] == 0:
                break
            self.rule(row_n, col_n, False)
            tmp_flag = self.solve(sid+1)
            if tmp_flag:
                return True
            self.rule(row_n, col_n, True)
        return False

    cdef void core(self):
        # 初始化列表
        cdef int i, j
        for i in range(11):
            for j in range(11):
                self.mark[i][j] = False
                self.row[i][j] = True
                self.col[i][j] = True
                self.part[i][j] = True
        # self.mark = [[False for _ in range(11)] for _ in range(11)]
        # self.row = [[True for _ in range(11)] for _ in range(11)]
        # self.col = [[True for _ in range(11)] for _ in range(11)]
        # self.part = [[True for _ in range(11)] for _ in range(11)]
        # 将所有未填的空标为True
        self.create_mark()
        self.uncertain()
        self.length = int(len(self.uncertain_ls))
        if not self.solve(0):
            print("文件中存在无解数独")
            sys.exit(0)

    # 解当前的问题，并写入解文件
    cdef void solve_part(self, int sid):
        self.core()
        self.write2file(self.a_plz, sid)
        if sid > 1000000:
            self.string[self.count] = ord('\0')
            fputs(self.string, self.sudoku)
            self.count = 0

        '''
        for i in range(9):
            for j in range(9):
                if j != 0:
                    fputs(" ", self.sudoku)
                fputc(self.a_plz[i][j] + 48, self.sudoku)
            fputs("\n", self.sudoku)
        '''

    # 每次从文件中读取一个问题并将终局写入解文件
    cdef void detach(self):
        cdef FILE* puzzle_file = fopen(self.arg.encode(), 'r')
        if puzzle_file == NULL:
            print("打开文件失败")
            sys.exit(0)
        cdef char line[30]
        cdef int k = 0, j = 0
        while True:
            #if feof(puzzle_file) != 0:
            #    break
            if fgets(line, 30, puzzle_file) == NULL:
                break
            if k == 9:
                k = 0
                # 求解:
                #if j != 9:
                #    fputs("\n", self.sudoku)
                self.solve_part(j)
                j += 1
                self.a_plz = []
            else:
                self.a_plz.append(list(map(int, (line.decode()).split())))
                k += 1
        self.solve_part(j)
        self.string[self.count] = ord('\0')
        fputs(self.string, self.sudoku)
        fclose(puzzle_file)
        fclose(self.sudoku)

    def main(self):
        cdef double time_start = time.time()
        if self.flag == '-c':
            self.create()
        elif self.flag == '-s':
            self.detach()
        cdef double time_end = time.time()
        print("总时间：%f s" % (time_end - time_start))


cdef int find_part(int row_n, int col_n):
    return 3*(row_n//3)+(col_n//3)
