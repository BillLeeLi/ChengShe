import numpy as np
import sympy
from sympy.abc import x
import scipy.optimize
import re

# from 科学计算器 import insert_multiplication, process_expression
from tkinter import *


def insert_multiplication(expr):
    expr = re.sub(
        r"([\d])([a-zA-Z\(])", r"\1*\2", expr
    )  # 字母或者左括号紧邻在数字的右侧时加上*
    expr = re.sub(r"\)([a-zA-Z\(])", r")*(", expr)
    print("insert multiplication:", expr)
    return expr


def process_expression(expr: str):
    functions = [
        "sin",
        "cos",
        "tan",
        "arcsin",
        "arccos",
        "arctan",
        "exp",
        "log",
        "abs",
        "sqrt",
        "sinh",
        "cosh",
        "arcsinh",
        "arccosh",
        "arctanh",
    ]
    for func in functions:
        expr = re.sub(rf"\b{func}\s*\(", f"np.{func}(", expr)
        # 如果检测到表达式中有"函数名("的形式，替换为"np.函数名("
    print("process expression", expr)
    return expr


# expr是一个字符串，也是一个函数的表达式(没有=，所以不是方程)
# 如果需要求解方程的根，只需要把方程的一侧移到另一侧，然后求函数的零点
def find_all_roots(expr: str, x_range=(-10, 10), error=1e-7):
    expr = insert_multiplication(expr)
    # expr = process_expression(expr)
    # sympy库中有常见函数，不需要给函数名前加上np.
    func = sympy.lambdify(x, expr, "numpy")
    xs = np.linspace(x_range[0], x_range[1], 1000)
    roots = []

    for s in xs:
        try:
            root = scipy.optimize.fsolve(func, s)[0]
            if not any(abs(root - r) < error for r in roots):
                roots.append(root)
        except Exception as e:
            print(e)
            return roots

    return sorted(roots)


def calc():
    roots = find_all_roots(txt.get())
    # print(roots)
    if len(roots) == 0:
        res.config(text="无零点")
        return
    s = "零点为："
    for root in roots:
        s += f" {root:.5f}"
    res.config(text=s)
    res.pack()


root = Tk()
root.geometry("400x400")
root.title("函数求零点")

Label(root, text="请输入需要求零点的函数", font=("bold", 15)).pack(pady=5)
txt = StringVar()
Entry(root, font=("bold", 15), textvariable=txt).pack(pady=5)
Button(root, command=calc, font=("bold", 15), text="计算").pack(pady=5)
res = Label(root, font=("bold", 15))


mainloop()
