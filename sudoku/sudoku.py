#!/usr/bin/env python3
#coding:utf-8

import sys
import os

class SD:

    def __init__(self, num):
        self.sudoku = open('sudoku.txt','w+')
        self.grid = []
        self.number = num
        self.counter = 0
        self.first_row = list(range(1,10))
        self.first_row.remove(8)
        self.tmprow = [8]+self.first_row
        self.cur = 1

    def write2file(self, gd):
        if self.counter != 1:
            self.sudoku.write("\n")
        for i in range(9):
            if i != 0:
                self.sudoku.write("\n")
            for j in range(9):
                if j != 0:
                    self.sudoku.write(" ")
                self.sudoku.write(str(gd[i][j]))
        return
            
    def exchange(self):
        tmpgrid = list(self.grid)
        grid345 = tmpgrid[3:6]
        grid678 = tmpgrid[6:]
        for a in [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]:
            for b in [[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]]:
                tmpgrid = tmpgrid[:3]+[grid345[a[0]],grid345[a[1]],grid345[a[2]]]+ \
                    [grid678[b[0]],grid678[b[1]],grid678[b[2]]]
                self.write2file(tmpgrid)
                self.counter += 1
                if self.counter ==self.number:
                    self.sudoku.close()
                    sys.exit(0)
        return

    def creat_grid(self, row):
        self.grid=[]
        for i in range(3):
            for j in range(3):
                x=i+3*j
                self.grid.append(row[-x:]+row[:-x])
        return

    def permutation(self, ls):
        if ls == []:
            self.creat_grid(self.tmprow)
            self.exchange()
            return
        for i in ls:
            self.tmprow[self.cur] = i
            self.cur += 1
            tmpls = list(ls)
            tmpls.remove(i)
            self.permutation(tmpls)
            self.cur -= 1
        return

    def main(self):
        self.permutation(self.first_row)
        

def help():
    print("sudoku.exe [选项] 参数")
    print("选项：")
    print("    -c <数字>\t生成<数字>个数独终局至文件sudoku.txt")
    print("    -s <绝对路径>\t从<绝对路径>中读取数独题目并生成一个可行解至sudoku.txt")
    print("    -h 显示当前帮助信息")
    sys.exit(0)

def main(argv):
    if len(argv) != 3:
        help()

    if argv[1] == '-c' and not argv[2].isdigit():
        print("-c 的参数必须为数字")
        sys.exit(0)

    if argv[1]  == '-c':
        sd=SD(int(argv[2]))
        sd.main()


if __name__ == '__main__':
    main(sys.argv)