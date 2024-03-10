import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPainter, QPen, QPixmap, QGuiApplication
import pyautogui
from datetime import datetime
import tkinter as tk
from pynput import mouse
from PIL import ImageGrab


class SelectAreaTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.4)
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.canvas = tk.Canvas(self.root, cursor="cross", bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.is_selecting = False
        self.finish_selection = False
        self.selected_area = None

    def on_click(self, event):
        if not self.is_selecting:
            self.is_selecting = True
            self.start_point = (event.x, event.y)
            self.rectangle = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline='red', width=3)
        else:
            self.is_selecting = False
            self.end_point = (event.x, event.y)
            self.selected_area = (self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1])
            self.root.quit()

    def on_move(self, event):
        if self.is_selecting:
            self.canvas.coords(self.rectangle, self.start_point[0], self.start_point[1], event.x, event.y)

    def run(self):
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_click)
        self.root.mainloop()
        self.root.destroy()
        return self.selected_area

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # 设置窗口的样式
        self.setStyleSheet("QWidget { background-color: #f0f0f0; }")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.take_screenshot)
        self.is_selecting = False
        self.rect = None
        self.area_tool = SelectAreaTool()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.path_label = QLabel('保存路径:')
        self.layout.addWidget(self.path_label)

        self.path_input = QLineEdit()
        self.layout.addWidget(self.path_input)

        self.path_button = QPushButton('选择路径')
        self.path_button.clicked.connect(self.choose_path)
        self.layout.addWidget(self.path_button)

        self.num_label = QLabel('截图数量:')
        self.layout.addWidget(self.num_label)

        self.num_input = QLineEdit()
        self.layout.addWidget(self.num_input)

        self.interval_label = QLabel('时间间隔（秒）:')
        self.layout.addWidget(self.interval_label)

        self.interval_input = QLineEdit()
        self.layout.addWidget(self.interval_input)

        self.select_area_button = QPushButton('选择截图区域')
        self.select_area_button.clicked.connect(self.select_area)
        self.layout.addWidget(self.select_area_button)

        self.start_button = QPushButton('开始截图')
        self.start_button.clicked.connect(self.start_screenshot)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        # 设置控件的样式
        button_style = """
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0053a6;
            }
            QPushButton:pressed {
                background-color: #00397a;
            }
        """
        self.path_button.setStyleSheet(button_style)
        self.select_area_button.setStyleSheet(button_style)
        self.start_button.setStyleSheet(button_style)

        label_style = "QLabel { color : #333333; }"
        self.path_label.setStyleSheet(label_style)
        self.num_label.setStyleSheet(label_style)
        self.interval_label.setStyleSheet(label_style)

        line_edit_style = "QLineEdit { border: 1px solid #ccc; border-radius: 2px; padding: 2px; }"
        self.path_input.setStyleSheet(line_edit_style)
        self.num_input.setStyleSheet(line_edit_style)
        self.interval_input.setStyleSheet(line_edit_style)


    def select_area(self):
        self.hide()  # 隐藏 PyQt5 主窗口
        selected_area = self.area_tool.run()  # 运行区域选择工具并获取选区
        if selected_area:
            self.rect = QRect(selected_area[0], selected_area[1], selected_area[2] - selected_area[0],
                              selected_area[3] - selected_area[1])
        self.show()  # 显示 PyQt5 主窗口

    def capture_area(self):
        screenshot = pyautogui.screenshot()
        screenshot_path = os.path.join(QGuiApplication.instance().applicationDirPath(), "temp_screenshot.png")
        screenshot.save(screenshot_path)
        self.full_screenshot = QPixmap(screenshot_path)
        self.setWindowState(Qt.WindowActive)  # 重新激活窗口
        self.showMaximized()  # 最大化显示窗口以进行区域选择


    def choose_path(self):
        path = QFileDialog.getExistingDirectory(self, '选择保存路径')
        self.path_input.setText(path)

    def start_screenshot(self):
        self.screenshot_count = 0
        self.total_screenshots = int(self.num_input.text())
        interval = int(self.interval_input.text()) * 1000  # 转换为毫秒
        self.timer.start(interval)

    def start_screenshot(self):
        self.screenshot_count = 0
        self.total_screenshots = int(self.num_input.text())
        interval = int(self.interval_input.text()) * 1000  # 转换为毫秒
        self.timer.start(interval)

    def take_screenshot(self):
        if self.screenshot_count < self.total_screenshots:
            if self.rect:
                # 使用 QRect 的坐标进行截图
                screenshot = pyautogui.screenshot(region=(self.rect.x(), self.rect.y(), self.rect.width(), self.rect.height()))
            else:
                screenshot = pyautogui.screenshot()
            path = self.path_input.text()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'screenShot_{timestamp}.png'
            full_path = os.path.join(path, filename)
            screenshot.save(full_path)
            self.screenshot_count += 1
            if self.screenshot_count >= self.total_screenshots:
                self.timer.stop()
                QMessageBox.information(self, "完成", "截图完成！")
        else:
            self.timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
