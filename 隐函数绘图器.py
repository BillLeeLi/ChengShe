import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import re
import sys


def insert_multiplication(expr):
    expr = re.sub(
        r"(\d)([a-zA-Z\(])", r"\1*\2", expr
    )  # 数字和括号或字母相邻的时候中间加上*
    # 比如3(x+y)和5x会被转化为3*(x+y)和5*x
    # expr = re.sub(r"([a-zA-Z\)])([a-zA-Z\(])", r"\1*\2", expr)
    expr = re.sub(
        r"\b([a-zA-Z\)])\(", r"\1*(", expr
    )  # 左括号前有数字或者右括号的时候加上*
    expr = re.sub(r"\^", r"**", expr)  # ^替换为**
    print(expr)
    return expr


def process_expression(expr):
    expr = insert_multiplication(expr)
    functions = [
        "sin",
        "cos",
        "tan",
        "exp",
        "log",
        "sqrt",
        "abs",
        "arcsin",
        "arccos",
        "arctan",
        "sinh",
        "cosh",
        "tanh",
    ]
    for func in functions:
        expr = re.sub(rf"\b{func}\s*\(", f"np.{func}(", expr)
    print(expr)
    return expr


def plot_implicit():
    expr = entry.get()
    if "=" not in expr:
        messagebox.showerror("格式错误", "请输入等式形式，如 x**2 + y**2 = 1")
        return

    left, right = expr.split("=")
    left = process_expression(left.strip())
    right = process_expression(right.strip())

    x = np.linspace(-10, 10, 400)
    y = np.linspace(-10, 10, 400)
    X, Y = np.meshgrid(x, y)

    try:
        # 构造等式左边减右边，作为隐函数
        F = eval(left, {"x": X, "y": Y, "np": np, "__builtins__": {}}) - eval(
            right, {"x": X, "y": Y, "np": np, "__builtins__": {}}
        )
        ax.clear()
        ax.contour(X, Y, F, levels=[0], colors="black")
        ctf = ax.contourf(X, Y, F, levels=50, cmap="rainbow")
        # fig.colorbar(ctf, ax)
        cbar = fig.colorbar(ctf, ax=ax)
        cbar.set_label("函数值")
        ax.set_title(f"隐函数图像: {expr}", fontsize=12)
        ax.set_xlabel("x", fontsize=10)
        ax.set_ylabel("y", fontsize=10)
        ax.set_aspect("equal")
        ax.grid(True)
        canvas.draw()
    except Exception as e:
        messagebox.showerror("错误", f"无法绘图:\n{e}")


def on_closing():
    root.quit()
    root.destroy()
    sys.exit()


# GUI 构建
root = tk.Tk()
root.title("隐函数绘图器")
root.protocol("WM_DELETE_WINDOW", on_closing)

tk.Label(root, text="输入隐函数(如 x**2 + y**2 = 1):", font=("bold", 20)).pack(pady=5)
entry = tk.Entry(root, width=50, font=("bold", 20))
entry.pack(pady=5)

tk.Button(root, text="绘图", command=plot_implicit, font=("bold", 20)).pack(pady=5)

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(fill="both", expand=True)

root.mainloop()
