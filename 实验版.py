from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import sys
import numpy as np
import re
import math
from keyboard import keyboard


def on_close():
    root.quit()
    root.destroy()
    sys.exit("程序终止")


def set_x():
    ax.set_xlim(float(x_min_str.get()), float(x_max_str.get()))
    picture_canvas.draw()


def set_y():
    ax.set_ylim(float(y_min_str.get()), float(y_max_str.get()))
    picture_canvas.draw()


# 在表达式中适当位置加入*的函数
def insert_multiplication(expr):
    expr = re.sub(
        r"(\d)([a-zA-Z\(])", r"\1*\2", expr
    )  # 数字和括号或字母相邻的时候中间加上*
    # 比如3(x+y)和5x会被转化为3*(x+y)和5*x
    # expr = re.sub(r"([a-zA-Z\)])([a-zA-Z\(])", r"\1*\2", expr)
    expr = re.sub(
        r"\b([a-zA-Z\)])\(", r"\1*(", expr
    )  # 左括号前有字母或者右括号的时候加上*
    # x(x+y)和(x+y)(x+3)分别转化为x*(x+y)和(x+y)*(x+3)
    expr = re.sub(r"\^", r"**", expr)  # ^替换为**
    print(expr)
    return expr


# 把常见函数名转化为np.函数名
def process_expr(expr: str):
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
    return expr


def draw_picture():
    expr = process_expr(insert_multiplication(str.get()))  # 获取表达式
    # print(expr)
    x = np.linspace(-5, 5, 100)
    try:
        # 禁用了所有的内置函数确保安全
        y = eval(expr, {"x": x, "np": np, "numpy": np, "__builtins__": {}})
        ax.plot(x, y)
        ax.set_label(f"y = {expr}")
        ax.set_xlabel("x", fontdict={"fontsize": 14})
        ax.set_ylabel("y", fontdict={"fontsize": 14})
        ax.grid(True)
        picture_canvas.draw()
        if x_max_str.get() == "" or x_min_str.get() == "":
            x_min_str.set("-5.0")
            x_max_str.set("5.0")
    except Exception as e:
        messagebox.showerror(title="表达式异常", message=f"无法解析表达式: {e}")


root = Tk()
root.protocol("WM_DELETE_WINDOW", on_close)
root.geometry("1000x1000")
root.title("实验版")

lb = Label(
    root, text="请输入Python风格的函数表达式(支持np库的函数):", font=("bold", 20)
)
str = StringVar()
ety = Entry(root, font=("bold", 20), textvariable=str, width=50)
# outer_fr = Frame(root)
# kb = keyboard(outer_fr, relief="solid", bd=2, bg="lightyellow")
btn = Button(root, text="绘图", command=draw_picture, font=("bold", 20))
fig = plt.figure()
ax = fig.add_subplot(111)
picture_canvas = FigureCanvasTkAgg(fig, master=root)


lb.pack(pady=5)
ety.pack(pady=5)
# kb.pack()
# outer_fr.pack(expand=True)
btn.pack(pady=5)
toolbar = NavigationToolbar2Tk(picture_canvas, root)
toolbar.update()
picture_canvas.get_tk_widget().pack(expand=True, fill="both")

fr_x = Frame(root)
x_min_str, x_max_str = StringVar(), StringVar()
x_min_ety = Entry(fr_x, textvariable=x_min_str, font=("bold", 20))
x_max_ety = Entry(fr_x, textvariable=x_max_str, font=("bold", 20))
Label(fr_x, text="x最小值:", font=("bold", 20)).pack(side="left", padx=(10, 5))
x_min_ety.pack(side="left", fill="x", expand=True)
Label(fr_x, text="x最大值:", font=("bold", 20)).pack(side="left", padx=(10, 5))
x_max_ety.pack(side="left", fill="x", expand=True)
Button(fr_x, text="设置x轴范围", command=set_x, font=("bold", 20)).pack(
    side="left", padx=5
)
fr_x.pack(fill="x")

fr_y = Frame(root)
y_min_str, y_max_str = StringVar(), StringVar()
y_min_ety = Entry(fr_y, textvariable=y_min_str, font=("bold", 20))
y_max_ety = Entry(fr_y, textvariable=y_max_str, font=("bold", 20))
Label(fr_y, text="y最小值:", font=("bold", 20)).pack(side="left", padx=(10, 5))
y_min_ety.pack(side="left", fill="x", expand=True)
Label(fr_y, text="y最大值:", font=("bold", 20)).pack(side="left", padx=(10, 5))
y_max_ety.pack(side="left", fill="x", expand=True)
Button(fr_y, text="设置y轴范围", command=set_y, font=("bold", 20)).pack(
    side="left", padx=5
)
fr_y.pack(fill="x")


mainloop()
print("hello")
