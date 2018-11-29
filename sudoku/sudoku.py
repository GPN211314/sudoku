#!/usr/bin/env python
#coding:utf-8

import sys
import copy

class SD:

    def __init__(self, flag, arg="puzzle.txt"):
        self.puzzle = 0
        self.sudoku = 0
        self.grid = []
        self.number = arg
        self.flag = flag
        self.path = arg
        self.counter = 0
        self.first_row = list(range(1, 10))
        self.first_row.remove(8)
        self.tmprow = [8]+self.first_row
        self.cur = 1
        self.uncertain = []

    # 将生成的每一种终局，写入文件
    def write2file(self, grid):
        self.counter += 1
        if self.counter != 1:
            self.sudoku.write("\n")
        for i in range(9):
            for j in range(9):
                if j != 0:
                    self.sudoku.write(" ")
                self.sudoku.write(str(grid[i][j]))
            self.sudoku.write("\n")

    # 对一种终局，交换其中一些行，衍生出其它终局
    def exchange(self):
        tmpgrid = list(self.grid)
        grid345 = tmpgrid[3:6]
        grid678 = tmpgrid[6:]
        for order_a in [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]:
            for order_b in [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]:
                tmpgrid = tmpgrid[:3]+ \
                    [grid345[order_a[0]], grid345[order_a[1]], grid345[order_a[2]]]+ \
                    [grid678[order_b[0]], grid678[order_b[1]], grid678[order_b[2]]]
                self.write2file(tmpgrid)
                # 当生成并写入相应数目的终局后，关闭文件并退出程序
                if self.counter == self.number:
                    self.sudoku.close()
                    sys.exit(0)

    # 对第一行不同的排列，生成不同的局面
    def creat_grid(self, row):
        self.grid = []
        for i in range(3):
            for j in range(3):
                slice_x = i+3*j
                self.grid.append(row[-slice_x:]+row[:-slice_x])

    # 生成第一行的全排列
    def permutation(self, arow):
        if arow == []:
            self.creat_grid(self.tmprow)
            self.exchange()
            return
        for i in arow:
            self.tmprow[self.cur] = i
            self.cur += 1
            tmpls = list(arow)
            tmpls.remove(i)
            self.permutation(tmpls)
            self.cur -= 1
        return

    def creat(self):
        self.number = int(self.number)
        self.sudoku = open('sudoku.txt', 'w+')
        self.permutation(self.first_row)

    def rowleft(self, row, rnum=-1):
        left = set(range(1, 10))
        for i in range(9):
            if len(row[i]) == 1:
                left.difference_update(row[i])
            elif rnum != -1:
                self.uncertain.append([rnum, i])
        return left

    # 递归求解核心
    def core(self, currentgrid):
        # 计算行、列、区约束
        row = []
        col = []
        part = []
        for i in range(9):
            row.append(self.rowleft(currentgrid[i], i))
            col.append(self.rowleft([rowincg[i] for rowincg in currentgrid]))
            part.append(self.rowleft(comb(currentgrid, 3*(int(i/3)), 3*(i%3))))
        # 如果行约束列表全为空，则已经全部填满
        if isnone(row):
            return currentgrid

        tmpcurgrid = copy.deepcopy(currentgrid)
        # 对每个不确定的空格，求其行、列、区约束的交集
        for ele in self.uncertain:
            tmpcurgrid[ele[0]][ele[1]] = \
                row[ele[0]].intersection(col[ele[1]]).intersection(
                    part[(3*int(ele[0]/3)+int(ele[1]/3))%9])
        # 如果约束交集和本身相等,则说明不存在唯一确定的解，将其取值集合pop至剩余一个元素，再递归求解
        if tmpcurgrid == currentgrid:
            tmpset = tmpcurgrid[self.uncertain[0][0]][self.uncertain[0][1]]
            for i in range(len(tmpset)-1):
                tmpset.pop()
        self.uncertain = []
        return self.core(tmpcurgrid)

    # 解数独函数
    def solve(self, puzzle):
        tmpuzzle = list(puzzle)
        initgrid = initgd(tmpuzzle)
        answer = self.core(initgrid)
        return answer

    # 解当前的问题，并写入解文件
    def solvepart(self, apuzzle):
        ans = self.solve(apuzzle)
        # 将集合形式的解转换成整型
        for i in range(9):
            for j in range(9):
                ans[i][j] = ans[i][j].pop()
        for i in range(9):
            for j in range(9):
                if j != 0:
                    self.sudoku.write(" ")
                self.sudoku.write(str(ans[i][j]))
            self.sudoku.write("\n")

    # 每次从文件中读取一个问题并将终局写入解文件
    def dispart(self):
        aplz = []
        self.puzzle = open(self.path)
        self.sudoku = open('sudoku.txt', 'w+')
        k = 0
        for line in self.puzzle:
            if k != 0 and k % 9 == 0:
                k += 1
                # 求解:
                self.solvepart(aplz)
                self.sudoku.write("\n")
                aplz = []
            else:
                aplz.append(list(map(int, line.split())))
                k += 1
        self.solvepart(aplz)
        self.puzzle.close()
        self.sudoku.close()

    def main(self):
        if self.flag == '-c':
            self.creat()
        elif self.flag == '-s':
            self.dispart()

def helpinformation():
    print("sudoku.exe [选项] 参数")
    print("选项：")
    print("    -c <数字>\t生成<数字>个数独终局至文件sudoku.txt")
    print("    -s <绝对路径>\t从<绝对路径>中读取数独题目并生成一个可行解至sudoku.txt")
    print("    -h 显示当前帮助信息")
    sys.exit(0)

    # 构造初始状态列表
def initgd(pzl):
    ini = []
    for i in range(9):
        tls = []
        for j in range(9):
            if pzl[i][j] == 0:
                tls.append({})
            else:
                tls.append({pzl[i][j]})
        ini.append(tls)
    return ini

def isnone(row):
    for i in row:
        if not i:
            return False
    return True

def comb(agrid, coor_x, coor_y):
    tmpart = []
    for i in range(3):
        tmpart += agrid[coor_x+i][coor_y:coor_y+3]
    return tmpart

def main(argv):
    if len(argv) != 3:
        helpinformation()

    if argv[1] == '-c' and not argv[2].isdigit():
        print("-c 的参数必须为数字")
        sys.exit(0)

    shudu = SD(argv[1], argv[2])
    shudu.main()


if __name__ == '__main__':
    main(sys.argv)
