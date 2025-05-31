import tkinter as tk
from funcs import *
from tkinter import ttk
import matplotlib.pyplot as plt
import sys


def on_close():  # 终止程序
    root.quit()
    root.destroy()
    sys.exit("程序终止")


root = tk.Tk()
root.title("科学计算器")
root.configure(bg="#f0f0f0")  # 设置背景色
root.protocol("WM_DELETE_WINDOW", on_close)  # 确保在窗口关闭时会终止程序
graph_window = None
exist = False
# 配置网格行列权重
for col in range(5):
    root.columnconfigure(col, weight=1)
for row in range(7):
    root.rowconfigure(row, weight=1)

# 顶部功能标签
input_entry = tk.Entry(
    root,
    font=("Arial", 24),
    bg="white",
    fg="black",
    insertbackground="#FF6600",
    insertwidth=2,
    justify="right",
    borderwidth=5,
)
input_entry.grid(row=0, column=0, columnspan=7, sticky="nsew", padx=10, pady=10)


def insert_char(char):
    """处理普通字符输入"""

    conversion = {
        "×": "*",
        "÷": "/",
        #'π': '3.1415926535',
        "()²": "()^2",
        "√()": "sqrt(",
        #'exp()': 'e^(',
        "ln()": "ln(",
    }
    cursor_pos = input_entry.index(tk.INSERT)  # 获取光标位置
    actual_char = conversion.get(char, char)

    if char in ["Sin()", "Cos()", "Tan()"]:
        formatted = f"{char[:3].lower()}()"
        input_entry.insert(cursor_pos, formatted[:-1])  # 右括号不会自动给出
        input_entry.icursor(cursor_pos + 4)  # 定位到括号内
        return
    elif char == "()²" or char == "()^":
        input_entry.insert(cursor_pos, actual_char)
        input_entry.icursor(cursor_pos + 1)
        return
    elif char == "exp()":
        input_entry.insert(cursor_pos, actual_char)
        input_entry.icursor(cursor_pos + 3)
        return
    input_entry.insert(cursor_pos, actual_char)

    input_entry.icursor(cursor_pos + len(actual_char))


def backspace():
    current = input_entry.get()
    cursor_pos = input_entry.index(tk.INSERT)
    if cursor_pos > 0:
        char = current[cursor_pos - 1]
        if (
            (char == "n" and current[cursor_pos - 2] != "l")
            or char == "s"
            or char == "p"
        ):
            input_entry.delete(cursor_pos - 3, cursor_pos)
            input_entry.icursor(cursor_pos - 3)
        elif char == "n" and current[cursor_pos - 2] == "l":
            input_entry.delete(cursor_pos - 2, cursor_pos)
            input_entry.icursor(cursor_pos - 2)
        elif char == "t":
            input_entry.delete(cursor_pos - 4, cursor_pos)
            input_entry.icursor(cursor_pos - 4)
        elif char == "r":
            input_entry.delete(cursor_pos - 5, cursor_pos)
            input_entry.icursor(cursor_pos - 5)
        else:
            input_entry.delete(cursor_pos - 1, cursor_pos)
            input_entry.icursor(cursor_pos - 1)


def equal():
    input = input_entry.get()
    if "x" not in input and "y" not in input:
        input_entry.delete(0, tk.END)
        try:
            output = calc(input)
            insert_char(output)
        except:
            insert_char("error")
    else:
        insert_char("=")


def all_clear():
    input_entry.delete(0, tk.END)


class child_window:

    def __init__(self, parent):

        global exist
        if exist:
            return
        exist = True
        self.window = tk.Toplevel(parent)
        self.window.title("画布")
        self.window.geometry("1000x600")  # 增大窗口尺寸
        self.current_act = 1
        self.entries = []

        # 主布局容器（左右分割比例调整为1:2）
        self.main_paned = tk.PanedWindow(self.window, orient=tk.HORIZONTAL, sashwidth=5)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # ========== 左侧输入框区域（宽度300） ==========
        self.left_frame = tk.Frame(self.main_paned, bg="#f0f0f0")
        self.main_paned.add(self.left_frame, width=300)  # 固定左侧宽度

        # 初始化5个固定输入框
        # self.create_scale()
        self._create_inputs()
        # self.create_scale()
        # ========== 右侧扩展区域（宽度自适应剩余空间） ==========
        self.right_frame = tk.Frame(self.main_paned, bg="white")
        self.main_paned.add(self.right_frame, minsize=400)
        self.fig, self.ax = plt.subplots()
        self.figCanvas = FigureCanvas(
            self.fig,
            self.ax,
            self.right_frame,
            self.slider_vars["α"]["var"],
            self.slider_vars["β"]["var"],
            self.slider_vars["γ"]["var"],
        )

        self.window.protocol(
            "WM_DELETE_WINDOW", self._on_close
        )  # 将叉号绑定_on_close函数
        self.update()

    def _on_close(self):
        global exist
        exist = False
        self.window.destroy()

    def create_scale(self):
        container = tk.Frame(self.left_frame, bg="#f0f0f0")
        container.pack(fill=tk.BOTH, expand=True, padx=5)

    def update(self):
        entry = self.entries[5]
        entry.delete(0, tk.END)
        entry.insert(0, f"方程{self.current_act}")
        names = ["α", "β", "γ"]
        for name in names:
            self.slider_vars[name]["var"].set(0)
            self.slider_vars[name]["label"].config(text="0.00")

    def _create_inputs(self):

        # 输入框容器
        input_container = tk.Frame(self.left_frame, bg="#f0f0f0")
        input_container.pack(fill=tk.BOTH, expand=True, padx=5)

        # 使用grid布局精准控制按钮位置
        for i in range(1, 6):
            row_frame = tk.Frame(input_container, bg="#f0f0f0")
            row_frame.grid(row=i, column=0, sticky="ew", pady=3)

            # 输入框标签
            lbl = tk.Label(
                row_frame, text=f"方程 {i}:", width=8, anchor="w", bg="#f0f0f0"
            )
            lbl.grid(row=0, column=0, padx=2)

            # 输入框
            entry = ttk.Entry(row_frame, width=18)
            entry.grid(row=0, column=1, padx=2, sticky="ew")

            # 清空按钮
            btn = ttk.Button(
                row_frame,
                text="×",
                width=3,
                command=lambda idx=i: self.clear_single(idx),
            )
            btn.grid(row=0, column=2, padx=2)

            # 行框架列配置（输入框自动扩展）
            row_frame.columnconfigure(1, weight=1)
            ttk.Button(
                row_frame,
                text="✎",
                width=3,
                command=lambda idx=i: self.edit_single(idx),
            ).grid(
                row=0, column=3, padx=(2, 5)
            )  # 左间距2，右间距5
            self.entries.append(entry)
        row_frame = tk.Frame(input_container, bg="#f0f0f0")
        row_frame.grid(row=7, column=0, sticky="ew", pady=3)
        lbl = tk.Label(row_frame, text=f"当前操作:", width=8, anchor="w", bg="#f0f0f0")
        lbl.grid(row=0, column=0, padx=2)

        # 输入框
        entry = ttk.Entry(row_frame, width=18)
        entry.grid(row=0, column=1, padx=2, sticky="ew")
        self.entries.append(entry)
        row_frame.columnconfigure(1, weight=1)
        # 调整列权重（让输入框列自动扩展）
        self.slider_vars = {}
        params = [("α", 0, 100), ("β", -10, 10), ("γ", 0, 1)]
        for i, (name, min, max) in enumerate(params):
            slider_frame = tk.Frame(input_container, bg="#f0f0f0")
            slider_frame.grid(row=i + 8, column=0, sticky="ew", pady=5)

            def _on_scale_moved(n, v):
                self.update_value(n, v)  # 更新标签
                cur_act = self.current_act  # 当前在操作的对象
                expr = self.entries[cur_act - 1].get()
                self.figCanvas.update_one_plot(expr=expr)

            label = tk.Label(slider_frame, text=name)
            label.grid(row=0, column=0, padx=2)
            var = tk.DoubleVar()
            scale = ttk.Scale(
                slider_frame,
                variable=var,
                from_=min,
                to=max,
                orient=tk.HORIZONTAL,
                # command=lambda v=0, n=name: self.update_value(n, v),
                command=lambda v=0, n=name: _on_scale_moved(n, v),
            )  # v即为滑块绑定的var变量
            scale.grid(row=0, column=1, padx=2, sticky="ew")
            value_label = tk.Label(slider_frame, text="0.0", width=5, bg="#f0f0f0")
            value_label.grid(row=0, column=2, padx=2)
            self.slider_vars[name] = {"var": var, "label": value_label}
            slider_frame.columnconfigure(1, weight=1)

        # 容器列配置
        input_container.columnconfigure(0, weight=1)
        self.create_toolbox(input_container)

    def create_toolbox(self, parent):
        toolbox_frame = tk.Frame(parent, bg="#f0f0f0")
        toolbox_frame.grid(row=11, column=0, sticky="nsew", pady=10, padx=5)
        lbl_toolbox = tk.Label(
            toolbox_frame, text="工具箱", bg="#e0e0e0", relief="ridge", padx=5
        )
        lbl_toolbox.pack(fill=tk.BOTH, pady=(0, 10))
        btn_frame = tk.Frame(toolbox_frame, bg="#f0f0f0")
        btn_frame.pack(fill=tk.BOTH, expand=True)

        # 定义工具集
        tools = [
            ("标极值点", self.extreme_point),
            ("标零点", self.zero_point),
            ("计算极值", self.calc_extreme),
            ("画出导函数", self.draw_deri),
        ]
        for idx, (text, command) in enumerate(tools):
            btn = ttk.Button(btn_frame, text=text, command=command, width=17)
            btn.grid(
                row=idx // 2, column=idx % 2, padx=5, pady=5, sticky="nsew", ipady=4
            )

    def extreme_point(self):
        cur_act = self.current_act
        entry = self.entries[cur_act - 1]
        # 把表达式里面的全部参数替换为对应的数值
        expr = entry.get()
        expr = insert_multiplication(expr)
        tmp = expr
        if not self.figCanvas.is_extrpts_exist[expr]:
            # 极值点还未标出
            alpha_val = self.slider_vars["α"]["var"].get()
            beta_val = self.slider_vars["β"]["var"].get()
            gamma_val = self.slider_vars["γ"]["var"].get()
            expr = re.sub(r"α", f"{alpha_val}", expr)
            expr = re.sub(r"β", f"{beta_val}", expr)
            expr = re.sub(r"γ", f"{gamma_val}", expr)
            extr_points = find_extreme_points(expr, self.ax.get_xlim())
            print(extr_points)
            if len(extr_points) > 0:
                xs = [float(p[0]) for p in extr_points]
                ys = [float(p[1]) for p in extr_points]
                self.figCanvas.extrpts[tmp] = self.ax.plot(
                    xs, ys, linestyle="None", marker="o"
                )[0]
                self.figCanvas._FigureCanvas__plot_canvas.draw()
                self.figCanvas.is_extrpts_exist[tmp] = True
        else:
            # 极值点已经标出了
            self.figCanvas.extrpts.pop(tmp).remove()  # 移出字典并消除图像
            self.figCanvas._FigureCanvas__plot_canvas.draw()
            self.figCanvas.is_extrpts_exist[tmp] = False

    def zero_point(self):
        cur_act = self.current_act
        entry = self.entries[cur_act - 1]
        expr = entry.get()
        expr = insert_multiplication(expr)
        tmp = expr
        if not self.figCanvas.is_zeropts_exist[expr]:
            alpha_val = self.slider_vars["α"]["var"].get()
            beta_val = self.slider_vars["β"]["var"].get()
            gamma_val = self.slider_vars["γ"]["var"].get()
            expr = re.sub(r"α", f"{alpha_val}", expr)
            expr = re.sub(r"β", f"{beta_val}", expr)
            expr = re.sub(r"γ", f"{gamma_val}", expr)
            print(expr)
            roots = find_roots(expr, self.ax.get_xlim())
            print(roots)
            if len(roots) > 0:
                ys = np.zeros(len(roots))
                self.figCanvas.zeropts[tmp] = self.ax.plot(
                    roots, ys, linestyle="None", marker="o"
                )[0]
                self.figCanvas._FigureCanvas__plot_canvas.draw()
                self.figCanvas.is_zeropts_exist[tmp] = True
        else:
            # 零点已经标出了
            self.figCanvas.zeropts.pop(tmp).remove()  # 移出字典并消除图像
            self.figCanvas._FigureCanvas__plot_canvas.draw()
            self.figCanvas.is_zeropts_exist[tmp] = False

    def calc_extreme(self):
        cur_act = self.current_act
        entry = self.entries[cur_act - 1]
        # 把表达式里面的全部参数替换为对应的数值
        expr = entry.get()
        expr = insert_multiplication(expr)
        alpha_val = self.slider_vars["α"]["var"].get()
        beta_val = self.slider_vars["β"]["var"].get()
        gamma_val = self.slider_vars["γ"]["var"].get()
        expr = re.sub(r"α", f"{alpha_val}", expr)
        expr = re.sub(r"β", f"{beta_val}", expr)
        expr = re.sub(r"γ", f"{gamma_val}", expr)
        extr_points = find_extreme_points(expr, self.ax.get_xlim())
        info = "极值点\t  极值\n"
        for x, y in extr_points:
            info += f"{x}\t  {y:.7f}\n"
        messagebox.showinfo(title="极值点和极值", message=info)

    def draw_deri(self):
        cur_act = self.current_act
        entry = self.entries[cur_act - 1]
        expr = entry.get()
        expr = insert_multiplication(expr)
        tmp = expr
        if not self.figCanvas.is_derivedfunc_exist[expr]:
            alpha_val = self.slider_vars["α"]["var"].get()
            beta_val = self.slider_vars["β"]["var"].get()
            gamma_val = self.slider_vars["γ"]["var"].get()
            expr = re.sub(r"α", f"{alpha_val}", expr)
            expr = re.sub(r"β", f"{beta_val}", expr)
            expr = re.sub(r"γ", f"{gamma_val}", expr)
            # print(expr, "***")
            print(expr, alpha_val, beta_val, gamma_val)
            derived_func = get_derived(expr=expr)
            self.figCanvas.draw_plots2(derived_func)
            self.figCanvas.is_derivedfunc_exist[tmp] = True
            self.figCanvas.derivedfunc[tmp] = derived_func
        else:
            derived_func = self.figCanvas.derivedfunc.pop(tmp)
            self.figCanvas.derived.pop(derived_func).remove()
            self.figCanvas._FigureCanvas__plot_canvas.draw()
            self.figCanvas.is_derivedfunc_exist[tmp] = False

    def update_value(self, name, value):
        value = float(value)
        self.slider_vars[name]["label"].config(text=f"{value:.2f}")

    def edit_single(self, input_id):
        index = input_id - 1
        self.current_act = input_id

        # entry = self.entries[index]
        # expr = entry.get()
        # if expr != "":
        #     self.figCanvas.draw_plots(expr=expr)  # 绘制新图像

        self.update()

    def clear_single(self, input_id):
        """清空指定输入框"""
        index = input_id - 1
        entry = self.entries[index]  # 第2个子组件是输入框

        expr = entry.get()  # 表达式
        self.figCanvas.delete_plots(expr=expr)  # 删除表达式对应的函数

        entry.delete(0, tk.END)


def open_graph():
    global graph_window
    graph_window=child_window(root)
def draw():
    input=input_entry.get()
    entry=graph_window.entries[graph_window.current_act-1]
    graph_window.clear_single(graph_window.current_act)
    entry.insert(0,input)
    graph_window.figCanvas.draw_plots(input)
    all_clear()

# 定义按钮布局
buttons = [
    (1, 0, "x"),
    (1, 1, "y"),
    (1, 2, "π"),
    (1, 3, "e"),
    (1, 4, "()²"),
    (1, 5, "√()"),
    (1, 6, "ln()"),
    (2, 0, "7"),
    (2, 1, "8"),
    (2, 2, "9"),
    (2, 3, "×"),
    (2, 4, "÷"),
    (3, 6, "("),
    (2, 5, "Sin()"),
    (2, 6, "()^"),
    (3, 0, "4"),
    (3, 1, "5"),
    (3, 2, "6"),
    (3, 3, "+"),
    (3, 4, "-"),
    (4, 6, ")"),
    (3, 5, "Cos()"),
    (4, 0, "1"),
    (4, 1, "2"),
    (4, 2, "3"),
    (4, 3, "α"),
    (4, 4, "β"),
    (4, 5, "γ"),
    (5, 0, "绘图"),
    (5, 1, "0"),
    (5, 2, "."),
    (5, 6, "🖌"),
    (5, 4, "0"),
    (5, 3, "="),
    (5, 4, "←"),
    (5, 5, "AC"),
]

# 创建按钮
for params in buttons:
    row, col, text = params[0], params[1], params[2]
    rowspan = params[3] if len(params) > 3 else 1
    try:
        int(text)
        btn = tk.Button(root, text=text, width=8, height=4, bg="white", relief="solid")
    except:
        btn = tk.Button(root, text=text, width=8, height=4, bg="white", relief="groove")
    if text == "=":
        btn.grid(row=row, column=col, rowspan=rowspan, sticky="nswe", padx=2, pady=2)
    elif text == "←":
        btn.grid(row=row, column=col, rowspan=rowspan, sticky="nswe", padx=2, pady=2)
    elif text == "AC":
        btn.grid(row=row, column=col, rowspan=rowspan, sticky="nswe", padx=2, pady=2)
    else:
        btn.grid(row=row, column=col, sticky="nswe", padx=2, pady=2)
    str = input_entry.get()
    if text == "←":
        btn.config(command=backspace)
    elif text == "=":
        btn.config(command=equal)
    elif text == "AC":
        btn.config(command=all_clear)
    elif text == "🖌":
        btn.config(command=open_graph)
    elif text=="绘图":
        btn.config(command=draw)
    else:
        btn.config(command=lambda t=text: insert_char(t))


root.mainloop()
