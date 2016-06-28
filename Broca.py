from enum import Enum

print("Projeto broca!")


def MainCodeExecution():
    # stringInput = "(" + input("Manual expression Override: ") + ")"
    # print(stringInput)
    ExpressionVariableDatabase()

    finalExpression = ExpressionBlock([
        ExpressionVariable("a"),
        ExpressionVariable("b")],
        Operators.XOR
    )

    finalExpression.print()
    print("After full optimization:")
    finalExpression.optimize(fullOptimization=True)
    finalExpression.print()
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

        self.optimize()

    def print(self, end="\n"):
        print("E(", end="")
        for i in range(len(self.expressionBlocks) + len(self.basicExpressionBlocks)):
            if i < len(self.expressionBlocks):
                self.expressionBlocks[i].print(end="")

            else:
                i2 = i - len(self.expressionBlocks)
                self.basicExpressionBlocks[i2].print(end="")

            if i < (len(self.expressionBlocks) + len(self.basicExpressionBlocks) - 1):
                print(" " + self.operator.value + " ", end="")

        print(")", end=end)

    def optimize(self, fullOptimization=False):  # Where maths are applied

        if fullOptimization:
            for block in self.expressionBlocks + self.basicExpressionBlocks:
                block.optimize()

        # Transform Expression Blocks (EB or EBo) with one Bae into one Bae
        for i in range(len(self.expressionBlocks)):
            if len(self.expressionBlocks[i].expressionBlocks) == 0 and len(self.expressionBlocks[i].basicExpressionBlocks) == 1:
                self.basicExpressionBlocks.append(self.expressionBlocks[i].basicExpressionBlocks[0])
                self.expressionBlocks[i] = ExpressionBlock([], Operators.NoOperator)

        # Remove empty Expression Blocks (EB or EBo)
        r = 0
        for i in range(len(self.expressionBlocks) - r):
            if i - r < len(self.expressionBlocks):
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
                        self.basicExpressionBlocks[i] = BasicExpressionBlock(
                            (
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

    def formatXor(self):
        if self.operator == Operators.XOR and len(self.basicExpressionBlocks + self.expressionBlocks) > 2:
            remainingEB = self.expressionBlocks + self.basicExpressionBlocks
            exp = []
            for i in range(1, len(remainingEB)):
                exp.append(remainingEB[i])

            remainingEB = list(set(remainingEB) - set(exp))
            return ExpressionBlock([remainingEB, ExpressionBlock(exp, Operators.XOR)], Operators.XOR)
        else:
            return self


class BasicExpressionBlock:
    # expressionVariables = []  # expVar
    # operator = ""

    def __init__(self, expvs, op):
        self.expressionVariables = expvs
        self.operator = op
        self.optimize()

    def print(self, end="\n"):
        if self.operator == Operators.NOT:
            print("!", end="")
            self.expressionVariables[0].print(end="")
        elif self.operator == Operators.NoOperator:
            self.expressionVariables[0].print(end="")
        else:
            print("B(", end="")
            for i in range(len(self.expressionVariables)):
                self.expressionVariables[i].print(end="")
                if i < (len(self.expressionVariables) - 1):
                    print(" " + self.operator.value + " ", end="")

            print(")", end=end)

    def optimize(self):  # Where simple maths are applied
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


class ExpressionVariable:
    # variableName = ""  # string
    # value = ""  # bool?

    def __init__(self, name, val=-1):
        self.variableName = name
        self.value = val
        self.index = len(ExpressionVariableDatabase().expressionVariables)
        ExpressionVariableDatabase().expressionVariables.append(self)

    def print(self, end="\n"):
        if self.value == -1:
            print(self.variableName, end=end)
        else:
            print(self.value, end=end)


class ExpressionVariableDatabase:
    expressionVariables = []  # expVar

    def __init__(self, expvs=[]):
        self.expressionVariables = expvs


class Operators(Enum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    XOR = "XOR"
    NoOperator = ""


if __name__ == "__main__":
    MainCodeExecution()
