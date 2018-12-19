import unittest
from unittest.mock import patch
from sudoku_calc import SD
import sudoku
import io

class TestSudoku(unittest.TestCase):

    def test_init(self):
        a = SD("-c","100")
        self.assertEqual(a.flag,"-c")
        self.assertEqual(a.arg,"100")
        self.assertTrue(isinstance(a,SD))

        b = SD("-s","100")
        self.assertEqual(b.flag,"-s")
        self.assertEqual(b.arg,"100")
        self.assertTrue(isinstance(b,SD))

        c = SD()
        self.assertEqual(c.flag,"")
        self.assertEqual(c.arg,"")
        self.assertTrue(isinstance(c,SD))

    def test_solve(self):
        a = SD("-s","b.txt")
        a.detach()
        pz=[]
        ans=[]
        with open("sudoku.txt") as f:
            for line in f:
                if line == "\n":
                    break
                ans.append(list(map(int, line.split())))
            
        with open("b.txt") as f:
            for line in f:
                if line == "\n":
                    break
                pz.append(list(map(int, line.split())))
    
        self.assertEqual(len(ans),9)
        self.assertEqual(len(ans[0]),9)
        self.assertEqual(len(pz),9)
        self.assertEqual(len(pz[0]),9)

        k = True
        for i in range(9):
            for j in range(9):
                if pz[i][j] != 0:
                    if pz[i][j] != ans[i][j]:
                        k = False

        self.assertEqual(k,True)

        flag = True
        for i in ans:
            if sorted(i) != list(range(1,10)):
                flag = False
        self.assertEqual(flag,True)

        for i in range(9):
            if sorted([t[i] for t in ans]) != list(range(1,10)):
                flag = False
        self.assertEqual(flag,True)

        for i in range(9):
            p=[]
            for j in range(9):
                p.append(ans[3*(i//3)+j//3][3*(i%3)+j%3])
            if sorted(p) != list(range(1,10)):
                flag = False
            self.assertEqual(flag,True)
                
        c=SD("-s","c.txt")
        string = ""
        try:
            with patch('sys.stdout', new=io.StringIO()) as string:
                c.detach()
        except:
            self.assertEqual(string.getvalue(), "文件中存在无解数独\n")

    def test_creat(self):
        a=SD("-c", "1")
        a.create()
        ans =[]
        with open("sudoku.txt") as f: 
            for line in f:
                ans.append(list(map(int,line.split())))
        flag = True
        for i in ans:
            if sorted(i) != list(range(1,10)):
                flag = False
        self.assertEqual(flag,True)

        for i in range(9):
            if sorted([t[i] for t in ans]) != list(range(1,10)):
                flag = False
        self.assertEqual(flag,True)

        for i in range(9):
            p=[]
            for j in range(9):
                p.append(ans[3*(i//3)+j//3][3*(i%3)+j%3])
            if sorted(p) != list(range(1,10)):
                flag = False
            self.assertEqual(flag,True)

        a=SD("-c", "1000")
        a.create()
        flag = True
        a_dict={}
        v=[]
        with open("sudoku.txt") as f: 
            for line in f:
                if line == "\n":
                    v = tuple(v)
                    if v not in a_dict:
                        a_dict[v]=True
                    else:
                        flag=False
                        break
                    v=[]
                else:
                    v.append(tuple(line.split()))
        self.assertEqual(flag,True)


    def test_main(self):
        a=SD("-c","10")
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            a.main()
            string = fake_out.getvalue()
            self.assertEqual(string.startswith("总时长：") and string.endswith("s\n"), True)

        a=SD("-s","b.txt")
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            a.main()
            string = fake_out.getvalue()
            self.assertEqual(string.startswith("总时长：") and string.endswith("s\n"), True)

    def test_input(self):
        expect_value = "sudoku.exe [选项] 参数\n选项：\n    -c <数字>\t生成<数字>个数独终局至文件sudoku.txt\n    -s <绝对路径>\t从<绝对路径>中读取数独题目并生成一个可行解至sudoku.txt\n    -h 显示当前帮助信息\n"
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            sudoku.main([0,'-c'])
            self.assertEqual(fake_out.getvalue(),expect_value )
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            sudoku.main([0,'-c','sd','f'])
            self.assertEqual(fake_out.getvalue(),expect_value )
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            sudoku.main([0,'-c','sf'])
            self.assertEqual(fake_out.getvalue(),expect_value )
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            sudoku.main(['sudoku.py','-c','10'])
            string = fake_out.getvalue()
            self.assertEqual(string.startswith("总时长：") and string.endswith("s\n"), True)


        


if __name__ == '__main__':
    unittest.main()




    
