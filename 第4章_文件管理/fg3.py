# -*- coding: utf-8 -*-
"""第4章 插图 第三部分：ch4-13 ~ ch4-17"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import matplotlib
import osfig
from osfig import (new_fig, rbox, box, rect, diamond, ellipse, circle, arrow,
                   line, tx, title, save, INK, BLUE, BLUE_L, GREEN, GREEN_L,
                   AMBER, AMBER_L, RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L,
                   GRAY, GRAY_L, PINK, PINK_L)
import matplotlib.pyplot as plt

FDIR = "/Users/levi/IdeaProjects/操作系统/第4章_文件管理/figures/"
osfig.setup()


def f13():
    fig, ax = new_fig(16, 11.8, (0, 16), (0, 11.8))
    title(ax, "成组链接法：用'空闲盘块号栈 + 跨块链'管理海量空闲块",
          "核心思想：每 100 个空闲块号为一组；每组最后一个块（连接块）的内容 = 下一组的 100 个块号", y=11.35)
    # ---------- 主图：栈 + 链
    tx(ax, 2.0, 10.8, "① 内存：空闲盘块号栈 S", fs=12.5, bold=True, color=BLUE)
    rbox(ax, 0.55, 6.3, 3.1, 4.0, "", fc=BLUE_L, ec=BLUE)
    tx(ax, 3.75, 10.08, "S.top = 100", fs=10.5, bold=True, color=RED, bg="white")
    stack_rows = [("S[99]=1099", "栈顶，先分配"), ("S[98]=1098", ""),
                  ("S[97]=1097", ""), ("......", "（中间 90 余块）"),
                  ("S[1]=1001", ""), ("S[0]=1000", "连接块：内容=下一组")]
    y = 9.6
    for nm, note in stack_rows:
        if nm == "......":
            rect(ax, 0.85, y - 0.42, 2.5, 0.72, "......", fc=GRAY_L, ec=GRAY, fs=9)
        else:
            fc = AMBER_L if nm.startswith("S[0]") else BLUE_L
            ec = AMBER if nm.startswith("S[0]") else BLUE
            rect(ax, 0.85, y, 2.5, 0.42, nm, fc=fc, ec=ec, fs=8.8)
            if note:
                tx(ax, 4.3, y + 0.18, note, fs=8.0,
                   color=RED if note.startswith("连接") else GRAY, ha="left")
        y -= 0.62
    arrow(ax, 4.9, 9.4, 4.9, 8.9, color=BLUE, lw=1.8, dx=0.1,
          text="分配：从栈顶弹出", fs=8.6)
    # ---- 盘块链
    rbox(ax, 6.4, 7.3, 3.9, 2.1, "", fc=AMBER_L, ec=AMBER)
    tx(ax, 8.35, 9.05, "盘块 1000（连接块）", fs=10.5, bold=True, color=AMBER)
    tx(ax, 8.35, 8.25, "内容 = 第 2 组块号：\n1100, 1101, ......, 1199", fs=9.6)
    arrow(ax, 3.68, 8.35, 6.35, 8.2, color=AMBER, lw=1.8, both=True,
          text="top=1 时：内容读入栈", fs=8.2, dy=0.85)
    rbox(ax, 10.9, 7.3, 4.2, 2.1, "", fc=PINK_L, ec=PINK)
    tx(ax, 13.0, 9.05, "盘块 1100（连接块）", fs=10.5, bold=True, color=PINK)
    tx(ax, 13.0, 8.25, "内容 = 第 3 组块号：\n1200, 1201, ......, 1299", fs=9.6)
    arrow(ax, 10.35, 8.35, 10.85, 8.35, color=PINK, lw=1.8)
    rbox(ax, 6.4, 6.3, 8.7, 0.8, "", fc=TEAL_L, ec=TEAL, dashed=True)
    tx(ax, 10.75, 6.7, "第 4、5 组……依此类推（1200 中存 1300~1399……）；最后一组的末块内容 = 0，链到此结束",
       fs=9.2)
    tx(ax, 2.0, 6.05, "第 1 组（栈中 100 块：1000~1099）", fs=9.6, bold=True, color=BLUE)
    # ---------- 两种特殊情况
    rbox(ax, 0.4, 3.95, 7.0, 1.95, fc=GREEN_L, ec=GREEN)
    tx(ax, 3.9, 5.6, "情景① 分配：栈中只剩 1 块（top = 1）", fs=11.5, bold=True, color=GREEN)
    tx(ax, 3.9, 4.75,
       "① 先把该块（如 1000）中记录的下一组块号\n    （1100~1199）全部读入栈 → 栈满 100 块\n② 再把块 1000 本身分配出去（数据已取走）", fs=9.8)
    rbox(ax, 8.2, 3.95, 7.4, 1.95, fc=PURPLE_L, ec=PURPLE)
    tx(ax, 11.9, 5.6, "情景② 回收：栈已满（top = 100）", fs=11.5, bold=True, color=PURPLE)
    tx(ax, 11.9, 4.75,
       "① 把栈中 100 个块号整体写入回收块 R 的内容区\n② 栈中只留下 R 一个块号（top = 1）\nR 成为【新一组】的连接块，其余 99 块'藏'在 R 中", fs=9.8)
    # ---------- 例题演算
    rbox(ax, 0.4, 0.5, 15.2, 3.2, fc=BLUE_L, ec=BLUE)
    tx(ax, 8.0, 3.4, "例题：初始栈 S[0]=1000,…,S[99]=1099（top=100）→ 分配 3 块 → 回收 2 块（回收块 2000、2001），画栈状态变化",
       fs=10.5, bold=True, color=BLUE)
    states = [
        ("初始状态（top=100）", [("S[0]", "1000"), ("S[1]", "1001"), ("......", "..."), ("S[97]", "1097"),
                  ("S[98]", "1098"), ("S[99]", "1099")], None),
        ("分配 3 块后", [("S[0]", "1000"), ("S[1]", "1001"), ("......", "..."), ("S[95]", "1095"),
                     ("S[96]", "1096")], "top = 97（弹出 1099/1098/1097）"),
        ("再回收 2 块后", [("S[0]", "1000"), ("S[1]", "1001"), ("S[96]", "1096"),
                       ("S[97]", "2000"), ("S[98]", "2001")], "top = 99（压入 2000/2001）"),
    ]
    for i, (name, items, top) in enumerate(states):
        x = 0.9 + i * 4.95
        tx(ax, x + 1.5, 2.9, (name + ("" if top is None else "  " + top)), fs=10.5, bold=True, color=BLUE)
        for j, (k, v) in enumerate(items):
            rect(ax, x, 2.35 - j * 0.28, 2.85, 0.22, k + " = " + v, fc=GRAY_L, ec=GRAY,
                 fs=7.0, lw=0.6)
    save(fig, FDIR + "ch4-13_grouped_linking.png")



def f14():
    fig, ax = new_fig(15, 9.2, (0, 15), (0, 9.2))
    title(ax, "磁盘的物理结构：盘面 · 磁道 · 扇区 · 柱面",
          "磁盘地址 = (柱面号 : 盘面号 : 扇区号)；读盘三步：寻道 → 旋转定位 → 读写传输", y=8.75)
    import math
    import matplotlib.patches as mpatches
    # ---------- 左：俯视图
    tx(ax, 3.3, 7.95, "俯视图（一个盘面）", fs=12, bold=True)
    cx, cy, r0, r1, r2 = 3.3, 5.45, 0.95, 1.8, 2.35
    ax.add_patch(mpatches.Circle((cx, cy), r2, facecolor="white", edgecolor="none", zorder=1))
    for r in [r0, r1, r2]:
        circle(ax, cx, cy, r, fc="none", ec=GRAY, lw=1.4, z=2)
    for k in range(8):
        ang = k * math.pi / 4
        line(ax, cx + r0 * math.cos(ang), cy + r0 * math.sin(ang),
             cx + r2 * math.cos(ang), cy + r2 * math.sin(ang), color=GRAY, lw=1.0, z=3)
    a1, a2 = 0, math.pi * 3 / 2
    p1 = [(cx + r0 * math.cos(a1), cy + r0 * math.sin(a1)),
          (cx + r2 * math.cos(a1), cy + r2 * math.sin(a1)),
          (cx + r2 * math.cos(a2), cy + r2 * math.sin(a2)),
          (cx + r0 * math.cos(a2), cy + r0 * math.sin(a2))]
    ax.add_patch(mpatches.Polygon(p1, closed=True, facecolor=AMBER_L, edgecolor=AMBER, lw=1.3, zorder=4))
    tx(ax, 6.05, 6.35, "扇区（最小寻址单位）", fs=10, bold=True, color=AMBER, ha="left")
    tx(ax, 6.05, 5.5,
       "磁道：同一盘面上圆周的一圈\n相邻磁道之间留有空隙；\n数据只存在扇区中\n（橙色扇形 = 1 个扇区）", fs=9.2, ha="left")
    # ---------- 中：侧视图
    tx(ax, 9.05, 7.95, "侧视图（盘组与磁头）", fs=12, bold=True)
    rect(ax, 7.7, 4.15, 2.9, 3.3, "", fc=GRAY_L, ec=GRAY)
    for i in range(4):
        y = 7.15 - i * 0.62
        line(ax, 7.7, y, 10.6, y, color=GRAY, lw=1.6)
        rbox(ax, 7.9 + (i % 2) * 0.3, y + 0.1, 0.55, 0.2, "", fc=GRAY, ec=GRAY, lw=1.0)
    line(ax, 9.15, 4.15, 9.15, 7.35, color=INK, lw=1.4)
    tx(ax, 9.15, 3.9, "主轴", fs=8.4)
    tx(ax, 9.7, 4.55, "磁头：每面一个，同步移动", fs=8.6, ha="left", bg="white")
    arrow(ax, 8.2, 4.15, 8.2, 4.9, color=PURPLE, lw=1.5, text="磁头臂", fs=8.4)
    tx(ax, 11.15, 7.5, "柱面 C 的示意：3 个盘面上\n半径相同的 3 条磁道构成\n同一个【柱面】", fs=9.2, ha="left")
    for k, yy in enumerate([7.05, 6.43, 5.81]):
        rbox(ax, 11.3, yy, 0.45, 0.26, "", fc=GRAY_L, ec=PURPLE, lw=1.1)
    line(ax, 11.7, 5.6, 11.7, 7.3, color=PURPLE, lw=0.8, ls="--")
    tx(ax, 11.15, 4.75, "同一柱面 = 所有盘面上半径相同的磁道集合；\n移动一次磁头臂即可访问同一柱面的所有盘面。\n正是这个原因，磁盘地址中【柱面号排在最前】。",
       fs=8.8, color=RED, ha="left")
    # ---------- 右：地址
    rbox(ax, 12.95, 5.6, 1.95, 2.4, "", fc=AMBER_L, ec=AMBER)
    tx(ax, 13.93, 7.6, "磁盘地址", fs=11, bold=True, color=AMBER)
    tx(ax, 13.93, 6.75, "(柱面号:\n盘面号:\n扇区号)", fs=9.6)
    tx(ax, 13.93, 5.85, "例如：(5:2:7)", fs=9.0)
    # ---------- 下：三步
    tx(ax, 7.5, 3.35, "读盘三步（理解磁盘时间的基础）", fs=12.5, bold=True)
    steps = [
        ("① 寻道", "磁头臂在盘面上径向移动\n把磁头移动到目标柱面的磁道上\n时间 = 寻道时间 Ts（最慢）", BLUE),
        ("② 旋转延迟", "盘片匀速旋转，等待目标扇区\n转到磁头正下方\n时间 = 旋转延迟 Tr（平均＝半圈）", GREEN),
        ("③ 读写传输", "磁头与经过其下的扇区做读写\n数据经总线传向内存\n时间 = 传输时间 Tt", AMBER),
    ]
    for i, (h, d, cc) in enumerate(steps):
        x = 0.4 + i * 5.0
        rbox(ax, x, 0.75, 4.6, 2.35, fc="white", ec=cc, lw=1.8)
        tx(ax, x + 2.3, 2.75, h, fs=13, bold=True, color=cc)
        tx(ax, x + 2.3, 1.9, d, fs=9.6)
    tx(ax, 7.5, 0.35,
       "容量公式：磁盘容量 = 柱面数 × 盘面数 × 每道扇区数 × 扇区大小；CHS 地址用（柱面号, 盘面号, 扇区号）唯一确定一个扇区。",
       fs=9.6)
    save(fig, FDIR + "ch4-14_disk_structure.png")


def f15():
    fig, axs = plt.subplots(2, 3, figsize=(17.5, 9.6))
    osfig.setup()
    spec = [
        ("FCFS：先来先服务", [53, 98, 183, 37, 122, 14, 124, 65, 67], "总寻道 = 640", BLUE),
        ("SSTF：最短寻道时间优先", [53, 65, 67, 37, 14, 98, 122, 124, 183], "总寻道 = 236", GREEN),
        ("SCAN（电梯）：扫到 199 再折返", [53, 65, 67, 98, 122, 124, 183, 199, 37, 14], "总寻道 = 331", TEAL),
        ("LOOK：到最远请求即折返", [53, 65, 67, 98, 122, 124, 183, 37, 14], "总寻道 = 299", PURPLE),
        ("C-SCAN：单向扫到 199 跳回 0", [53, 65, 67, 98, 122, 124, 183, 199, 14, 37], "总寻道 = 382", AMBER),
        ("C-LOOK：单向扫到 183 跳回 14", [53, 65, 67, 98, 122, 124, 183, 14, 37], "总寻道 = 322", PINK),
    ]
    for i, (name, pts, total, cc) in enumerate(spec):
        axi = axs[i // 3][i % 3]
        axi.set_xlim(-8, 210)
        axi.set_ylim(-0.7, len(pts) - 0.1)
        axi.set_xticks([0, 50, 100, 150, 199])
        axi.tick_params(labelsize=8, colors=GRAY)
        axi.set_ylabel("服务顺序", fontsize=8, color=GRAY)
        axi.grid(True, color="#E5E7EB", lw=0.7)
        axi.set_title(name + "\n" + total, fontsize=11, color=INK, fontweight="bold")
        xs = [p for p in pts]
        ys = list(range(len(pts)))
        # 跳回段（虚线灰色）
        for k in range(len(pts) - 1):
            gap = abs(xs[k + 1] - xs[k])
            dashed = (name.startswith("C-SCAN") and xs[k] >= 199 and xs[k + 1] <= 14) or \
                     (name.startswith("C-LOOK") and xs[k] >= 183 and xs[k + 1] <= 14)
            if dashed:
                axi.plot([xs[k], xs[k + 1]], [ys[k], ys[k + 1]], color=GRAY,
                         ls="--", lw=1.4, zorder=1)
            else:
                axi.plot([xs[k], xs[k + 1]], [ys[k], ys[k + 1]], color=cc, lw=2.2, zorder=2)
            if not dashed:
                mx, my = (xs[k] + xs[k + 1]) / 2, (ys[k] + ys[k + 1]) / 2
                axi.text(mx, my + 0.12, str(gap), fontsize=9, color=RED,
                         ha="center", va="bottom", fontweight="bold",
                         bbox=dict(facecolor="white", edgecolor="none", pad=0.6, alpha=0.9))
        # 起点标记
        axi.plot(xs[0], ys[0], "o", color=BLUE, ms=7, zorder=5)
        axi.text(xs[0], ys[0] + 0.22, "起点53", fontsize=8, color=BLUE, ha="center", fontweight="bold")
        axi.plot(xs[-1], ys[-1], "s", color=RED, ms=6, zorder=5)
        axi.text(xs[-1], ys[-1] - 0.28, "终点%d" % xs[-1], fontsize=8, color=RED, ha="center")
        for p, yy in zip(xs, ys):
            axi.text(p, yy - 0.18, str(p), fontsize=7, color=GRAY, ha="center", va="top")
    fig.tight_layout()
    save(fig, FDIR + "ch4-15_disk_scheduling.png")


def f16():
    fig, ax = new_fig(15, 9.6, (0, 15), (0, 9.6))
    title(ax, "磁盘读写时间：寻道 + 旋转延迟 + 传输",
          "平均访问时间 = 寻道时间 + 平均旋转延迟 + 传输时间；旋转延迟平均 ≈ 转过半圈", y=9.15)
    # 时间条
    tx(ax, 7.5, 8.35, "① 一次磁盘访问的时间构成（时间条示意，宽度不按比例）", fs=12, bold=True)
    segs = [("寻道时间 Ts = 6 ms", 5.4, BLUE, BLUE_L),
            ("旋转延迟 Tr = 5 ms", 5.0, GREEN, GREEN_L),
            ("传输时间 Tt = 0.1 ms", 3.2, AMBER, AMBER_L)]
    x = 0.6
    for txt, w, ec, fc in segs:
        rect(ax, x, 7.35, w, 0.8, "", fc=fc, ec=ec, lw=1.4)
        tx(ax, x + w / 2, 7.75, txt, fs=11, bold=True)
        x += w + 0.18
    tx(ax, 7.5, 6.72, "→ 平均访问时间 = Ts + Tr + Tt = 6 + 5 + 0.1 = 11.1 ms",
       fs=11, bold=True, color=RED)
    tx(ax, 7.5, 7.02, "寻道：磁头移动到目标磁道（最耗时）｜旋转延迟：等目标扇区转到磁头下（平均半圈）｜传输：读出一扇区数据",
       fs=9.2)
    # 转盘示意
    tx(ax, 7.5, 6.05, "② 为什么平均旋转延迟 = 转半圈？", fs=12, bold=True)
    import math
    cx, cy, r = 3.2, 4.55, 2.0
    circle(ax, cx, cy, r, fc="none", ec=GRAY, lw=1.3)
    for k in range(12):
        ang = k * math.pi / 6
        line(ax, cx, cy, cx + r * math.cos(ang), cy + r * math.sin(ang), color=GRAY, lw=0.8)
    # 磁头尖端（左侧）
    arrow(ax, 0.75, cy, 1.15, cy, color=RED, lw=2.6, text="磁头（固定不转）", fs=9.0, dy=-0.3)
    # 目标扇区（当前在正下方，要转到磁头下需转 1/4~3/4 圈）
    import matplotlib.patches as mpatches
    a1, a2 = -math.pi / 2, -math.pi / 2 + math.pi / 3
    p1 = [(cx, cy)]
    for k in range(6):
        a = a1 + (a2 - a1) * k / 5
        p1.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    ax.add_patch(mpatches.Polygon(p1, facecolor=AMBER_L, edgecolor=AMBER, lw=1.0, zorder=2))
    tx(ax, cx + 0.75, cy - 1.15, "目标扇区", fs=9.2, bold=True, color=AMBER)
    arc_txt = "平均角度差 180° → 平均转半圈"
    # 顶部扫过的角度
    tx(ax, 7.1, 5.5, "扇区（目标）到达磁头下方的角度\n0° ~ 360° 等概率 → 平均值 = 180°\n→ 平均旋转延迟 = 半圈用时", fs=9.4, ha="left")
    tx(ax, 7.1, 4.6,
       "公式：平均旋转延迟 Tr = 1 / (2 × 转速)\n例：6000 转/分 = 100 转/秒 → 每圈 10 ms\n→ Tr = 10 / 2 = 5 ms", fs=9.4, ha="left", color=RED)
    # 例题
    tx(ax, 7.5, 3.55, "③ 例题：一块数据的平均读写时间（逐步计算）", fs=12, bold=True)
    rbox(ax, 0.4, 0.75, 14.2, 2.4, fc=GRAY_L, ec=GRAY)
    tx(ax, 7.5, 2.85, "已知：磁盘转速 6000 r/min；磁头移动跨越的平均寻道时间 6 ms；每磁道 100 个扇区，每扇区 512 B（一次读写 1 个扇区）",
       fs=10.2, bold=True)
    tx(ax, 7.5, 2.0,
       "解：\n① 转一圈的时间 = 60 s / 6000 = 0.01 s = 10 ms\n② 平均旋转延迟 Tr = 10 ms / 2 = 5 ms\n③ 传输一个扇区的时间 Tt = 10 ms / 100 = 0.1 ms（每转读写一整道 100 扇区）\n④ 平均访问时间 = Ts + Tr + Tt = 6 + 5 + 0.1 = 11.1 ms",
       fs=9.8, ha="left")
    save(fig, FDIR + "ch4-16_disk_time.png")


def f17():
    fig, ax = new_fig(15, 8.6, (0, 15), (0, 8.6))
    title(ax, "RAID：磁盘阵列（Redundant Array of Independent Disks）",
          "把多块磁盘组织成一个阵列并行工作：分条提高性能，冗余提高可靠性", y=8.15)
    panels = [
        ("RAID 0：条带化（无冗余）", 0.4, BLUE, BLUE_L,
         [["A0", "B0", "C0", "D0"], ["A1", "B1", "C1", "D1"], ["A2", "B2", "C2", "D2"]],
         "数据分条交错存放：并行读写，速度最快、容量利用率 100%；\n但任何一块盘坏了 → 数据全丢（无容错）"),
        ("RAID 1：镜 像", 5.6, GREEN, GREEN_L,
         [["A0", "A0", "B0", "B0"], ["A1", "A1", "B1", "B1"], ["A2", "A2", "B2", "B2"]],
         "每份数据同时写两块盘：可靠性最高；读可并行、更快；\n写要双写较慢；容量利用率只有 50%（代价大）"),
        ("RAID 5：分布式奇偶校验", 10.8, AMBER, AMBER_L,
         [["P0", "A0", "B0", "C0"], ["C1", "P1", "A1", "B1"], ["B2", "C2", "P2", "A2"]],
         "校验块 P 轮流分布在各盘：读性能近 RAID 0；写需计算校验；\n坏一块盘可由其余盘数据 + 校验恢复；利用率 (N-1)/N"),
    ]
    for name, x0, cc, cl, rows, note in panels:
        rbox(ax, x0, 3.0, 4.8, 4.6 if len(name) < 12 else 4.6, fc=cl, ec=cc)
        tx(ax, x0 + 2.4, 7.25, name, fs=11.5, bold=True, color=cc)
        for i, row in enumerate(rows):
            for j, v in enumerate(row):
                rect(ax, x0 + 0.35 + j * 1.12, 5.45 - i * 0.6, 1.0, 0.52, v,
                     fc=RED_L if v.startswith("P") else ("white" if i % 2 else cl),
                     ec=cc, fs=9.6, bold=(v.startswith("P")))
        for j in range(4):
            tx(ax, x0 + 0.35 + j * 1.12 + 0.5, 6.85, "盘%d" % (j + 1), fs=8.0, color=GRAY)
        tx(ax, x0 + 2.4, 3.5, note, fs=8.8)
    # 对比表
    tx(ax, 7.5, 2.55, "三方案对比", fs=12, bold=True)
    heads = ["方案", "思路", "容量利用率", "读性能", "写性能", "容错能力"]
    xs = [0.4, 2.6, 4.9, 6.8, 8.7, 10.7]
    ws = [2.2, 2.3, 1.9, 1.9, 2.0, 2.4]
    for cx2, w2, h in zip(xs, ws, heads):
        rect(ax, cx2, 1.9, w2, 0.55, h, fc=BLUE_L, ec=BLUE, fs=10, bold=True)
    rows2 = [("RAID 0", "条带化", "100%", "快（并行）", "快", "无冗余，坏 1 块全丢"),
             ("RAID 1", "镜像", "50%", "更快（并行读多副本）", "较慢（双写）", "坏 1 块仍可用"),
             ("RAID 5", "条带+分布式校验", "(N-1)/N", "快（近 0）", "慢（算校验）", "坏 1 块可恢复")]
    for r, row in enumerate(rows2):
        y = 1.3 - r * 0.55
        for cx2, w2, v in zip(xs, ws, row):
            rect(ax, cx2, y, w2, 0.55, v, fc=GRAY_L if r % 2 == 0 else "white", ec=GRAY, fs=9.4, lw=1.0)
    save(fig, FDIR + "ch4-17_raid.png")
