#!/usr/bin/env python3
import re
import math
import sys
import random
from typing import List, Dict, Any, Tuple, Optional

class BlipFunction:
    __slots__ = ('name', 'params', 'body')
    def __init__(self, name: str, params: List[str], body: List[str]):
        self.name = name
        self.params = params
        self.body = body

class ReturnException(Exception):
    __slots__ = ('value',)
    def __init__(self, value):
        self.value = value

class BlipInterpreter:
    TOKEN_PATTERN = re.compile(r'(?P<NUMBER>-?\d+\.?\d*)|(?P<STRING>"[^"]*")|(?P<KEYWORD>if|else|end|func|return|for|while|break|continue|in)|(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z0-9_]*)|(?P<COMPARISON>==|!=|<=|>=|<|>)|(?P<LOGICAL>and|or|not)|(?P<ASSIGN>=)|(?P<SEMICOLON>;)|(?P<LPAREN>\()|(?P<RPAREN>\))|(?P<LBRACKET>\[)|(?P<RBRACKET>\])|(?P<COMMA>,)|(?P<DOT>\.)|(?P<OPERATOR>[\+\-\*/%])|(?P<POWER>\*\*)|(?P<WHITESPACE>\s+)|(?P<UNKNOWN>.)')
    
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, BlipFunction] = {}
        self.builtin_functions = {
            'print': lambda *args: print(' '.join(str(arg) for arg in args)),
            'input': lambda prompt="": input(str(prompt)),
            'abs': abs, 'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan, 'atan2': math.atan2,
            'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
            'log': math.log, 'log10': math.log10, 'log2': math.log2, 'exp': math.exp,
            'floor': math.floor, 'ceil': math.ceil, 'round': round, 'max': max, 'min': min,
            'pow': pow, 'len': len, 'type': lambda x: type(x).__name__,
            'sum': lambda lst: sum(lst) if isinstance(lst, list) else lst,
            'avg': lambda lst: sum(lst) / len(lst) if isinstance(lst, list) and lst else 0,
            'factorial': lambda n: math.factorial(int(n)) if n >= 0 else (_ for _ in ()).throw(ValueError("Factorial not defined for negative numbers")),
            'gcd': math.gcd, 'lcm': lambda a, b: abs(int(a) * int(b)) // math.gcd(int(a), int(b)),
            'mod': lambda x, y: x % y, 'div': lambda x, y: x // y,
            'random': random.random, 'randint': random.randint,
            'range': lambda *args: list(range(*[int(a) for a in args])),
            'append': lambda lst, item: lst.append(item) or lst if isinstance(lst, list) else (_ for _ in ()).throw(TypeError("append() requires a list")),
            'pop': lambda lst, index=-1: lst.pop(int(index)) if isinstance(lst, list) else (_ for _ in ()).throw(TypeError("pop() requires a list")),
            'size': len, 'sort': sorted, 'reverse': lambda lst: lst[::-1] if isinstance(lst, list) else lst,
            'pi': lambda: math.pi, 'e': lambda: math.e, 'deg': math.degrees, 'rad': math.radians,
            'is_prime': lambda n: n > 1 and all(n % i for i in range(2, int(n**0.5) + 1)),
            'fibonacci': self._fib
        }
    
    def _fib(self, n):
        n = int(n)
        if n <= 0: return 0
        if n == 1: return 1
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    def tokenize(self, code: str) -> List[Tuple[str, str]]:
        return [(match.lastgroup, match.group()) for match in self.TOKEN_PATTERN.finditer(code) if match.lastgroup != 'WHITESPACE']
    
    def parse_expression(self, tokens: List[Tuple[str, str]], start: int = 0) -> Tuple[Any, int]:
        return self.parse_logical_or(tokens, start)
    
    def parse_logical_or(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        left, pos = self.parse_logical_and(tokens, start)
        while pos < len(tokens) and tokens[pos] == ('LOGICAL', 'or'):
            pos += 1
            right, pos = self.parse_logical_and(tokens, pos)
            left = left or right
        return left, pos
    
    def parse_logical_and(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        left, pos = self.parse_logical_not(tokens, start)
        while pos < len(tokens) and tokens[pos] == ('LOGICAL', 'and'):
            pos += 1
            right, pos = self.parse_logical_not(tokens, pos)
            left = left and right
        return left, pos
    
    def parse_logical_not(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        if start < len(tokens) and tokens[start] == ('LOGICAL', 'not'):
            expr, pos = self.parse_comparison(tokens, start + 1)
            return not expr, pos
        return self.parse_comparison(tokens, start)
    
    def parse_comparison(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        left, pos = self.parse_addition(tokens, start)
        if pos < len(tokens) and tokens[pos][0] == 'COMPARISON':
            op = tokens[pos][1]
            pos += 1
            right, pos = self.parse_addition(tokens, pos)
            ops = {'==': lambda x, y: x == y, '!=': lambda x, y: x != y, '<': lambda x, y: x < y, '>': lambda x, y: x > y, '<=': lambda x, y: x <= y, '>=': lambda x, y: x >= y}
            left = ops[op](left, right)
        return left, pos
    
    def parse_addition(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        left, pos = self.parse_multiplication(tokens, start)
        while pos < len(tokens) and tokens[pos][0] == 'OPERATOR' and tokens[pos][1] in '+-':
            op = tokens[pos][1]
            pos += 1
            right, pos = self.parse_multiplication(tokens, pos)
            left = left + right if op == '+' else left - right
        return left, pos
    
    def parse_multiplication(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        left, pos = self.parse_power(tokens, start)
        while pos < len(tokens) and tokens[pos][0] == 'OPERATOR' and tokens[pos][1] in '*/%':
            op = tokens[pos][1]
            pos += 1
            right, pos = self.parse_power(tokens, pos)
            left = left * right if op == '*' else left / right if op == '/' else left % right
        return left, pos
    
    def parse_power(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        left, pos = self.parse_primary(tokens, start)
        if pos < len(tokens) and tokens[pos][0] == 'POWER':
            pos += 1
            right, pos = self.parse_power(tokens, pos)
            left = left ** right
        return left, pos
    
    def parse_primary(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        if start >= len(tokens):
            raise SyntaxError("Unexpected end of expression")
        
        token_type, token_value = tokens[start]
        
        if token_type == 'NUMBER':
            return (float(token_value) if '.' in token_value else int(token_value)), start + 1
        if token_type == 'STRING':
            return token_value[1:-1], start + 1
        if token_type == 'LBRACKET':
            return self.parse_list(tokens, start)
        if token_type == 'IDENTIFIER':
            if start + 1 < len(tokens):
                if tokens[start + 1][0] == 'LPAREN':
                    return self.parse_function_call(tokens, start)
                if tokens[start + 1][0] == 'LBRACKET':
                    return self.parse_list_access(tokens, start)
                if tokens[start + 1][0] == 'DOT':
                    return self.parse_property_access(tokens, start)
            if token_value in self.variables:
                return self.variables[token_value], start + 1
            raise NameError(f"Variable '{token_value}' not defined")
        if token_type == 'LPAREN':
            expr, pos = self.parse_expression(tokens, start + 1)
            if pos >= len(tokens) or tokens[pos][0] != 'RPAREN':
                raise SyntaxError("Expected closing parenthesis")
            return expr, pos + 1
        
        raise SyntaxError(f"Unexpected token: {token_value}")
    
    def parse_property_access(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        var_name = tokens[start][1]
        if start + 2 >= len(tokens) or tokens[start + 1][0] != 'DOT' or tokens[start + 2][0] != 'IDENTIFIER':
            raise SyntaxError("Invalid property access")
        
        property_name = tokens[start + 2][1]
        
        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' not defined")
        
        var_value = self.variables[var_name]
        
        if property_name == 'length':
            if isinstance(var_value, list):
                return len(var_value), start + 3
            else:
                raise TypeError(f"'{var_name}' does not have a length property")
        else:
            raise AttributeError(f"'{type(var_value).__name__}' object has no attribute '{property_name}'")
    
    def parse_list(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[List[Any], int]:
        pos = start + 1
        elements = []
        
        if pos < len(tokens) and tokens[pos][0] != 'RBRACKET':
            while True:
                elem, pos = self.parse_expression(tokens, pos)
                elements.append(elem)
                if pos >= len(tokens):
                    raise SyntaxError("Expected closing bracket")
                if tokens[pos][0] == 'RBRACKET':
                    break
                if tokens[pos][0] == 'COMMA':
                    pos += 1
                else:
                    raise SyntaxError("Expected comma or closing bracket")
        
        return elements, pos + 1
    
    def parse_list_access(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        var_name = tokens[start][1]
        pos = start + 2
        index, pos = self.parse_expression(tokens, pos)
        if pos >= len(tokens) or tokens[pos][0] != 'RBRACKET':
            raise SyntaxError("Expected closing bracket")
        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' not defined")
        var_value = self.variables[var_name]
        if not isinstance(var_value, list):
            raise TypeError(f"'{var_name}' is not indexable")
        try:
            return var_value[int(index)], pos + 1
        except IndexError:
            raise IndexError("List index out of range")
    
    def parse_function_call(self, tokens: List[Tuple[str, str]], start: int) -> Tuple[Any, int]:
        func_name = tokens[start][1]
        pos = start + 2
        args = []
        
        if pos < len(tokens) and tokens[pos][0] != 'RPAREN':
            while True:
                arg, pos = self.parse_expression(tokens, pos)
                args.append(arg)
                if pos >= len(tokens):
                    raise SyntaxError("Expected closing parenthesis")
                if tokens[pos][0] == 'RPAREN':
                    break
                if tokens[pos][0] == 'COMMA':
                    pos += 1
                else:
                    raise SyntaxError("Expected comma or closing parenthesis")
        
        pos += 1
        
        if func_name in self.builtin_functions:
            result = self.builtin_functions[func_name](*args)
            return result, pos
        if func_name in self.functions:
            result = self.call_user_function(func_name, args)
            return result, pos
        
        raise NameError(f"Function '{func_name}' not defined")
    
    def call_user_function(self, func_name: str, args: List[Any]) -> Any:
        func = self.functions[func_name]
        if len(args) != len(func.params):
            raise TypeError(f"Function '{func_name}' expects {len(func.params)} arguments, got {len(args)}")
        
        old_vars = self.variables.copy()
        for param, arg in zip(func.params, args):
            self.variables[param] = arg
        
        try:
            result = self.execute_function_body(func.body)
        except ReturnException as e:
            result = e.value
        finally:
            self.variables = old_vars
        
        return result if result is not None else 0
    
    def execute_function_body(self, body_lines: List[str]) -> Optional[Any]:
        for line in body_lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('return '):
                return_expr = line[7:-1]
                tokens = self.tokenize(return_expr)
                value, _ = self.parse_expression(tokens, 0)
                raise ReturnException(value)
            else:
                self.execute_line(line)
        return None
    
    def parse_statement(self, tokens: List[Tuple[str, str]]) -> None:
        if not tokens:
            return
        
        if tokens[0] == ('KEYWORD', 'if'):
            self.parse_if_statement(tokens)
        elif tokens[0] == ('KEYWORD', 'func'):
            self.parse_function_definition(tokens)
        elif tokens[0] == ('KEYWORD', 'for'):
            self.parse_for_statement(tokens)
        elif tokens[0] == ('KEYWORD', 'while'):
            self.parse_while_statement(tokens)
        elif len(tokens) >= 3 and tokens[0][0] == 'IDENTIFIER' and tokens[1] == ('ASSIGN', '='):
            var_name = tokens[0][1]
            value, _ = self.parse_expression(tokens, 2)
            self.variables[var_name] = value
        elif len(tokens) >= 5 and tokens[0][0] == 'IDENTIFIER' and tokens[1] == ('LBRACKET', '['):
            var_name = tokens[0][1]
            index, pos = self.parse_expression(tokens, 2)
            if pos < len(tokens) and tokens[pos] == ('RBRACKET', ']') and pos + 1 < len(tokens) and tokens[pos + 1] == ('ASSIGN', '='):
                value, _ = self.parse_expression(tokens, pos + 2)
                if var_name not in self.variables or not isinstance(self.variables[var_name], list):
                    raise TypeError(f"'{var_name}' is not a list")
                self.variables[var_name][int(index)] = value
            else:
                raise SyntaxError("Invalid list assignment")
        else:
            self.parse_expression(tokens, 0)
    
    def parse_function_definition(self, tokens: List[Tuple[str, str]]) -> Tuple[str, str, List[str]]:
        if len(tokens) < 4:
            raise SyntaxError("Invalid function definition")
        func_name = tokens[1][1]
        if tokens[2] != ('LPAREN', '('):
            raise SyntaxError("Expected '(' after function name")
        pos = 3
        params = []
        if pos < len(tokens) and tokens[pos] != ('RPAREN', ')'):
            while True:
                if tokens[pos][0] != 'IDENTIFIER':
                    raise SyntaxError("Expected parameter name")
                params.append(tokens[pos][1])
                pos += 1
                if pos >= len(tokens):
                    raise SyntaxError("Expected closing parenthesis")
                if tokens[pos] == ('RPAREN', ')'):
                    break
                if tokens[pos] == ('COMMA', ','):
                    pos += 1
                else:
                    raise SyntaxError("Expected comma or closing parenthesis")
        return ('func', func_name, params)
    
    def parse_if_statement(self, tokens: List[Tuple[str, str]]) -> Tuple[str, Any]:
        condition, _ = self.parse_expression(tokens, 1)
        return ('if', condition)
    
    def parse_for_statement(self, tokens: List[Tuple[str, str]]) -> Tuple[str, str, Any]:
        if len(tokens) < 4:
            raise SyntaxError("Invalid for statement")
        var_name = tokens[1][1]
        if len(tokens) < 3 or tokens[2][1] != 'in':
            raise SyntaxError("Expected 'in' in for statement")
        iterable, _ = self.parse_expression(tokens, 3)
        return ('for', var_name, iterable)
    
    def parse_while_statement(self, tokens: List[Tuple[str, str]]) -> Tuple[str, Any]:
        condition, _ = self.parse_expression(tokens, 1)
        return ('while', condition)
    
    def find_block_end(self, lines: List[str], start_line: int) -> int:
        brace_count = 1
        end_line = start_line + 1
        while end_line < len(lines) and brace_count > 0:
            line = lines[end_line].strip()
            if line.startswith(('for ', 'while ', 'if ')):
                brace_count += 1
            elif line.startswith('end;'):
                brace_count -= 1
            end_line += 1
        if brace_count > 0:
            raise SyntaxError("Missing 'end;' for block")
        return end_line - 1
    
    def execute_function_block(self, lines: List[str], start_line: int) -> int:
        func_line = lines[start_line].strip()[:-1]
        tokens = self.tokenize(func_line)
        _, func_name, params = self.parse_function_definition(tokens)
        end_line = start_line + 1
        while end_line < len(lines):
            if lines[end_line].strip().startswith('end;'):
                break
            end_line += 1
        if end_line >= len(lines):
            raise SyntaxError("Missing 'end;' for function definition")
        body_lines = lines[start_line + 1:end_line]
        self.functions[func_name] = BlipFunction(func_name, params, body_lines)
        return end_line
    
    def execute_for_block(self, lines: List[str], start_line: int) -> int:
        for_line = lines[start_line].strip()[:-1]
        tokens = self.tokenize(for_line)
        _, var_name, iterable = self.parse_for_statement(tokens)
        end_line = self.find_block_end(lines, start_line)
        old_var = self.variables.get(var_name)
        try:
            for item in iterable:
                self.variables[var_name] = item
                self.execute_block_body(lines, start_line + 1, end_line)
        finally:
            if old_var is not None:
                self.variables[var_name] = old_var
            elif var_name in self.variables:
                del self.variables[var_name]
        return end_line
    
    def execute_while_block(self, lines: List[str], start_line: int) -> int:
        while_line = lines[start_line].strip()[:-1]
        tokens = self.tokenize(while_line)
        _, condition = self.parse_while_statement(tokens)
        end_line = self.find_block_end(lines, start_line)
        while condition:
            self.execute_block_body(lines, start_line + 1, end_line)
            tokens = self.tokenize(while_line)
            _, condition = self.parse_while_statement(tokens)
        return end_line
    
    def execute_if_block(self, lines: List[str], start_line: int) -> int:
        condition_line = lines[start_line].strip()[:-1]
        tokens = self.tokenize(condition_line)
        condition, _ = self.parse_expression(tokens, 1)
        end_line = self.find_block_end(lines, start_line)
        else_line = None
        for i in range(start_line + 1, end_line):
            if lines[i].strip().startswith('else;'):
                else_line = i
                break
        if condition:
            self.execute_block_body(lines, start_line + 1, else_line or end_line)
        elif else_line:
            self.execute_block_body(lines, else_line + 1, end_line)
        return end_line
    
    def execute_block_body(self, lines: List[str], start: int, end: int) -> None:
        i = start
        while i < end:
            line = lines[i].strip()
            if line.startswith(('for ', 'while ', 'if ')):
                if line.startswith('for '):
                    i = self.execute_for_block(lines, i)
                elif line.startswith('while '):
                    i = self.execute_while_block(lines, i)
                elif line.startswith('if '):
                    i = self.execute_if_block(lines, i)
            else:
                self.execute_line(lines[i])
            i += 1
    
    def execute_line(self, line: str) -> None:
        line = line.strip()
        if not line or line.startswith('#'):
            return
        if not line.endswith(';'):
            raise SyntaxError("Statement must end with semicolon")
        tokens = self.tokenize(line[:-1])
        self.parse_statement(tokens)
    
    def execute_code(self, code: str) -> None:
        lines = code.split('\n')
        line_num = 0
        while line_num < len(lines):
            try:
                line = lines[line_num].strip()
                if not line or line.startswith('#'):
                    line_num += 1
                    continue
                if line.startswith('func '):
                    line_num = self.execute_function_block(lines, line_num) + 1
                elif line.startswith('if '):
                    line_num = self.execute_if_block(lines, line_num) + 1
                elif line.startswith('for '):
                    line_num = self.execute_for_block(lines, line_num) + 1
                elif line.startswith('while '):
                    line_num = self.execute_while_block(lines, line_num) + 1
                elif line in ('end;', 'else;'):
                    line_num += 1
                else:
                    self.execute_line(line)
                    line_num += 1
            except Exception as e:
                print(f"Error on line {line_num + 1}: {e}")
                break
    
    def run_file(self, filename: str) -> None:
        if not filename.endswith('.blip'):
            print("Error: File must have .blip extension")
            return
        try:
            with open(filename, 'r') as f:
                self.execute_code(f.read())
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
        except Exception as e:
            print(f"Error reading file: {e}")

def main():
    interpreter = BlipInterpreter()
    if len(sys.argv) > 1:
        interpreter.run_file(sys.argv[1])

if __name__ == "__main__":
    main()