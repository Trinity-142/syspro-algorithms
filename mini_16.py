import pytest


class Stack:
    def __init__(self):
        self.list = []

    def push(self, item):
        self.list.append(item)

    def pop(self):
        return self.list.pop()

    def peek(self):
        return self.list[-1]

    def empty(self):
        return len(self.list) == 0


operators = [('!', '~'), ('*', '/', '%'), ('+', '-'), ('<<', '>>'), '&', '^', '|', '&&', '||']
r2l = [('!', '~')]


def priority(operator: str) -> int:
    for i in range(len(operators)):
        if operator in operators[i]:
            return i


def l2r(operator: str) -> bool:
    for i in range(len(r2l)):
        if operator in r2l[i]:
            return False
    return True


def infix_to_rpn(expression: str) -> str:
    expression = expression.split()
    stack = Stack()
    ans = []
    for curr in expression:
        if curr.isdigit():
            ans.append(curr)
        elif stack.empty() or curr == '(' or stack.peek() == '(':
            stack.push(curr)

        elif curr == ')':
            while stack.peek() != '(':
                ans.append(stack.pop())
            stack.pop()

        elif priority(stack.peek()) < priority(curr) or (priority(stack.peek()) == priority(curr) and l2r(curr)):
            ans.append(stack.pop())
            stack.push(curr)
        else:
            stack.push(curr)

    while not stack.empty():
        ans.append(stack.pop())

    return ' '.join(ans)


@pytest.mark.parametrize("input_expr, expected_rpn", [
    ("3 + 4 * 2 / ( 1 - 5 )", "3 4 2 * 1 5 - / +"),
    ("( 3 + 4 ) * 2", "3 4 + 2 *"),
    ("5 + 2 * ( 3 - 1 )", "5 2 3 1 - * +"),
    ("4 << 2 + 3", "4 2 3 + <<"),
    ("6 & ( 2 | 3 )", "6 2 3 | &"),
    ("7 ^ 3 & 1", "7 3 1 & ^"),
    ("8 | 3 ^ 1", "8 3 1 ^ |"),
    ("9 && 2 || 1", "9 2 && 1 ||"),
    ("~ 5 + 3", "5 ~ 3 +"),
    ("! 4 && 2", "4 ! 2 &&")
])
def test_infix_to_rpn(input_expr, expected_rpn):
    assert infix_to_rpn(input_expr) == expected_rpn
