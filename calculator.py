from collections import deque


class Calculator:

    def __init__(self):
        self.variables = dict()
        while (True):
            string = input()
            string = string.strip()
            if string == '':
                continue
            if string[0] == '/':
                if string == '/exit':
                    print('Bye!')
                    break
                elif string == '/help':
                    self.help_()
                    continue
                else:
                    print('Unknown command')
                    continue
            if '=' in string:
                self.assignment(string)
                continue
            if string == 'Unknown variable':
                print(string)
                continue
            string = self.intopost(string)
            if string == 'Invalid expression':
                print(string)
                continue
            result = self.posttoval(string)
            if string == 'Invalid expression':
                print(string)
                continue
            print(result)

    # assignment
    def assignment(self, string):
        contains = string.split('=')
        lc = len(contains)
        if lc < 2:
            print('Invalid expression')
            return
        for i in range(lc - 1):
            contains[i] = contains[i].strip()
            if contains[i] in self.variables:
                continue
            if not contains[i].isalpha():
                print('Invalid identifier')
                return
        contains[lc - 1] = contains[lc - 1].strip()
        try:
            if contains[lc - 1] in self.variables:
                num = self.variables[contains[lc - 1]]
            else:
                num = int(contains[lc - 1])
        except ValueError:
            if not contains[lc - 1].isalpha():
                print('Invalid assignment')
                return
            print('Unknown variable')
            return
        for i in range(lc - 1):
            self.variables[contains[i]] = num
        return

    # converting postfix to val
    def posttoval(self, postfix):
        postfix = postfix.split(',')
        numstack = deque()
        #print(postfix)
        for x in postfix:
            if x.isalpha():
                if x in self.variables:
                    numstack.append(self.variables[x])
                else:
                    return 'Unknown variable'
            elif self.is_int(x):
                numstack.append(int(x))
            else:
                b = numstack.pop()
                a = numstack.pop()
                if x == '+':
                    numstack.append(a + b)
                elif x == '-':
                    numstack.append(a - b)
                elif x == '*':
                    numstack.append(a * b)
                elif x == '/':
                    try:
                        numstack.append(int(a / b))
                    except ZeroDivisionError:
                        return 'ZeroDivisionError'
                else:
                    numstack.append(a ** b)
        return numstack.pop()

    def is_int(self, x):
        try:
            int(x)
            return True
        except Exception:
            return False

    # help function
    def help_(self):
        print('The program calculates the sum and subtraction of numbers')
        return

    # converting infix to postfix
    def intopost(self, infix):
        li = len(infix)
        lp = 0
        s = 0
        e = 0
        postfix = ''
        opstack = deque()
        num = True
        op = False
        if li == 0:
            return ''
        while (li > s):

            x = infix[s]
            # print(x,num,op)
            if x == ' ':
                s += 1
                continue
            elif x.isdigit():
                if op:
                    return 'Invalid expression'
                e = s + 1
                while (1):
                    if li > e and infix[e].isdigit():
                        e += 1
                    else:
                        break
                postfix += infix[s:e] + ','
                op = True
                # print('in digit',op)
                num = False
                lp += e - s
                s = e
            elif x.isalpha():  # variables
                if op:
                    # print(op)
                    return 'Invalid expression'
                e = s + 1
                while (1):
                    if li > e and infix[e].isalpha():
                        e += 1
                    else:
                        break
                postfix += infix[s:e] + ','
                op = True
                num = False
                lp += e - s
                s = e

            elif x == '(':
                e = s + 1
                while 1:
                    if li <= e:
                        return 'Invalid expression'
                    if infix[e] == ')':
                        subpostfix = self.intopost(infix[s + 1:e])
                        break
                    else:
                        e += 1
                if infix[e] != ')':
                    return 'Invalid expression'
                postfix += subpostfix + ','
                lp = e - s + 1
                op = True
                num = False
                s = e + 1
            else:
                if num:
                    # print('in num',op)
                    if infix[s] in '+-':
                        e = s + 1
                        opr = infix[s]
                        while 1:
                            if li > e and infix[e] == '+':
                                e += 1
                                pass
                            elif li > e and infix[e] == '-':
                                e += 1
                                if opr == '-':
                                    opr = '+'
                                else:
                                    opr = '-'
                            else:
                                break
                        lp += e - s
                        if infix[e].isdigit():
                            s = e
                            e += 1
                            while (1):
                                if li > e and infix[e].isdigit():
                                    e += 1
                                else:
                                    break
                            postfix += opr + infix[s:e] + ','
                            op = True
                            num = False
                            lp += e - s
                            s = e
                        else:
                            return 'Invalid expression'

                    else:
                        return 'Invalid expression'
                elif x == '+' or x == '-':  # +,-
                    opr = x
                    e = s + 1
                    while 1:
                        if li > e and infix[e] == '+':
                            e += 1
                        elif li > e and infix[e] == '-':
                            e += 1
                            if opr == '+':
                                opr = '-'
                            else:
                                opr = '+'
                        else:
                            break
                    while 1:
                        if len(opstack) == 0:
                            opstack.append(opr)
                            break
                        if self.hashigherpercendence(opr, opstack[-1]):
                            opstack.append(opr)
                            break
                        else:
                            postfix += opstack.pop() + ','
                    lp += e - s
                    num = True
                    op = False
                    s = e

                elif x == '*' or x == '/' or x == '^':  # *,/,^
                    opr = x
                    while 1:
                        if len(opstack) == 0:
                            opstack.append(opr)
                            break
                        elif self.hashigherpercendence(opr, opstack[-1]):
                            opstack.append(opr)
                            break
                        else:
                            postfix += opstack.pop() + ','
                    num = True
                    op = False
                    lp += 1
                    s += 1
                else:
                    return 'Invalid expression'
        l = len(opstack)
        while (l):
            postfix += opstack.pop() + ','
            l -= 1
        postfix = postfix[:-1]
        return postfix

    def hashigherpercendence(self, opr, sopr):
        if self.getoperatorweight(opr) > self.getoperatorweight(sopr):
            return True
        else:
            return False

    def getoperatorweight(self, opq):
        if opq == '+' or opq == '-':
            return 1
        if opq == '*' or opq == '/':
            return 2
        else:
            return 3


Calculator()