# -*- coding: utf-8 -*-
"""第3章 内存管理 · 全部插图绘制脚本（写作顺序：确认图片成功后再写正文）"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig as O
from matplotlib.patches import Polygon

INK, BLUE, BLUE_L = O.INK, O.BLUE, O.BLUE_L
GREEN, GREEN_L = O.GREEN, O.GREEN_L
AMBER, AMBER_L = O.AMBER, O.AMBER_L
RED, RED_L = O.RED, O.RED_L
PURPLE, PURPLE_L = O.PURPLE, O.PURPLE_L
TEAL, TEAL_L = O.TEAL, O.TEAL_L
GRAY, GRAY_L = O.GRAY, O.GRAY_L
PINK, PINK_L = O.PINK, O.PINK_L

FIG = "/Users/levi/IdeaProjects/操作系统/第3章_内存管理/figures"

def t(ax, *a, **k): return O.tx(ax, *a, **k)
def bk(ax, *a, **k): return O.box(ax, *a, **k)
def rk(ax, *a, **k): return O.rbox(ax, *a, **k)
def rc(ax, *a, **k): return O.rect(ax, *a, **k)
def dm(ax, *a, **k): return O.diamond(ax, *a, **k)
def el(ax, *a, **k): return O.ellipse(ax, *a, **k)
def al(ax, *a, **k): return O.arrow(ax, *a, **k)
def ln(ax, *a, **k): return O.line(ax, *a, **k)


# ============ ch3-00 本章知识框架导图 ============
def fig00():
    fig, ax = O.new_fig(11.6, 8.6, (0, 11.6), (0, 8.6))
    O.title(ax, "第3章 内存管理 · 知识框架导图",
            "主线：程序的地址如何变成内存地址（装哪里、怎么装、装不下怎么办）")
    bk(ax, 5.8, 6.95, 3.0, 0.8, "内存管理", fc=PURPLE_L, ec=PURPLE, fs=15, bold=True)
    cols = [
        (1.35, BLUE,  "3.1 内存基础", ["存储器层次结构", "三种装入方式", "三种链接方式"]),
        (3.62, GREEN, "3.2 内存扩充", ["覆盖技术(已淘汰)", "交换技术", "覆盖 vs 交换"]),
        (5.90, AMBER, "3.3 连续分配", ["单一/固定分区", "动态分区分配", "分配算法FF·NF·BF·WF"]),
        (8.18, TEAL,  "3.4~3.8 离散分配", ["基本分页+页表", "TLB与多级页表", "分段·段页式"]),
        (10.45, PINK, "3.9~3.12 虚拟内存", ["请求分页·缺页处理", "置换算法·页框分配", "抖动与工作集"]),
    ]
    for cx, c, head, kids in cols:
        bk(ax, cx, 5.75, 2.12, 0.72, head, fc=GRAY_L, ec=c, fs=11, bold=True, color=c)
        al(ax, 5.8, 6.52, cx, 6.13, lw=1.8, color=c)
        ys = [4.25, 3.05, 1.85]
        light = {BLUE: BLUE_L, GREEN: GREEN_L, AMBER: AMBER_L,
                 TEAL: TEAL_L, PINK: PINK_L}
        for i, k in enumerate(kids):
            bk(ax, cx, ys[i], 2.1, 0.78, k, fc=light[c],
               ec=c, fs=9.6)
            if i == 0:
                al(ax, cx, 5.38, cx, ys[i] + 0.42, lw=1.6, color=c)
            else:
                al(ax, cx, ys[i - 1] - 0.42, cx, ys[i] + 0.42, lw=1.6, color=c)
    rk(ax, 0.5, 0.35, 10.6, 0.75,
       "本章计算四大件：①地址拆分与物理地址  ②EAT=命中×快+TLB未命中×(1次/2次)访存  ③各置换算法缺页次数  ④多级页表位数与访存次数",
       fc=AMBER_L, ec=AMBER, fs=10)
    save_fig(fig, "ch3-00_chapter_map")


def save_fig(fig, name):
    O.save(fig, f"{FIG}/{name}.png")


# ============ ch3-01 存储器层次金字塔 ============
def fig01():
    fig, ax = O.new_fig(11, 7.8, (0, 11), (0, 7.8))
    O.title(ax, "图：存储器层次结构（金字塔）", "越往上：速度越快、容量越小、价格越高 —— 用Cache缓解速度差，用磁盘缓解容量差")
    layers = [
        ("寄存器(CPU内部)", "容量：几十~几百 B", "访问时间：~1 ns",
         "寄存器堆", RED, RED_L),
        ("高速缓存 Cache", "容量：几十 KB~几 MB", "访问时间：~几 ns",
         "Cache", AMBER, AMBER_L),
        ("主存（内存）", "容量：几 GB~几十 GB", "访问时间：~100 ns",
         "主存", BLUE, BLUE_L),
        ("辅助存储器（外存）", "容量：几百 GB~几 TB", "访问时间：~几 ms",
         "磁盘/SSD", TEAL, TEAL_L),
    ]
    n = len(layers)
    top, bot = 6.55, 1.05
    h = (top - bot) / n
    hw_top, hw_bot = 2.6, 5.6
    for i, (nm, cap, tm, short, c, cl) in enumerate(layers):
        yt = top - i * h
        yb = top - (i + 1) * h
        hwt = hw_top + (hw_bot - hw_top) * i / n
        hwb = hw_top + (hw_bot - hw_top) * (i + 1) / n
        ax.add_patch(Polygon(
            [(5.5 - hwt, yt), (5.5 + hwt, yt), (5.5 + hwb, yb), (5.5 - hwb, yb)],
            closed=True, facecolor=cl, edgecolor=c, lw=2.0, zorder=2))
        t(ax, 5.5 - (hwt + hwb) / 2, (yt + yb) / 2, nm, fs=11.5, bold=True, color=c, z=6)
        t(ax, 5.5 + hwt - 0.1, (yt + yb) / 2 + 0.28, cap, fs=9.5, ha="left", z=6)
        t(ax, 5.5 + hwt - 0.1, (yt + yb) / 2 - 0.22, tm, fs=9.5, ha="left", z=6)
    al(ax, 0.75, 1.0, 0.75, 6.6, color=RED, lw=2.2, ms=18)
    t(ax, 0.62, 3.9, "速度越快\n价格越高", fs=10.5, color=RED, bold=True, rotation=90)
    al(ax, 10.25, 6.6, 10.25, 1.0, color=BLUE, lw=2.2, ms=18)
    t(ax, 10.42, 3.9, "容量越来越大（成本下降）", fs=10.5, color=BLUE, bold=True, rotation=90)
    rk(ax, 1.1, 0.22, 8.8, 0.62,
       "层次间小者充当大者的缓存（Cache/主存、主存/磁盘）→ 局部性原理见 3.9 节；考研常考“各级速度/容量数量级”",
       fc=GRAY_L, ec=GRAY, fs=10)
    save_fig(fig, "ch3-01_memory_hierarchy")


# ============ ch3-02 三种装入方式与三种链接方式 ============
def fig02():
    fig, ax = O.new_fig(13.4, 9.2, (0, 13.4), (0, 9.2))
    O.title(ax, "三种装入方式 · 三种链接方式", "链路：源程序 →编译→ 目标模块 →链接→ 装入模块 →装入→ 内存")
    # ---- 上半：三种装入 ----
    t(ax, 6.7, 7.9, "① 三种装入方式（重点：动态重定位）", fs=14, bold=True, color=BLUE)
    pp = [(0.35, 4.85), (4.63, 4.85), (8.91, 4.85)]
    for (px, py), (title, lines) in zip(pp, [
        ("绝对装入（早期单道）", [
            "编译/链接时直接生成绝对地址，",
            "装入哪就是哪；只适合单道环境；",
            "逻辑地址=物理地址。",
            "缺点：利用率低、不灵活。"]),
        ("静态重定位（可重定位装入）", [
            "装入时对程序一次性“偏移”重定位，",
            "把逻辑地址换算成物理地址；",
            "运行期间不能移动，移动需重新装入；",
            "再装入时使用与当时不同地址→换入后需重新定位。"]),
        ("动态重定位（现代OS基础）", [
            "装入时不做地址换算，程序内仍用逻辑地址；",
            "运行时由CPU按：物理地址=逻辑地址+重定位寄存器；",
            "重定位寄存器由OS设置，进程运行时不断随地址变动；",
            "优点：可移动、可紧凑、可共享 → 支持虚拟存储。"]),
    ]):
        bk(ax, px + 1.35, py + 1.85, 2.7, 0.5, title, fc=BLUE_L, ec=BLUE, fs=11, bold=True, color=BLUE)
        for i, s in enumerate(lines):
            t(ax, px + 0.18, py + 1.45 - 0.36 * i, s, fs=8.8, ha="left", va="center")
        # 内存条示意
        rc(ax, px + 0.18, py - 0.62, 2.7, 0.62, "OS 系统区", fc=GRAY_L, ec=GRAY, fs=8.5)
        rc(ax, px + 0.18, py - 1.42, 2.7, 0.62, "装入的程序", fc=GREEN_L, ec=GREEN, fs=9.5, bold=True)
    # 动态重定位小图（第三格下方，水平链式）
    t(ax, 11.6, 1.22, "动态重定位实例（物理地址=逻辑地址+重定位寄存器值）", fs=9.2, bold=True, color=PURPLE)
    bk(ax, 9.5, 0.18, 1.8, 0.85, "CPU逻辑地址\nL = 500", fc=PURPLE_L, ec=PURPLE, fs=8.6)
    al(ax, 10.42, 0.6, 10.85, 0.6, lw=1.6, ms=13)
    bk(ax, 11.3, 0.18, 1.8, 0.85, "重定位寄存器\nRR = 100K", fc=AMBER_L, ec=AMBER, fs=8.6)
    t(ax, 12.22, 0.6, "+", fs=14, bold=True, color=RED)
    bk(ax, 12.68, 0.18, 1.95, 0.85, "物理地址\n= 500 + 102400\n= 102900", fc=RED_L, ec=RED, fs=8.4, bold=True)
    # ---- 下半：三种链接 ----
    t(ax, 6.7, 3.1, "② 三种链接方式", fs=14, bold=True, color=GREEN)
    qq = [(0.35, 1.0), (4.63, 1.0), (8.91, 1.0)]
    for (px, py), (title, lines) in zip(qq, [
        ("静态链接", ["运行前一次性把多个目标模块链接成完整的",
                      "可执行文件（装入模块），此后不可拆分；",
                      "数据/代码在磁盘→内存“一次性转入”。"]),
        ("装入时动态链接", ["装入时边装入边链接（模块还在磁盘上）；",
                           "每次运行都重新装配，可分别更新各模块；",
                           "比静态链接节省对换区空间。"]),
        ("运行时动态链接", ["运行中需要哪块才装入、才链接；",
                           "可更新、可共享（如动态链接库）；",
                           "对换时省空间。"]),
    ]):
        bk(ax, px + 1.35, py + 1.55, 2.9, 0.52, title, fc=GREEN_L, ec=GREEN, fs=11, bold=True, color=GREEN)
        for i, s in enumerate(lines):
            t(ax, px + 0.18, py + 1.15 - 0.34 * i, s, fs=8.8, ha="left", va="center")
        al(ax, px + 1.35, py + 1.26, px + 1.35, py + 1.02, lw=1.4, color=GRAY)
    rk(ax, 0.5, 0.42, 8.3, 0.72,
       "一句话：装入解决“地址从哪来”，链接解决“多模块怎么拼”（静态=拼好再装；装入时=边装边拼；运行时=用到才拼）",
       fc=GRAY_L, ec=GRAY, fs=9)
    save_fig(fig, "ch3-02_loading_linking")


# ============ ch3-03 覆盖与交换 ============
def fig03():
    fig, ax = O.new_fig(13.4, 9.6, (0, 13.4), (0, 9.6))
    O.title(ax, "内存扩充技术：覆盖（以段为单位）与交换（以进程为单位）",
            "共同点：内存不够时把东西暂时“挪”到外存——覆盖是程序内部的挪，交换是进程之间的挪")
    # ---- 左：覆盖 ----
    t(ax, 3.35, 8.35, "① 覆盖技术（已淘汰·考研常考概念）", fs=13, bold=True, color=BLUE)
    rc(ax, 0.4, 4.0, 1.9, 3.6, "OS", fc=GRAY_L, ec=GRAY, fs=10)
    rc(ax, 2.5, 5.9, 3.0, 1.7, "固定区：常驻内存\n主程序M + 公用子程序C1\n(20K + 10K)", fc=BLUE_L, ec=BLUE, fs=9.4)
    rc(ax, 2.5, 4.85, 3.0, 0.9, "覆盖区1（互斥装入）\nA1=80K  或  B1=90K", fc=AMBER_L, ec=AMBER, fs=9)
    rc(ax, 2.5, 3.9, 3.0, 0.8, "覆盖区2（互斥装入）\nA2=60K  或  B2=70K", fc=AMBER_L, ec=AMBER, fs=9)
    t(ax, 2.5, 3.42, "A1、B1 共用覆盖区1，A2、B2 共用覆盖区2：\n同一时刻只放一组 → 所需最大内存 = 固定区 + 最大覆盖区",
      fs=8.4, ha="left", color=GRAY)
    # ---- 右：交换 ----
    t(ax, 10.0, 8.35, "② 交换技术（中级调度）", fs=13, bold=True, color=GREEN)
    rc(ax, 7.5, 4.3, 2.3, 3.1, "", fc=BLUE_L, ec=BLUE)
    t(ax, 8.65, 7.15, "内存", fs=11, bold=True, color=BLUE)
    rc(ax, 8.65, 5.9, 1.8, 0.85, "进程P1\n(运行)", fc=GREEN_L, ec=GREEN, fs=9.4)
    rc(ax, 8.65, 4.6, 1.8, 0.8, "(空闲/换出后空位)", fc=GRAY_L, ec=GRAY, fs=8.4)
    rc(ax, 11.0, 4.3, 2.3, 3.1, "", fc=AMBER_L, ec=AMBER)
    t(ax, 12.15, 7.15, "对换区(磁盘)", fs=11, bold=True, color=AMBER)
    rc(ax, 12.15, 5.9, 1.8, 0.85, "进程P2\n(就绪/挂起)", fc=GREEN_L, ec=GREEN, fs=9.2)
    rc(ax, 12.15, 4.6, 1.8, 0.8, "进程P3\n(就绪/挂起)", fc=GREEN_L, ec=GREEN, fs=9.2)
    al(ax, 9.85, 6.3, 10.9, 6.3, "换出 P1→对换区", color=RED, lw=2.0, dy=0.28)
    al(ax, 10.9, 5.3, 9.85, 5.3, "换入 对换区→内存", color=GREEN, lw=2.0, dy=-0.3)
    t(ax, 10.0, 3.45, "时机：内存紧张或进程长时间阻塞时，OS自动换出/换入；\n以“进程”为单位；对换区为连续分配、速度更快", fs=8.6, ha="center", color=GRAY)
    # ---- 底部对比表 ----
    tb = [("对比项", "覆盖技术", "交换技术"),
          ("单位", "段（程序内部模块）", "进程（整个进程）"),
          ("发生时机", "运行前/中由程序员设计安排", "OS 在内存紧张时自动进行"),
          ("是否需要程序员声明", "需要（程序员划分覆盖结构）", "不需要（OS 自动管理）"),
          ("是否与中级调度相关", "无关（先于交换的早期技术）", "交换 = 中级调度的实现手段"),
          ("现状", "已被淘汰（概念常考）", "现代OS“挂起/对换”机制基础")]
    x0, bh = 0.5, 0.46
    widths = [3.0, 4.35, 4.5]
    y0 = 2.3
    for r, row in enumerate(tb):
        for cidx, cell in enumerate(row):
            fc = GRAY_L if r == 0 else ("white" if cidx == 0 else GREEN_L if cidx == 1 else AMBER_L)
            ec = GRAY if r == 0 else O.INK
            rc(ax, x0 + sum(widths[:cidx]) + 0.05 * cidx, y0 - r * bh, widths[cidx], bh,
               cell, fc=fc, ec=ec, fs=9.2, bold=(r == 0 or cidx == 0), lw=1.0)
    save_fig(fig, "ch3-03_swap_cover")


# ============ ch3-04 动态分区分配四算法 ============
def mem_bar(ax, px, py, w, segs, maxk=1700):
    """segs: (startK, sizeK, kind, label)  kind='free'|'alloc'"""
    kx = lambda k: px + 0.12 + k / maxk * (w - 0.24)
    rc(ax, kx(0), py, kx(maxk) - kx(0), 1.0, "", fc=GRAY_L, ec=GRAY, lw=1.0)
    for (s, sz, kind, lab) in segs:
        fcc = AMBER_L if kind == "free" else GREEN_L
        ecc = AMBER if kind == "free" else GREEN
        txt = lab
        if kind == "free" and sz >= 100:
            txt = f"空{sz}K"
        rc(ax, kx(s), py, kx(s + sz) - kx(s), 1.0, txt, fc=fcc, ec=ecc, fs=8.0, lw=1.0)
    al(ax, kx(0), py + 1.16, kx(maxk), py + 1.16, lw=1.4, color=GRAY, ms=10)
    t(ax, kx(0), py + 1.38, "0", fs=7.5, color=GRAY)


def fig04():
    fig, ax = O.new_fig(16.2, 10.9, (0, 16.2), (0, 10.9))
    O.title(ax, "动态分区分配：FF / NF / BF / WF 四算法同一例子对比",
            "空闲分区（地址递增，黄=空闲区）：100K·500K·200K·300K·600K 共1700K；请求序列：212K→417K→112K→426K（绿=已分配）")
    panels = [
        (0.35, 5.3, "FF 首次适应（顺序查第一个满足的）", BLUE,
         [(0, 100, "free", ""), (100, 212, "alloc", "①212K"), (312, 112, "alloc", "③112K"),
          (424, 176, "free", ""), (600, 200, "free", ""), (800, 300, "free", ""),
          (1100, 417, "alloc", "②417K"), (1517, 183, "free", "")],
         ["① 212K→②号块(500K)，剩 288K", "② 417K→⑤号块(600K)，剩 183K",
          "③ 112K→②号块(288K)，剩 176K", "④ 426K→剩余最大仅 300K → 分配失败"],
         "结论：低地址空闲区被反复切割，高地址块保留；综合性能最好，实际系统常用。"),
        (8.25, 5.3, "NF 循环/下次适应（从上次处接着找）", GREEN,
         [(0, 100, "free", ""), (100, 212, "alloc", "①212K"), (312, 112, "alloc", "③112K"),
          (424, 176, "free", ""), (600, 200, "free", ""), (800, 300, "free", ""),
          (1100, 417, "alloc", "②417K"), (1517, 183, "free", "")],
         ["① 212K→②号块(500K)，剩 288K，指针至③", "② 417K→⑤号块(600K)，剩 183K，指针绕回①",
          "③ 112K→②号块(288K)，剩 176K，指针至③", "④ 426K→③200K/④300K/⑤183K…均不足 → 失败"],
         "结论：碎片分布更均匀，但大空闲区易被过早割裂，性能略差于 FF。"),
        (0.35, 0.2, "BF 最佳适应（找满足的最小空闲区）", AMBER,
         [(0, 100, "free", ""), (100, 417, "alloc", "②417K"), (517, 83, "free", ""),
          (600, 112, "alloc", "③112K"), (712, 88, "free", ""), (800, 212, "alloc", "①212K"),
          (1012, 88, "free", ""), (1100, 426, "alloc", "④426K"), (1526, 174, "free", "")],
         ["① 212K→④号块(300K)，剩 88K（最小满足）", "② 417K→②号块(500K)，剩 83K",
          "③ 112K→③号块(200K)，剩 88K", "④ 426K→⑤号块(600K)，剩 174K → 全部满足"],
         "结论：产生大量极小碎片（83K/88K/88K…），查找开销大，性能较差；本例恰好全满足。"),
        (8.25, 0.2, "WF 最坏适应（找满足的最大空闲区）", PURPLE,
         [(0, 100, "free", ""), (100, 417, "alloc", "②417K"), (517, 83, "free", ""),
          (600, 200, "free", ""), (800, 300, "free", ""), (1100, 212, "alloc", "①212K"),
          (1312, 112, "alloc", "③112K"), (1424, 276, "free", "")],
         ["① 212K→⑤号块(600K)，剩 388K（最大满足）", "② 417K→②号块(500K)，剩 83K",
          "③ 112K→⑤号块(388K)，剩 276K", "④ 426K→最大空闲 300K<426K → 失败"],
         "结论：大块被削成小块、小碎片少；适合装入中等进程，但大块越剩越碎。"),
    ]
    for px, py, title, c, segs, logs, note in panels:
        bk(ax, px + 3.9, py + 3.95, 7.65, 0.62, title, fc=GRAY_L, ec=c, fs=13, bold=True, color=c)
        for i, s in enumerate(logs):
            t(ax, px + 0.12, py + 3.15 - 0.43 * i, s, fs=9.3, ha="left", va="center", color=INK)
        mem_bar(ax, px + 0.15, py + 0.78, 7.6, segs)
        rk(ax, px + 0.12, py + 0.06, 7.55, 0.6, note, fc=GRAY_L, ec=GRAY, fs=8.0)
    save_fig(fig, "ch3-04_partition_algorithms")


# ============ ch3-05 分页基本原理 ============
def fig05():
    fig, ax = O.new_fig(13.6, 9.0, (0, 13.6), (0, 9.0))
    O.title(ax, "基本分页存储管理：等分逻辑空间为页、等分物理内存为页框",
            "页面=页框/页帧=4KB；页表把“页号→页框号”映射起来，进程可以散装进任意页框")
    t(ax, 1.95, 7.62, "进程P的地址空间 16KB = 4页", fs=11.5, bold=True, color=BLUE)
    t(ax, 5.95, 7.62, "页表（连续存放于内存，每项=页框号）", fs=11.5, bold=True, color=TEAL)
    t(ax, 10.6, 7.62, "物理内存 64KB = 16个页框", fs=11.5, bold=True, color=GREEN)
    # 页（左）
    pg = [(6.65, "页0：程序代码段"), (5.45, "页1：堆/栈"),
          (4.25, "页2：数据段"), (3.05, "页3：末尾页(仅用3KB)")]
    for (py, lab) in pg:
        bk(ax, 1.95, py, 2.9, 1.05, "", fc=BLUE_L, ec=BLUE)
        t(ax, 1.95, py + 0.3, lab, fs=9.6, bold=True, color=BLUE, z=6)
        for k in range(4):
            rc(ax, 0.72 + k * 0.72, py - 0.32, 0.68, 0.42, f"{k}", fc="white", ec=BLUE, lw=0.8, fs=7)
        t(ax, 1.95, py - 0.62, "4KB(4×1KB子块)", fs=7.4, color=GRAY, z=6)
    # 页表（中）
    rows = [("0", "3", "程序"), ("1", "12", "栈/堆"), ("2", "6", "数据"), ("3", "7", "末页")]
    ytop = 7.3
    for i, (pn, fn, nm) in enumerate(rows):
        y = ytop - i * 0.95
        rc(ax, 4.65, y - 0.42, 1.28, 0.84, f"页{pn}", fc="white", ec=TEAL, fs=10, bold=True, lw=1.2)
        rc(ax, 6.05, y - 0.42, 1.28, 0.84, f"页框{fn}", fc=TEAL_L, ec=TEAL, fs=10, bold=True, lw=1.2)
        al(ax, 5.94, y, 6.03, y, lw=1.8, color=TEAL, ms=13)
        al(ax, 3.42, ytop - i * 0.95, 4.62, y, lw=1.4, color=INK, ms=12)
    # 页框（右，4列x4行）
    frames = {3: "页0(程序)", 6: "页2(数据)", 7: "页3(3KB)", 12: "页1(栈)"}
    x0, y0, cw, ch = 8.55, 7.3, 1.25, 1.5
    for r in range(4):
        for c in range(4):
            idx = r * 4 + c
            x = x0 + c * cw
            y = y0 - r * ch
            if idx in frames:
                rc(ax, x, y - ch, cw, ch, "", fc=GREEN_L, ec=GREEN, fs=8)
                t(ax, x + cw / 2, y - 0.24, frames[idx], fs=8.6, bold=True, color=GREEN)
                t(ax, x + cw / 2, y - 0.58 + 0.3, f"框{idx}", fs=7.4, color=GREEN)
            else:
                rc(ax, x, y - ch, cw, ch, f"框{idx}:空闲", fc=GRAY_L, ec=GRAY, fs=7.6)
    rk(ax, 8.55, 0.35, 4.95, 0.85,
       "页3只用3KB → 页框7中有1KB = 内部碎片；\n页表项=页框号，页表连续存放、项数=页数。",
       fc=RED_L, ec=RED, fs=8.6)
    rk(ax, 0.55, 0.35, 5.6, 0.85,
       "逻辑地址0~16KB看似连续，实际按页散装在任意页框；\n地址变换由硬件+OS完成，对用户完全透明。",
       fc=BLUE_L, ec=BLUE, fs=8.6)
    rk(ax, 4.15, 2.45, 4.2, 0.95,
       "映射关系（页表项与绿色页框标注一一对应）：\n页0→框3、页1→框12、页2→框6、页3→框7",
       fc=TEAL_L, ec=TEAL, fs=8.8)
    save_fig(fig, "ch3-05_paging_basics")


# ============ ch3-06 逻辑地址结构拆分 ============
def fig06():
    fig, ax = O.new_fig(13.6, 8.0, (0, 13.6), (0, 8.0))
    O.title(ax, "逻辑地址结构：32位 / 页大小4KB → 页号20位 + 页内偏移12位",
            "偏移位数由“页大小”决定：log2(4KB=2^12)=12；页号位数=地址位数-偏移位数")
    # 地址结构条
    rc(ax, 0.6, 5.9, 8.0, 0.8, "页号 P（20位，0 ~ 2^20-1）\n决定进程最多占 2^20 页", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
    rc(ax, 8.6, 5.9, 4.4, 0.8, "页内偏移 W（12位，0~4095）\nW 由页大小 2^12=4096B 决定", fc=AMBER_L, ec=AMBER, fs=10.5, bold=True)
    al(ax, 4.6, 5.82, 4.6, 5.26, color=INK, lw=1.6, ms=12)
    al(ax, 10.8, 5.82, 10.8, 5.26, color=INK, lw=1.6, ms=12)
    t(ax, 4.6, 5.05, "页号 = A div L（除法）", fs=9.5, bold=True, color=BLUE)
    t(ax, 10.8, 5.05, "偏移 = A mod L（取余）", fs=9.5, bold=True, color=AMBER)
    t(ax, 6.8, 4.6, "二进制秒拆：P = A >> 12；W = A & 0xFFF（低12位直接截取）", fs=10, color=INK, bg="white")
    # 公式区
    rk(ax, 0.6, 3.3, 12.4, 0.9,
       "通用公式：  P = A div L（商）        W = A mod L（余数）        校验：若 W ≥ L 说明拆分错误/越界；页表越界用“页号 ≥ 页表长度M”判断",
       fc=GRAY_L, ec=GRAY, fs=10)
    # 例子：十进制
    rk(ax, 0.6, 0.55, 6.1, 2.5, "", fc=GREEN_L, ec=GREEN)
    t(ax, 3.65, 2.82, "例1：十进制除法（页大小 L=4KB=4096B）", fs=11, bold=True, color=GREEN)
    t(ax, 3.65, 2.35, "给定逻辑地址 A = 8644\nP = 8644 div 4096 = 2\nW = 8644 mod 4096 = 452\n物理地址 = f×4096 + 452\n（f为页框号，由页表查得）",
      fs=10.5, ha="center", color=INK, ls=1.6)
    # 例子：二进制
    rk(ax, 6.9, 0.55, 6.1, 2.5, "", fc=AMBER_L, ec=AMBER)
    t(ax, 9.95, 2.82, "例2：二进制截取（同一地址）", fs=11, bold=True, color=AMBER)
    t(ax, 9.95, 2.38, "A = 8644 = 0b10 0001 1100 0100\n(32位补零：0000 0000 0000 0000 0000 10 | 0001 1100 0100)",
      fs=9.6, ha="center", ls=1.6)
    t(ax, 9.95, 1.55, "  │←── 页号P = 0b10 = 2 ──→│\n  │←─ 偏移W = 0b0001 1100 0100 = 452 ─→│\n  ←─共32位: 20位(页号)+12位(偏移)─→",
      fs=9.6, ha="center", ls=1.6)
    save_fig(fig, "ch3-06_page_address")


# ============ ch3-07 基本地址变换流程 ============
def fig07():
    fig, ax = O.new_fig(15.2, 11.6, (0, 15.2), (0, 11.6))
    O.title(ax, "基本地址变换流程（无TLB）：拆地址 → 越界检查 → 查页表 → 拼物理地址",
            "例：A=8644，L=4096 → P=2，W=452；页表长度M=4，P=2<4不越界；页2→页框6 → 物理地址=6×4096+452=25028")
    X = 3.0
    def step(y, txt, fc=BLUE_L, ec=BLUE, fs=10.4, w=3.8, h=0.8):
        bk(ax, X, y, w, h, txt, fc=fc, ec=ec, fs=fs, z=5)
    def flow(y1, y2, lab=""):
        al(ax, X, y1 - 0.41, X, y2 + 0.41, text=lab, lw=2.0, ms=15)
    step(10.15, "① CPU 发出逻辑地址 A\n（页号/偏移由硬件自动拆分）")
    flow(10.15, 9.1)
    step(9.1, "② 按页大小 L 拆分：\nP = A div 4096 = 2，W = A mod 4096 = 452")
    flow(9.1, 7.95, "P=2")
    dm(ax, X, 7.85, 3.8, 0.95, "③ P ≥ 页表长度 M ?\n（越界检查：P=2, M=4）", fs=9.4)
    al(ax, X + 1.95, 7.85, 8.55, 8.62, color=RED, lw=2.2, ms=16)
    t(ax, 5.6, 8.15, "是", fs=11, color=RED, bold=True, bg="white")
    rk(ax, 8.7, 8.55, 5.9, 1.0, "越界中断（进程被终止/异常）\n页号超过页表范围 = 访问了不存在的空间", fc=RED_L, ec=RED, fs=10)
    flow(7.85, 6.75, "否 成立")
    step(6.75, "④ 页表项地址 = 页表始址 F + P × 4B\n= F + 8（页表项大小4B）")
    flow(6.75, 5.65, "第一次访存")
    step(5.65, "⑤ 访存①：读该页表项 → 得页框号 f = 6\n（假设状态位P=1，页已装入内存）", fc=TEAL_L, ec=TEAL)
    flow(5.65, 4.55)
    step(4.55, "⑥ 物理地址 = f × L + W\n= 6×4096 + 452 = 25028", fc=AMBER_L, ec=AMBER)
    flow(4.55, 3.45, "第二次访存")
    step(3.45, "⑦ 访存②：按物理地址25028访问内存单元", fc=TEAL_L, ec=TEAL)
    flow(3.45, 2.35)
    step(2.35, "⑧ 数据送CPU：一次访存完成（⑤+⑦）", fc=GREEN_L, ec=GREEN)
    # 右侧：PTBR 与 页表
    rk(ax, 9.9, 9.55, 4.7, 1.0, "页表寄存器 PTBR（放在CPU中）：\n①页表始址 F  ②页表长度 M\n进程切换时由OS重新装入", fc=PURPLE_L, ec=PURPLE, fs=9)
    t(ax, 12.25, 7.95, "内存中的页表（连续存放，每项4B）", fs=10.2, bold=True, color=TEAL)
    ptab = [("表项0（页0）", "F+0B  → 页框3"), ("表项1（页1）", "F+4B  → 页框12"),
            ("表项2（页2）", "F+8B  → 页框6"), ("表项3（页3）", "F+12B → 页框7")]
    for i, (a, b) in enumerate(ptab):
        y = 7.35 - i * 0.72
        fc = AMBER_L if i == 2 else "white"
        rc(ax, 9.9, y - 0.32, 2.35, 0.64, a, fc=fc, ec=TEAL, fs=9, lw=1.1)
        rc(ax, 12.25, y - 0.32, 2.35, 0.64, b, fc=fc, ec=TEAL, fs=9, lw=1.1)
    el(ax, 6.3, 5.65, 2.3, 0.62, "访存①=查页表", fc=RED_L, ec=RED, fs=9, bold=True, color=RED)
    el(ax, 6.3, 3.45, 2.4, 0.62, "访存②=取数据", fc=RED_L, ec=RED, fs=9, bold=True, color=RED)
    t(ax, 12.25, 3.85, "物理内存中：页框6 + 偏移452", fs=10.2, bold=True, color=GREEN)
    rc(ax, 10.2, 1.95, 4.1, 1.35, "页框6内偏移452处\n存放所需数据（4B）\n定位地址 = 25028", fc=GREEN_L, ec=GREEN, fs=9.6)
    rk(ax, 0.55, 0.45, 13.9, 0.85,
       "【记忆口诀】先拆分 → 先查边界（P<M）→ 再查页表（访存①）→ 拼物理地址 → 再访存数据（访存②）。无TLB时一次访存=两次访存；",
       fc=AMBER_L, ec=AMBER, fs=10.2)
    save_fig(fig, "ch3-07_paging_translation")


# ============ ch3-08 快表TLB ============
def fig08():
    fig, ax = O.new_fig(15.2, 11.6, (0, 15.2), (0, 11.6))
    O.title(ax, "带快表TLB的地址变换流程：先查TLB（命中省一次访存），未命中再查内存页表",
            "TLB=快表，位于CPU内（相联存储器），保存最近使用的“页号→页框号”；h=命中率，t=TLB查找时间，m=一次访存时间")
    X = 3.0
    def step(y, txt, fc=BLUE_L, ec=BLUE, fs=10.6, w=3.7, h=0.8):
        bk(ax, X, y, w, h, txt, fc=fc, ec=ec, fs=fs, z=5)
    def flow(y1, y2, lab=""):
        al(ax, X, y1 - 0.41, X, y2 + 0.41, text=lab, lw=2.0, ms=15)
    step(10.0, "① CPU 发出逻辑地址 A，硬件拆出\n页号P=2、页内偏移W=452")
    flow(10.0, 8.95)
    step(8.95, "② 查快表 TLB：\n按键值(页号2)与TLB各项并行比较", fc=GREEN_L, ec=GREEN)
    flow(8.95, 7.85, "查TLB耗时 t")
    dm(ax, X, 7.85, 3.7, 0.95, "③ 命中TLB？\n（h=90%时命中倾向）", fc=AMBER_L, ec=AMBER, fs=9.4)
    # 命中分支（右）
    al(ax, X + 1.87, 7.85, 5.72, 7.85, text="命中", color=GREEN, lw=2.2, ms=16, dy=0.24, fs=10)
    bk(ax, 7.6, 7.85, 3.75, 0.8, "④ 命中：直接由TLB得页框号 f=6\n（省去访存①，只差访存②）", fc=GREEN_L, ec=GREEN, fs=9.8, z=5)
    ln(ax, 7.6, 7.45, 7.6, 4.55, color=GREEN, lw=2.0)
    al(ax, 7.6, 4.55, 4.92, 4.55, color=GREEN, lw=2.0, ms=15)
    # 未命中分支（下）
    flow(7.85, 6.75, "未命中")
    step(6.75, "⑤ 访存①：查内存中的页表\n得页框号f=6（完整页表永远在内存）", fc=TEAL_L, ec=TEAL)
    flow(6.75, 5.65, "把该表项写入TLB")
    step(5.65, "⑥ 未命中时同时把完整页表项装入TLB\n以后再访问同页就命中（TLB容量小，需置换）", fs=9.8)
    flow(5.65, 4.55)
    step(4.55, "⑦ 物理地址 = f × L + W = 6×4096+452 = 25028", fc=AMBER_L, ec=AMBER)
    flow(4.55, 3.45, "访存②")
    step(3.45, "⑧ 访存②：按物理地址访问内存取数据", fc=TEAL_L, ec=TEAL)
    flow(3.45, 2.35)
    step(2.35, "⑨ 数据送CPU — 完成", fc=GREEN_L, ec=GREEN)
    # 右侧：TLB与页表
    rk(ax, 10.5, 9.45, 4.1, 1.15, "TLB（快表）在CPU内：\n可并行比较的相联存储器，容量小（几~几百项）\n命中→1次访存；未命中→2次访存", fc=GREEN_L, ec=GREEN, fs=9)
    t(ax, 12.55, 8.85, "TLB 初始内容（命中率 h）", fs=10, bold=True, color=GREEN)
    for i, (a, b) in enumerate([("页1", "框12"), ("页3", "框7"), ("页0", "框3")]):
        y = 8.3 - i * 0.62
        rc(ax, 11.0, y - 0.28, 1.6, 0.52, f"页{a}", fc="white", ec=GREEN, fs=9, lw=1.0)
        rc(ax, 12.6, y - 0.28, 1.6, 0.52, f"框{b}", fc=GREEN_L, ec=GREEN, fs=9, lw=1.0)
    rk(ax, 10.5, 4.35, 4.1, 1.6, "EAT（有效访问时间）：\nEAT = h×(t+m) + (1-h)×(t+2m)\n例：t=20ns, m=100ns, h=90%\n= 0.9×120 + 0.1×220 = 130ns", fc=AMBER_L, ec=AMBER, fs=9.4)
    al(ax, 4.92, 5.65, 10.75, 7.0, color=PURPLE, lw=1.8, ls="--", ms=13)
    t(ax, 7.6, 6.4, "更新TLB\n（装入页2→框6）", fs=9, color=PURPLE, ha="center", bg="white")
    el(ax, 11.6, 3.35, 3.0, 0.6, "两次访存：①查页表 ②取数据", fc=RED_L, ec=RED, fs=9, bold=True, color=RED)
    rk(ax, 0.55, 0.5, 13.9, 0.85,
       "【考点】“快表命中仍需查t”且未命中时的访存次数按（t+2m）计——快表把90%的访问从两次访存降到一次",
       fc=GRAY_L, ec=GRAY, fs=10)
    save_fig(fig, "ch3-08_tlb")


# ============ ch3-09 两级页表 ============
def fig09():
    fig, ax = O.new_fig(14.6, 9.9, (0, 14.6), (0, 9.9))
    O.title(ax, "两级页表：把20位页号再分成“一级页号10位 + 二级页号10位”",
            "32位地址/页面4KB(2^12)/页表项4B：单级页表需2^20×4B=4MB（必须连续常驻）→ 多级页表把页表本身也分页")
    # 地址结构
    rc(ax, 0.6, 7.9, 4.4, 0.85, "一级页号 P1（10位）\n表项指向二级页表", fc=PURPLE_L, ec=PURPLE, fs=9.6, bold=True)
    rc(ax, 5.0, 7.9, 4.4, 0.85, "二级页号 P2（10位）\n表项指向页框", fc=BLUE_L, ec=BLUE, fs=9.6, bold=True)
    rc(ax, 9.4, 7.9, 4.6, 0.85, "页内偏移 W（12位）\nW = A mod 4096", fc=AMBER_L, ec=AMBER, fs=9.6, bold=True)
    rk(ax, 0.6, 6.7, 13.4, 1.0,
       "例：A=12605892 → P1=3, P2=5, W=2500（二进制 0000000011 | 0000000101 | 100111000100）\n十进制：P1=A div 2^22=3；P2=(A div 2^12) mod 2^10=5；W=A mod 2^12=2500",
       fc=GRAY_L, ec=GRAY, fs=9.8)
    # 顶级页表
    t(ax, 2.6, 6.15, "顶级页表（页目录，常驻内存）\n共2^10项 ×4B = 4KB，且只能有一个", fs=9.6, bold=True, color=PURPLE)
    rc(ax, 0.8, 3.95, 3.7, 2.0, "", fc=PURPLE_L, ec=PURPLE)
    for i, lab in enumerate(["P1=0 → 二级页表0", "P1=1 → 二级页表1", "P1=2 → 二级页表2", "P1=3 → 二级页表3", "…"]):
        y = 5.6 - i * 0.4
        fc = AMBER_L if i == 3 else "white"
        rc(ax, 0.95, y - 0.18, 3.4, 0.36, lab, fc=fc, ec=PURPLE, fs=8.6, lw=1.0)
    # 二级页表
    t(ax, 7.5, 6.15, "二级页表（离散存放、可换出磁盘）\n二级页表每张 2^10项×4B=4KB，用到才调入", fs=9.6, bold=True, color=BLUE)
    rc(ax, 5.8, 3.95, 3.5, 2.0, "", fc=BLUE_L, ec=BLUE)
    for i, lab in enumerate(["P2=4 → 页框k", "P2=5 → 页框7", "P2=6 → 页框…", "P2=2^10-1 → …", "…"]):
        y = 5.6 - i * 0.4
        fc = AMBER_L if i == 1 else "white"
        rc(ax, 5.95, y - 0.18, 3.2, 0.36, lab, fc=fc, ec=BLUE, fs=8.6, lw=1.0)
    # 内存
    t(ax, 12.4, 6.15, "内存（页框）", fs=9.6, bold=True, color=GREEN)
    x0, y0, cs = 10.35, 6.0, 0.95
    for r in range(4):
        for c in range(4):
            idx = r * 4 + c
            x = x0 + c * cs
            y = y0 - r * cs
            fc = GREEN_L if idx == 7 else GRAY_L
            rc(ax, x, y - cs, cs, cs, f"框{idx}", fc=fc, ec=GREEN if idx == 7 else GRAY, fs=7.4, lw=1.0)
    # 箭头
    al(ax, 4.6, 4.45, 5.7, 4.45, color=PURPLE, lw=2.0, ms=14)
    al(ax, 7.45, 4.45, 10.28, 4.45, text="P2=5\n→页框7", color=BLUE, lw=2.0, ms=14, fs=8.6, dy=0.34)
    rk(ax, 0.6, 0.3, 13.4, 1.65,
       "【记忆口诀】单级→多级：把4MB连续页表切成1024张4KB二级页表，用一张4KB顶级页表索引（顶级常驻，二级按需装入、可换出）。\n"
       "【考点】①无TLB、两级页表时一次访存=3次访存（顶级表、二级表、数据）；②多级页表省空间但换时间（每多一级多访存一次）；③顶级页表必须连续、只有一个。",
       fc=AMBER_L, ec=AMBER, fs=9.8)
    save_fig(fig, "ch3-09_two_level")


# ============ ch3-10 分段与地址变换 ============
def fig10():
    fig, ax = O.new_fig(14.8, 10.4, (0, 14.8), (0, 10.4))
    O.title(ax, "分段存储管理：按程序逻辑单位划分段，两次越界检查 → 物理地址=基址+偏移",
            "逻辑地址(段号S, 段内偏移W)；段表项=(段长C, 基址B)；段内连续、段间可不连续")
    # 左：逻辑空间
    t(ax, 2.35, 9.05, "进程逻辑地址空间（按逻辑单位划分）", fs=11.5, bold=True, color=BLUE)
    segs = [(7.85, "段0：主程序", "200K", 1.3), (6.55, "段1：数据段", "80K", 0.85),
            (5.45, "段2：栈段", "60K", 0.85), (4.35, "段3：公用库", "50K", 0.85)]
    for (ytop, nm, sz, hgt) in segs:
        bk(ax, 2.35, ytop - hgt / 2, 3.3, hgt, "", fc=BLUE_L, ec=BLUE)
        t(ax, 2.35, ytop - hgt / 2 + 0.22, nm, fs=9.8, bold=True, color=BLUE)
        t(ax, 2.35, ytop - hgt / 2 - 0.22, f"段长 {sz}（段内偏移从0开始）", fs=8.4, color=GRAY)
    # 中：段表
    t(ax, 7.1, 9.05, "段表（段表寄存器 STLR 存放其始址和长度）", fs=11.5, bold=True, color=TEAL)
    rc(ax, 5.7, 7.9, 1.3, 0.62, "段号", fc=GRAY_L, ec=GRAY, fs=9.2, bold=True)
    rc(ax, 7.0, 7.9, 1.3, 0.62, "段长C", fc=GRAY_L, ec=GRAY, fs=9.2, bold=True)
    rc(ax, 8.3, 7.9, 1.3, 0.62, "基址B", fc=GRAY_L, ec=GRAY, fs=9.2, bold=True)
    st = [("#0", "200K", "300K"), ("#1", "80K", "800K"), ("#2", "60K", "500K"), ("#3", "50K", "900K")]
    for i, (a, b, c2) in enumerate(st):
        y = 7.05 - i * 0.72
        fc = AMBER_L if i == 1 else "white"
        rc(ax, 5.7, y, 1.3, 0.62, a, fc=fc, ec=TEAL, fs=9.2, lw=1.0)
        rc(ax, 7.0, y, 1.3, 0.62, b, fc=fc, ec=TEAL, fs=9.2, lw=1.0)
        rc(ax, 8.3, y, 1.3, 0.62, c2, fc=fc, ec=TEAL, fs=9.2, lw=1.0)
    rk(ax, 5.3, 3.7, 3.9, 1.25, "两条检查线（必须都通过）：\n① 段号 S ≥ 段表长度M？\n② 段内偏移 W ≥ 段长C？\n任一出错 → 越界中断", fc=PURPLE_L, ec=PURPLE, fs=9.4)
    # 右：内存
    t(ax, 11.75, 9.05, "物理内存（段间可以不连续）", fs=11.5, bold=True, color=GREEN)
    kx, x0, wd = lambda k: 9.95 + k / 1000.0 * 3.6, 9.95, 3.6
    rc(ax, kx(0), 5.9, kx(1000) - kx(0), 2.0, "", fc=GRAY_L, ec=GRAY, lw=1.0)
    for (s, sz, lab, c) in [(0, "300K", "OS", GRAY), (300, "200K", "段0", BLUE), (500, "60K", "段2", GREEN),
                            (800, "80K", "段1", AMBER), (900, "50K", "段3", TEAL)]:
        rc(ax, kx(s), 5.9, kx(s + int(sz.replace("K", ""))) - kx(s), 2.0, f"{lab} {sz}",
           fc={"OS": GRAY_L, "段0": BLUE_L, "段1": AMBER_L, "段2": GREEN_L, "段3": TEAL_L}[lab],
           ec={"OS": GRAY, "段0": BLUE, "段1": AMBER, "段2": GREEN, "段3": TEAL}[lab], fs=10, lw=1.2)
    t(ax, 11.75, 5.4, "段1基址800K、段0基址300K：段间分散但段内连续；\n段与段之间的空隙 → 外部碎片（段长不等造成）", fs=8.8, color=GRAY)
    # 变换流程（一行）
    bk(ax, 1.85, 2.4, 2.7, 0.95, "① 取逻辑地址\n（段号S=1，偏移W=30K）", fc=BLUE_L, ec=BLUE, fs=9.2)
    al(ax, 3.2, 2.9, 3.9, 2.9, lw=2.0, ms=14)
    dm(ax, 5.2, 2.4, 2.35, 1.1, "② S ≥ 段表长度M？\n（M=4，S=1 → 不越界）", fc=AMBER_L, ec=AMBER, fs=8.6)
    al(ax, 6.38, 2.9, 7.05, 2.9, "成立", lw=2.0, ms=14, fs=8.6, dy=0.22)
    dm(ax, 8.35, 2.4, 2.35, 1.1, "③ W ≥ 段长C？\n（30K < 80K → 不越界）", fc=AMBER_L, ec=AMBER, fs=8.6)
    al(ax, 9.53, 2.9, 10.2, 2.9, "成立", lw=2.0, ms=14, fs=8.6, dy=0.22)
    bk(ax, 11.5, 2.4, 2.9, 0.95, "④ 物理地址\n= 基址 + 偏移\n= 800K + 30K = 830K", fc=GREEN_L, ec=GREEN, fs=9.4, bold=True)
    rk(ax, 0.5, 0.5, 6.4, 1.1,
       "【考点】分段是用户可见的（按段编程）；段便于共享：不同进程段表项指向同一段的同一基址\n保护：越界检查 + 存取权限（读/写/执行）",
       fc=GRAY_L, ec=GRAY, fs=8.8)
    rk(ax, 7.2, 0.5, 7.1, 1.1,
       "例2：(段号2, 偏移70K) → 70K ≥ 段长60K → 段内越界中断；例3：段号4 ≥ 段表长度4 → 段号越界中断\n（段号越界与偏移越界是两个独立检查，先查段号再查偏移）",
       fc=RED_L, ec=RED, fs=8.8)
    save_fig(fig, "ch3-10_segmentation")


# ============ ch3-11 分页 vs 分段 ============
def fig11():
    fig, ax = O.new_fig(14.8, 11.8, (0, 14.8), (0, 11.8))
    O.title(ax, "分页 vs 分段：目的不同 → 地址空间维数不同 → 碎片类型不同",
            "分页是“为了让内存更好用”（一维地址、对用户透明）；分段是“为了让程序更好用”（二维地址、用户可见）")
    # 左：分页
    bk(ax, 3.8, 10.0, 6.6, 0.62, "① 分页：把逻辑空间切成等大的页", fc=BLUE_L, ec=BLUE, fs=12.5, bold=True, color=BLUE)
    for i, y in enumerate([9.05, 8.15, 7.25, 6.35]):
        bk(ax, 3.8, y, 2.4, 0.68, f"页{i}（4KB）", fc=BLUE_L, ec=BLUE, fs=9.4)
    t(ax, 3.8, 5.75, "每页等大 → 地址跨度内天然对齐；\n页的大小固定 → 硬件自动拆页号/偏移", fs=9, color=GRAY)
    t(ax, 6.9, 7.7, "一维地址：0,1,2,…,N\n页号偏移是“硬件在背后拆的”", fs=9.4, ha="center", color=INK, bg="white")
    rk(ax, 0.5, 3.5, 6.7, 1.9,
       "分页的特点：\n· 目的：提高内存利用率（消除外部碎片）\n· 对用户透明：地址一维，用户不感知页\n· 碎片：最后一次装入可能不满 → 内部碎片\n· 缺点：不支持按逻辑单位/按需共享保护", fc=BLUE_L, ec=BLUE, fs=9.2)
    # 右：分段
    bk(ax, 11.0, 10.0, 6.6, 0.62, "② 分段：按程序逻辑单位切成不等的段", fc=GREEN_L, ec=GREEN, fs=12.5, bold=True, color=GREEN)
    for (y, hgt, lab) in [(9.05, 0.7, "段0 主程序 200K"), (8.2, 0.6, "段1 数据区 80K"), (7.4, 0.52, "段2 栈区 60K"), (6.62, 0.45, "段3 公用库 50K")]:
        bk(ax, 11.0, y, 2.4, hgt, lab, fc=GREEN_L, ec=GREEN, fs=8.8)
    t(ax, 11.0, 5.75, "段长度可变（由程序逻辑决定）；\n段内连续、段间可以不连续", fs=9, color=GRAY)
    t(ax, 14.0, 7.7, "二维地址：(段号S, 段内偏移W)", fs=9.4, ha="center", color=INK, bg="white")
    rk(ax, 7.7, 3.5, 6.7, 1.9,
       "分段的特点：\n· 目的：按逻辑单位组织，便于共享与保护\n· 用户可见：地址是二维的（段号+偏移）\n· 碎片：段长不等、段间零散 → 外部碎片\n· 优点：代码/数据可共享、存取保护灵活", fc=GREEN_L, ec=GREEN, fs=9.2)
    # 底部对比表
    tb = [("对比项", "分页", "分段"),
          ("划分目的", "提高内存利用率、消除外部碎片", "按程序逻辑单位组织，方便共享/保护"),
          ("地址空间维数", "一维（线性地址）", "二维（段号S + 段内偏移W）"),
          ("长度", "页面固定（2的整数次幂，常4KB）", "段长可变（由程序结构决定）"),
          ("碎片类型", "内部碎片（最后一页不满）", "外部碎片（段间空隙）"),
          ("对用户透明性", "透明（用户感知不到页的存在）", "用户可见（编程时按段管理）"),
          ("共享与保护", "不方便（难按逻辑边界共享）", "方便（以段为单位共享、存取控制）")]
    x0, y0, bh = 0.5, 2.95, 0.42
    widths = [2.7, 5.6, 5.6]
    for r, row in enumerate(tb):
        for cidx, cell in enumerate(row):
            fc = GRAY_L if r == 0 else ("white" if cidx == 0 else BLUE_L if cidx == 1 else GREEN_L)
            rc(ax, x0 + sum(widths[:cidx]) + 0.06 * cidx, y0 - r * bh, widths[cidx], bh,
               cell, fc=fc, ec=GRAY if r == 0 else O.INK, fs=8.8, bold=(r == 0 or cidx == 0), lw=1.0)
    save_fig(fig, "ch3-11_seg_vs_page")


# ============ ch3-12 段页式管理 ============
def fig12():
    fig, ax = O.new_fig(14.8, 9.8, (0, 14.8), (0, 9.8))
    O.title(ax, "段页式存储管理：先分段、每段再分页（兼顾共享保护与内存利用率）",
            "地址结构（32位示例）：段号S（8位）| 段内页号P（12位）| 页内偏移W（12位）——注意没有“段内位移”，只有“页内偏移”")
    # 地址条
    rc(ax, 0.7, 7.7, 2.9, 0.8, "段号 S (8位)", fc=PURPLE_L, ec=PURPLE, fs=10.5, bold=True)
    rc(ax, 3.6, 7.7, 4.3, 0.8, "段内页号 P (12位)", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
    rc(ax, 7.9, 7.7, 5.5, 0.8, "页内偏移 W (12位)", fc=AMBER_L, ec=AMBER, fs=10.5, bold=True)
    # 段表
    t(ax, 2.2, 7.35, "① 段表（每进程一张）", fs=10.4, bold=True, color=PURPLE)
    rc(ax, 0.7, 6.2, 1.5, 0.52, "段号", fc=GRAY_L, ec=GRAY, fs=9, bold=True)
    rc(ax, 2.2, 6.2, 1.5, 0.52, "页表长度", fc=GRAY_L, ec=GRAY, fs=9, bold=True)
    rc(ax, 3.7, 6.2, 1.6, 0.52, "页表始址", fc=GRAY_L, ec=GRAY, fs=9, bold=True)
    for i, (a, b, c2) in enumerate([("#0", "4页", "PT0"), ("#1", "8页", "PT1"), ("#2", "2页", "PT2")]):
        y = 5.52 - i * 0.5
        fc = AMBER_L if i == 1 else "white"
        rc(ax, 0.7, y, 1.5, 0.44, a, fc=fc, ec=PURPLE, fs=8.8, lw=1.0)
        rc(ax, 2.2, y, 1.5, 0.44, b, fc=fc, ec=PURPLE, fs=8.8, lw=1.0)
        rc(ax, 3.7, y, 1.6, 0.44, c2, fc=fc, ec=PURPLE, fs=8.8, lw=1.0)
    # 页表（段1）
    t(ax, 8.0, 7.35, "② 段1的页表（每段一张，可离散存放）", fs=10.4, bold=True, color=BLUE)
    rc(ax, 5.6, 6.2, 1.9, 0.52, "页号", fc=GRAY_L, ec=GRAY, fs=9, bold=True)
    rc(ax, 7.5, 6.2, 1.9, 0.52, "页框号", fc=GRAY_L, ec=GRAY, fs=9, bold=True)
    for i, (a, b) in enumerate([("0", "3"), ("1", "12"), ("2", "7"), ("3", "5"), ("4", "9")]):
        y = 5.52 - i * 0.5
        fc = AMBER_L if i == 2 else "white"
        rc(ax, 5.6, y, 1.9, 0.44, f"页{a}", fc=fc, ec=BLUE, fs=8.8, lw=1.0)
        rc(ax, 7.5, y, 1.9, 0.44, f"框{b}", fc=fc, ec=BLUE, fs=8.8, lw=1.0)
    # 内存
    t(ax, 12.7, 7.35, "③ 物理内存（页框）", fs=10.4, bold=True, color=GREEN)
    x0, y0, cs = 11.0, 6.7, 0.9
    for r in range(4):
        for c in range(4):
            idx = r * 4 + c
            fc, ec = (AMBER_L, AMBER) if idx == 7 else (GRAY_L, GRAY)
            rc(ax, x0 + c * cs, y0 - (r + 1) * cs, cs, cs, f"框{idx}", fc=fc, ec=ec, fs=7.6, lw=1.0)
    # 变换流程
    rk(ax, 0.7, 0.9, 13.6, 2.2,
       "【变换流程（一次访存=3次访存）】① 查段表得到该段的页表始址（访存①）→ ② 查段内页表得到页框号（访存②）→ ③ 物理地址 = 页框号×页大小 + 页内偏移W → ④ 按物理地址访存（访存③）\n"
       "【例】段号S=1，段内页号P=2，页内偏移W=2500；段1页表：页2→页框7 → 物理地址 = 7×4096+2500 = 31172\n"
       "【考点】段页式兼具分段（共享/保护）与分页（无外部碎片）优点；每段最多 2^12页×4KB=16MB；无TLB时EAT=3次访存，有TLB可降到1~3次。",
       fc=AMBER_L, ec=AMBER, fs=9.4)
    save_fig(fig, "ch3-12_seg_page")


# ============ ch3-13 局部性原理与虚拟内存 ============
def fig13():
    fig, ax = O.new_fig(14.8, 8.8, (0, 14.8), (0, 8.8))
    O.title(ax, "局部性原理 → 虚拟内存：为什么“程序不用全部装进内存”",
            "传统存储管理：一次性+驻留性 → 内存不够就装不下；局部性说明：没必要一次全装")
    # 左：代码与局部性
    t(ax, 3.6, 7.35, "例：C 程序循环（局部性的典型来源）", fs=11.5, bold=True, color=BLUE)
    rk(ax, 0.6, 3.6, 6.0, 3.5, "", fc=GRAY_L, ec=GRAY)
    t(ax, 3.6, 6.7, "int a[10000];", fs=10.5, ha="center", style="italic", color=INK)
    t(ax, 3.6, 5.95, "for (i = 0; i < 10000; i++)", fs=10.5, ha="center", style="italic", color=INK, bg="white")
    t(ax, 3.6, 5.2, "    a[i] = 0;", fs=10.5, ha="center", style="italic", color=INK, bg="white")
    t(ax, 3.6, 4.35, "循环体反复访问 i 和 a[i]：刚用过的又用；\na[i] 与 a[i+1] 相邻：用了一个接着用下一个", fs=9.2, color=GRAY)
    rk(ax, 0.6, 1.9, 6.0, 1.4, "时间局部性：刚被访问的单元不久后被再次访问\n空间局部性：刚被访问的单元其相邻单元即将被访问\n（两者都指向：内存中只要留“惯用的小集合”）",
       fc=BLUE_L, ec=BLUE, fs=9)
    rk(ax, 0.6, 0.35, 6.0, 1.2, "后果：装入时只按需调入“使用中的部分”，\n用不到的页放在外存（还省内存、易共享）",
       fc=GRAY_L, ec=GRAY, fs=9)
    # 右：虚拟内存
    t(ax, 10.9, 7.35, "虚拟存储的定义与容量", fs=11.5, bold=True, color=GREEN)
    rk(ax, 8.0, 3.1, 6.2, 4.2, "", fc=GREEN_L, ec=GREEN)
    t(ax, 11.1, 6.95, "虚拟地址空间（最大 2^地址位数）", fs=11, bold=True, color=GREEN)
    t(ax, 11.1, 6.3, "逻辑上：一个“很大”的地址空间\n（32位→4GB；64位→极大）", fs=9.4)
    rc(ax, 8.35, 3.6, 2.6, 1.9, "物理内存：只装常用页\n（内存 256MB）", fc=GREEN_L, ec=GREEN, fs=9.2)
    rc(ax, 11.3, 3.6, 2.85, 1.9, "外存/对换区（磁盘 100GB）\n存放暂不用的页", fc=AMBER_L, ec=AMBER, fs=9.2)
    al(ax, 11.28, 4.9, 11.0, 4.9, color=GREEN, lw=1.8, ms=13)
    al(ax, 11.0, 4.15, 11.26, 4.15, color=RED, lw=1.8, ms=13)
    t(ax, 11.14, 5.25, "换入", fs=8.6, color=GREEN, bold=True, bg="white")
    t(ax, 11.14, 3.75, "换出", fs=8.6, color=RED, bold=True, bg="white")
    rk(ax, 8.0, 0.5, 6.2, 2.3,
       "虚拟内存最大容量 = min(2^地址位数, 内存+外存之和)\n例如：32位地址、内存256MB、外存100GB\n→ 虚拟存储容量 = min(4GB, 100.25GB) = 4GB\n【三大特征】多次性（多次装入）、对换性（运行中换入换出）、虚拟性（逻辑上扩大了内存）",
       fc=AMBER_L, ec=AMBER, fs=9.4)
    save_fig(fig, "ch3-13_locality_vm")


# ============ ch3-14 请求分页的页表项 ============
def fig14():
    fig, ax = O.new_fig(14.2, 7.8, (0, 14.2), (0, 7.8))
    O.title(ax, "请求分页：页表项在“页框号”基础上扩展——P、A、M、外存地址",
            "基本分页只要页框号；请求分页还会“缺页”，所以必须知道：在不在内存？用过没？改过没？在哪张盘的什么地方")
    fields = [("外存地址", 4.4, AMBER, AMBER_L),
              ("修改位 M (1位)", 1.9, RED, RED_L),
              ("访问字段 A", 1.7, PURPLE, PURPLE_L),
              ("状态位 P (1位)", 1.7, TEAL, TEAL_L),
              ("页框号", 3.2, BLUE, BLUE_L)]
    x = 0.7
    for (nm, w0, c, cl) in fields:
        rc(ax, x, 5.6, w0, 0.9, nm, fc=cl, ec=c, fs=11, bold=True, lw=1.6)
        x += w0 + 0.15
    al(ax, 2.9, 5.52, 2.9, 4.95, color=INK, lw=1.5)
    al(ax, 5.2, 5.52, 5.2, 4.95, color=INK, lw=1.5)
    al(ax, 6.9, 5.52, 6.9, 4.95, color=INK, lw=1.5)
    al(ax, 8.6, 5.52, 8.6, 4.95, color=INK, lw=1.5)
    t(ax, 6.55, 4.6, "请把这四个新字段读成“一句话”：\nP：这页现在在不在内存？A：最近用过吗？M：被改过（脏）吗？外存地址：不在内存时它放在磁盘哪个位置？",
      fs=10.5, color=INK, bg="white")
    t(ax, 2.9, 4.2, "外存地址\n缺页时的调入来源", fs=8.2, color=AMBER, ha="center", ls=1.4)
    t(ax, 5.2, 4.2, "M=1：该页改过\n换出前要写回磁盘", fs=8.2, color=RED, ha="center", ls=1.4)
    t(ax, 6.9, 4.2, "A：访问次数/时间\n置换算法的依据", fs=8.2, color=PURPLE, ha="center", ls=1.4)
    t(ax, 8.6, 4.2, "P=1：在内存\nP=0：缺页中断", fs=8.2, color=TEAL, ha="center", ls=1.4)
    rk(ax, 0.7, 0.55, 12.9, 3.2,
       "【各字段作用速记表】\n"
       "状态位P：1=在内存; 0=不在内存（此时才可能发生缺页中断）——【考点】只有P=0才缺页;\n"
       "访问字段A：每次访问时硬件/OS 更新，置换算法据此淘汰“最久/最少用”的页;\n"
       "修改位M：1=被修改过（脏页/脏位、写回位）→换出时要写回磁盘，0=干净页可直接丢弃;\n"
       "外存地址：缺页时用于从磁盘把该页调入内存（调入的来源：磁盘对换区/文件区）。\n"
       "【易错】缺页中断发生后：先从外存读页→写内存→改P=1等页表项→重新执行被中断指令（见 ch3-15）",
       fc=GRAY_L, ec=GRAY, fs=9.8)
    save_fig(fig, "ch3-14_page_table_entry")


# ============ ch3-15 缺页中断处理全流程 ============
def fig15():
    fig, ax = O.new_fig(15.4, 13.6, (0, 15.4), (0, 13.6))
    O.title(ax, "缺页中断处理全流程：P=0 → 缺页中断 → 置换/调入 → 更新页表 → 重新执行被中断指令",
            "缺页中断 = 内中断中的“故障”(fault)：CPU在指令执行中途打断；处理完后重新执行同一条指令")
    X = 3.4
    def step(y, txt, fc=BLUE_L, ec=BLUE, fs=10.2, w=4.6, h=0.85):
        bk(ax, X, y, w, h, txt, fc=fc, ec=ec, fs=fs, z=5)
    def fl(y1, y2, lab=""):
        al(ax, X, y1 - 0.44, X, y2 + 0.44, text=lab, lw=2.0, ms=15)
    step(11.75, "① CPU 访问内存：执行“取数据”指令，\n发出一条逻辑地址（访存在指令执行中途发生）", fc=PINK_L, ec=PINK)
    fl(11.75, 10.7)
    step(10.7, "② 硬件拆分逻辑地址 → 页号P、偏移W，\n去查页表项（读状态位P）")
    fl(10.7, 9.7)
    dm(ax, X, 9.55, 4.4, 0.95, "③ 状态位 P = 1？\n（页在内存中？）", fc=AMBER_L, ec=AMBER, fs=9.6)
    al(ax, X + 2.24, 9.55, 8.85, 9.55, text="是", color=GREEN, lw=2.2, ms=16, dy=0.24, fs=10)
    rk(ax, 8.9, 8.95, 5.9, 1.2, "④ 正常路径：页框号f拼物理地址\n→ 访存①→访存② → 取数完成\n（基本地址变换，见 ch3-07）", fc=GREEN_L, ec=GREEN, fs=9.6)
    fl(9.55, 8.35, "否（P=0 缺页）")
    step(8.35, "④ 缺页中断（页在外存需重新调入；属于“故障型”\n内中断，可以恢复：处理完后重新执行该指令）", fc=RED_L, ec=RED, fs=9.8)
    fl(8.35, 7.25)
    step(7.25, "⑤ 保护现场：断点、寄存器、进程状态全部保存；\nOS缺页处理程序接管（转入内核态）", fc=PURPLE_L, ec=PURPLE, fs=9.8)
    fl(7.25, 6.15)
    step(6.15, "⑥ 查空闲页框表 + 读“外存地址”字段：\n确定该页在磁盘上的位置", fc=PURPLE_L, ec=PURPLE, fs=9.8)
    fl(6.15, 5.4)
    dm(ax, X, 5.05, 4.4, 0.95, "⑦ 有足够空闲页框？", fc=AMBER_L, ec=AMBER, fs=9.6)
    al(ax, X + 2.24, 5.05, 6.42, 5.05, text="否（需置换）", color=RED, lw=2.2, ms=16, dy=0.24, fs=9.4)
    fl(5.05, 3.85, "是（有空闲页框）")
    # 置换分支（右侧）
    rk(ax, 9.25, 5.05, 5.6, 1.0, "⑧ 页面置换：按置换算法(OPT/FIFO/LRU/CLOCK)\n选出“被淘汰的页”，其页表项P置0", fc=PURPLE_L, ec=PURPLE, fs=9.4)
    al(ax, 9.25, 4.54, 9.25, 4.28, lw=1.8, ms=13)
    dm(ax, 9.25, 3.75, 4.6, 0.95, "⑧′ 淘汰页的修改位 M = 1 ？", fc=AMBER_L, ec=AMBER, fs=9.4)
    al(ax, 6.95, 3.75, 5.78, 3.9, text="否：M=0 直接覆盖", color=GREEN, lw=1.8, ms=13, dy=0.34, fs=8.8)
    al(ax, 9.25, 3.27, 9.25, 3.44, lw=1.8, ms=13)
    rk(ax, 6.6, 2.55, 5.6, 0.85, "是：先写回磁盘（M=1 为脏页，写回后改 M=0）\n——否则丢失数据——然后执行调入", fc=PINK_L, ec=PINK, fs=9.2)
    al(ax, 6.58, 3.0, 5.78, 3.85, color=PINK, lw=1.8, ms=13)
    step(3.85, "⑨ 从外存调入该页到空闲/刚腾出的页框\n（磁盘I/O：进程被阻塞等待；从对换区调入更快）", fc=TEAL_L, ec=TEAL, fs=9.6)
    fl(3.85, 2.75)
    step(2.75, "⑩ 更新页表项：P=1、填入新页框号、A清零（记录访问）、\nM=0；同时把表项装入/刷新TLB", fc=TEAL_L, ec=TEAL, fs=9.6)
    fl(2.75, 1.65)
    step(1.65, "(11) 恢复现场，重新执行被中断的那条指令\n（不是下一条！）→ 此时P=1 → 正常访存取数", fc=GREEN_L, ec=GREEN, fs=9.8)
    # 回环
    al(ax, 0.8, 1.65, 0.8, 12.15, color=GREEN, lw=2.0, ls="--", ms=14)
    al(ax, 0.8, 12.15, 1.02, 12.15, color=GREEN, lw=2.0, ls="--", ms=14)
    t(ax, 0.45, 6.8, "重新访存（P=1→命中）", fs=9, color=GREEN, ha="center", rotation=90, bg="white")
    # 侧注
    rk(ax, 12.6, 10.75, 2.3, 1.5, "注意：一条指令可能引发多次缺页（如数据跨两个页框、指令跨页），每次都要重新执行该指令",
       fc=RED_L, ec=RED, fs=8.4)
    rk(ax, 12.75, 6.6, 2.15, 1.6, "缺页时机：地址变换/取指阶段，“故障”型内中断只读数据现；处理时进OS（内核态）",
       fc=GRAY_L, ec=GRAY, fs=8.4)
    rk(ax, 0.35, 0.15, 14.6, 0.75, "缺页率 = 缺页次数 / 访问总次数；缺页抖动 → CPU利用率骤降（见3.12节）；高频考点：置换算法选谁、是否写回、调入来源",
       fc=AMBER_L, ec=AMBER, fs=9.8)
    save_fig(fig, "ch3-15_page_fault_flow")


# ============ ch3-16 OPT/FIFO/LRU 三算法对比 ============
SEQ = [4, 3, 2, 1, 4, 3, 5, 4, 3, 2, 1, 5]

def sim_paging(alg, n):
    frames, out = [], []
    for i, x in enumerate(SEQ):
        hit = x in frames
        if hit:
            if alg == "LRU":
                frames.remove(x)
                frames.append(x)
            out.append((list(frames), True))
        else:
            if len(frames) < n:
                frames.append(x)
            else:
                if alg == "FIFO":
                    frames.pop(0)
                elif alg == "LRU":
                    frames.pop(0)
                elif alg == "OPT":
                    nxt = {}
                    for j in range(i, len(SEQ)):
                        if SEQ[j] in frames and SEQ[j] not in nxt:
                            nxt[SEQ[j]] = j
                    victim = max(frames, key=lambda p: nxt.get(p, 9999))
                    frames = [p for p in frames if p != victim]
                frames.append(x)
            out.append((list(frames), False))
    return out


def panel_grid(ax, x0, ytop, alg, title, colw=1.03, cw=None, hh=0.44):
    res = sim_paging(alg, 3)
    misses = sum(1 for _, h in res if not h)
    bk(ax, x0 + 6.18, ytop + 0.55, 12.3, 0.52, title, fc=GRAY_L, ec=GRAY,
       fs=11.5, bold=True, color=INK)
    for c, (x, hit) in enumerate(zip(SEQ, res)):
        t(ax, x0 + c * colw + colw / 2, ytop + 0.22, f"第{c+1}\n{x}", fs=7.6, color=GRAY)
    rows = [r[0] for r in res]
    n_frames = len(rows[0]) if rows else 0
    for r in range(3):
        y = ytop - 0.08 - r * hh
        for c in range(len(SEQ)):
            fc = "white"
            ec = GRAY
            txt = ""
            fs = 9
            snap = rows[c]
            if r < len(snap):
                txt = str(snap[r])
                ec = BLUE
            rc(ax, x0 + c * colw + 0.03, y - hh / 2, colw - 0.06, hh, txt,
               fc=fc, ec=ec, fs=9, bold=True, lw=1.0)
    y = ytop - 0.08 - 3 * hh - 0.30
    for c in range(len(SEQ)):
        hit = res[c][1]
        rc(ax, x0 + c * colw + 0.03, y, colw - 0.06, 0.34,
           "命" if hit else "缺",
           fc=GREEN_L if hit else RED_L, ec=GREEN if hit else RED, fs=8, lw=1.0,
           bold=True, color=GREEN if hit else RED)
    t(ax, x0 + 12.5, y + 0.17, f"缺页 {misses} 次 / 命中 {len(SEQ)-misses} 次 → 缺页率 {round(misses/len(SEQ)*100)}%",
      fs=9.6, ha="left", color=RED, bold=False, bg="white")


def fig16():
    fig, ax = O.new_fig(16.0, 10.8, (0, 16.0), (0, 10.8))
    O.title(ax, "OPT / FIFO / LRU 三算法对比：访问序列 4,3,2,1,4,3,5,4,3,2,1,5（3个页框）",
            "格子里 = 页框内容（上=最早装入/最久未用，下=最新）；行末统计缺页次数；绿=命中，红=缺页")
    panel_grid(ax, 0.9, 8.5, "OPT", "OPT 最佳置换：淘汰“将来最久不再使用/不再出现”的页（理论最优，不可实现）")
    panel_grid(ax, 0.9, 5.85, "FIFO", "FIFO 先进先出：淘汰最先进入内存的页（实现简单；可能发生 Belady 异常）")
    panel_grid(ax, 0.9, 3.2, "LRU", "LRU 最近最久未用：淘汰（最近）最久未被访问的页（栈式算法，无Belady异常；硬件开销大）")
    rk(ax, 1.1, 0.2, 14.2, 1.05,
       "结论：OPT 7次 < FIFO 9次 < LRU 10次——本题 LRU 反而最差！帧数增大时 LRU/OPT 的缺页数单调不增（栈式算法），而 FIFO 可能反常地增加（见下节 Belady 异常）。\n"
       "【易错】刷题最稳妥的办法：逐行手算（把每次访问后3个页框的内容写出来），不要背“LRU总是最好”的结论。",
       fc=AMBER_L, ec=AMBER, fs=9.4)
    save_fig(fig, "ch3-16_replacement_compare")


# ============ ch3-17 CLOCK 与改进CLOCK ============
def fig17():
    fig, ax = O.new_fig(14.0, 10.2, (0, 14.0), (0, 10.2))
    O.title(ax, "CLOCK（NRU）与改进型CLOCK：访问位+修改位 的循环扫描置换",
            "CLOCK=LRU的折中：用访问位A近似“最近用过没有”，循环扫描——只扫一圈，硬件开销小")
    import math
    # ---- 左：基本CLOCK ----
    t(ax, 3.3, 9.0, "① 基本CLOCK：循环链 + 访问位A", fs=12.5, bold=True, color=BLUE)
    cx, cy, r = 3.3, 5.9, 2.2
    ax.add_patch(O.Circle((cx, cy), r, fill=False, ec=GRAY, lw=1.4, ls="--", zorder=1))
    cells = [("页5", 1), ("页8", 0), ("页2", 1), ("页3", 0), ("页9", 1), ("页4", 1), ("页7", 0), ("页6", 1)]
    for i, (pg, a) in enumerate(cells):
        ang = math.pi / 2 - i * math.pi / 4
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        fc = BLUE_L if a == 1 else GRAY_L
        bk(ax, x, y, 1.5, 0.78, f"{pg}\nA={a}", fc=fc, ec=BLUE if a == 1 else GRAY, fs=9.2)
    al(ax, cx, cy, cx + r * 0.7 * math.cos(math.pi / 2 - 3 * math.pi / 4),
       cy + r * 0.7 * math.sin(math.pi / 2 - 3 * math.pi / 4), color=RED, lw=2.2, ms=16)
    t(ax, cx, cy - 0.42, "指针（停在“页3”上，A=0）", fs=9.4, color=RED, bold=True)
    rk(ax, 0.4, 0.45, 5.8, 2.7,
       "扫描规则（指针循环移动）：\n① 若 A=1：把它清成 A=0（“正在用”，先记下），指针后移，继续扫；\n"
       "② 若 A=0：立即置换该页，新页 A=1，指针后移；\n"
       "③ 一轮中若全是 A=1：相当于全清0后再扫，必找到 A=0；\n"
       "【本质】A=1 相当于“记录在案”，给它一次再生的机会。", fc=BLUE_L, ec=BLUE, fs=9.0)
    # ---- 右：改进CLOCK ----
    t(ax, 10.6, 9.0, "② 改进型CLOCK：同时考虑访问位A与修改位M", fs=12.5, bold=True, color=GREEN)
    g = [("页1", 1, 1), ("页2", 0, 1), ("页3", 0, 0), ("页4", 1, 0),
         ("页5", 1, 1), ("页6", 0, 0), ("页7", 0, 1), ("页8", 1, 0)]
    for i, (pg, a, m) in enumerate(g):
        x = 7.4 + (i % 4) * 1.45
        y = 8.05 - (i // 4) * 1.0
        fc = AMBER_L if (a, m) == (0, 0) else (RED_L if (a, m) == (0, 1) else (BLUE_L if (a, m) == (1, 0) else GRAY_L))
        bk(ax, x, y, 1.32, 0.8, f"{pg} (A={a},M={m})", fc=fc, ec=AMBER, fs=8.4)
    rk(ax, 7.35, 3.4, 6.1, 2.4,
       "扫描优先级（一轮扫描的动作）：\n① 第一轮：找 (A=0, M=0)——干净页优先淘汰（不产生写回I/O）；\n"
       "② 扫到 (A=1, *) → 只清 A=0，指针后移；\n③ 第二轮：找 (A=0, M=1)——脏页，淘汰时需写回；\n"
       "④ 若还找不到：再清一遍A，第三、四轮必能找到。", fc=AMBER_L, ec=AMBER, fs=9.0)
    rk(ax, 7.35, 0.55, 6.1, 1.5,
       "【考点】淘汰优先级：(0,0) → (0,1) → (1,0)（清A=0后再找）→ (1,1)（清A=0再找）。\n"
       "改进之处：优先淘汰“未修改”的干净页，减少写回I/O开销。", fc=GREEN_L, ec=GREEN, fs=9.0)
    save_fig(fig, "ch3-17_clock")


# ============ ch3-18 Belady 异常与抖动 ============
def mini_panel(ax, x0, ytop, n, title, colw=0.78):
    res = sim_paging("FIFO", n)
    misses = sum(1 for _, h in res if not h)
    t(ax, x0 - 0.15, ytop + 0.72, title, fs=11, bold=True, color=BLUE, ha="left")
    t(ax, x0 + 12 * colw + 0.25, ytop + 0.72, f"缺页 {misses} 次", fs=11, color=RED, bold=True, ha="left")
    for c in range(len(SEQ)):
        t(ax, x0 + c * colw + colw / 2, ytop + 0.32, f"{SEQ[c]}", fs=8.2, color=INK)
    for r in range(n):
        y = ytop - 0.04 - r * 0.42
        for c in range(len(SEQ)):
            snap = res[c][0]
            txt = str(snap[r]) if r < len(snap) else ""
            rc(ax, x0 + c * colw + 0.03, y - 0.19, colw - 0.06, 0.38, txt,
               fc="white", ec=BLUE, fs=8.4, bold=True, lw=1.0)
    y = ytop - 0.04 - n * 0.42
    for c in range(len(SEQ)):
        hit = res[c][1]
        rc(ax, x0 + c * colw + 0.03, y, colw - 0.06, 0.32,
           "命" if hit else "缺",
           fc=GREEN_L if hit else RED_L, ec=GREEN if hit else RED, fs=7.6, lw=1.0,
           bold=True, color=GREEN if hit else RED)
    return misses


def fig18():
    fig, ax = O.new_fig(15.8, 9.7, (0, 15.8), (0, 9.7))
    O.title(ax, "Belady 异常（左）与 抖动/工作集（右）",
            "同一访问序列：FIFO 3帧缺页9次 < 4帧缺页10次 —— 帧数增加，缺页反而变多；右侧：为何多道程度不能一味提高")
    t(ax, 4.9, 8.95, "左：FIFO 3帧 vs 4帧（红三角列=4帧反而多缺页的访问：第8、9、12次）", fs=9.8, color=RED, ha="center")
    mini_panel(ax, 0.55, 7.6, 4, "FIFO：4个页框")
    mini_panel(ax, 0.55, 4.9, 3, "FIFO：3个页框")
    for c in (7, 8, 11):
        t(ax, 0.55 + c * 0.78 + 0.39, 8.62, "▲", fs=10, color=RED, bold=True)
    rk(ax, 0.45, 2.5, 9.75, 0.75,
       "结论：3帧缺页9次 < 4帧缺页10次 → Belady异常：FIFO算法帧数增加缺页数反而增加（LRU/OPT等栈式算法不存在）",
       fc=RED_L, ec=RED, fs=9.4)
    rk(ax, 0.45, 0.5, 9.75, 1.75,
       "为何？FIFO 只看“谁先进来”，把常用页也不小心换出；\n"
       "【考点】判断是否栈式算法：LRU、OPT 的驻留集随帧数增加只增不减（栈式）；FIFO 非栈式→有Belady异常。\n"
       "缺页率 = 缺页次数 / 访问总次数。", fc=GRAY_L, ec=GRAY, fs=9.2)
    # ---- 右：抖动曲线 ----
    al(ax, 11.05, 2.0, 15.55, 2.0, lw=1.8, ms=12, color=INK)
    al(ax, 11.05, 2.0, 11.05, 8.9, lw=1.8, ms=12, color=INK)
    t(ax, 15.2, 1.75, "多道程序度", fs=9.2, color=INK)
    t(ax, 10.75, 5.4, "CPU\n利用率", fs=9.2, color=INK, rotation=90)
    pts = [(11.5, 1.9), (12.15, 4.3), (12.8, 6.8), (13.45, 8.0), (14.1, 6.8), (14.75, 4.0), (15.4, 1.9)]
    ln(ax, *pts[0], *pts[1], color=BLUE, lw=2.4)
    for i in range(1, len(pts) - 1):
        ln(ax, *pts[i], *pts[i + 1], color=BLUE, lw=2.4)
    for p in pts:
        O.circle(ax, p[0], p[1], 0.075, "", fc=BLUE, ec=BLUE, z=5)
    t(ax, 13.45, 8.45, "峰值：道数再增→每进程帧数不足", fs=8.4, color=GRAY, ha="center")
    t(ax, 13.45, 7.9, "→频繁缺页→CPU利用率骤降", fs=8.4, color=GRAY, ha="center")
    t(ax, 14.6, 5.0, "抖动区", fs=12, bold=True, color=RED)
    ax.add_patch(O.Ellipse((14.6, 4.6), 1.7, 4.6, fill=False, ec=RED, lw=1.6, ls="--", zorder=1))
    rk(ax, 11.05, 0.32, 4.6, 1.35,
       "工作集模型：窗口Δ内实际访问过的页面集合；\n常驻集 ≥ 工作集 → 进程才顺畅；\n防抖措施：适度降低多道程序度（挂起进程）/ 给进程足够帧数。",
       fc=AMBER_L, ec=AMBER, fs=8.6)
    save_fig(fig, "ch3-18_belady_thrift")


# ============ ch3-19 全链路综合地址变换总图 ============
def fig19():
    fig, ax = O.new_fig(16.0, 13.6, (0, 16.0), (0, 13.6))
    O.title(ax, "全链路总图：一次访存的完整旅程（TLB → 页表 → 缺页 → 置换 → 回写 → 重执行）",
            "绿色=快路径（绝大多数访存）；蓝色=页表；红色=缺页；紫色=置换；黑色/粉色=外存")
    X, Y = 2.75, 8.0  # A/B 竖列中心
    def st(cx, cy, txt, w, h, fc, ec, fs=9.6):
        bk(ax, cx, cy, w, h, txt, fc=fc, ec=ec, fs=fs, z=5)
    def fld(y1, y2, lab=""):
        al(ax, X, y1 - 0.42, X, y2 + 0.42, text=lab, lw=2.0, ms=15)
    # A 列
    st(X, 12.15, "① 进程访存：CPU发出逻辑地址A\n（用户态的一次取数据/取指令）", 4.2, 0.95, PINK_L, PINK)
    fld(12.15, 11.25)
    st(X, 11.25, "② 硬件拆分地址：页号P、偏移W\n（与此同时 并行查找TLB）", 4.2, 0.95, BLUE_L, BLUE)
    fld(11.25, 9.9)
    dm(ax, X, 9.85, 4.2, 1.0, "③ 快表 TLB 命中？\n（命中率 h 一般>99%）", fc=AMBER_L, ec=AMBER, fs=9.6)
    # 命中 → 右侧绿块
    al(ax, X + 2.13, 9.85, 5.75, 9.85, text="命中", color=GREEN, lw=2.2, ms=16, dy=0.26, fs=10)
    st(8.05, 9.85, "④ 命中：直接得页框号f\n⑤ 物理地址 = f×4096+W\n⑥ 访存取数 → 完成（只差一次访存）", 4.5, 1.05, GREEN_L, GREEN, fs=9.4)
    # 未命中 → B列
    fld(9.85, 8.75, "未命中")
    st(8.05, 8.75, "⑦ 未命中TLB：查内存中的多级页表\n（顶级→二级页表：访存①+②），并准备更新TLB", 4.6, 0.9, BLUE_L, BLUE, fs=9.4)
    fld(8.75, 7.35)
    dm(ax, 8.05, 7.35, 4.4, 0.95, "⑧ 页表项 状态位P = 1？", fc=AMBER_L, ec=AMBER, fs=9.8)
    fld(7.35, 6.25, "是（页在内存）")
    st(8.05, 6.25, "⑨ 得页框号f → 物理地址=f×4096+W\n→ 访存取数（访存③④）→ 完成；同时把表项装进TLB", 4.6, 0.9, GREEN_L, GREEN, fs=9.4)
    fld(6.25, 5.25, "否（P=0 缺页）")
    st(8.05, 5.25, "⑩ 缺页中断（故障型·可恢复）→ 保护现场；\n进程被阻塞等待I/O；OS转入内核态处理", 4.6, 0.9, RED_L, RED, fs=9.4)
    fld(5.25, 4.35)
    st(8.05, 4.35, "(11) 查“该页外存地址”字段 + 空闲页框表", 4.6, 0.8, PURPLE_L, PURPLE, fs=9.5)
    fld(4.35, 3.45)
    dm(ax, 8.05, 3.45, 4.2, 0.9, "(12) 有空闲页框？", fc=AMBER_L, ec=AMBER, fs=9.8)
    fld(3.45, 2.45, "是")
    st(8.05, 2.45, "(15) 从外存/对换区调入该页\n（磁盘I/O：毫秒级，最慢的一步）", 4.6, 0.85, TEAL_L, TEAL, fs=9.4)
    fld(2.45, 1.45)
    st(8.05, 1.45, "(16) 更新页表项：P=1、页框号、M=0、\n刷新A；同时更新TLB", 4.6, 0.85, TEAL_L, TEAL, fs=9.4)
    fld(1.45, 0.55)
    st(8.05, 0.55, "(17) 恢复现场 → 重新执行被中断的指令\n（此时P=1→命中通道）→ 完成", 4.6, 0.85, GREEN_L, GREEN, fs=9.4)
    # C 列：置换/回写
    al(ax, 10.15, 3.45, 11.05, 3.45, text="否（无空闲页框）", color=PURPLE, lw=2.2, ms=16, dy=0.0, fs=9.2)
    st(13.15, 3.45, "(13) 页面置换：按算法选淘汰页\n（CLOCK/LRU/FIFO…）；其页表项P置0", 4.3, 0.85, PURPLE_L, PURPLE, fs=9.2)
    al(ax, 13.15, 3.0, 13.15, 2.85, lw=1.8, ms=13)
    dm(ax, 13.15, 2.35, 4.2, 0.9, "(14) 淘汰页修改位 M = 1 ？", fc=AMBER_L, ec=AMBER, fs=9.4)
    al(ax, 13.15, 1.86, 13.15, 1.75, lw=1.8, ms=13)
    st(13.15, 1.3, "M=1：先写回磁盘（改M=0）\nM=0：干净页 直接覆盖", 4.3, 0.85, PINK_L, PINK, fs=9.2)
    al(ax, 11.0, 1.3, 10.38, 2.3, text="然后调入", color=PINK, lw=2.0, ms=14, dx=-0.1, dy=0.0, fs=9)
    # 回环（重新执行）
    ln(ax, 5.75, 0.55, 0.62, 0.55, color=GREEN, lw=2.0, ls="--")
    ln(ax, 0.62, 0.55, 0.62, 12.3, color=GREEN, lw=2.0, ls="--")
    al(ax, 0.62, 12.3, 0.72, 12.3, color=GREEN, lw=2.0, ls="--", ms=14)
    t(ax, 0.33, 6.2, "缺页处理后：重新执行被中断的指令（不是下一条！）", fs=8.8, color=GREEN, rotation=90, bg="white")
    # 右侧注释
    rk(ax, 12.4, 9.15, 3.4, 2.2, "时间尺度对比：\n· TLB命中：t+m ≈ 120ns\n· 未命中：t+2m ≈ 220ns\n· 缺页处理：毫秒级（磁盘I/O）\n→ 快表命中率是性能关键",
       fc=GRAY_L, ec=GRAY, fs=9.2)
    rk(ax, 12.4, 5.6, 3.4, 1.7, "【考点】\n· 一次访存的访存次数：\n  单级页表2次/两级3次；\n· TLB命中率≥99%时，\n  EAT≈ t+m，接近最优。", fc=AMBER_L, ec=AMBER, fs=9.2)
    rk(ax, 10.85, 0.12, 5.05, 0.7,
       "本图串联全章：3.4分页 → 3.5快表 → 3.6多级页表 →\n3.10请求分页(缺页) → 3.11置换 → 3.12抖动与工作集",
       fc=GRAY_L, ec=GRAY, fs=8.6)
    save_fig(fig, "ch3-19_full_translation")


if __name__ == "__main__":
    for name, fn in [
        ("ch3-00_chapter_map", fig00), ("ch3-01_memory_hierarchy", fig01),
        ("ch3-02_loading_linking", fig02), ("ch3-03_swap_cover", fig03),
        ("ch3-04_partition_algorithms", fig04), ("ch3-05_paging_basics", fig05),
        ("ch3-06_page_address", fig06), ("ch3-07_paging_translation", fig07),
        ("ch3-08_tlb", fig08), ("ch3-09_two_level", fig09),
        ("ch3-10_segmentation", fig10), ("ch3-11_seg_vs_page", fig11),
        ("ch3-12_seg_page", fig12), ("ch3-13_locality_vm", fig13),
        ("ch3-14_page_table_entry", fig14), ("ch3-15_page_fault_flow", fig15),
        ("ch3-16_replacement_compare", fig16), ("ch3-17_clock", fig17),
        ("ch3-18_belady_thrift", fig18), ("ch3-19_full_translation", fig19),
    ]:
        fn()
        print("done:", name)
    print("---- 校验：置换算法统计 ----")
    for alg in ("OPT", "FIFO", "LRU"):
        r3 = sim_paging(alg, 3)
        r4 = sim_paging("FIFO", 4)
        m3 = sum(1 for _, h in r3 if not h)
        print(alg, "3帧缺页:", m3)
    r4 = sim_paging("FIFO", 4)
    print("FIFO 4帧缺页:", sum(1 for _, h in r4 if not h))










