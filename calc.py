import math

ADD     = 10        # + 0
MINUS   = 11        # -
MUL     = 12        # × 1
DIV     = 13        # ÷
LP      = 14        # ( 2
RP      = 15        # )
END     = 16        # \0

def getDisplay(results):
    displayText = ""
    for literal in results:
        if literal == ADD:
            displayText += "+"
        elif literal == MINUS:
            displayText += "-"
        elif literal == MUL:
            displayText += "×"
        elif literal == DIV:
            displayText += "÷"
        elif literal == LP:
            displayText += "("
        elif literal == RP:
            displayText += ")"
        else:
            displayText += str(literal)
    displayText += "="
    return displayText

def operate(op1, op2, op):
    if op == ADD:
        return op1 + op2
    elif op == MINUS:
        return op1 - op2
    elif op == MUL:
        return op1 * op2
    elif op == DIV:
        if op2 == 0:
            return math.inf
        else:
            return op1 / op2
    else:
        raise Exception("ERROR")

def getPriority(op):
    if op == ADD or op == MINUS:
        return 0
    elif op == MUL or op == DIV:
        return 1
    else:
        return 2

def makeCalculation(results):
    # conflicting naming scheme bans
    # the use of postfix method.
    results.append(END)  # add an ending symbol
    numStack = []
    opStack = []
    curnum = 0
    for i, literal in enumerate(results):
        if literal < 10: # single number
            curnum = curnum * 10 + literal
        else: # operator
            if literal == LP:
                if i>0 and results[i-1] < 10:
                    numStack.append(curnum)
                    curnum = 0
                    opStack.append(MUL) # handle 2(3) -> 2 * (3)
                opStack.append(literal)
            else:
                if i>0 and results[i-1]>=10:
                    # the previous is a symbol
                    if (results[i-1] == LP and literal == RP):
                        numStack.append(0) # handle () -> 0
                        curnum = 0
                    if (literal == RP or literal == END) and results[i-1]<LP:
                        return "ERROR"
                else:
                    # push the current num
                    numStack.append(curnum)
                    curnum = 0
                if len(opStack) == 0:
                    opStack.append(literal)
                    continue
                while True:
                    topOp = opStack[-1]
                    if literal == RP and topOp == LP:
                        topOp = opStack.pop()
                        break
                    if (getPriority(topOp) - getPriority(literal) >= 0 and topOp != LP) or literal == RP or literal == END:
                        # topOp is of higher priority or the same priority
                        # or it meets RP or END to collapse
                        # make calculation now
                        topOp = opStack.pop()
                        try: 
                            op2 = numStack.pop()
                            op1 = numStack.pop()
                            numStack.append(operate(op1, op2, topOp))
                        except:
                            return "ERROR"
                    else:
                        # topOp is of lower priority
                        # push the literal
                        opStack.append(literal)
                        break
                    if len(opStack)==0:
                        if literal == RP:
                            # the ) doesn't match (
                            return "ERROR"
                        else:
                            opStack.append(literal)
                            break
    return numStack.pop()

def calc(results):
    displayText = getDisplay(results)
    displayText += str(makeCalculation(results))
    return displayText
