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
            res = eval(expr, {"np": np, "π": np.pi, "e": np.e, "__builtins__": {}})
            return str(res)
    except Exception as e:
        print(e)  # 用于测试，后期会注释掉
        messagebox.showerror(title="错误", message="请检查算术表达式")
        return None


class FigureCanvas:
    def __init__(self, fig, ax, parent):
        # 成员都设置私有的
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
        self.__ax.callbacks.connect("xlim_changed", self.__on_view_changed)
        self.__ax.callbacks.connect("ylim_changed", self.__on_view_changed)
        self.__lines = {}  # 普通函数图像
        self.__is_updating = False  # 记录图像是否在更新，避免无限的递归调用

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
                    ys = eval(
                        expr,
                        {"np": np, "x": xs, "π": np.pi, "e": np.e, "__builtins__": {}},
                    )
                    # 把图像保存下来，方便之后操作
                    self.__lines[expr] = self.__ax.plot(xs, ys)[0]
                    self.__plot_canvas.draw()
            except Exception as e:
                print(e)
                messagebox.showerror(title="错误", message="请检查函数表达式")
        else:
            # 绘制隐函数图像
            x_min, x_max = self.__ax.get_xlim()
            y_min, y_max = self.__ax.get_ylim()
            xs = np.linspace(x_min, x_max, 1000)
            ys = np.linspace(y_min, y_max, 1000)
            X, Y = np.meshgrid(xs, ys)

            left, right = expr.split("=")  # 等式一分为二
            left, right = left.strip(), right.strip()
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    F = eval(
                        left,
                        {
                            "x": X,
                            "y": Y,
                            "np": np,
                            "π": np.pi,
                            "e": np.e,
                            "__builtins__": {},
                        },
                    ) - eval(
                        right,
                        {
                            "x": X,
                            "y": Y,
                            "np": np,
                            "π": np.pi,
                            "e": np.e,
                            "__builtins__": {},
                        },
                    )  # 写成左减去右的形式

                    self.__lines[expr] = plt.contour(X, Y, F, levels=[0])  # 绘制等高线
                    self.__plot_canvas.draw()
            except Exception as e:
                print(e)
                messagebox.showerror(title="错误", message="请检查隐函数表达式")

    # 删除expr对应的函数图像
    def delete_plots(self, expr: str):
        expr = self.__process(expr)
        if expr in self.__lines:
            line = self.__lines.pop(expr)
            line.remove()
            self.__plot_canvas.draw()

    def __on_view_changed(self, event):
        if self.__is_updating:
            return
        self.__is_updating = True
        self.__update_plot()
        self.__is_updating = False

    def __update_plot(self):
        # print(self.__lines)
        x_min, x_max = self.__ax.get_xlim()
        xs = np.linspace(x_min, x_max, 1000)
        for expr, line in self.__lines.items():
            if not "=" in expr:
                # 普通函数
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", category=RuntimeWarning)
                        ys = eval(
                            expr,
                            {
                                "np": np,
                                "x": xs,
                                "π": np.pi,
                                "e": np.e,
                                "__builtins__": {},
                            },
                        )
                        line.set_data(xs, ys)
                        self.__plot_canvas.draw_idle()
                except Exception as e:
                    print(e)
                    messagebox.showerror(title="错误", message="请检查函数表达式")
            else:
                # 隐函数
                y_min, y_max = self.__ax.get_ylim()
                ys = np.linspace(y_min, y_max, 1000)
                X, Y = np.meshgrid(xs, ys)

                left, right = expr.split("=")
                left, right = left.strip(), right.strip()
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", category=RuntimeWarning)
                        F = eval(
                            left,
                            {
                                "x": X,
                                "y": Y,
                                "np": np,
                                "π": np.pi,
                                "e": np.e,
                                "__builtins__": {},
                            },
                        ) - eval(
                            right,
                            {
                                "x": X,
                                "y": Y,
                                "np": np,
                                "π": np.pi,
                                "e": np.e,
                                "__builtins__": {},
                            },
                        )
                        cs = self.__lines[expr]
                        cs.remove()
                        self.__lines[expr] = plt.contour(X, Y, F, levels=[0])
                        self.__plot_canvas.draw_idle()
                except Exception as e:
                    print(e)
                    messagebox.showerror(title="错误", message="请检查隐函数表达式")


def find_roots(expr: str, x_range=(-10, 10), error=1e-7):
    """
    对于给定的函数表达式expr,求出在x_range区间内的全部零点
    error是误差,由于数值求解方程时存在误差,只有差值超过error我们才认为过程中求出的两个根不是同一个根
    """
    if "=" in expr:
        messagebox.showerror(title="错误", message="请输入函数表达式而非等式")
        return
    if x_range[0] > x_range[1]:
        x_range[0], x_range[1] = x_range[1], x_range[0]
    expr = insert_multiplication(expr)
    # sympy库中有常见函数，不需要给函数名前加上np.
    x = sympy.symbols("x")
    try:
        func = sympy.lambdify(x, expr, "numpy")  # func是转化为函数
    except Exception as e:
        print(e)
        messagebox.showerror(title="错误", message="请检查函数表达式")
    xs = np.linspace(x_range[0], x_range[1], 1000)
    roots = []

    for s in xs:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                root = scipy.optimize.fsolve(func, s)[0]
                # 如果根介于区间内且与之前出现过的所有根不同
                if (not any(abs(root - r) < error for r in roots)) and x_range[
                    0
                ] - error < root < x_range[1] + error:
                    roots.append(root)
        except Exception as e:
            print(e)
            messagebox.showerror(title="错误", message="请检查函数表达式")

    return sorted(roots)  # 返回升序排列的区间内的所有根


def find_extreme_points(expr: str, x_range=(-10, 10), error=1e-7):
    """
    对于给定的函数表达式expr,求出在x_range区间内的全部极值点和极值,返回值是元组(极值点, 极值)的数组
    error是误差
    只能计算普通函数的极值点,不能计算隐函数的极值点
    """
    expr = insert_multiplication(expr)
    try:
        expr = sympy.sympify(expr)  # 转化为sympy表达式，否则下面不能用于进行求导运算
        x = sympy.symbols("x")
        derived_func1 = sympy.diff(expr, x)  # 一阶导数
        stag_points = find_roots(
            str(derived_func1), x_range=x_range, error=error
        )  # 所有驻点
        extr_points = []
        for sp in stag_points:
            # 检验驻点是不是极值点，需要依次求导
            i = 2  # 记录导数的阶数
            dfunc = derived_func1
            while True:  # 一直求导下去，直到导函数在驻点的值不为零
                dfunc = sympy.diff(dfunc, x)
                if abs(dfunc.subs(x, sp).evalf()) > 1e-5:
                    # 这一阶导数不是0,偶数阶是极值点，奇数阶不是极值点
                    if i % 2 == 0:
                        extr_points.append(sp)
                    break
                i += 1
        return extr_points
    except Exception as e:
        print(e)
        messagebox.showerror(title="错误", message="请检查函数表达式")
        return
