print("Projeto broca!")


def MainCodeExecution():
    # stringInput = "(" + input("Manual expression Override: ") + ")"
    # print(stringInput)
    a = ExpressionVariable("a", "")
    b = ExpressionVariable("b", "")
    c = ExpressionVariable("c", "")

    finalExpression = ExpressionBlock([
        ExpressionBlock([
            BasicExpressionBlock([a], "NOT"),
            BasicExpressionBlock([b], "NOT"),
            BasicExpressionBlock([c], "")],
            "OR"),
        BasicExpressionBlock([
            a,
            b,
            c],
            "OR")],
        "AND")

    finalExpression.print()
    print("\nFunciona??")


class ExpressionBlock:
    expressionBlocks = []  # ExpBlock
    basicExpressionBlocks = []  # BasicExpBlock
    operator = ""

    def __init__(self, expressions, op):
        self.operator = op
        for expression in expressions:
            if type(expression) is ExpressionBlock:
                self.expressionBlocks.append(expression)
            elif type(expression) is BasicExpressionBlock:
                self.basicExpressionBlocks.append(expression)

    def print(self):
        print("(",end="")
        for i in range(len(self.expressionBlocks) + len(self.basicExpressionBlocks)):
            if i < len(self.expressionBlocks):
                self.expressionBlocks[i].print()

            else:
                i2 = i - len(self.expressionBlocks)
                self.basicExpressionBlocks[i2].print()

            if i < (len(self.expressionBlocks) + len(self.basicExpressionBlocks) - 1):
                print(" " + self.operator + " ", end="")

        print(")", end="")


class BasicExpressionBlock:
    expressionVariables = []  # expVar
    operator = ""

    def __init__(self, expvs, op):
        self.expressionVariables = expvs
        self.operator = op

    def print(self):
        if self.operator == "NOT":
            print("!", end="")
            self.expressionVariables[0].print()
        else:
            print("(", end="")
            for i in range(len(self.expressionVariables)):
                self.expressionVariables[i].print()
                if i < (len(self.expressionVariables) - 1):
                    print(" " + self.operator + " ", end="")

            print(")", end="")


class ExpressionVariable:
    variableName = ""  # string
    value = ""  # bool?

    def __init__(self, name, val):
        self.variableName = name
        self.value =  val

    def print(self):
        print(self.variableName, end="")


class ExpressionVariableDatabase:
    indexer = []  # varReferencer
    expressionVariables = []  # expVar

    def __init__(self, idx, expvs):
        self.indexer = idx
        self.expressionVariables = expvs


class VariableReferencer:
    variableName = ""  # string
    variableIndex = 0  # int

    def __init__(self, name, index):
        self.variableName = name
        self.variableIndex = index


if __name__ == "__main__":
    MainCodeExecution()