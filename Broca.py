from enum import Enum

print("Projeto broca!")

showClass = 0 == 1


def MainCodeExecution():
    # stringInput = "(" + input("Manual expression Override: ") + ")"
    # print(stringInput)
    ExpressionVariableDatabase()  # Variable database initialization

    e0 = ExpressionVariable("e0")
    e1 = ExpressionVariable("e1")
    d0 = ExpressionVariable("d0")
    d1 = ExpressionVariable("d1")
    c0 = ExpressionBlock([e0, d0], Operators.XOR)
    k0 = ExpressionBlock([ExpressionVariable("LITERAL", 0), ExpressionVariable("LITERAL", 0)], Operators.XOR)
    k0 = k0.doMaths()
    k1 = ExpressionBlock([
        ExpressionBlock([
            ExpressionBlock([
                e0,
                d0],
                Operators.XOR),
            k0],
            Operators.AND),
        ExpressionBlock([
            e0,
            d0],
            Operators.AND)],
        Operators.OR)

    k2 = ExpressionBlock([
        ExpressionBlock([
            ExpressionBlock([
                e1,
                d1],
                Operators.XOR),
            k1],
            Operators.AND),
        ExpressionBlock([
            e1,
            d1],
            Operators.AND)],
        Operators.OR)

    print("c0 = " + c0.print())
    print("k1 = " + k1.print())
    print("Running maths...")
    c0 = c0.doMaths()
    k1 = k1.doMaths()
    print("c0 = " + c0.print())
    print("k1 = " + k1.print())

    e0.setValue(0)

    print("Running maths...")
    c0 = c0.doMaths()
    k1 = k1.doMaths()
    print("c0 = " + c0.print())
    print("k1 = " + k1.print())

    print("\nFunciona!")


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
        self.formatXor(checkChild=True)

    def __str__(self):
        return self.print("")

    def print(self, str=""):
        str += "E(" if showClass else "("
        for i in range(len(self.expressionBlocks) + len(self.basicExpressionBlocks)):
            if i < len(self.expressionBlocks):
                str += self.expressionBlocks[i].print()

            else:
                i2 = i - len(self.expressionBlocks)
                str += self.basicExpressionBlocks[i2].print()

            if i < (len(self.expressionBlocks) + len(self.basicExpressionBlocks) - 1):
                str += " " + self.operator.value + " "

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

        # Join Basic Expression Blocks (BEB or BaEB or Bae) with the same operator into one
        for i in range(len(self.basicExpressionBlocks) - 1):
            if self.basicExpressionBlocks[i].operator == Operators.NOT:
                continue

            if self.basicExpressionBlocks[i].operator == Operators.NoOperator and len(self.basicExpressionBlocks[i].expressionVariables) > 0:
                for j in range(i + 1, len(self.basicExpressionBlocks)):
                    if self.basicExpressionBlocks[j].operator == Operators.NoOperator:
                        self.basicExpressionBlocks[i] = BasicExpressionBlock((
                            self.basicExpressionBlocks[i].expressionVariables +
                            self.basicExpressionBlocks[j].expressionVariables),
                            self.operator)
                        self.basicExpressionBlocks[j] = BasicExpressionBlock([], Operators.NoOperator)

            if self.basicExpressionBlocks[i].operator != Operators.NoOperator:
                for j in range(i + 1, len(self.basicExpressionBlocks)):
                    if self.basicExpressionBlocks[i].operator == self.basicExpressionBlocks[j].operator:
                        self.basicExpressionBlocks[i].expressionVariables += self.basicExpressionBlocks[j].expressionVariables
                        self.basicExpressionBlocks[j] = BasicExpressionBlock([], Operators.NoOperator)

        # Remove empty Basic Expression Blocks (BEB or BaEB or Bae)
        r = 0
        for i in range(len(self.basicExpressionBlocks)):
            if i - r < len(self.basicExpressionBlocks):
                if len(self.basicExpressionBlocks[i - r].expressionVariables) == 0:
                    self.basicExpressionBlocks.pop(i - r)
                    r += 1

        if len(self.expressionBlocks) == 1 and len(self.basicExpressionBlocks) == 0 and self.operator != Operators.NOT:
            holder = self.expressionBlocks[0]
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

            self.basicExpressionBlocks = newBae
            self.expressionBlocks = newEB

        if self.operator == Operators.XOR and len(self.basicExpressionBlocks + self.expressionBlocks) > 2:
            remainingEB = self.expressionBlocks + self.basicExpressionBlocks
            exp = []
            for i in range(1, len(remainingEB)):
                exp.append(remainingEB[i])

            remainingEB = list(set(remainingEB) - set(exp))
            return ExpressionBlock([remainingEB, ExpressionBlock(exp, Operators.XOR)], Operators.XOR)
        else:
            return self

    def doMaths(self):
        expressions = []
        for expression in self.expressionBlocks + self.basicExpressionBlocks:
            expressions.append(expression.doMaths())

        if len(expressions) > 1:
            if self.operator == Operators.XOR:
                if expressions[0].isDefined() and expressions[1].isDefined():
                    v0, v1 = expressions[0].value, expressions[1].value
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
            return Not(expression[0]).doMaths()

        return ExpressionBlock(expressions, Operators.NoOperator)

    def isDefined(self):
        if len(self.expressionBlocks) == 0 and len(self.basicExpressionBlocks) == 1:
            if len(self.basicExpressionBlocks[0].expressionVariables) == 1:
                return self.basicExpressionBlocks[0].expressionVariables[0].isDefined()
        return False

    def getValue(self):
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
        self.expression.formatXor(checkChild)

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
        if type(self.expression) is Not:
            return self.expression.doMaths()
        elif type(self.expression) is ExpressionVariable:
            if self.expression.isDefined():
                return BasicExpressionBlock([ExpressionVariable("LITERAL", 1 - self.expression.value)], Operators.NoOperator)
            else:
                return self
        else:
            return Not(self.expression.doMaths())


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

    def formatXor(self):
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


if __name__ == "__main__":
    MainCodeExecution()
