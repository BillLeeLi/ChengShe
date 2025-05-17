import tkinter as tk
from tkinter import messagebox
import sympy
from sympy.abc import x, y
import scipy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import re


def insert_multiplication(expr: str):
    """
    该方法接受一个字符串expr,作用是为表达式插入*,因为在习惯上某些数学表达式往往省去乘号
    返回值是插入*之后的字符串
    """
    expr = re.sub(
        r"([xyeπ\d\)])([πa-zA-Z\(])", r"\1*\2", expr
    )  # 数字、xyeπ或)在左且(、字母和π在右的时候中间加上*
    print(expr)
    return expr


def process_expr(expr: str):
    """
    该方法接受一个字符串expr,作用是把常见函数名转化为np.函数名的形式
    """
    expr = re.sub(r"ln", r"log", expr)  # ln转化为log
    expr = re.sub(r"\^", r"**", expr)
    functions = [
        "sin",
        "cos",
        "tan",
        "arcsin",
        "arccos",
        "arctan",
        # "exp", 我个人的想法是表达式里面不要出现exp,全都用e^...的形式,然后转化为np.e**...就可处理
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
    print(expr)
    return expr


def draw_plots(master, expr: str, plot_canvas: FigureCanvasTkAgg, ax):
    """
    该方法以master为父窗口,插入画板绘出expr对应的图像
    plot_canvas是一个FigureCanvasTkAgg对象, ax是轴对象
    plot_canvas最好作为窗口的一个组件存在,而不是在函数的内部存在
    """
    original_expr = expr
    expr = insert_multiplication(expr)
    expr = process_expr(expr)
    xs = np.linspace(-5, 5, 100)  # x轴上打出点列
    try:
        ys = eval(expr, {"x": xs, "np": np, "__builtins__": {}})
        ax.plot(xs, ys)
        ax.set_label(f"y={original_expr}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        plot_canvas.draw()
    except Exception as e:
        print(e)  # 测试语句
        messagebox.showerror(title="错误", message=f"无法解析表达式: {e}")


def calc(expr: str):
    """
    该方法计算表达式expr的值,表达式中不应该含有变量如x y
    如果表达式计算出现异常,弹出窗口并返回None
    如果正常,返回计算式的结果
    """
    expr = insert_multiplication(expr)
    expr = process_expr(expr)
    try:
        res = eval(expr, {"np": np, "π": np.pi, "__builtins__": {}})
        return str(res)
    except Exception as e:
        print(e)  # 用于测试，后期会注释掉
        messagebox.showerror(title="错误", message="请检查算术表达式")

        # 后期可以增加异常类型的判断，来更好地提示用户。比如用户可能在算式中包含了未知量，或者计算除以0这种常见错误
        return None
