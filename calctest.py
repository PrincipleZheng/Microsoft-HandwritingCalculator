import unittest
from calc import *

def convertToStream(str):
    streamList = []
    for literal in str:
        if literal == '+':
            streamList.append(ADD)
        elif literal == '-':
            streamList.append(MINUS)
        elif literal == '*':
            streamList.append(MUL)
        elif literal == '/':
            streamList.append(DIV)
        elif literal == '(':
            streamList.append(LP)
        elif literal == ')':
            streamList.append(RP)
        else:
            streamList.append(int(literal))
    return streamList

def testCalc(str):
    return makeCalculation(convertToStream(str))

class CalcTest(unittest.TestCase):
    def test1(self):
        self.assertEqual(testCalc('1+2'),3)
    def test2(self):
        self.assertEqual(testCalc('1+(2-3)*4+4/2'),-1)
    def test3(self):
        self.assertEqual(testCalc('1+)3-2'),"ERROR")
    def test4(self):
        self.assertEqual(testCalc('12+34-5*2'),36)
    def test5(self):
        self.assertEqual(testCalc('1+1/0'),math.inf)
    def test6(self):
        self.assertEqual(testCalc('1+(2+3'),"ERROR")
    def test7(self):
        self.assertEqual(testCalc('1+2(3)'),7)
    def test8(self):
        self.assertEqual(testCalc('1+2+3()'),3)
    def test9(self):
        self.assertEqual(testCalc('1+(2+(2+((1)+2'),"ERROR")
    def test10(self):
        self.assertEqual(testCalc('1+3*(1+(1+2)/(1+2))'),7)

if __name__ == '__main__':
    unittest.main()