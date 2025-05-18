import tkinter as tk
from tkinter import messagebox
import sympy
import scipy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import re
import warnings


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


def calc(expr: str):
    """
    该方法计算表达式expr的值,表达式中不应该含有变量如x y
    如果表达式计算出现异常,弹出窗口并返回None
    如果正常,返回计算式的结果
    """
    expr = insert_multiplication(expr)
    expr = process_expr(expr)
    try:
        with warnings.catch_warnings():  # 忽略计算中的异常，只捕获算式不合法导致的错误
            warnings.simplefilter("ignore", category=RuntimeWarning)
            res = eval(expr, {"np": np, "π": np.pi, "__builtins__": {}})
            return str(res)
    except Exception as e:
        print(e)  # 用于测试，后期会注释掉
        messagebox.showerror(title="错误", message="请检查算术表达式")
        return None


class FigureCanvas:
    def __init__(self, fig, ax, parent):
        # fig是绑定的图像，ax是轴，parent是父窗口
        # 成员都设置为私有的
        self.__ax = ax
        self.__plot_canvas = FigureCanvasTkAgg(fig, master=parent)
        self.__toolbar = NavigationToolbar2Tk(self.__plot_canvas, parent)
        self.__toolbar.update()
        self.__plot_canvas.get_tk_widget().pack(expand=True, fill="both")

        self.__ax.set_xlabel("x")
        self.__ax.set_ylabel("y")
        self.__ax.set_xlim(-10, 10)
        self.__ax.set_ylim(-10, 10)
        self.__ax.set_aspect("equal")
        self.__ax.grid(True)
        self.__ax.callbacks.connect("xlim_changed", self.__on_xlim_changed)
        self.__lines = {}

    # 为了方便把处理字符串的两个函数合成一个类方法了
    def __process(self, expr: str):
        expr = insert_multiplication(expr)
        expr = process_expr(expr)
        return expr

    # 绘制expr对应的函数图像
    def draw_plots(self, expr: str):
        expr = self.__process(expr)
        if expr in self.__lines:  # 这条图像已经在画布中了
            return

        if not "=" in expr:  # 绘制普通函数图像
            x_min, x_max = self.__ax.get_xlim()
            xs = np.linspace(x_min, x_max, 1000)
            try:
                with warnings.catch_warnings():  # 忽略计算中的警告，只捕获算式不合法导致的错误
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    ys = eval(expr, {"np": np, "x": xs, "π": np.pi, "__builtins__": {}})
                    # 把图像保存下来，方便之后操作
                    self.__lines[expr] = self.__ax.plot(xs, ys)[0]
                    self.__plot_canvas.draw()
            except Exception as e:
                print(e)
                messagebox.showerror(title="错误", message="请检查函数表达式")
        else:
            # 绘制隐函数图像
            pass

    # 删除expr对应的函数图像
    def delete_plots(self, expr: str):
        expr = self.__process(expr)
        if expr in self.__lines:
            line = self.__lines.pop(expr)
            line.remove()
            self.__plot_canvas.draw()

    def __on_xlim_changed(self, event):
        self.__update_plot()

    def __update_plot(self):
        x_min, x_max = self.__ax.get_xlim()
        xs = np.linspace(x_min, x_max, 1000)
        for expr, line in self.__lines.items():
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    ys = eval(expr, {"np": np, "x": xs, "π": np.pi, "__builtins__": {}})
                    line.set_data(xs, ys)
                    self.__plot_canvas.draw_idle()
            except Exception as e:
                print(e)
                messagebox.showerror(title="错误", message="请检查函数表达式")
