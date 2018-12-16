#!/usr/bin/env python
# coding:utf-8
import sys
import sudoku_calc
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
from pycallgraph import GlobbingFilter

def comb(a_grid, coord_x, coord_y):
    tmp_art = []
    for i in range(3):
        tmp_art += a_grid[coord_x+i][coord_y:coord_y+3]
    return tmp_art


def row_left(row):
    left = set(range(1, 10))
    for i in range(9):
        if len(row[i]) == 1:
            left.difference_update(row[i])
    return left


def isnone(row):
    for i in row:
        if i:
            return False
    return True

def help_information():
    print("sudoku.exe [选项] 参数")
    print("选项：")
    print("    -c <数字>\t生成<数字>个数独终局至文件sudoku.txt")
    print("    -s <绝对路径>\t从<绝对路径>中读取数独题目并生成一个可行解至sudoku.txt")
    print("    -h 显示当前帮助信息")
    sys.exit(0)


def main(argv):
    if len(argv) != 3 or argv[1] not in ['-c', '-s', '-h']:
        help_information()

    if argv[1] == '-c' and not argv[2].isdigit():
        print("-c 的参数必须为数字")
        sys.exit(0)

    sudoku_instance = sudoku_calc.SD(argv[1], argv[2])
    sudoku_instance.main()


if __name__ == '__main__':
    config = Config()
    config.trace_filter = GlobbingFilter(include=[ 'main', 'sudoku_calc.SD.*' ])
    graphviz = GraphvizOutput()
    graphviz.output_file = 'solve.png'
    with PyCallGraph(output=graphviz, config=config):
        main(sys.argv)
