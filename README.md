# 截图助手

这个截图助手是一个基于 PyQt5 和 pyautogui 的简单桌面应用程序，允许用户选择屏幕上的特定区域并定时自动截图。

## 功能

- **选择保存路径**：允许用户选择截图保存的目录。
- **设置截图数量**：用户可以指定要捕获的截图数量。
- **设置时间间隔**：用户可以设置连续截图之间的时间间隔（秒）。
- **选择截图区域**：用户可以选择屏幕上的一个区域，仅对该区域进行截图。
- **开始截图**：开始自动截图过程，根据用户设置的参数定时捕获屏幕或选定区域。

## 注意事项
- 在选择截图区域时，主窗口会暂时隐藏，以便用户选择区域。
- 确保在开始截图之前，所有设置（保存路径、截图数量、时间间隔和截图区域）都已正确配置。
- 如果需要重新选择截图区域，可以重新打开该程序。

## 安装

确保您的系统已安装 Python 3，然后安装所需的库：

```bash
pip install PyQt5 pyautogui Pillow