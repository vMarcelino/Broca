from enum import Enum

print("Projeto broca!")

showClass = 0 == 1


def MainCodeExecution():
    # stringInput = "(" + input("Manual expression Override: ") + ")"
    # print(stringInput)
    ExpressionVariableDatabase()  # Variable database initialization

    e0 = ExpressionVariable("e0")
    e1 = ExpressionVariable("e1")
    e2 = ExpressionVariable("e2")
    e3 = ExpressionVariable("e3")
    e4 = ExpressionVariable("e4")

    d0 = ExpressionVariable("d0")
    d1 = ExpressionVariable("d1")
    d2 = ExpressionVariable("d2")
    d3 = ExpressionVariable("d3")

    b0 = ExpressionVariable("b0")
    b1 = ExpressionVariable("b1")
    b2 = ExpressionVariable("b2")
    b3 = ExpressionVariable("b3")

    c0 = ExpressionBlock([e0, d0], Operators.XOR)
    k0 = ExpressionBlock([ExpressionVariable("LITERAL", 0), ExpressionVariable("LITERAL", 0)], Operators.XOR)
    k0 = k0.doMaths()

    k1 = kTemplate(k0, c0, d0)
    c1 = cTemplate(k1, e1, d1)

    k2 = kTemplate(k1, c1, d1)
    c2 = cTemplate(e2, d2, k2)

    k3 = kTemplate(k2, d2, c2)
    c3 = cTemplate(k3, d3, e3)

    l0 = k0
    a0 = ExpressionBlock([c0, b0], Operators.XOR)

    l1 = kTemplate(l0, c0, b0)
    a1 = cTemplate(l1, b1, c1)

    l2 = kTemplate(l1, c1, b1)
    a2 = cTemplate(l2, c2, b2)

    l3 = kTemplate(l2, c2, b2)
    a3 = cTemplate(l3, c3, b3)

    functions = [c0, "c0", c1, "c1", c2, "c2", c3, "c3", k0, "k0", k1, "k1", k2, "k2", k3, "k3", a0, "a0", a1, "a1", a2, "a2", a3, "a3", l0, "l0", l1, "l1", l2,
                 "l2", l3, "l3"]

    c0.optimize(True)
    k1.optimize(True)
    c1.optimize(True)
    k2.optimize(True)
    c2.optimize(True)
    k3.optimize(True)
    c3.optimize(True)
    printThings(functions)
    print("Running maths...")
    doMaths(functions)
    printThings(functions)

    while True:
        ExpressionVariableDatabase.getVariableWithName(input("Nome da variavel: ")).setValue(int(input("Valor da variável: ")))
        doMaths(functions)
        printThings(functions)
        # a0 = a0.doMaths()
        # a1 = a1.doMaths()
        # a2 = a2.doMaths()
        # a3 = a3.doMaths()
        # print(a0.print())
        # print(a1.print())
        # print(a2.print())
        # print(a3.print())

    print("\n NAO Funciona!!!")


def printThings(fncs):
    for i in range(int(len(fncs) / 2)):
        print(fncs[i * 2 + 1] + " = " + fncs[i * 2].print())


def doMaths(fncs):
    for i in range(int(len(fncs) / 2)):
        fncs[i * 2] = fncs[i * 2].doMaths()


def kTemplate(k, c, d):
    kc = ExpressionBlock([k, c], Operators.AND)
    kd = ExpressionBlock([k, d], Operators.AND)
    cd = ExpressionBlock([c, d], Operators.AND)
    return ExpressionBlock([kc, kd, cd], Operators.OR)


def cTemplate(e, d, k):
    return ExpressionBlock([e, d, k], Operators.XOR)


class ExpressionBlock:
    # expressionBlocks = []  # ExpBlock
    # basicExpressionBlocks = []  # BasicExpBlock
    # operator = ""
    # tempName = ""

    def __init__(self, expressions, op):
        self.operator = op
        self.expressionBlocks = []
        self.basicExpressionBlocks = []
        for expression in expressions:
            if type(expression) is ExpressionBlock:
                expression = expression.formatXor()
                self.expressionBlocks.append(expression)
            elif type(expression) is BasicExpressionBlock:
                if expression.operator == Operators.XOR and len(expression.expressionVariables) > 2:
                    expression = expression.formatXor()
                    self.expressionBlocks.append(expression)
                else:
                    self.basicExpressionBlocks.append(expression)
            elif type(expression) is ExpressionVariable:
                self.basicExpressionBlocks.append(BasicExpressionBlock([expression], Operators.NoOperator))
            elif type(expression) is Not:
                self.expressionBlocks.append(expression)

        self.optimize()
        newSelf = self.formatXor(checkChild=True)
        self.basicExpressionBlocks = newSelf.basicExpressionBlocks
        self.expressionBlocks = newSelf.expressionBlocks
        self.operator = newSelf.operator
        newSelf = self.convertXor()
        self.basicExpressionBlocks = newSelf.basicExpressionBlocks
        self.expressionBlocks = newSelf.expressionBlocks
        self.operator = newSelf.operator

    def __str__(self):
        return self.print("")

    def print(self, str=""):
        str += "E(" if showClass else "("
        i = 0
        for expression in self.expressionBlocks + self.basicExpressionBlocks:
            str += expression.print()
            if i < (len(self.expressionBlocks) + len(self.basicExpressionBlocks) - 1):
                str += " " + self.operator.value + " "
            i += 1

        str += ")"
        return str

    def optimize(self, fullOptimization=False):  # Where maths are applied

        if fullOptimization:
            for block in self.expressionBlocks + self.basicExpressionBlocks:
                block.optimize(fullOptimization)

        # Transform Expression Blocks (EB or EBo) with one Bae into one Bae
        for i in range(len(self.expressionBlocks)):
            if type(self.expressionBlocks[i]) is not Not:
                if len(self.expressionBlocks[i].expressionBlocks) == 0 and len(self.expressionBlocks[i].basicExpressionBlocks) == 1:
                    self.basicExpressionBlocks.append(self.expressionBlocks[i].basicExpressionBlocks[0])
                    self.expressionBlocks[i] = ExpressionBlock([], Operators.NoOperator)

        # Remove empty Expression Blocks (EB or EBo)
        r = 0
        for i in range(len(self.expressionBlocks) - r):
            if i - r < len(self.expressionBlocks):
                if type(self.expressionBlocks[i - r]) is Not:
                    continue
                if len(self.expressionBlocks[i - r].expressionBlocks) == 0 and len(self.expressionBlocks[i - r].basicExpressionBlocks) == 0:
                    self.expressionBlocks.pop(i - r)
                    r += 1

        # Join Basic Expression Blocks (BEB or BaEB or Bae) with the same operator into one (WRONG!!!!!)
        # for i in range(len(self.basicExpressionBlocks) - 1):
        #    if self.basicExpressionBlocks[i].operator == Operators.NOT:
        #        continue

        #   if self.basicExpressionBlocks[i].operator == Operators.NoOperator and len(self.basicExpressionBlocks[i].expressionVariables) > 0:
        #        for j in range(i + 1, len(self.basicExpressionBlocks)):
        #            if self.basicExpressionBlocks[j].operator == Operators.NoOperator:
        #                self.basicExpressionBlocks[i] = BasicExpressionBlock((
        #                    self.basicExpressionBlocks[i].expressionVariables +
        #                    self.basicExpressionBlocks[j].expressionVariables),
        #                    self.operator)
        #                self.basicExpressionBlocks[j] = BasicExpressionBlock([], Operators.NoOperator)

        #    if self.basicExpressionBlocks[i].operator != Operators.NoOperator:
        #        for j in range(i + 1, len(self.basicExpressionBlocks)):
        #            if self.basicExpressionBlocks[i].operator == self.basicExpressionBlocks[j].operator:
        #                self.basicExpressionBlocks[i].expressionVariables += self.basicExpressionBlocks[j].expressionVariables
        #                self.basicExpressionBlocks[j] = BasicExpressionBlock([], Operators.NoOperator)

        # Remove empty Basic Expression Blocks (BEB or BaEB or Bae)
        r = 0
        for i in range(len(self.basicExpressionBlocks)):
            if i - r < len(self.basicExpressionBlocks):
                if len(self.basicExpressionBlocks[i - r].expressionVariables) == 0:
                    self.basicExpressionBlocks.pop(i - r)
                    r += 1

        if len(self.expressionBlocks) == 1 and len(self.basicExpressionBlocks) == 0 and self.operator != Operators.NOT:
            holder = self.expressionBlocks[0]
            if type(holder) is not Not:
                self.expressionBlocks = holder.expressionBlocks
                self.basicExpressionBlocks = holder.basicExpressionBlocks
                self.operator = holder.operator

    def formatXor(self, checkChild=False):
        if checkChild:
            newBae = []
            newEB = []
            for expression in self.basicExpressionBlocks:
                exp = expression.formatXor()
                if type(exp) is BasicExpressionBlock:
                    newBae.append(exp)
                elif type(exp) is ExpressionBlock:
                    newEB.append(exp)

            for expression in self.expressionBlocks:
                exp = expression.formatXor()
                if type(exp) is BasicExpressionBlock:
                    newBae.append(exp)
                elif type(exp) is ExpressionBlock:
                    newEB.append(exp)
                else:
                    newEB.append(exp)

            self.basicExpressionBlocks = newBae
            self.expressionBlocks = newEB

        if self.operator == Operators.XOR and len(self.basicExpressionBlocks + self.expressionBlocks) > 2:
            remainingEB = self.expressionBlocks + self.basicExpressionBlocks
            exp = []
            for i in range(1, len(remainingEB)):
                exp.append(remainingEB[i])

            remainingEB = list(set(remainingEB) - set(exp))
            return ExpressionBlock(remainingEB + [ExpressionBlock(exp, Operators.XOR)], Operators.XOR)
        else:
            return self

    def convertXor(self):
        for i in range(len(self.expressionBlocks)):
            self.expressionBlocks[i] = self.expressionBlocks[i].convertXor()

        for i in range(len(self.basicExpressionBlocks)):
            self.basicExpressionBlocks[i] = self.basicExpressionBlocks[i].convertXor()

        if len(self.expressionBlocks + self.basicExpressionBlocks) != 2 and self.operator == Operators.XOR:
            print("WRONG!!!!!!!!!!!!!!!!!!!!!")

        self.optimize()
        self.formatXor()
        self.optimize()

        if self.operator != Operators.XOR:
            return self
        else:
            # A XOR B = (A + B) * !(A * B)
            A = (self.expressionBlocks + self.basicExpressionBlocks)[0]
            B = (self.expressionBlocks + self.basicExpressionBlocks)[1]
            return ExpressionBlock([
                ExpressionBlock([
                    A,
                    B],
                    Operators.OR),
                Not(
                    ExpressionBlock([
                        A,
                        B],
                        Operators.AND))],
                Operators.AND)

    def doMaths(self):
        expressions = []
        for expression in self.expressionBlocks + self.basicExpressionBlocks:
            expressions.append(expression.doMaths())

        if len(expressions) > 1:
            if self.operator == Operators.XOR:
                if expressions[0].isDefined() and expressions[1].isDefined():
                    v0, v1 = expressions[0].getValue(), expressions[1].getValue()
                    val = v0 + v1 - 2 * v0 * v1
                    return BasicExpressionBlock([ExpressionVariable("LITERAL", val)], Operators.NoOperator).doMaths()
                elif expressions[1].isDefined():
                    if expressions[1].getValue() == 1:
                        return Not(expressions[0]).doMaths()
                    else:
                        return ExpressionBlock([expressions[0]], self.operator)
                elif expressions[0].isDefined():
                    if expressions[0].getValue() == 1:
                        return Not(expressions[1]).doMaths()
                    else:
                        return ExpressionBlock([expressions[1]], self.operator)
                else:
                    return ExpressionBlock(expressions, self.operator)
            if self.operator == Operators.AND:
                isZero = False
                remainingVariables = []
                for expressionVariable in expressions:
                    if expressionVariable.getValue() == 0:
                        isZero = True
                        break
                    elif not expressionVariable.isDefined():
                        remainingVariables.append(expressionVariable)

                if isZero:
                    return BasicExpressionBlock([ExpressionVariable("LITERAL", 0)], Operators.NoOperator)
                elif len(remainingVariables) == 0:
                    return BasicExpressionBlock([ExpressionVariable("LITERAL", 1)], Operators.NoOperator)
                else:
                    return ExpressionBlock(remainingVariables, Operators.AND)

            if self.operator == Operators.OR:
                isOne = False
                remainingVariables = []
                for expressionVariable in expressions:
                    if expressionVariable.isDefined():
                        if expressionVariable.getValue() == 1:
                            isOne = True
                            break
                    elif not expressionVariable.isDefined():
                        remainingVariables.append(expressionVariable)

                if isOne:
                    return BasicExpressionBlock([ExpressionVariable("LITERAL", 1)], Operators.NoOperator)
                elif len(remainingVariables) == 0:
                    return BasicExpressionBlock([ExpressionVariable("LITERAL", 0)], Operators.NoOperator)
                else:
                    return ExpressionBlock(remainingVariables, Operators.OR)

        if self.operator == Operators.NOT:
            return Not(expressions[0]).doMaths()

        return ExpressionBlock(expressions, Operators.NoOperator)

    def isDefined(self):
        if len(self.expressionBlocks) == 0 and len(self.basicExpressionBlocks) == 1:
            if len(self.basicExpressionBlocks[0].expressionVariables) == 1:
                return self.basicExpressionBlocks[0].expressionVariables[0].isDefined()
        return False

    def getValue(self):
        # afterMath = self.doMaths()
        if len(self.expressionBlocks) == 0 and len(self.basicExpressionBlocks) == 1:
            if len(self.basicExpressionBlocks[0].expressionVariables) == 1:
                return self.basicExpressionBlocks[0].expressionVariables[0].getValue()
        return -999


class Not:
    def __init__(self, exp):
        self.expression = exp
        self.basic = type(exp) is ExpressionVariable

    def __repr__(self):
        return self.print("")

    def __str__(self):
        return self.print("")

    def formatXor(self, checkChild=False):
        self.expression = self.expression.formatXor(checkChild)
        return self

    def convertXor(self):
        self.expression = self.expression.convertXor()
        return self

    def isDefined(self):
        return self.expression.isDefined()

    def getValue(self):
        return self.expression.getValue()

    def print(self, str=""):
        str += "!" + self.expression.print("")
        return str

    def optimize(self, fullOptimize=False):
        self.expression.optimize(fullOptimize)

    def doMaths(self):
        exp = optimize(self.expression.doMaths())
        if type(exp) is Not:
            return exp.expression
        elif type(exp) is ExpressionVariable:
            if exp.isDefined():
                return BasicExpressionBlock([ExpressionVariable("LITERAL", 1 - exp.value)], Operators.NoOperator)
            else:
                return Not(exp)
        elif type(exp) is BasicExpressionBlock:
            if len(exp.expressionVariables) == 1 and exp.expressionVariables[0].isDefined():
                return BasicExpressionBlock([ExpressionVariable("LITERAL", 1 - exp.expressionVariables[0].getValue())], Operators.NoOperator)
            else:
                return Not(exp)
        else:
            return Not(exp)


class BasicExpressionBlock:
    # expressionVariables = []  # expVar
    # operator = ""

    def __init__(self, expvs, op):
        self.expressionVariables = expvs
        self.operator = op
        self.optimize()

    def __str__(self):
        return self.print("")

    def __repr__(self):
        return self.print("")

    def print(self, str=""):
        if self.operator == Operators.NOT:
            str += "!"
            str += self.expressionVariables[0].print()
        elif self.operator == Operators.NoOperator:
            str += self.expressionVariables[0].print()
        else:
            str += "B(" if showClass else "("
            for i in range(len(self.expressionVariables)):
                str += self.expressionVariables[i].print()
                if i < (len(self.expressionVariables) - 1):
                    str += " " + self.operator.value + " "

            str += ")"
        return str

    def optimize(self, fullOptimize=False):  # Where simple maths are applied
        self.expressionVariables = list(set(self.expressionVariables))

    def formatXor(self, checkChild=False):
        if self.operator == Operators.XOR and len(self.expressionVariables) > 2:
            remainingEV = self.expressionVariables
            exp = []
            for i in range(1, len(remainingEV)):
                exp.append(remainingEV[i])

            remainingEV = list(set(remainingEV) - set(exp))
            remainingEV.append(ExpressionBlock(exp, Operators.XOR))
            return ExpressionBlock(remainingEV, Operators.XOR)
        else:
            return self

    def convertXor(self):
        for i in range(len(self.expressionVariables)):
            self.expressionVariables[i] = self.expressionVariables[i].convertXor()

        if self.operator != Operators.XOR:
            return self
        else:
            A = self.expressionVariables[0]
            B = self.expressionVariables[1]
            return ExpressionBlock([
                ExpressionBlock([
                    A,
                    B],
                    Operators.OR),
                Not(
                    ExpressionBlock([
                        A,
                        B],
                        Operators.AND))],
                Operators.AND)

    def doMaths(self):
        if self.operator == Operators.XOR:
            if self.expressionVariables[0].isDefined() and self.expressionVariables[1].isDefined():
                v0, v1 = self.expressionVariables[0].value, self.expressionVariables[1].value
                val = v0 + v1 - 2 * v0 * v1
                return BasicExpressionBlock([ExpressionVariable("LITERAL", val)], Operators.NoOperator).doMaths()
            elif self.expressionVariables[0].isDefined() or self.expressionVariables[1].isDefined():
                v0, v1 = self.expressionVariables[0].value, self.expressionVariables[1].value
                if v0 == -1:
                    if v1 == 1:
                        return Not(self.expressionVariables[0]).doMaths()
                    else:
                        return BasicExpressionBlock([self.expressionVariables[0]], Operators.NoOperator)
                else:
                    if v0 == 1:
                        return Not(self.expressionVariables[1]).doMaths()
                    else:
                        return BasicExpressionBlock([self.expressionVariables[1]], Operators.NoOperator)
            else:
                return self
        if self.operator == Operators.AND:
            isZero = False
            remainingVariables = []
            for expressionVariable in self.expressionVariables:
                if expressionVariable.value == 0:
                    isZero = True
                    break
                elif not expressionVariable.isDefined():
                    remainingVariables.append(expressionVariable)

            if isZero:
                return BasicExpressionBlock([ExpressionVariable("LITERAL", 0)], Operators.NoOperator)
            elif len(remainingVariables) == 0:
                return BasicExpressionBlock([ExpressionVariable("LITERAL", 1)], Operators.NoOperator)
            else:
                return BasicExpressionBlock(remainingVariables, Operators.AND)

        if self.operator == Operators.OR:
            isOne = False
            remainingVariables = []
            for expressionVariable in self.expressionVariables:
                if expressionVariable.value == 1:
                    isOne = True
                    break
                elif not expressionVariable.isDefined():
                    remainingVariables.append(expressionVariable)

            if isOne:
                return BasicExpressionBlock([ExpressionVariable("LITERAL", 1)], Operators.NoOperator)
            elif len(remainingVariables) == 0:
                return BasicExpressionBlock([ExpressionVariable("LITERAL", 0)], Operators.NoOperator)
            else:
                return BasicExpressionBlock(remainingVariables, Operators.OR)

        if self.operator == Operators.NOT:
            return Not(self.expressionVariables[0]).doMaths()

        return self

    def isDefined(self):
        afterMath = self.doMaths()
        if type(afterMath) is BasicExpressionBlock:
            return len(afterMath.expressionVariables) == 1 and afterMath.expressionVariables[0].isDefined()
        if type(afterMath) is Not:
            return afterMath.expression.isDefined()
        return False

    def getValue(self):
        afterMath = self.doMaths()
        if type(afterMath) is BasicExpressionBlock:
            if len(afterMath.expressionVariables) == 1 and afterMath.expressionVariables[0].isDefined():
                return afterMath.expressionVariables[0].getValue()
        if type(afterMath) is Not:
            return afterMath.expression.getValue()
        return -999


class ExpressionVariable:
    # variableName = ""  # string
    # value = ""  # bool?

    def __init__(self, name, val=-1, toDb=True):
        self.variableName = name
        if name == "LITERAL":
            toDb = False
        self.value = val
        self.index = len(ExpressionVariableDatabase.expressionVariables)
        self.isdefined = val != -1
        if toDb: ExpressionVariableDatabase.expressionVariables.append(self)

    def __str__(self):
        return self.print("")

    def __repr__(self):
        return self.print("")

    def print(self, str=""):
        if self.value == -1:
            str += self.variableName
        else:
            str += self.value.__str__()

        return str

    def setValue(self, val):
        self.value = val
        self.isdefined = val != -1

    def getValue(self):
        return self.value

    def optimize(self, fullOptimize=False):
        return

    def isDefined(self):
        return self.isdefined

    def convertXor(self):
        return self


class ExpressionVariableDatabase:
    expressionVariables = []  # expVar

    def __init__(self, expvs=142857):
        if expvs == 142857: expvs = []
        self.expressionVariables = expvs

    @staticmethod
    def getVariableWithName(name):
        for var in ExpressionVariableDatabase.expressionVariables:
            if var.variableName == name: return var


class Operators(Enum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    XOR = "XOR"
    NoOperator = ""


def optimize(expression):
    if type(expression) is ExpressionBlock:
        if len(expression.expressionBlocks) == 0 and len(expression.basicExpressionBlocks) == 1:
            return expression.basicExpressionBlocks[0]
        elif len(expression.expressionBlocks) == 1 and len(expression.basicExpressionBlocks) == 0:
            return expression.expressionBlocks[0]
        else:
            return expression
    if type(expression) is BasicExpressionBlock:
        return expression
    if type(expression) is Not:
        return optimize(expression.expression)
    if type(expression) is ExpressionVariable:
        return expression


if __name__ == "__main__":
    MainCodeExecution()
