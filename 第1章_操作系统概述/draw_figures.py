# -*- coding: utf-8 -*-
"""
draw_figures.py —— 《操作系统》第1章 操作系统概述 · 全部插图生成脚本
运行：python3 /Users/levi/IdeaProjects/操作系统/第1章_操作系统概述/draw_figures.py
所有图保存到 第1章_操作系统概述/figures/ 下，文件名固定。
"""
import sys
import matplotlib.patches as mpatches

sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L,
                   GRAY, GRAY_L, PINK, PINK_L, YELLOW)

FIGDIR = "/Users/levi/IdeaProjects/操作系统/第1章_操作系统概述/figures"
F = lambda name: FIGDIR + "/" + name


def seg(ax, x, y, w, h, text="", fc=BLUE_L, ec=BLUE, fs=10, bold=True,
        tc=INK, hatch=None, lw=1.4, z=2, alpha=1.0):
    """甘特图/时间轴上的一小段矩形条。"""
    ax.add_patch(mpatches.Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec,
                                    lw=lw, hatch=hatch, zorder=z, alpha=alpha))
    if text:
        osfig.tx(ax, x + w / 2, y + h / 2, text, fs=fs, color=tc, bold=bold, z=z + 1)


# ================================================================
# ch1-00 本章知识框架导图（大脑图）
# ================================================================
def fig00():
    fig, ax = osfig.new_fig(14, 8, (0, 14), (0, 8))
    osfig.title(ax, "第1章 操作系统概述 · 知识框架导图",
                sub="一条主线：操作系统如何管理资源、如何向上提供服务（★ ≈ 考查频率）")
    osfig.tx(ax, 0.35, 7.55, "★ ≈ 考频", fs=9.5, color=GRAY, ha="left")

    cx, cy = 7.0, 4.05
    nodes = [  # (x, y, 主文字, 副文字, 描边色, 填充色, 星级)
        (2.75, 6.5, "1.1 概念与定义", "是什么 · 管什么", TEAL, TEAL_L, "★★"),
        (2.05, 5.15, "1.2 四大特征", "并发·共享·虚拟·异步", RED, RED_L, "★★★"),
        (2.05, 2.95, "1.3 发展与分类", "从手工到分布式", AMBER, AMBER_L, "★★"),
        (2.75, 1.25, "1.4 运行机制与内核", "指令 · 状态 · 内核", BLUE, BLUE_L, "★★★"),
        (11.25, 6.5, "1.5 中断与异常", "内中断 vs 外中断", PURPLE, PURPLE_L, "★★★"),
        (11.95, 5.15, "1.6 系统调用", "用户态→核心态的大门", PINK, PINK_L, "★★"),
        (11.95, 2.95, "1.7 体系结构", "大内核 · 微内核…", GREEN, GREEN_L, "★★"),
        (11.25, 1.25, "1.8 操作系统引导", "从加电到内核启动", BLUE, BLUE_L, "★★"),
    ]
    # 连线（先画，压在节点下面）
    for (x, y, *_r) in nodes:
        osfig.line(ax, cx, cy, x, y, color=GRAY, lw=2.0, z=1)
    osfig.line(ax, cx, cy, cx, 1.42, color=GRAY, lw=2.0, z=1)

    osfig.circle(ax, cx, cy, 1.5, fc=BLUE_L, ec=BLUE, lw=2.4)
    osfig.tx(ax, cx, cy, "第1章\n操作系统概述", fs=13, bold=True, color=INK)

    for (x, y, main, sub, ec, fc, stars) in nodes:
        osfig.ellipse(ax, x, y, 3.1, 1.15, fc=fc, ec=ec, lw=2.0)
        osfig.tx(ax, x, y + 0.18, main + "　" + stars, fs=11.5, bold=True, color=ec)
        osfig.tx(ax, x, y - 0.27, sub, fs=8.7, color=GRAY)
    # 底部节点 1.9
    osfig.ellipse(ax, 7.0, 0.95, 3.2, 1.0, fc=GRAY_L, ec=GRAY, lw=2.0)
    osfig.tx(ax, 7.0, 1.13, "1.9 虚拟机　★", fs=11.5, bold=True, color=INK)
    osfig.tx(ax, 7.0, 0.68, "两类 Hypervisor", fs=8.7, color=GRAY)
    osfig.save(fig, F("ch1-00_chapter_map.png"))


# ================================================================
# ch1-01 计算机系统层次结构
# ================================================================
def fig01():
    fig, ax = osfig.new_fig(11.2, 7, (0, 11.2), (0, 7))
    osfig.title(ax, "计算机系统层次结构：操作系统“承上启下”",
                sub="裸机 → 操作系统 → 应用软件 → 用户（自下而上逐层抽象）")
    layers = [  # (y, 主文字, 副文字, 描边, 填充)
        (0.75, "裸机（硬件）", "CPU · 内存 · 磁盘 · I/O 设备 —— 一切软件的物质基础", GRAY, GRAY_L),
        (2.05, "操作系统（OS）", "控制和管理整个计算机系统的软硬件资源，向上层提供服务和接口", BLUE, BLUE_L),
        (3.35, "应用软件", "浏览器 · 微信 · 数据库 · 编译器 · 游戏引擎……", GREEN, GREEN_L),
        (4.65, "最终用户", "你和我：通过命令、点击图标来使用计算机", AMBER, AMBER_L),
    ]
    for (y, main, sub, ec, fc) in layers:
        osfig.rbox(ax, 1.1, y, 6.5, 1.05, fc=fc, ec=ec, lw=2.0)
        osfig.tx(ax, 4.35, y + 0.63, main, fs=13, bold=True, color=ec)
        osfig.tx(ax, 4.35, y + 0.27, sub, fs=8.8, color=GRAY)
    osfig.tx(ax, 0.55, 3.2, "自下而上：逐层抽象", fs=9, color=GRAY, rotation=90)

    osfig.arrow(ax, 8.6, 0.9, 8.6, 5.55, color=BLUE, lw=2.4)
    osfig.arrow(ax, 9.9, 5.55, 9.9, 0.9, color=AMBER, lw=2.4)
    osfig.tx(ax, 8.6, 4.95, "向上：提供服务与接口\n（命令行 · 图形界面 · 系统调用）",
             fs=9, color=BLUE, bg="white")
    osfig.tx(ax, 9.9, 1.6, "向下：管理软硬件资源\n（处理机 · 存储器 · 文件 · 设备）",
             fs=9, color=AMBER, bg="white")
    osfig.tx(ax, 4.35, 0.28, "OS＝夹在硬件与用户之间的“大管家”：向下管资源，向上做服务",
             fs=9.5, color=GRAY)
    osfig.save(fig, F("ch1-01_system_layers.png"))


# ================================================================
# ch1-02 OS 作为资源管理者
# ================================================================
def fig02():
    fig, ax = osfig.new_fig(13, 8.5, (0, 13), (0, 8.5))
    osfig.title(ax, "操作系统：计算机系统的“资源管理者”",
                sub="四大管理职能（考试常考：哪个职能对应哪一章）")
    # 中央 OS
    osfig.rbox(ax, 5.0, 3.25, 3.0, 1.7, fc=BLUE_L, ec=BLUE, lw=2.4)
    osfig.tx(ax, 6.5, 4.5, "操作系统", fs=15, bold=True, color=BLUE)
    osfig.tx(ax, 6.5, 3.75, "计算机系统的“大管家”", fs=9, color=GRAY)
    # 四大资源
    osfig.rbox(ax, 4.1, 5.65, 4.8, 1.5, fc=TEAL_L, ec=TEAL, lw=2.0)
    osfig.tx(ax, 6.5, 6.8, "① 处理机管理", fs=12.5, bold=True, color=TEAL)
    osfig.tx(ax, 6.5, 6.1, "进程控制 · 进程同步 · 进程通信\n作业与进程调度", fs=9, color=INK)
    osfig.rbox(ax, 4.1, 1.05, 4.8, 1.5, fc=AMBER_L, ec=AMBER, lw=2.0)
    osfig.tx(ax, 6.5, 2.2, "② 存储器管理", fs=12.5, bold=True, color=AMBER)
    osfig.tx(ax, 6.5, 1.5, "内存分配与回收 · 地址映射\n内存保护 · 内存扩充", fs=9, color=INK)
    osfig.rbox(ax, 0.55, 3.35, 3.9, 1.5, fc=PURPLE_L, ec=PURPLE, lw=2.0)
    osfig.tx(ax, 2.5, 4.5, "③ 文件管理", fs=12.5, bold=True, color=PURPLE)
    osfig.tx(ax, 2.5, 3.8, "文件存储空间管理 · 目录管理\n文件读写与保护", fs=9, color=INK)
    osfig.rbox(ax, 8.55, 3.35, 3.9, 1.5, fc=GREEN_L, ec=GREEN, lw=2.0)
    osfig.tx(ax, 10.5, 4.5, "④ 设备管理", fs=12.5, bold=True, color=GREEN)
    osfig.tx(ax, 10.5, 3.8, "缓冲管理 · 设备分配与回收\n设备驱动 · 虚拟设备", fs=9, color=INK)
    # 双向箭头
    osfig.arrow(ax, 6.5, 4.95, 6.5, 5.65, both=True, color=GRAY, lw=1.8, shrink=3)
    osfig.arrow(ax, 6.5, 3.25, 6.5, 2.55, both=True, color=GRAY, lw=1.8, shrink=3)
    osfig.arrow(ax, 5.0, 4.1, 4.45, 4.1, both=True, color=GRAY, lw=1.8, shrink=3)
    osfig.arrow(ax, 8.0, 4.1, 8.55, 4.1, both=True, color=GRAY, lw=1.8, shrink=3)
    osfig.tx(ax, 6.5, 0.55,
             "四大管理职能 对应 全书第 2~5 章；OS 通过管理资源，把裸机变成“方便好用的虚拟机”",
             fs=10, color=GRAY)
    osfig.save(fig, F("ch1-02_os_as_manager.png"))


# ================================================================
# ch1-03 四大特征关系图
# ================================================================
def fig03():
    fig, ax = osfig.new_fig(12.5, 8, (0, 12.5), (0, 8))
    osfig.title(ax, "操作系统的四大特征及其关系",
                sub="并发与共享互为存在条件；虚拟以并发＋共享为前提；异步以并发为前提")
    # 虚拟（顶部）
    osfig.rbox(ax, 1.8, 5.55, 4.6, 1.2, fc=PURPLE_L, ec=PURPLE, lw=2.2)
    osfig.tx(ax, 4.1, 6.45, "虚拟", fs=14, bold=True, color=PURPLE)
    osfig.tx(ax, 4.1, 5.85, "一个物理实体 → 若干个逻辑对应物", fs=9, color=INK)
    # 三个主特征
    osfig.rbox(ax, 0.4, 2.7, 3.0, 1.6, fc=GREEN_L, ec=GREEN, lw=2.2)
    osfig.tx(ax, 1.9, 3.9, "共享", fs=14, bold=True, color=GREEN)
    osfig.tx(ax, 1.9, 3.25, "资源可被多个\n进程共同使用", fs=8.8, color=INK)
    osfig.tx(ax, 1.9, 2.38, "最基本的特征之一", fs=8.5, color=GREEN)
    osfig.rbox(ax, 4.9, 2.7, 3.0, 1.6, fc=BLUE_L, ec=BLUE, lw=2.2)
    osfig.tx(ax, 6.4, 3.9, "并发", fs=14, bold=True, color=BLUE)
    osfig.tx(ax, 6.4, 3.25, "同一时间段内\n多个进程交替执行", fs=8.8, color=INK)
    osfig.tx(ax, 6.4, 2.38, "最基本的特征之一", fs=8.5, color=BLUE)
    osfig.rbox(ax, 9.1, 2.7, 3.0, 1.6, fc=AMBER_L, ec=AMBER, lw=2.2)
    osfig.tx(ax, 10.6, 3.9, "异步", fs=14, bold=True, color=AMBER)
    osfig.tx(ax, 10.6, 3.25, "进程“走走停停”\n推进速度不可预知", fs=8.8, color=INK)
    # 箭头
    osfig.arrow(ax, 3.45, 3.5, 4.85, 3.5, both=True, color=RED, lw=2.4, shrink=2)
    osfig.tx(ax, 4.15, 4.0, "互为存在条件", fs=10.5, bold=True, color=RED, bg="white")
    osfig.arrow(ax, 2.4, 4.35, 3.55, 5.5, color=PURPLE, lw=2.0, shrink=3)
    osfig.tx(ax, 2.55, 4.85, "前提", fs=9, color=PURPLE, bg="white")
    osfig.arrow(ax, 5.9, 4.35, 4.65, 5.5, color=PURPLE, lw=2.0, shrink=3)
    osfig.tx(ax, 5.75, 4.85, "前提", fs=9, color=PURPLE, bg="white")
    osfig.arrow(ax, 7.95, 3.5, 9.05, 3.5, color=AMBER, lw=2.4, shrink=2)
    osfig.tx(ax, 8.5, 3.98, "以并发为前提", fs=9.5, color=AMBER, bg="white")
    # 底部论证
    osfig.tx(ax, 0.7, 1.5, "① 并发与共享互为存在条件：程序要并发执行，就必须共享资源；资源允许共享，多道程序才能真正并发",
             fs=9.5, color=INK, ha="left")
    osfig.tx(ax, 0.7, 0.95, "② 虚拟靠“时分复用 / 空分复用”实现“一变多”，而复用正是并发＋共享的直接产物",
             fs=9.5, color=INK, ha="left")
    osfig.tx(ax, 0.7, 0.4, "③ 没有并发就没有异步：单道程序顺序执行、一步接一步，根本不存在“走走停停”",
             fs=9.5, color=INK, ha="left")
    osfig.save(fig, F("ch1-03_four_features.png"))


# ================================================================
# ch1-04 并发 vs 并行
# ================================================================
def fig04():
    fig, ax = osfig.new_fig(12.5, 7.5, (0, 12.5), (0, 7.5))
    osfig.title(ax, "并发 vs 并行：一字之差，天壤之别",
                sub="并发＝同一时间段内交替（单核即可）；并行＝同一时刻同时（必须多核/多CPU）")
    ticks = [1.3 + 2.0 * k for k in range(6)]
    # 虚线时间基准线
    for x in ticks:
        osfig.line(ax, x, 0.9, x, 6.0, color="#D1D5DB", lw=1.0, ls="--", z=1)
    # 上半：并发
    osfig.tx(ax, 0.7, 6.3, "① 并发（单核 CPU）：宏观上并行，微观上串行交替",
             fs=13, bold=True, color=BLUE, ha="left")
    labels = ["A", "B", "A", "B", "A"]
    for i, lb in enumerate(labels):
        fc, ec = (BLUE_L, BLUE) if lb == "A" else (GREEN_L, GREEN)
        seg(ax, 1.3 + 2.0 * i, 5.15, 2.0, 0.8, lb, fc, ec, fs=13)
    osfig.tx(ax, 1.08, 5.55, "CPU", fs=10, bold=True, ha="right")
    for k in range(6):
        osfig.tx(ax, ticks[k], 4.8, str(k), fs=9, color=GRAY)
    osfig.tx(ax, 11.95, 5.55, "时间→", fs=9, ha="left")
    osfig.tx(ax, 6.3, 4.25, "微观：任一时刻 CPU 上只有一道程序在运行；宏观：一段时间内 A、B 都在推进（“看似同时”）",
             fs=10, color=INK, bg="white")
    # 下半：并行
    osfig.tx(ax, 0.7, 3.5, "② 并行（多核 CPU）：真正的“同一时刻同时执行”",
             fs=13, bold=True, color=GREEN, ha="left")
    seg(ax, 1.3, 2.4, 10.0, 0.7, "作业 A —— 在核心 1 上运行", BLUE_L, BLUE, fs=10.5)
    seg(ax, 1.3, 1.5, 10.0, 0.7, "作业 B —— 在核心 2 上运行", GREEN_L, GREEN, fs=10.5)
    osfig.tx(ax, 1.08, 2.75, "核心1", fs=9.5, ha="right")
    osfig.tx(ax, 1.08, 1.85, "核心2", fs=9.5, ha="right")
    for k in range(6):
        osfig.tx(ax, ticks[k], 1.15, str(k), fs=9, color=GRAY)
    osfig.tx(ax, 11.95, 2.75, "时间→", fs=9, ha="left")
    osfig.tx(ax, 6.3, 0.5, "并行需要硬件支持（多核 / 多 CPU）：同一时刻，多个程序真的在同时执行",
             fs=10, color=INK, bg="white")
    osfig.save(fig, F("ch1-04_concurrency_vs_parallel.png"))


# ================================================================
# ch1-05 两种共享方式
# ================================================================
def fig05():
    fig, ax = osfig.new_fig(12.5, 7.5, (0, 12.5), (0, 7.5))
    osfig.title(ax, "两种资源共享方式：互斥共享 vs 同时共享",
                sub="“共享”不等于“任何时刻都能同时用”——这是高频易错点！")
    # 上半：互斥共享
    osfig.tx(ax, 0.7, 6.35, "① 互斥共享方式 —— 例：打印机", fs=13, bold=True, color=PINK, ha="left")
    osfig.rbox(ax, 0.8, 5.0, 2.2, 0.75, text="打印机", fc=PINK_L, ec=PINK, fs=12.5, bold=True, color=PINK)
    names = ["P1", "P2", "P1", "P2", "P1"]
    for i, lb in enumerate(names):
        fc, ec = (PINK_L, PINK) if lb == "P1" else (AMBER_L, AMBER)
        seg(ax, 3.6 + 1.62 * i, 5.0, 1.62, 0.75, lb, fc, ec, fs=11)
    for k in range(6):
        osfig.tx(ax, 3.6 + 1.62 * k, 4.68, "t%d" % k, fs=8.5, color=GRAY)
    osfig.tx(ax, 11.95, 5.38, "时间→", fs=9, ha="left")
    osfig.tx(ax, 6.3, 4.05, "打印机同一时刻只能服务一个进程：P1 用时 P2 必须等 → 各进程“轮流独占”，宏观上都“用过”打印机",
             fs=10, color=INK, bg="white")
    osfig.line(ax, 0.7, 3.7, 12.0, 3.7, color="#D1D5DB", lw=1.2)
    # 下半：同时共享
    osfig.tx(ax, 0.7, 3.3, "② 同时共享方式 —— 例：磁盘", fs=13, bold=True, color=TEAL, ha="left")
    osfig.rbox(ax, 0.8, 1.6, 2.2, 0.9, text="硬盘", fc=TEAL_L, ec=TEAL, fs=12.5, bold=True, color=TEAL)
    # 重叠时段高亮
    ax.add_patch(mpatches.Rectangle((6.0, 1.28), 2.4, 1.34, facecolor=AMBER_L,
                                    edgecolor=AMBER, lw=1.2, zorder=0, alpha=0.55))
    seg(ax, 3.6, 2.7, 3.0, 0.55, "进程1 读文件", TEAL_L, TEAL, fs=9.5)
    seg(ax, 4.8, 2.02, 3.6, 0.55, "进程2 读文件", TEAL_L, TEAL, fs=9.5)
    seg(ax, 6.0, 1.34, 3.6, 0.55, "进程3 写文件", AMBER_L, AMBER, fs=9.5)
    osfig.tx(ax, 9.95, 2.28, "时间→", fs=9, ha="left")
    osfig.tx(ax, 7.2, 0.85, "↑ 这一时段：多个进程“同时”访问磁盘（宏观同时）", fs=9.5, color=AMBER, bg="white")
    osfig.tx(ax, 6.3, 0.3, "宏观同时 ≠ 微观并行：访问不同磁道可真正并行；访问同一磁道微观上仍需交替",
             fs=10, color=INK, bg="white")
    osfig.save(fig, F("ch1-05_two_sharing.png"))


# ================================================================
# ch1-06 虚拟技术实例
# ================================================================
def fig06():
    fig, ax = osfig.new_fig(12.5, 8, (0, 12.5), (0, 8))
    osfig.title(ax, "虚拟技术：“一个变多个”的三种玩法",
                sub="本质：时分复用（轮流用）与空分复用（切开用）")
    cols = [2.3, 6.25, 10.2]
    osfig.tx(ax, cols[0], 6.55, "① 时分复用技术", fs=12.5, bold=True, color=BLUE)
    osfig.tx(ax, cols[1], 6.55, "② 空分复用技术", fs=12.5, bold=True, color=GREEN)
    osfig.tx(ax, cols[2], 6.55, "③ SPOOLing 假脱机", fs=12.5, bold=True, color=PURPLE)
    # 物理设备
    osfig.rbox(ax, cols[0] - 1.6, 5.075, 3.2, 0.85, text="1 个物理 CPU", fc=BLUE_L, ec=BLUE, fs=12, bold=True)
    osfig.rbox(ax, cols[1] - 1.6, 5.075, 3.2, 0.85, text="1 块物理磁盘", fc=GREEN_L, ec=GREEN, fs=12, bold=True)
    osfig.rbox(ax, cols[2] - 1.6, 5.075, 3.2, 0.85, text="1 台物理打印机", fc=PURPLE_L, ec=PURPLE, fs=12, bold=True)
    # 箭头
    osfig.arrow(ax, cols[0], 5.03, cols[0], 3.5, color=GRAY, lw=2.0, shrink=2)
    osfig.tx(ax, cols[0] + 1.25, 4.2, "时间片轮转\n轮流使用", fs=9, color=BLUE)
    osfig.arrow(ax, cols[1], 5.03, cols[1], 2.65, color=GRAY, lw=2.0, shrink=2)
    osfig.tx(ax, cols[1] + 1.35, 4.2, "划分存储区域\n各占一块", fs=9, color=GREEN)
    osfig.arrow(ax, cols[2], 5.03, cols[2], 2.65, color=GRAY, lw=2.0, shrink=2)
    osfig.tx(ax, cols[2] + 1.3, 4.2, "输出先存入磁盘\n队列，逐份打印", fs=9, color=PURPLE)
    # 逻辑对应物
    for i, s in enumerate(["逻辑 CPU ①", "逻辑 CPU ②", "逻辑 CPU ③"]):
        osfig.box(ax, cols[0], 3.1 - 0.75 * i, 2.4, 0.6, s, fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
    for i, s in enumerate(["C:", "D:", "E:"]):
        osfig.box(ax, 5.1 + 1.15 * i, 2.2, 1.05, 0.8, s, fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    osfig.tx(ax, cols[1], 1.5, "逻辑卷（如 C: D: E: 盘）", fs=8.8, color=GRAY)
    for i, s in enumerate(["打印机①", "打印机②", "打印机③"]):
        osfig.box(ax, 9.05 + 1.15 * i, 2.2, 1.05, 0.8, s, fc=PURPLE_L, ec=PURPLE, fs=8.8, bold=True)
    osfig.tx(ax, cols[2], 1.5, "虚拟打印机（排队输出）", fs=8.8, color=GRAY)
    osfig.tx(ax, 6.25, 0.55, "用户感受：每个程序都以为“独占”了一台设备 —— 一个物理实体 → 多个逻辑对应物，这就是“虚拟”",
             fs=10, color=INK)
    osfig.save(fig, F("ch1-06_virtualization.png"))


# ================================================================
# ch1-07 发展历程时间轴
# ================================================================
def fig07():
    fig, ax = osfig.new_fig(13.5, 8, (0, 13.5), (0, 8))
    osfig.title(ax, "操作系统的发展历程：每一步都是为了解决上一代的痛点",
                sub="手工 → 单道批处理 → 多道批处理 → 分时 → 实时 → 网络与分布式")
    osfig.arrow(ax, 0.7, 4.0, 13.2, 4.0, color=INK, lw=2.6, ms=22)
    xs = [1.5, 3.55, 5.6, 7.65, 9.7, 11.75]
    nums = ["①", "②", "③", "④", "⑤", "⑥"]
    ecs = [GRAY, BLUE, GREEN, PURPLE, RED, TEAL]
    fcs = [GRAY_L, BLUE_L, GREEN_L, PURPLE_L, RED_L, TEAL_L]
    years = ["1945—1955", "20世纪50年代", "20世纪60年代初",
             "20世纪60年代起", "20世纪60年代", "20世纪80年代至今"]
    for i, x in enumerate(xs):
        osfig.circle(ax, x, 4.0, 0.28, text=nums[i], fc=fcs[i], ec=ecs[i], fs=9.5)
        above = (i % 2 == 0)
        if above:
            osfig.line(ax, x, 4.28, x, 4.85, color=ecs[i], lw=1.6)
            cy = 5.85
            yr_y = 3.6
        else:
            osfig.line(ax, x, 3.72, x, 3.05, color=ecs[i], lw=1.6)
            cy = 2.05
            yr_y = 4.4
        osfig.tx(ax, x, yr_y, years[i], fs=8, color=GRAY)
        # 分阶段盒子
        osfig.rbox(ax, x - 1.3, cy - 1.0, 2.6, 2.0, fc=fcs[i], ec=ecs[i], lw=1.8)
        osfig.tx(ax, x, cy + 0.68, ["手工阶段", "单道批处理", "多道批处理",
                                    "分时系统", "实时系统", "网络/分布式OS"][i],
                 fs=11.5, bold=True, color=ecs[i])
        body = ["无OS，用户独占全机\nCPU 等待人工操作",
                "作业自动逐道执行\n内存中始终只有一道\nI/O 时 CPU 空等",
                "内存同时驻留多道程序\nCPU 与 I/O 并行工作",
                "CPU 时间切成时间片\n轮流服务多个终端",
                "在截止时间内必须完成\n硬实时 / 软实时",
                "多机互联、资源共享\n分布式：多机如一机"][i]
        osfig.tx(ax, x, cy + 0.08, body, fs=8.4, color=INK)
        note = ["痛点：人机矛盾\n利用率极低",
                "特点：自动性\n顺序性 · 单道性",
                "优：利用率高\n吞吐量大\n缺：无交互",
                "同时·交互\n独立·及时",
                "可靠性优先\n于吞吐量",
                "了解即可"][i]
        ncolor = RED if i in (0, 1) else (GREEN if i in (2, 3, 4) else GRAY)
        osfig.tx(ax, x, cy - 0.62, note, fs=8.2, color=ncolor)
    osfig.tx(ax, 6.75, 0.45, "记忆口诀：手工等人 → 单道排队 → 多道并行 → 分时轮转 → 实时保命 → 网络互联",
             fs=10.5, bold=True, color=PURPLE)
    osfig.save(fig, F("ch1-07_history_timeline.png"))


# ================================================================
# ch1-08 多道程序提高利用率（单道 vs 多道）
# ================================================================
def fig08():
    fig, ax = osfig.new_fig(14, 9, (0, 14), (0, 9))
    osfig.title(ax, "多道程序设计：让 CPU 和 I/O“忙”起来",
                sub="作业A：CPU 20ms → I/O 30ms → CPU 10ms；作业B：CPU 30ms → I/O 20ms → CPU 10ms")
    X = lambda ms: 1.6 + ms / 10.0
    # ① 单道
    osfig.tx(ax, 0.7, 7.7, "① 单道批处理：一道做完，才轮到下一道", fs=12.5, bold=True, color=BLUE, ha="left")
    seg(ax, 9.8, 7.55, 0.55, 0.3, fc=BLUE_L, ec=BLUE)
    osfig.tx(ax, 10.45, 7.7, "占用 CPU", fs=9, ha="left")
    seg(ax, 11.5, 7.55, 0.55, 0.3, fc=GRAY_L, ec=GRAY, hatch="//")
    osfig.tx(ax, 12.15, 7.7, "I/O（不占 CPU）", fs=9, ha="left")
    osfig.tx(ax, 1.4, 6.74, "作业A", fs=10.5, bold=True, ha="right")
    seg(ax, X(0), 6.4, 2.0, 0.68, "CPU 20ms", BLUE_L, BLUE, fs=9.5)
    seg(ax, X(20), 6.4, 3.0, 0.68, "I/O 30ms", GRAY_L, GRAY, fs=9.5, hatch="//")
    seg(ax, X(50), 6.4, 1.0, 0.68, "CPU10ms", BLUE_L, BLUE, fs=8.5)
    osfig.tx(ax, 1.4, 5.74, "作业B", fs=10.5, bold=True, ha="right")
    seg(ax, X(60), 5.4, 3.0, 0.68, "CPU 30ms", GREEN_L, GREEN, fs=9.5)
    seg(ax, X(90), 5.4, 2.0, 0.68, "I/O 20ms", GRAY_L, GRAY, fs=9.5, hatch="//")
    seg(ax, X(110), 5.4, 1.0, 0.68, "CPU10ms", GREEN_L, GREEN, fs=8.5)
    for k in range(7):
        osfig.tx(ax, X(20 * k), 5.05, str(20 * k), fs=8.5, color=GRAY)
    osfig.tx(ax, 7.7, 4.55, "单道：总时长 120ms；CPU 利用率 = 70/120 ≈ 58.3%",
             fs=11, bold=True, color=RED, bg="white")
    osfig.line(ax, 0.7, 4.1, 13.4, 4.1, color="#D1D5DB", lw=1.2)
    # ② 多道
    osfig.tx(ax, 0.7, 3.65, "② 多道批处理：A 做 I/O 时，B 上 CPU（CPU 与 I/O 并行）",
             fs=12.5, bold=True, color=GREEN, ha="left")
    osfig.tx(ax, 1.4, 2.94, "作业A", fs=10.5, bold=True, ha="right")
    seg(ax, X(0), 2.6, 2.0, 0.68, "CPU 20ms", BLUE_L, BLUE, fs=9.5)
    seg(ax, X(20), 2.6, 3.0, 0.68, "I/O 30ms", GRAY_L, GRAY, fs=9.5, hatch="//")
    seg(ax, X(50), 2.6, 1.0, 0.68, "CPU10ms", BLUE_L, BLUE, fs=8.5)
    osfig.tx(ax, X(60) + 0.25, 2.94, "A 完成√", fs=9.5, color=GREEN, ha="left")
    osfig.tx(ax, 1.4, 1.94, "作业B", fs=10.5, bold=True, ha="right")
    seg(ax, X(0), 1.6, 2.0, 0.68, "等待", "white", GRAY, fs=9.5)
    seg(ax, X(20), 1.6, 3.0, 0.68, "CPU 30ms", GREEN_L, GREEN, fs=9.5)
    seg(ax, X(50), 1.6, 2.0, 0.68, "I/O 20ms", GRAY_L, GRAY, fs=9.5, hatch="//")
    seg(ax, X(70), 1.6, 1.0, 0.68, "CPU10ms", GREEN_L, GREEN, fs=8.5)
    osfig.tx(ax, X(80) + 0.25, 1.94, "B 完成√", fs=9.5, color=GREEN, ha="left")
    osfig.tx(ax, 1.4, 1.04, "CPU", fs=9.5, bold=True, ha="right")
    seg(ax, X(0), 0.8, 2.0, 0.48, "A", BLUE_L, BLUE, fs=9)
    seg(ax, X(20), 0.8, 3.0, 0.48, "B", GREEN_L, GREEN, fs=9)
    seg(ax, X(50), 0.8, 1.0, 0.48, "A", BLUE_L, BLUE, fs=9)
    seg(ax, X(60), 0.8, 1.0, 0.48, "闲", "white", GRAY, fs=9)
    seg(ax, X(70), 0.8, 1.0, 0.48, "B", GREEN_L, GREEN, fs=9)
    for k in range(5):
        osfig.tx(ax, X(20 * k), 0.35, str(20 * k), fs=8.5, color=GRAY)
    osfig.tx(ax, 11.55, 2.6, "多道：总时长 80ms\nCPU 利用率 = 70/80\n= 87.5%", fs=10.5, bold=True,
             color=RED, ha="left")
    osfig.save(fig, F("ch1-08_multiprogramming_timeline.png"))


# ================================================================
# ch1-09 两类指令与两种处理器状态
# ================================================================
def fig09():
    fig, ax = osfig.new_fig(13.5, 7.5, (0, 13.5), (0, 7.5))
    osfig.title(ax, "两类指令 · 两种处理器状态 · 两种程序",
                sub="CPU 靠 PSW 中的标志位区分用户态/核心态；状态的切换由中断/异常引发")
    # 左：特权指令
    osfig.rbox(ax, 0.6, 3.5, 6.2, 3.2, fc=RED_L, ec=RED, lw=2.0)
    osfig.tx(ax, 3.7, 6.4, "特权指令（内核专用，禁止用户程序使用）", fs=12.5, bold=True, color=RED)
    pri = ["• I/O 指令（向设备发命令 / 传数据）",
           "• 置时钟指令（修改系统时间）",
           "• 开中断 / 关中断（中断屏蔽）",
           "• 修改页表基址寄存器",
           "• 送程序状态字 PSW、停机指令"]
    for i, s in enumerate(pri):
        osfig.tx(ax, 1.0, 5.85 - 0.43 * i, s, fs=10, color=INK, ha="left")
    # 左：非特权指令
    osfig.rbox(ax, 0.6, 0.35, 6.2, 2.75, fc=GREEN_L, ec=GREEN, lw=2.0)
    osfig.tx(ax, 3.7, 2.8, "非特权指令（普通指令，人人可用）", fs=12.5, bold=True, color=GREEN)
    nonpri = ["• 算术 / 逻辑运算、数据传送（取数、存数）",
              "• 条件转移、读时钟日期"]
    for i, s in enumerate(nonpri):
        osfig.tx(ax, 1.0, 2.32 - 0.42 * i, s, fs=10, color=INK, ha="left")
    osfig.tx(ax, 1.0, 1.35, "• 陷入指令（访管指令）—— 本身是非特权指令，在用户态执行！",
             fs=9.5, color=RED, bold=True, ha="left")
    # 右：核心态 / 用户态
    osfig.rbox(ax, 7.75, 5.0, 3.2, 1.1, fc=RED_L, ec=RED, lw=2.2)
    osfig.tx(ax, 9.35, 5.81, "核心态（管态）", fs=12.5, bold=True, color=RED)
    osfig.tx(ax, 9.35, 5.28, "运行内核程序", fs=9, color=INK)
    osfig.rbox(ax, 7.75, 1.25, 3.2, 1.1, fc=BLUE_L, ec=BLUE, lw=2.2)
    osfig.tx(ax, 9.35, 2.06, "用户态（目态）", fs=12.5, bold=True, color=BLUE)
    osfig.tx(ax, 9.35, 1.53, "运行应用程序", fs=9, color=INK)
    osfig.arrow(ax, 8.35, 2.4, 8.35, 4.95, color=RED, lw=2.2)
    osfig.arrow(ax, 10.45, 4.95, 10.45, 2.4, color=GREEN, lw=2.2)
    osfig.tx(ax, 9.25, 3.68, "① 由中断 / 异常 / 陷入引发\n（硬件自动完成切换）", fs=9.5, color=RED, bg="white")
    osfig.tx(ax, 11.85, 3.68, "② 中断返回时\n（特权指令修改 PSW）", fs=9.5, color=GREEN, bg="white")
    osfig.rbox(ax, 7.4, 0.3, 5.7, 0.95, fc=GRAY_L, ec=GRAY, lw=1.8)
    osfig.tx(ax, 10.25, 0.99, "PSW（程序状态字）：用标志位记录 CPU 当前处于哪种状态", fs=9.5, bold=True, color=INK)
    osfig.tx(ax, 10.25, 0.58, "两种程序：内核程序 → 核心态运行；应用程序 → 用户态运行", fs=9, color=GRAY)
    osfig.save(fig, F("ch1-09_cpu_modes.png"))


# ================================================================
# ch1-10 中断与异常分类树
# ================================================================
def fig10():
    fig, ax = osfig.new_fig(13, 8.6, (0, 13), (0, 8.6))
    osfig.title(ax, "中断与异常的分类树",
                sub="外中断＝来自 CPU 外部（与当前指令无关）；内中断＝来自 CPU 内部（与当前指令有关）")
    osfig.rbox(ax, 4.7, 6.55, 3.6, 0.72, text="中断（广义）", fc=BLUE_L, ec=BLUE, fs=13, bold=True)
    # 二级
    osfig.rbox(ax, 1.7, 5.2, 3.4, 1.0, fc=TEAL_L, ec=TEAL, lw=2.2)
    osfig.tx(ax, 3.4, 5.86, "外中断（狭义的“中断”）", fs=12, bold=True, color=TEAL)
    osfig.tx(ax, 3.4, 5.47, "来自 CPU 外部、与当前指令无关", fs=8.8, color=GRAY)
    osfig.rbox(ax, 7.9, 5.2, 3.4, 1.0, fc=PURPLE_L, ec=PURPLE, lw=2.2)
    osfig.tx(ax, 9.6, 5.86, "内中断（又称“异常”）", fs=12, bold=True, color=PURPLE)
    osfig.tx(ax, 9.6, 5.47, "来自 CPU 内部、与当前指令有关", fs=8.8, color=GRAY)
    osfig.line(ax, 6.5, 6.55, 3.4, 6.2, color=GRAY, lw=1.8)
    osfig.line(ax, 6.5, 6.55, 9.6, 6.2, color=GRAY, lw=1.8)
    # 叶子
    leaves = [
        (1.4, TEAL, TEAL_L, "时钟中断", "例：时间片用完", "例：实时钟到时"),
        (3.4, TEAL, TEAL_L, "I/O 中断", "例：打印机打印完成", "例：键盘有输入"),
        (5.4, TEAL, TEAL_L, "人工干预", "例：用户按下 Ctrl+C", "例：管理员强制重启"),
        (7.8, PURPLE, PURPLE_L, "陷入 trap", "例：系统调用", "特点：有意安排、主动"),
        (9.6, PURPLE, PURPLE_L, "故障 fault", "例：缺页、除零", "特点：可修复后继续"),
        (11.4, PURPLE, PURPLE_L, "终止 abort", "例：非法访存、硬件故障", "特点：致命，终止进程"),
    ]
    for (x, ec, fc, name, e1, e2) in leaves:
        src = 3.4 if x < 6.5 else 9.6
        osfig.line(ax, src, 5.2, x, 4.25, color=GRAY, lw=1.5)
        osfig.rbox(ax, x - 0.95, 2.35, 1.9, 1.9, fc=fc, ec=ec, lw=1.8)
        osfig.tx(ax, x, 3.92, name, fs=11, bold=True, color=ec)
        osfig.tx(ax, x, 3.18, e1, fs=8.4, color=INK)
        osfig.tx(ax, x, 2.78, e2, fs=8.4, color=GRAY)
    # 判别方法
    osfig.rbox(ax, 2.4, 0.35, 8.2, 1.5, fc=AMBER_L, ec=AMBER, lw=2.0, dashed=True)
    osfig.tx(ax, 6.5, 1.56, "判别方法（必考）", fs=11, bold=True, color=AMBER)
    osfig.tx(ax, 6.5, 1.12, "一看事件来自 CPU 内部还是外部；二看与当前执行的指令是否有关", fs=9.8, color=INK)
    osfig.tx(ax, 6.5, 0.68, "除零、缺页、非法访存 → 内中断；时钟到时、I/O 完成、按键 → 外中断",
             fs=9.8, bold=True, color=AMBER)
    osfig.save(fig, F("ch1-10_interrupt_tree.png"))


# ================================================================
# ch1-11 中断处理全过程流程
# ================================================================
def fig11():
    fig, ax = osfig.new_fig(9, 11.5, (0, 9), (0, 11.5))
    osfig.title(ax, "中断处理全过程", sub="硬件（中断隐指令）先做①~③；软件（中断服务程序）做④~⑩")
    steps = [  # (框文字, 旁注, 描边, 填充)
        ("中断请求", "中断源向 CPU 发出请求信号", GRAY, GRAY_L),
        ("① 关中断", "防止保存断点/现场过程被新中断打扰", AMBER, AMBER_L),
        ("② 保存断点", "保存 PC（程序计数器），以便返回", AMBER, AMBER_L),
        ("③ 引出中断服务程序", "查中断向量表，找到服务程序入口地址", AMBER, AMBER_L),
        ("④ 保存现场和屏蔽字", "通用寄存器等内容压栈保存", BLUE, BLUE_L),
        ("⑤ 开中断", "允许响应更高级的中断请求", BLUE, BLUE_L),
        ("⑥ 执行中断服务程序", "真正为中断源服务（如取走设备数据）", BLUE, BLUE_L),
        ("⑦ 关中断", "恢复现场期间禁止新中断", BLUE, BLUE_L),
        ("⑧ 恢复现场和屏蔽字", "从栈中恢复寄存器内容", BLUE, BLUE_L),
        ("⑨ 开中断", "允许响应新的中断请求", BLUE, BLUE_L),
        ("⑩ 中断返回", "回到断点，继续执行原程序", BLUE, BLUE_L),
    ]
    y0, dy, bh = 9.85, 0.88, 0.62
    for i, (label, note, ec, fc) in enumerate(steps):
        cy = y0 - dy * i
        osfig.rbox(ax, 3.6 - 2.15, cy - bh / 2, 4.3, bh, fc=fc, ec=ec, lw=2.0)
        osfig.tx(ax, 3.6, cy, label, fs=11, bold=True, color=ec)
        osfig.tx(ax, 5.95, cy, note, fs=8.8, color=GRAY, ha="left")
        if i < len(steps) - 1:
            osfig.arrow(ax, 3.6, cy - bh / 2, 3.6, cy - dy + bh / 2,
                        color=GRAY, lw=1.6, shrink=2)
    # 左侧分组括线
    osfig.line(ax, 1.15, 9.28, 1.15, 6.9, color=AMBER, lw=1.8)
    osfig.line(ax, 1.0, 9.28, 1.15, 9.28, color=AMBER, lw=1.8)
    osfig.line(ax, 1.0, 6.9, 1.15, 6.9, color=AMBER, lw=1.8)
    osfig.tx(ax, 0.62, 8.09, "中断隐指令（硬件自动完成）", fs=10, bold=True, color=AMBER, rotation=90)
    osfig.line(ax, 1.15, 6.64, 1.15, 0.74, color=BLUE, lw=1.8)
    osfig.line(ax, 1.0, 6.64, 1.15, 6.64, color=BLUE, lw=1.8)
    osfig.line(ax, 1.0, 0.74, 1.15, 0.74, color=BLUE, lw=1.8)
    osfig.tx(ax, 0.62, 3.69, "中断服务程序（内核软件完成）", fs=10, bold=True, color=BLUE, rotation=90)
    osfig.tx(ax, 4.7, 0.22, "橙色＝硬件自动（中断隐指令）；蓝色＝内核软件（中断服务程序）；开/关中断本身是特权指令",
             fs=9.5, color=GRAY)
    osfig.save(fig, F("ch1-11_interrupt_flow.png"))


# ================================================================
# ch1-12 系统调用全过程
# ================================================================
def fig12():
    fig, ax = osfig.new_fig(12, 11, (0, 12), (0, 11))
    osfig.title(ax, "系统调用的执行过程", sub="注意每一步处于用户态还是核心态——“陷入指令”本身在用户态执行！")
    # 三个泳道
    ax.add_patch(mpatches.Rectangle((0.4, 6.9), 10.4, 2.9, facecolor=PURPLE_L,
                                    edgecolor=PURPLE, lw=1.4, zorder=0, alpha=0.35))
    ax.add_patch(mpatches.Rectangle((0.4, 3.1), 10.4, 3.1, facecolor=RED_L,
                                    edgecolor=RED, lw=1.4, zorder=0, alpha=0.3))
    ax.add_patch(mpatches.Rectangle((0.4, 0.9), 10.4, 1.7, facecolor=PURPLE_L,
                                    edgecolor=PURPLE, lw=1.4, zorder=0, alpha=0.35))
    osfig.tx(ax, 0.78, 8.35, "用户态（目态）", fs=11, bold=True, color=PURPLE, rotation=90)
    osfig.tx(ax, 0.78, 4.65, "核心态（管态）", fs=11, bold=True, color=RED, rotation=90)
    osfig.tx(ax, 0.78, 1.75, "用户态（目态）", fs=11, bold=True, color=PURPLE, rotation=90)

    boxes = [
        (9.2, "① 用户程序调用库函数 / 系统调用接口（如 read()）", BLUE_L, BLUE, False),
        (8.25, "② 传参：把系统调用号和参数放入指定寄存器（仍在用户态）", BLUE_L, BLUE, False),
        (7.3, "③ 执行陷入指令（trap / 访管指令）", PINK_L, PINK, True),
        (5.45, "④ 陷入机制：硬件自动保存断点、切换核心态，按调用号查入口表", AMBER_L, AMBER, False),
        (4.5, "⑤ 执行对应的内核服务例程 —— 真正的资源操作都在核心态完成", AMBER_L, AMBER, False),
        (3.55, "⑥ 结果放入约定寄存器，准备返回", AMBER_L, AMBER, False),
        (1.75, "⑦ 中断返回：恢复现场、切回用户态，从断点继续执行", GREEN_L, GREEN, True),
    ]
    for (cy, text, fc, ec, bold) in boxes:
        osfig.rbox(ax, 2.4, cy - 0.36, 7.2, 0.72, fc=fc, ec=ec, lw=2.0)
        osfig.tx(ax, 6.0, cy, text, fs=10.3, bold=bold, color=(ec if bold else INK))
    osfig.arrow(ax, 6.0, 8.84, 6.0, 8.61, color=GRAY, lw=1.8, shrink=2)
    osfig.arrow(ax, 6.0, 7.89, 6.0, 7.66, color=GRAY, lw=1.8, shrink=2)
    osfig.arrow(ax, 6.0, 6.94, 6.0, 5.81, color=RED, lw=2.2, shrink=2)
    osfig.tx(ax, 6.0, 6.5, "★ 陷入引发：用户态 → 核心态（硬件完成）", fs=9.8, bold=True, color=RED, bg="white")
    osfig.arrow(ax, 6.0, 5.09, 6.0, 4.86, color=GRAY, lw=1.8, shrink=2)
    osfig.arrow(ax, 6.0, 4.14, 6.0, 3.91, color=GRAY, lw=1.8, shrink=2)
    osfig.arrow(ax, 6.0, 3.19, 6.0, 2.11, color=GREEN, lw=2.2, shrink=2)
    osfig.tx(ax, 6.0, 2.65, "★ 中断返回：核心态 → 用户态", fs=9.8, bold=True, color=GREEN, bg="white")
    osfig.tx(ax, 11.0, 7.3, "陷入指令本身\n是非特权指令，\n在用户态执行！", fs=8.8, color=PINK, ha="left")
    osfig.tx(ax, 11.0, 4.5, "凡与资源有关的\n操作，都必须\n进入核心态完成", fs=8.8, color=RED, ha="left")
    osfig.tx(ax, 6.0, 0.4, "记忆：传参 → 陷入 → 核心态执行 → 返回；系统调用号决定调用哪个内核例程",
             fs=10, color=GRAY)
    osfig.save(fig, F("ch1-12_syscall_flow.png"))


# ================================================================
# ch1-13 操作系统体系结构对比
# ================================================================
def fig13():
    fig, ax = osfig.new_fig(14.5, 9, (0, 14.5), (0, 9))
    osfig.title(ax, "五种操作系统内核体系结构对比",
                sub="大内核 / 微内核 / 分层 / 模块化 / 外核 —— 微内核的优缺点是高频考点")
    GRAYE = "#9CA3AF"

    def panel(x, y, name, ec):
        cx = x + 2.15
        osfig.rbox(ax, x, y, 4.3, 3.0, fc="white", ec=GRAYE, lw=1.6, z=1)
        osfig.tx(ax, cx, y + 2.72, name, fs=12.5, bold=True, color=ec)
        return cx

    def std_box(cx, cy, w, h, fc, ec, lw=1.6):
        osfig.rbox(ax, cx - w / 2, cy - h / 2, w, h, fc=fc, ec=ec, lw=lw, z=2)

    # ---- P1 大内核（row1 left）
    cx = panel(0.5, 4.5, "大内核（单内核）", BLUE)
    std_box(cx, 6.8, 3.5, 0.4, GRAY_L, GRAY)
    osfig.tx(ax, cx, 6.8, "用户程序", fs=9, color=INK)
    std_box(cx, 6.0, 3.5, 0.8, BLUE_L, BLUE)
    osfig.tx(ax, cx, 6.2, "操作系统内核（全部功能）", fs=9.5, bold=True, color=BLUE)
    osfig.tx(ax, cx, 5.8, "进程·内存·文件·设备·驱动 全在核心态", fs=7.8, color=GRAY)
    std_box(cx, 5.25, 3.5, 0.4, GRAY_L, GRAY)
    osfig.tx(ax, cx, 5.25, "硬件", fs=9, color=INK)
    osfig.tx(ax, cx, 4.78, "优：性能高（内部直接调用）\n缺：耦合度极高，一处崩溃全崩", fs=8.3, color=GRAY)

    # ---- P2 微内核（row1 middle）
    cx = panel(5.1, 4.5, "微内核", RED)
    std_box(cx, 6.7, 3.5, 0.7, RED_L, RED)
    osfig.tx(ax, cx, 6.88, "用户程序 ＋ 各类服务进程", fs=9, bold=True, color=INK)
    osfig.tx(ax, cx, 6.55, "（文件服务、进程服务等 —— 都在用户态）", fs=7.8, color=GRAY)
    std_box(cx, 5.85, 3.5, 0.55, RED_L, RED)
    osfig.tx(ax, cx, 5.85, "微内核：只留中断·时钟·原语等最基本功能", fs=8.2, bold=True, color=RED)
    std_box(cx, 5.25, 3.5, 0.4, GRAY_L, GRAY)
    osfig.tx(ax, cx, 5.25, "硬件", fs=9, color=INK)
    osfig.tx(ax, cx, 4.78, "优：可靠性稳定性高、便于维护扩展\n缺：频繁切换核心态 → 性能开销大", fs=8.3, color=GRAY)

    # ---- P3 分层（row1 right）
    cx = panel(9.7, 4.5, "分层结构", GREEN)
    for (yy, txt) in [(6.85, "用户程序"), (6.35, "层 n：只调用低一层提供的功能"),
                      (5.85, "层 2 / 层 1（最底层贴近硬件）"), (5.35, "硬件")]:
        std_box(cx, yy, 3.5, 0.4, GREEN_L, GREEN)
        osfig.tx(ax, cx, yy, txt, fs=8.8, color=INK)
    osfig.tx(ax, cx, 4.78, "优：层间解耦、易调试维护\n缺：通信开销大、层次难界定", fs=8.3, color=GRAY)

    # ---- P4 模块化（row2 left）
    cx = panel(0.5, 0.7, "模块化结构", TEAL)
    std_box(cx, 3.05, 3.5, 0.4, TEAL_L, TEAL)
    osfig.tx(ax, cx, 3.05, "主模块（统一调度接口）", fs=9, color=INK)
    for (mx, txt) in [(cx - 1.3, "调度"), (cx - 0.4, "内存"), (cx + 0.5, "文件"), (cx + 1.4, "驱动")]:
        std_box(mx, 2.6, 0.8, 0.45, TEAL_L, TEAL)
        osfig.tx(ax, mx, 2.6, txt, fs=8.5, color=INK)
    std_box(cx, 2.1, 3.5, 0.4, GRAY_L, GRAY)
    osfig.tx(ax, cx, 2.1, "硬件", fs=9, color=INK)
    osfig.tx(ax, cx, 1.3, "优：高内聚低耦合、易扩展维护\n缺：模块间接口设计要求高", fs=8.3, color=GRAY)

    # ---- P5 外核（row2 middle）
    cx = panel(5.1, 0.7, "外核（Exokernel）", AMBER)
    std_box(cx, 3.05, 3.5, 0.45, AMBER_L, AMBER)
    osfig.tx(ax, cx, 3.05, "应用程序 ＋ 定制库（libOS）", fs=8.8, bold=True, color=INK)
    std_box(cx, 2.5, 3.5, 0.5, AMBER_L, AMBER)
    osfig.tx(ax, cx, 2.5, "外核：只做资源分配与多路复用", fs=8.5, bold=True, color=AMBER)
    std_box(cx, 1.9, 3.5, 0.4, GRAY_L, GRAY)
    osfig.tx(ax, cx, 1.9, "硬件", fs=9, color=INK)
    osfig.tx(ax, cx, 1.3, "优：应用可“定制”使用硬件\n缺：全局协调弱、实现复杂", fs=8.3, color=GRAY)

    # ---- P6 典型系统（row2 right）
    cx = panel(9.7, 0.7, "典型系统 & 必背考点", INK)
    lines = ["• 大内核：Linux、UNIX", "• 微内核：Minix、QNX、seL4",
             "• 分层结构：THE 系统", "• 模块化：Solaris", "• 外核：MIT Exokernel"]
    for i, s in enumerate(lines):
        osfig.tx(ax, 10.05, 3.05 - 0.37 * i, s, fs=8.8, color=INK, ha="left")
    osfig.tx(ax, cx, 0.98, "微内核必考：把非基本功能\n移到用户态服务进程；缺点\n＝频繁切换、性能开销大",
             fs=8.5, bold=True, color=RED)
    osfig.save(fig, F("ch1-13_kernel_architectures.png"))


# ================================================================
# ch1-14 操作系统引导流程
# ================================================================
def fig14():
    fig, ax = osfig.new_fig(13.6, 9.5, (0, 13.6), (0, 9.5))
    osfig.title(ax, "操作系统的引导：从按下电源到 OS 接管整机",
                sub="BIOS 自检 → 读 MBR → 读 PBR → 启动管理器 → 装入内核")
    flow = [
        ("① CPU 加电 → CS:IP 指向 ROM 的 FFFF0H", GRAY, GRAY_L),
        ("② 执行 ROM 中的 BIOS 程序：硬件自检（POST）", GRAY, GRAY_L),
        ("③ BIOS 读磁盘 0 号扇区（MBR）到内存执行", AMBER, AMBER_L),
        ("④ MBR 中的磁盘引导程序找活动分区，读 PBR", AMBER, AMBER_L),
        ("⑤ PBR 中的分区引导程序加载启动管理器", AMBER, AMBER_L),
        ("⑥ 启动管理器把 OS 内核装入内存", BLUE, BLUE_L),
        ("⑦ CPU 执行内核初始化 → OS 接管整机", BLUE, BLUE_L),
    ]
    ys = [8.0, 7.05, 6.1, 5.15, 4.2, 3.25, 2.3]
    for (text, ec, fc), y in zip(flow, ys):
        osfig.rbox(ax, 0.9, y - 0.375, 5.4, 0.75, fc=fc, ec=ec, lw=2.0)
        osfig.tx(ax, 3.6, y, text, fs=10.2, color=INK)
    for i in range(len(ys) - 1):
        osfig.arrow(ax, 3.6, ys[i] - 0.375, 3.6, ys[i + 1] + 0.375, color=GRAY, lw=1.8, shrink=2)
    # 右侧：ROM + 磁盘
    osfig.rbox(ax, 9.5, 7.6, 3.4, 0.9, fc=GRAY_L, ec=GRAY, lw=2.0)
    osfig.tx(ax, 11.2, 8.2, "ROM：BIOS 程序", fs=11, bold=True, color=INK)
    osfig.tx(ax, 11.2, 7.85, "出厂固化、不可修改", fs=8.5, color=GRAY)
    osfig.rbox(ax, 7.9, 2.1, 5.3, 4.9, fc="white", ec=INK, lw=1.8, z=1)
    osfig.tx(ax, 8.6, 6.75, "磁盘（硬盘）", fs=11.5, bold=True, color=INK)
    osfig.rbox(ax, 8.15, 5.75, 4.8, 0.7, fc=AMBER_L, ec=AMBER, lw=1.8, z=2)
    osfig.tx(ax, 10.55, 6.1, "③ MBR＝磁盘引导程序＋硬盘分区表", fs=9, color=INK)
    osfig.tx(ax, 10.55, 5.82, "（位于 0 号扇区）", fs=7.8, color=GRAY)
    osfig.rbox(ax, 8.05, 2.2, 5.0, 3.35, fc="white", ec=GRAY, lw=1.4, dashed=True, z=1)
    osfig.tx(ax, 12.85, 5.38, "活动分区（如 C 盘）", fs=8.5, color=GRAY, ha="right")
    osfig.rbox(ax, 8.15, 4.5, 4.8, 0.7, fc=TEAL_L, ec=TEAL, lw=1.8, z=2)
    osfig.tx(ax, 10.55, 4.85, "④ PBR＝活动分区第 1 扇区的引导程序", fs=9, color=INK)
    osfig.rbox(ax, 8.15, 3.55, 4.8, 0.7, fc=BLUE_L, ec=BLUE, lw=1.8, z=2)
    osfig.tx(ax, 10.55, 3.9, "⑤ 启动管理器（bootmgr / GRUB）", fs=9, color=INK)
    osfig.rbox(ax, 8.15, 2.4, 4.8, 0.7, fc=GREEN_L, ec=GREEN, lw=1.8, z=2)
    osfig.tx(ax, 10.55, 2.75, "⑥⑦ OS 内核文件 → 装入内存执行", fs=9, color=INK)
    osfig.arrow(ax, 9.9, 7.55, 9.9, 6.52, color=GRAY, lw=1.8, shrink=2, text="③ 读取", fs=9)
    osfig.arrow(ax, 11.2, 5.72, 11.2, 5.25, color=GRAY, lw=1.8, shrink=2)
    osfig.arrow(ax, 11.2, 4.47, 11.2, 4.28, color=GRAY, lw=1.8, shrink=2)
    osfig.arrow(ax, 11.2, 3.52, 11.2, 3.13, color=GRAY, lw=1.8, shrink=2)
    osfig.tx(ax, 6.5, 1.1, "一句话：BIOS 自检 → 读 MBR → 读 PBR → 启动管理器 → 内核", fs=10.5, bold=True, color=INK)
    osfig.tx(ax, 6.5, 0.55, "考点：MBR 在磁盘 0 号扇区（含分区表）；PBR 在活动分区第一扇区；OS 最终被加载到 RAM（2015 真题）",
             fs=9.5, color=GRAY)
    osfig.save(fig, F("ch1-14_boot_process.png"))


# ================================================================
# ch1-15 两类虚拟机
# ================================================================
def fig15():
    fig, ax = osfig.new_fig(13, 7.8, (0, 13), (0, 7.8))
    osfig.title(ax, "两类虚拟机管理程序（Hypervisor）",
                sub="第一类直接跑在硬件上（裸机型）；第二类寄居在宿主 OS 上（寄居型）")
    # 第一类
    osfig.rbox(ax, 0.5, 0.7, 6.0, 5.8, fc="white", ec=BLUE, lw=1.8)
    osfig.tx(ax, 3.5, 6.1, "第一类：裸机型（Type 1）", fs=13, bold=True, color=BLUE)
    for cxv, name in [(2.35, "虚拟机 1"), (4.65, "虚拟机 2")]:
        osfig.rbox(ax, cxv - 1.05, 4.325, 2.1, 1.05, fc=BLUE_L, ec=BLUE, lw=1.8)
        osfig.tx(ax, cxv, 5.08, name, fs=10.5, bold=True, color=BLUE)
        osfig.tx(ax, cxv, 4.62, "客户OS＋应用", fs=8.8, color=INK)
    osfig.rbox(ax, 1.2, 3.4, 4.6, 0.85, fc=RED_L, ec=RED, lw=2.0)
    osfig.tx(ax, 3.5, 4.0, "虚拟机管理程序 Hypervisor", fs=10.5, bold=True, color=RED)
    osfig.tx(ax, 3.5, 3.66, "直接运行在硬件之上", fs=8.8, color=INK)
    osfig.rbox(ax, 1.2, 2.3, 4.6, 0.7, fc=GRAY_L, ec=GRAY, lw=1.8, text="硬件（物理服务器）",
               fs=10.5, bold=True)
    osfig.rbox(ax, 1.0, 1.35, 5.0, 0.75, fc=BLUE_L, ec=BLUE, lw=1.6)
    osfig.tx(ax, 3.5, 1.87, "典型：VMware ESXi、Xen、Hyper-V", fs=9.5, bold=True, color=BLUE)
    osfig.tx(ax, 3.5, 1.56, "多用于数据中心 / 服务器", fs=8.5, color=GRAY)
    osfig.tx(ax, 3.5, 0.98, "性能高、隔离性强、安全性好", fs=9.5, color=BLUE)
    # 第二类
    osfig.rbox(ax, 7.0, 0.7, 6.0, 5.8, fc="white", ec=GREEN, lw=1.8)
    osfig.tx(ax, 10.0, 6.1, "第二类：寄居型（Type 2）", fs=13, bold=True, color=GREEN)
    for cxv, name in [(8.85, "虚拟机 1"), (11.15, "虚拟机 2")]:
        osfig.rbox(ax, cxv - 1.05, 4.425, 2.1, 1.05, fc=GREEN_L, ec=GREEN, lw=1.8)
        osfig.tx(ax, cxv, 5.18, name, fs=10.5, bold=True, color=GREEN)
        osfig.tx(ax, cxv, 4.72, "客户OS＋应用", fs=8.8, color=INK)
    osfig.rbox(ax, 7.7, 3.85, 4.6, 0.8, fc=AMBER_L, ec=AMBER, lw=2.0)
    osfig.tx(ax, 10.0, 4.4, "Hypervisor（VMM）", fs=10, bold=True, color=AMBER)
    osfig.tx(ax, 10.0, 4.08, "作为宿主 OS 上的一个程序/模块", fs=8.3, color=INK)
    osfig.rbox(ax, 7.7, 2.95, 4.6, 0.7, fc=PURPLE_L, ec=PURPLE, lw=1.8, text="宿主操作系统（Windows / macOS…）",
               fs=9.5, bold=True)
    osfig.rbox(ax, 7.7, 2.05, 4.6, 0.7, fc=GRAY_L, ec=GRAY, lw=1.8, text="硬件", fs=10.5, bold=True)
    osfig.rbox(ax, 7.7, 1.28, 4.6, 0.7, fc=GREEN_L, ec=GREEN, lw=1.6)
    osfig.tx(ax, 10.0, 1.8, "典型：VMware Workstation、VirtualBox", fs=9, bold=True, color=GREEN)
    osfig.tx(ax, 10.0, 1.5, "个人电脑上的日常虚拟化", fs=8.5, color=GRAY)
    osfig.tx(ax, 10.0, 0.98, "安装使用方便；多一层转发 → 性能略低", fs=9.5, color=GREEN)
    osfig.tx(ax, 6.5, 0.3, "实现方式（了解）：陷入-模拟、二进制翻译、硬件辅助 —— 考点级别：低频选择题",
             fs=10, color=GRAY)
    osfig.save(fig, F("ch1-15_vm_types.png"))


if __name__ == "__main__":
    for fn in [fig00, fig01, fig02, fig03, fig04, fig05, fig06, fig07,
               fig08, fig09, fig10, fig11, fig12, fig13, fig14, fig15]:
        fn()
    print("全部插图生成完毕。")
