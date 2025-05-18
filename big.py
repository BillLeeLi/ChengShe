import tkinter as tk
from test import calc
from tkinter import ttk

root = tk.Tk()
root.title("科学计算器")
root.configure(bg='#f0f0f0')  # 设置背景色
graph_window = None
exist=False
# 配置网格行列权重
for col in range(5):
    root.columnconfigure(col, weight=1)
for row in range(7):
    root.rowconfigure(row, weight=1)

# 顶部功能标签
input_entry = tk.Entry(root, font=('Arial', 24), bg='white', fg='black', insertbackground='#FF6600',  
                      insertwidth=2,justify='right', borderwidth=5)
input_entry.grid(row=0, column=0, columnspan=7, sticky="nsew", padx=10, pady=10)
def insert_char(char):
    """处理普通字符输入"""
    
    conversion = {
        '×': '*', 
        '÷': '/',
        #'π': '3.1415926535',
        '()²': '()^2',
        '√()': 'sqrt(',
        #'exp()': 'e^(',
        'ln()':'ln('
    }
    cursor_pos = input_entry.index(tk.INSERT)#获取光标位置
    actual_char = conversion.get(char, char)
    
    if char in ['Sin()', 'Cos()', 'Tan()']:
        formatted = f"{char[:3].lower()}()"
        input_entry.insert(cursor_pos, formatted[:-1])#右括号不会自动给出
        input_entry.icursor(cursor_pos + 4)  # 定位到括号内
        return
    elif char =='()²'or char=='()^':
        input_entry.insert(cursor_pos, actual_char)
        input_entry.icursor(cursor_pos + 1)
        return
    elif char=='exp()':
        input_entry.insert(cursor_pos, actual_char)
        input_entry.icursor(cursor_pos + 3)
        return
    input_entry.insert(cursor_pos, actual_char)
    
    
    input_entry.icursor(cursor_pos + len(actual_char))
    


def backspace():
    current=input_entry.get()
    cursor_pos = input_entry.index(tk.INSERT)
    if cursor_pos > 0:
        char=current[cursor_pos-1]
        if (char=='n' and current[cursor_pos-2]!='l') or char=='s' or char=='p':
            input_entry.delete(cursor_pos - 3, cursor_pos)
            input_entry.icursor(cursor_pos - 3)
        elif char=='n' and current[cursor_pos-2]=='l':
            input_entry.delete(cursor_pos - 2, cursor_pos)
            input_entry.icursor(cursor_pos - 2)
        elif char=='t':
            input_entry.delete(cursor_pos - 4, cursor_pos)
            input_entry.icursor(cursor_pos - 4)
        elif char=='r':
            input_entry.delete(cursor_pos - 5, cursor_pos)
            input_entry.icursor(cursor_pos - 5)
        else:
            input_entry.delete(cursor_pos - 1, cursor_pos)
            input_entry.icursor(cursor_pos - 1)





def equal():
    input=input_entry.get()
    if   'x' not in input and 'y' not in input:
        input_entry.delete(0,tk.END)
        try:
            output=(calc(input))
            insert_char(output)
        except:
            insert_char('error')
    else:
        insert_char('=')

def all_clear():
    input_entry.delete(0,tk.END)



class child_window:
    
    def __init__(self, parent):
        
        global exist
        if exist:
            return
        exist=True
        self.window = tk.Toplevel(parent)
        self.window.title("画布")
        self.window.geometry("900x500")  # 增大窗口尺寸
        self.current_act=1
        self.entries=[]
        
        # 主布局容器（左右分割比例调整为1:2）
        self.main_paned = tk.PanedWindow(self.window, orient=tk.HORIZONTAL, sashwidth=5)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # ========== 左侧输入框区域（宽度300） ==========
        self.left_frame = tk.Frame(self.main_paned, bg="#f0f0f0")
        self.main_paned.add(self.left_frame, width=300)  # 固定左侧宽度
        
        # 初始化5个固定输入框
        self._create_inputs()
        
        # ========== 右侧扩展区域（宽度自适应剩余空间） ==========
        self.right_frame = tk.Frame(self.main_paned, bg="white")
        self.main_paned.add(self.right_frame, minsize=400)  
        
       
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)#将叉号绑定_on_close函数
        self.update()
    def _on_close(self):
        global exist
        exist=False
        self.window.destroy()
    def update(self):
        entry=self.entries[5]
        entry.delete(0,tk.END)
        entry.insert(0,f"方程{self.current_act}")
        
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
                row_frame,
                text=f"方程 {i}:",
                width=8,
                anchor='w',
                bg="#f0f0f0"
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
                command=lambda idx=i: self.clear_single(idx)
            )
            btn.grid(row=0, column=2, padx=2)
            
            # 行框架列配置（输入框自动扩展）
            row_frame.columnconfigure(1, weight=1)
            ttk.Button(
            row_frame,
            text="✎",  
            width=3,
            command=lambda idx=i: self.edit_single(idx)
            ).grid(row=0, column=3, padx=(2,5))  # 左间距2，右间距5
            self.entries.append(entry)
        row_frame = tk.Frame(input_container, bg="#f0f0f0")
        row_frame.grid(row=7, column=0, sticky="ew", pady=3)
        lbl = tk.Label(
                row_frame,
                text=f"当前操作:",
                width=8,
                anchor='w',
                bg="#f0f0f0"
            )
        lbl.grid(row=0, column=0, padx=2)
            
            # 输入框
        entry = ttk.Entry(row_frame, width=18)
        entry.grid(row=0, column=1, padx=2, sticky="ew")
        self.entries.append(entry)
        # 调整列权重（让输入框列自动扩展）
        row_frame.columnconfigure(1, weight=1)
        
        # 容器列配置
        input_container.columnconfigure(0, weight=1)
        
    
    
    def edit_single(self,input_id):
        index=input_id-1
        self.current_act=input_id
        self.update()
    def clear_single(self, input_id):
        """清空指定输入框"""
        index=input_id-1
        entry = self.entries[index]  # 第2个子组件是输入框
        entry.delete(0, tk.END)
def open_graph():
    child_window(root)
    
    

# 定义按钮布局
buttons = [
    
    (1, 0, 'x'), (1, 1, 'y'), (1, 2, 'π'), (1, 3, 'e'),
    (1, 4, '()²'), (1, 5, '√()'),(1,6,'ln()'),
    
    
    (2, 0, '7'), (2, 1, '8'), (2, 2, '9'), (2, 3, '×'), (2, 4, '÷'),(3, 6, '(' ),(2,5,'Sin()'),(2,6,'()^'),
    
    
    (3, 0, '4'), (3, 1, '5'), (3, 2, '6'), (3, 3, '+'), (3, 4, '-'),(4, 6, ')'),(3,5,'Cos()'),
    
    
    (4, 0, '1'), (4, 1, '2'), (4, 2, '3'), (4, 3, '=', 2),  # 跨2行
    
    
    (5, 0, '绘图'), (5, 1, '0'), (5, 2, '.'), (5,6,'🖌'),#(5, 4, '0'),
    
    
    (4, 4, '←',2),(4,5,'AC',2)
]

# 创建按钮
for params in buttons:
    row, col, text = params[0], params[1], params[2]
    rowspan = params[3] if len(params) > 3 else 1
    try:
        int(text)
        btn = tk.Button(root, text=text, width=8, height=4, bg='white', relief='solid')
    except:
        btn = tk.Button(root, text=text, width=8, height=4, bg='white', relief='groove')
    if text == '=':
        btn.grid(row=row, column=col, rowspan=rowspan, sticky='nswe', padx=2, pady=2)
    elif text=='←':
        btn.grid(row=row, column=col, rowspan=rowspan, sticky='nswe', padx=2, pady=2)
    elif text=='AC':
        btn.grid(row=row, column=col, rowspan=rowspan, sticky='nswe', padx=2, pady=2)
    else:
        btn.grid(row=row, column=col, sticky='nswe', padx=2, pady=2)
    str=input_entry.get()
    if text=='←':
        btn.config(command=backspace)
    elif text=='=' :
        btn.config(command=equal)
    elif text=='AC':
        btn.config(command=all_clear)
    elif text=='🖌':
        btn.config(command=open_graph)
    else:
        btn.config(command=lambda t=text: insert_char(t))


root.mainloop()
