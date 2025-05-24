import tkinter as tk
from math import *


class Point:
    def __init__(self, canvas: tk.Canvas, x, y):
        self.id = canvas.create_oval(
            x - 5, y - 5, x + 5, y + 5, fill="blue", tags="points"
        )
        self.canvas = canvas
        self.canvas.tag_bind(self.id, "<Motion>", self.motion)

    def motion(self, event):
        # self.canvas.itemconfig(self.id, fill="red")
        self.wider()
        self.canvas.tag_bind(self.id, "<Leave>", self.leave)

    def leave(self, event):
        # self.canvas.itemconfig(self.id, fill="blue")
        self.recover()
        self.canvas.tag_bind(self.id, "<Motion>", self.motion)

    def wider(self):
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        self.canvas.coords(self.id, cx - 7, cy - 7, cx + 7, cy + 7)

    def recover(self):
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        self.canvas.coords(self.id, cx - 5, cy - 5, cx + 5, cy + 5)

    def remove(self):
        self.canvas.delete(self.id)

    def center(self):
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        return ((x1 + x2) / 2, (y1 + y2) / 2)


class Line:
    def __init__(self, canvas: tk.Canvas, x1, y1, x2, y2):
        self.id = canvas.create_line(x1, y1, x2, y2, width=3)
        self.canvas = canvas
        self.canvas.tag_bind(self.id, "<Motion>", self.motion)

    def motion(self, event):
        self.wider()
        self.canvas.tag_bind(self.id, "<Leave>", self.leave)

    def leave(self, event):
        self.recover()
        self.canvas.tag_bind(self.id, "<Motion>", self.motion)

    def wider(self):
        self.canvas.itemconfig(self.id, width=5)

    def recover(self):
        self.canvas.itemconfig(self.id, width=3)


class Circle:
    def __init__(self, canvas: tk.Canvas, x1, y1, x2, y2):
        # 圆心和圆上一个点的坐标
        self.radius = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)  # 半径
        self.id = canvas.create_oval(
            x1 - self.radius,
            y1 - self.radius,
            x1 + self.radius,
            y1 + self.radius,
            width=3,
        )
        self.canvas = canvas
        self.canvas.tag_bind(self.id, "<Motion>", self.motion)

    def motion(self, event):
        self.wider()
        self.canvas.tag_bind(self.id, "<Leave>", self.leave)

    def leave(self, event):
        self.recover()
        self.canvas.tag_bind(self.id, "<Motion>", self.motion)

    def wider(self):
        self.canvas.itemconfig(self.id, width=5)

    def recover(self):
        self.canvas.itemconfig(self.id, width=3)


class myCanvas:
    def __init__(self, master):
        self.canvas = tk.Canvas(
            master=master, scrollregion=(0, 0, 1000, 1000), confine=False
        )
        self.canvas.pack(expand=True, fill="both")
        self.points = {}  # 存放id和点的键值对
        self.lines = {}  # 存放id和线的键值对
        self.circles = {}  # 存放id和圆的键值对

        self.ybar = tk.Scrollbar(
            self.canvas, command=self.canvas.yview, orient="vertical", width=20
        )
        self.ybar.pack(side="right", fill="y")
        self.xbar = tk.Scrollbar(
            self.canvas, command=self.canvas.xview, orient="horizontal", width=20
        )
        self.xbar.pack(side="bottom", fill="x")
        self.canvas.config(yscrollcommand=self.ybar.set, xscrollcommand=self.xbar.set)

    def start_draw_points(self):
        self.canvas.bind("<Button-1>", self.__draw_points)

    def __draw_points(self, event: tk.Event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(
            event.y
        )  # 安装滑动条之后需要获取鼠标在画布上的实际位置
        # if not any(
        #     sqrt((p.center()[0] - x) ** 2 + (p.center()[1] - y) ** 2) < 5
        #     for p in self.points
        # ):
        p = Point(self.canvas, x, y)
        self.points[p.id] = p

    def start_draw_lines(self):
        points = []
        self.canvas.bind(
            "<Button-1>", lambda event: self.__draw_lines(event=event, points=points)
        )

    def __draw_lines(self, event: tk.Event, points: list):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        flag = False
        min_dis = inf

        # 如果这个是已经存在的点，我们取距离最近的点
        for _, p in self.points.items():
            dis = sqrt((p.center()[0] - x) ** 2 + (p.center()[1] - y) ** 2)
            if dis < 7 and dis < min_dis:
                tp = p
                min_dis = dis
                flag = True
                # print("已存在的点!")
        if not flag:
            tp = Point(self.canvas, x, y)
            self.points[tp.id] = tp

        points.append(tp)
        if len(points) == 2:
            p1, p2 = points[0], points[1]
            points.clear()
            l = Line(
                self.canvas,
                p1.center()[0],
                p1.center()[1],
                p2.center()[0],
                p2.center()[1],
            )
            self.lines[l.id] = l

    def start_draw_circles(self):
        points = []
        self.canvas.bind(
            "<Button-1>", lambda event: self.__draw_circles(event=event, points=points)
        )

    def __draw_circles(self, event: tk.Event, points: list):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        flag = False
        min_dis = inf

        # 如果这个是已经存在的点，我们取距离最近的点
        for _, p in self.points.items():
            dis = sqrt((p.center()[0] - x) ** 2 + (p.center()[1] - y) ** 2)
            if dis < 7 and dis < min_dis:
                tp = p
                min_dis = dis
                flag = True
                # print("已存在的点!")
        if not flag:
            tp = Point(self.canvas, x, y)
            self.points[tp.id] = tp

        points.append(tp)
        if len(points) == 2:
            p1, p2 = points[0], points[1]
            points.clear()
            c = Circle(
                self.canvas,
                p1.center()[0],
                p1.center()[1],
                p2.center()[0],
                p2.center()[1],
            )
            self.circles[c.id] = c

    def start_delete(self):
        self.canvas.bind("<Button-1>", self.__on_figure_clicked)

    def __on_figure_clicked(self, event: tk.Event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        overlapping_items = self.canvas.find_overlapping(
            x, y, x, y
        )  # 找到所有的重叠的对象
        if overlapping_items:
            clicked_id = overlapping_items[-1]
            self.canvas.delete(clicked_id)
        else:
            return

        # 还要把该对象从同类图形的集合中删去
        if clicked_id in self.points:
            self.points.pop(clicked_id)
        if clicked_id in self.lines:
            self.lines.pop(clicked_id)
        if clicked_id in self.circles:
            self.circles.pop(clicked_id)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    canvas = myCanvas(root)
    tk.Button(root, text="点", command=canvas.start_draw_points).pack()
    tk.Button(root, text="线", command=canvas.start_draw_lines).pack()
    tk.Button(root, text="圆", command=canvas.start_draw_circles).pack()
    tk.Button(root, text="删除", command=canvas.start_delete).pack()

    tk.mainloop()
