# -*- coding: utf-8 -*-
"""第4章 文件管理 —— 全部插图生成脚本
运行：python3 /Users/levi/IdeaProjects/操作系统/第4章_文件管理/draw_figures.py
"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统/第4章_文件管理")
import fg1, fg2, fg3


def main():
    for f in ["f00", "f01", "f02", "f03", "f04", "f05", "f06"]:
        getattr(fg1, f)()
    for f in ["f07", "f08", "f09", "f10", "f11", "f12"]:
        getattr(fg2, f)()
    for f in ["f13", "f14", "f15", "f16", "f17"]:
        getattr(fg3, f)()
    print("ALL DONE")


if __name__ == "__main__":
    main()
