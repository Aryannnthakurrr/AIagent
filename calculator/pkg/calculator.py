class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else float('inf'),
        }
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = self._tokenize(expression)
        return self._evaluate_infix(tokens)

    def _tokenize(self, expression):
        tokens = []
        current_number = ""
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            elif char in self.operators:
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                tokens.append(char)
            elif char == '(' or char == ')':
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
                tokens.append(char)

            elif char.isspace():
                if current_number:
                    tokens.append(current_number)
                    current_number = ""
            else:
                raise ValueError(f"Invalid character: {char}")
        if current_number:
            tokens.append(current_number)
        return tokens

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while operators and operators[-1] != '(' and self.precedence[token] <= self.precedence.get(operators[-1], 0):
                    self._apply_operator(operators, values)
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, values)
                if operators:
                    operators.pop()  # Remove '('
                else:
                    raise ValueError("Unmatched parentheses")
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"Not enough operands for operator {operator}")
        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))
