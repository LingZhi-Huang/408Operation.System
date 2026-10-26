# -*- coding: utf-8 -*-
"""第4章 插图 第一部分：ch4-00 ~ ch4-06"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (new_fig, rbox, box, rect, diamond, ellipse, circle, arrow,
                   line, tx, title, save, INK, BLUE, BLUE_L, GREEN, GREEN_L,
                   AMBER, AMBER_L, RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L,
                   GRAY, GRAY_L, PINK, PINK_L)

FDIR = "/Users/levi/IdeaProjects/操作系统/第4章_文件管理/figures/"


def f00():
    fig, ax = new_fig(15, 10, (0, 15), (0, 10))
    title(ax, "第4章 文件管理 · 知识框架导图",
          "从文件的定义到磁盘调度：一张图串起全章四条主线", y=9.45)
    # 中心
    circle(ax, 7.5, 5.15, 0.85, "文件\n管理系统", fc=AMBER_L, ec=AMBER, fs=12)
    qs = [(3.7, 7.15), (11.3, 7.15), (3.7, 2.75), (11.3, 2.75)]
    starts = [(6.9, 5.75), (8.1, 5.75), (6.9, 4.55), (8.1, 4.55)]
    for (qx, qy), (sx, sy) in zip(qs, starts):
        arrow(ax, sx, sy, qx, qy, color=GRAY, lw=1.6, shrink=10)
    # 四象限
    rbox(ax, 0.4, 5.75, 6.6, 3.0, fc=BLUE_L, ec=BLUE)
    tx(ax, 0.75, 8.35, "4.1–4.2  文件基本概念与逻辑结构", fs=12, bold=True, color=BLUE, ha="left")
    tx(ax, 0.75, 7.35,
       "· 文件定义 / 属性 / FCB\n· 打开与关闭（引用计数）\n· 逻辑结构：顺序文件、索引文件、\n  索引顺序文件（N/2 → √N）\n· 无结构文件（流式文件）",
       fs=10.5, ha="left", color=INK)
    rbox(ax, 8.0, 5.75, 6.6, 3.0, fc=PINK_L, ec=PINK)
    tx(ax, 8.35, 8.35, "4.3  文件的物理结构（本章重点 ★）", fs=12, bold=True, color=PINK, ha="left")
    tx(ax, 8.35, 7.35,
       "· 连续分配：随机快 / 扩展难 / 碎片\n· 隐式链接：只能顺序 / 断链风险\n· 显式链接 FAT：表驻内存，1 次访盘\n· 索引分配 / 链接·多层·混合索引\n· UNIX 混合索引（必考计算题）",
       fs=10.5, ha="left", color=INK)
    rbox(ax, 0.4, 1.05, 6.6, 3.3, fc=GREEN_L, ec=GREEN)
    tx(ax, 0.75, 3.95, "4.4–4.6  目录 · 共享 · 保护", fs=12, bold=True, color=GREEN, ha="left")
    tx(ax, 0.75, 2.95,
       "· 目录：FCB 与索引结点 inode\n  目录项瘦身与检索效率\n· 目录结构演进：单级→两级→\n  树形→无环图\n· 共享：硬链接 vs 软链接\n· 保护：口令 / 加密 / 访问控制",
       fs=10.5, ha="left", color=INK)
    rbox(ax, 8.0, 1.05, 6.6, 3.3, fc=PURPLE_L, ec=PURPLE)
    tx(ax, 8.35, 3.95, "4.7–4.11  外存与磁盘管理", fs=12, bold=True, color=PURPLE, ha="left")
    tx(ax, 8.35, 2.95,
       "· 文件系统层次结构（逐层判断考点）\n· 空闲空间：空闲表/链 → 位示图 →\n  成组链接（必考计算）\n· 磁盘结构 / CHS / 读写时间（计算）\n· 磁盘调度：FCFS·SSTF·SCAN·LOOK·\n  C-SCAN·C-LOOK（必考计算题 ★）\n· RAID 0 / 1 / 5",
       fs=10.5, ha="left", color=INK)
    tx(ax, 7.5, 0.45,
       "计算题四大题型：① 混合索引访盘次数  ② 位示图(字号,位号)互算盘块号  ③ 成组链接分配/回收  ④ 磁盘时间与调度寻道距离",
       fs=11.5, bold=True, color=RED)
    save(fig, FDIR + "ch4-00_chapter_map.png")


def f01():
    fig, ax = new_fig(15, 9.6, (0, 15), (0, 9.6))
    title(ax, "文件、FCB 与文件的基本操作",
          "文件 = 一组信息项的有序集合；FCB = 文件存在的唯一标志；打开文件表 = 避免反复检索目录", y=9.1)
    # ---- 面板A：文件定义与属性
    rbox(ax, 0.4, 5.3, 4.7, 3.4, fc=BLUE_L, ec=BLUE)
    tx(ax, 2.75, 8.35, "① 文件的定义与常用属性", fs=12.5, bold=True, color=BLUE)
    tx(ax, 2.75, 7.55, "文件：具有文件名的一组相关信息的集合\n外存存储，按名存取，读写以块为单位",
       fs=10, color=INK)
    attrs = [("名称", "用户按名存取的依据"), ("标识符", "系统内部唯一编号"),
             ("类型", "普通/目录/设备…"), ("位置", "指向盘块的指针"),
             ("大小", "文件长度(字节/块)"), ("保护", "读写执行权限"),
             ("时间", "创建/修改/存取")]
    for i, (k, v) in enumerate(attrs):
        cx = 0.6 + (i % 2) * 2.25
        cy = 6.75 - (i // 2) * 0.52
        rect(ax, cx, cy, 2.15, 0.45, "", fc=GRAY_L, ec=GRAY, lw=1.0)
        tx(ax, cx + 1.07, cy + 0.22, k + "：" + v, fs=8.6, color=INK)
    # ---- 面板B：FCB
    rbox(ax, 5.3, 5.3, 4.7, 3.4, fc=GREEN_L, ec=GREEN)
    tx(ax, 7.65, 8.35, "② 文件控制块 FCB", fs=12.5, bold=True, color=GREEN)
    tx(ax, 7.65, 7.62, "FCB 中保存文件的全部管理信息，建立文件时\n首先生成 FCB；目录 = FCB 的集合", fs=9.6, color=INK)
    fcb = [("文件名", "按名存取"), ("类型", "普通/目录"), ("物理位置", "首块号/索引块号"),
           ("大小", "当前长度"), ("存取权限", "读/写/执行"), ("时间", "建/改/存取")]
    for i, (k, v) in enumerate(fcb):
        cy = 6.85 - i * 0.46
        rect(ax, 5.55, cy, 2.1, 0.4, "", fc=GRAY_L, ec=GRAY, lw=1.0)
        tx(ax, 6.6, cy + 0.2, k, fs=9.2, bold=True)
        rect(ax, 7.72, cy, 2.1, 0.4, "", fc=AMBER_L, ec=AMBER, lw=1.0)
        tx(ax, 8.77, cy + 0.2, v, fs=9.2)
    # ---- 面板C：打开文件表
    rbox(ax, 10.2, 5.3, 4.4, 3.4, fc=PURPLE_L, ec=PURPLE)
    tx(ax, 12.4, 8.35, "③ 打开文件表与引用计数", fs=12.5, bold=True, color=PURPLE)
    tx(ax, 12.4, 7.7, "open() 时：检索目录表，把目录项/FCB 调入内存\n建立（或复用）打开文件表项", fs=9.3, color=INK)
    # 表项
    rect(ax, 10.45, 6.55, 3.9, 0.5, "", fc=BLUE_L, ec=BLUE, lw=1.2)
    tx(ax, 12.4, 6.8, "打开文件表项：读/写指针 | 引用计数 = 2 | 文件号、路径", fs=9.0, bold=True)
    rbox(ax, 10.55, 5.72, 1.75, 0.55, "进程 P1", fc=GRAY_L, ec=GRAY, fs=10)
    rbox(ax, 12.45, 5.72, 1.75, 0.55, "进程 P2", fc=GRAY_L, ec=GRAY, fs=10)
    arrow(ax, 11.4, 6.28, 12.0, 6.55, color=PURPLE, lw=1.5)
    arrow(ax, 13.3, 6.28, 12.75, 6.55, color=PURPLE, lw=1.5)
    tx(ax, 12.4, 5.42, "同一文件被 2 个进程打开 → 引用计数 = 2", fs=9.3, color=PURPLE, bold=True)
    # ---- 下排：基本操作流程图
    tx(ax, 7.5, 4.55, "文件的基本操作：打开 / 关闭 / 读 / 写 / 创建 / 删除", fs=13, bold=True)
    steps = [
        ("① 创建", "申请一个 FCB → 磁盘空闲块\n并写入目录（在目录中登记）"),
        ("② 打开", "按文件名查目录，找到 FCB\n把 FCB 调入内存建立表项"),
        ("③ 读 / 写", "查打开文件表定位文件\n按逻辑块号进行块级读写"),
        ("④ 关闭", "引用计数 -1；计数为 0\n撤销该打开文件表项"),
        ("⑤ 删除", "从目录中删去 FCB、收回\n全部数据块（空闲表/图登记）"),
    ]
    for i, (h, t) in enumerate(steps):
        x = 0.5 + i * 2.9
        rbox(ax, x, 1.85, 2.65, 2.0, "", fc=BLUE_L, ec=BLUE)
        tx(ax, x + 1.32, 3.55, h, fs=12, bold=True, color=BLUE)
        tx(ax, x + 1.32, 2.65, t, fs=9.0, color=INK)
        if i < 4:
            arrow(ax, x + 2.68, 2.85, x + 2.88, 2.85, color=GRAY, lw=1.8)
    tx(ax, 7.5, 1.1,
       "要点：① 读/写之前必须先打开（系统调用参数 = 文件名 + 操作类型，返回文件描述符 fd）；② 打开 ≠ 读出数据，只是把目录项信息调入内存；"
       "③ 引用计数机制：多个进程同时打开同一文件时不必重复检索目录。",
       fs=10, color=RED)
    tx(ax, 7.5, 0.45, "【记忆口诀】打开借户口、关闭销户口；先开后读、各算各（计数）。",
       fs=11, bold=True, color=INK)
    save(fig, FDIR + "ch4-01_file_basics.png")


def f02():
    fig, ax = new_fig(15, 9.4, (0, 15), (0, 9.4))
    title(ax, "文件的逻辑结构",
          "逻辑结构 = 从用户/程序角度看记录的组织方式：顺序文件 → 索引文件 → 索引顺序文件", y=8.9)
    # Q1 定长顺序文件
    rbox(ax, 0.4, 5.15, 7.2, 3.4, fc=BLUE_L, ec=BLUE)
    tx(ax, 3.95, 8.15, "① 定长顺序文件（每条记录等长）", fs=12.5, bold=True, color=BLUE)
    for i in range(6):
        rect(ax, 0.6 + i * 1.18, 6.95, 1.08, 0.75, "R%d" % (i + 1), fc=BLUE_L, ec=BLUE, fs=10.5)
    rect(ax, 0.6, 6.05, 6.8, 0.62, "", fc=AMBER_L, ec=AMBER, lw=1.2)
    tx(ax, 4.0, 6.36, "第 i 条记录地址 = 首地址 + (i-1)×L        → 可直接定位", fs=10.5, bold=True)
    tx(ax, 3.95, 5.5, "· 定长 → 支持随机存取（O(1) 定位）· 增删需移动大量记录、效率低\n· 记录按写入先后组织 = 串结构；按关键字有序 = 顺序结构（折半查找更快）",
       fs=9.6, ha="center")
    # Q2 变长顺序文件
    rbox(ax, 7.9, 5.15, 7.2, 3.4, fc=TEAL_L, ec=TEAL)
    tx(ax, 11.5, 8.15, "② 变长顺序文件（记录长度不固定）", fs=12.5, bold=True, color=TEAL)
    widths = [1.5, 1.0, 1.35, 0.8, 1.15]
    x = 8.1
    for i, w in enumerate(widths):
        rect(ax, x, 6.95, w, 0.75, "R%d" % (i + 1), fc=TEAL_L, ec=TEAL, fs=10)
        x += w + 0.18
    tx(ax, 11.5, 6.3, "记录长度不一 → 无法由公式直接算出第 i 条的地址", fs=10, bold=True, color=TEAL)
    tx(ax, 11.5, 5.5,
       "· 只能顺序存取：读到第 i 条需先扫过前 i-1 条\n· 查找慢；增删记录后往往需要移动/重写大量数据\n· 常配合下一节的【索引文件】使用",
       fs=9.6)
    # Q3 索引文件
    rbox(ax, 0.4, 0.9, 7.2, 3.7, fc=GREEN_L, ec=GREEN)
    tx(ax, 3.95, 4.2, "③ 索引文件（为变长记录建索引表）", fs=12.5, bold=True, color=GREEN)
    tx(ax, 1.75, 3.8, "索引表", fs=10.5, bold=True)
    keys = [("关键字", "地址"), ("K1", "R1→"), ("K2", "R2→"), ("K3", "R3→"), ("K4", "R4→")]
    for i, (a, b) in enumerate(keys):
        cy = 3.4 - i * 0.5
        rect(ax, 0.65, cy, 1.15, 0.42, a, fc=GRAY_L, ec=GRAY, fs=9.2, lw=1.0)
        rect(ax, 1.88, cy, 1.15, 0.42, b, fc=GREEN_L, ec=GREEN, fs=9.2, lw=1.0)
    tx(ax, 4.35, 3.9, "数据区（变长记录，地址+长度定位）", fs=10.5, bold=True)
    dlen = [1.0, 0.75, 1.1, 0.8]
    x = 3.35
    for i, w in enumerate(dlen):
        arrow(ax, 3.0, 3.3 - i * 0.5, x + 0.9, 3.3 - i * 0.5, color=GREEN, lw=1.2)
        rect(ax, x, 3.08 - i * 0.5, w, 0.45, "R%d" % (i + 1), fc=GREEN_L, ec=GREEN, fs=8.6, lw=1.0)
        x += w + 0.25
    tx(ax, 3.95, 1.25,
       "· 索引表按关键字排序 → 折半查找，检索速度快\n· 增删记录只需改索引表，不必移动数据\n· 代价：索引表本身占用额外磁盘空间",
       fs=9.6)
    # Q4 索引顺序文件
    rbox(ax, 7.9, 0.9, 7.2, 3.7, fc=PINK_L, ec=PINK)
    tx(ax, 11.5, 4.2, "④ 索引顺序文件（大文件的折中方案）", fs=12.5, bold=True, color=PINK)
    tx(ax, 11.5, 3.72, "N = 100 条记录 → 分成 √N = 10 组，每组 10 条（组内顺序，组间有序）", fs=9.6)
    for g in range(5):
        x = 8.15 + g * 1.38
        rect(ax, x, 2.15, 1.28, 1.15, "", fc=PINK_L, ec=PINK, lw=1.1)
        tx(ax, x + 0.64, 2.78, "组%d" % (g + 1), fs=9.0, bold=True, color=PINK)
        tx(ax, x + 0.64, 2.45, "记录 1~10", fs=7.5)
        if g < 4:
            arrow(ax, x + 1.3, 3.9, x + 1.36, 3.9, color=PINK, lw=1.2)
    tx(ax, 11.5, 1.78, "索引表（每组 1 行）：只存每条组记录的【最大关键字 + 起始地址】", fs=9.2)
    tx(ax, 11.5, 1.25,
       "查找 = 先查索引表（平均 √N/2 = 5 次）再组内顺序（平均 √N/2 = 5 次）\n→ 总平均比较 ≈ √N = 10 次，而纯顺序文件需 N/2 = 50 次",
       fs=9.6, bold=True, color=RED)
    save(fig, FDIR + "ch4-02_logical_structures.png")


def f03():
    fig, ax = new_fig(14, 8.8, (0, 14), (0, 8.8))
    title(ax, "连续分配：文件块在磁盘上连续存放",
          "连续分配 = 为文件分配一组相邻的物理盘块；目录项只需记录（起始块号，长度）", y=8.3)
    tx(ax, 7.0, 7.45, "磁盘块序列（块号标在格内，横向展开盘的逻辑编址）", fs=11, bold=True)
    x = 0.55
    for i in range(16):
        if 3 <= i <= 7:
            fc, ec, txt = BLUE_L, BLUE, "A%d" % (i - 3)
        elif 10 <= i <= 12:
            fc, ec, txt = GREEN_L, GREEN, "B%d" % (i - 10)
        else:
            fc, ec, txt = GRAY_L, GRAY, "空"
        rect(ax, x, 6.35, 0.78, 0.95, txt + "\n" + str(i), fc=fc, ec=ec, fs=8.0, lw=1.2)
        x += 0.81
    rect(ax, 0.55, 5.75, 6.6, 0.5, "", fc=BLUE_L, ec=BLUE, lw=1.0)
    tx(ax, 3.85, 6.0, "文件 A：起始块号 3，长度 5 块", fs=10, bold=True)
    rect(ax, 7.6, 5.75, 5.6, 0.5, "", fc=GREEN_L, ec=GREEN, lw=1.0)
    tx(ax, 10.4, 6.0, "文件 B：起始块号 10，长度 3 块", fs=10, bold=True)
    tx(ax, 7.0, 5.32, "▲ 块 8、9、13、14、15 是零散的空闲块——不能被大文件利用，这就是【外部碎片】",
       fs=10, color=RED, bold=True)
    rect(ax, 0.55, 4.3, 12.9, 0.82, "", fc=AMBER_L, ec=AMBER, lw=1.4)
    tx(ax, 7.0, 4.71,
       "随机访问公式：物理块号 = 起始块号 + 逻辑块号          →  读任意第 i 块只需 1 次访盘（直接定位 O(1)）",
       fs=12, bold=True)
    tx(ax, 7.0, 3.98, "目录项 & 索引简单：FCB 中只存（起始块号，长度）；既支持顺序存取，也支持随机存取",
       fs=10)
    # 优缺点
    rbox(ax, 0.4, 0.75, 6.6, 3.0, fc=GREEN_L, ec=GREEN)
    tx(ax, 0.75, 3.4, "√ 连续分配的优点", fs=12, bold=True, color=GREEN, ha="left")
    tx(ax, 0.75, 2.55,
       "① 顺序存取快：磁头按物理顺序移动，寻道少\n② 随机存取也快：公式一步定位，O(1)\n③ 结构简单：起始块号 + 长度即可描述文件\n④ 适合顺序写入、不常修改的文件",
       fs=10, ha="left")
    rbox(ax, 7.4, 0.75, 6.6, 3.0, fc=RED_L, ec=RED)
    tx(ax, 7.75, 3.4, "× 连续分配的缺点", fs=12, bold=True, color=RED, ha="left")
    tx(ax, 7.75, 2.55,
       "① 扩展难：文件末尾的块可能已被其余文件占用\n    只能整体搬移（或一开始就预留空间）\n② 外部碎片：空闲块零散无法利用，需紧凑化\n③ 紧凑化需复制整个文件，代价高",
       fs=10, ha="left")
    save(fig, FDIR + "ch4-03_physical_continuous.png")


def f04():
    fig, ax = new_fig(15, 9.2, (0, 15), (0, 9.2))
    title(ax, "链接分配：隐式链接 vs 显式链接（FAT）",
          "链接分配 = 用指针把分散的盘块串成链表；指针放哪（块内 or 独立表格）决定成败", y=8.7)
    # ---------- 左：隐式链接
    rbox(ax, 0.4, 0.8, 7.0, 7.6, fc=BLUE_L, ec=BLUE)
    tx(ax, 3.9, 7.95, "① 隐式链接（链接分配）", fs=13.5, bold=True, color=BLUE)
    tx(ax, 3.9, 7.5, "指针保存在【每个数据块内部】的尾部", fs=10.5, color=INK)
    rbox(ax, 0.75, 6.6, 1.62, 0.72, "目录项：\n首块号 = 3", fc=GRAY_L, ec=GRAY, fs=9)
    arrow(ax, 2.42, 6.96, 2.75, 6.96, color=BLUE, lw=1.8)
    chain = [("3", "next=5"), ("5", "next=12"), ("12", "next=8"), ("8", "next=NULL")]
    cx = 2.75
    for j, (a, b) in enumerate(chain):
        rbox(ax, cx, 6.15, 0.88, 1.15, "", fc=BLUE_L, ec=BLUE, fs=10)
        tx(ax, cx + 0.44, 6.8, "块" + a, fs=9.6, bold=True)
        tx(ax, cx + 0.44, 6.35, b, fs=6.8, color=BLUE)
        if j < 3:
            arrow(ax, cx + 0.9, 6.72, cx + 1.18, 6.72, color=BLUE, lw=1.5, ms=12)
        cx += 1.22
    tx(ax, 3.9, 5.55, "盘块 3→5→12→8 串成链；后继块号只存在前一块中", fs=9.0, color=INK)
    tx(ax, 3.9, 4.95, "× 缺点（重点）", fs=12.5, bold=True, color=RED)
    tx(ax, 3.9, 3.7,
       "① 只能【顺序存取】：读第 i 块必须先读出\n   前 i-1 块取指针 → 读第 i 块要 i 次访盘\n② 指针占用块内空间（每块尾部 4B）\n③ 坏其中一块 → 断链，其后数据全部丢失\n④ 适合写后一次读（顺序读）的文件",
       fs=9.6)
    tx(ax, 3.9, 2.35, "√ 优点：无外部碎片、扩展容易（链尾加块）", fs=10, color=GREEN, bold=True)
    tx(ax, 3.9, 1.6, "【考点】隐式链接为什么不能随机存取？\n—— 因为目标块号藏在前一块的内部，必须顺序读链。", fs=9.4, color=PURPLE, bold=True)
    # ---------- 右：FAT
    rbox(ax, 7.6, 0.8, 7.0, 7.6, fc=GREEN_L, ec=GREEN)
    tx(ax, 11.1, 7.9, "② 显式链接 FAT（文件分配表）", fs=13.5, bold=True, color=GREEN)
    tx(ax, 11.1, 7.35, "把指针【集中存放】到一张表里，整张表常驻内存", fs=10.5, color=INK)
    # FAT 表
    tx(ax, 8.0, 6.95, "FAT 表（内存中）：每项 = 块号 → 下一块号", fs=10.5, bold=True, ha="left")
    head = ["3", "5", "7", "8", "12", "15", "20"]
    nxt = ["5", "12", "0", "EOF", "8", "0", "0"]
    for i, (h, n) in enumerate(zip(head, nxt)):
        x0 = 7.95 + i * 0.88
        rect(ax, x0, 6.15, 0.78, 0.4, "块" + h, fc=GRAY_L, ec=GRAY, fs=7.4, lw=0.9)
        rect(ax, x0, 5.7, 0.78, 0.4, n, fc=GREEN_L, ec=GREEN, fs=7.4, lw=0.9)
    tx(ax, 14.2, 5.9, "…", fs=11, color=GRAY)
    # 磁盘块
    tx(ax, 8.0, 5.15, "磁盘上的数据块", fs=10, bold=True, ha="left", bg="white")
    dis = [("3", "A0"), ("5", "A1"), ("8", "A3"), ("12", "A2")]
    for i, (a, b) in enumerate(dis):
        x0 = 7.95 + i * 1.35
        rect(ax, x0, 4.2, 1.2, 0.65, "块%s\n%s" % (a, b), fc=BLUE_L, ec=BLUE, fs=9)
        arrow(ax, 8.4 + i * 1.35, 6.15, 8.5 + i * 1.35, 4.9, color=GRAY, lw=1.0, ms=10)
    tx(ax, 11.1, 3.62, "文件 A 的物理块：3 → 5 → 12 → 8（查 FAT 表即得）", fs=9.2, bold=True)
    tx(ax, 11.1, 3.05, "√ 优点", fs=12, bold=True, color=GREEN)
    tx(ax, 11.1, 2.35,
       "① FAT 常驻内存，查 FAT = 查数组 O(1)\n② 读任意块只需 1 次访盘（先查内存 FAT\n    得到块号，再读数据块），随机存取快\n③ 无外部碎片、扩展容易",
       fs=10)
    tx(ax, 11.1, 1.55, "× 缺点", fs=12, bold=True, color=RED)
    tx(ax, 11.1, 1.0,
       "① FAT 占用额外空间：每个盘块一条表项\n② FAT 损坏 → 全部文件链都丢了（可做备份）",
       fs=10)
    save(fig, FDIR + "ch4-04_physical_linked.png")


def f05():
    fig, ax = new_fig(15, 9.2, (0, 15), (0, 9.2))
    title(ax, "索引分配：为每个文件建立一张索引块",
          "索引分配 = 文件的 FCB 指向索引块，索引块中登记本文件所有数据块的块号", y=8.7)
    # 主图
    tx(ax, 7.5, 8.0, "基本方案：单级索引（一个文件一张索引表）", fs=13, bold=True)
    rbox(ax, 0.6, 6.15, 2.0, 1.3, "文件\n(FBC：索引块号)", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
    arrow(ax, 2.65, 6.8, 3.4, 6.8, color=BLUE, lw=2)
    rbox(ax, 3.45, 6.15, 2.4, 1.3, "索引块\n块号: 0 1 2 … k", fc=AMBER_L, ec=AMBER, fs=10.5)
    arrow(ax, 5.9, 6.8, 6.45, 6.8, color=BLUE, lw=2, text="块号→", fs=9)
    for i in range(6):
        rect(ax, 6.5 + i * 0.95, 6.15, 0.85, 1.3, "块%d\n数据" % i, fc=GREEN_L, ec=GREEN, fs=9.5)
    tx(ax, 7.5, 5.7,
       "读第 i 块 = 读索引块(1 次) + 读数据块(1 次) = 2 次访盘（若索引块已常驻内存则只 1 次）",
       fs=11, color=RED, bold=True)
    tx(ax, 7.5, 5.02,
       "√ 支持随机存取、无外部碎片、文件可动态增长；× 需额外空间存索引块；索引块放不下全部块号时 → 用下面的三种变体",
       fs=10)
    # 三种变体
    tx(ax, 7.5, 4.25, "索引块装不下？三种改进方案", fs=13, bold=True)
    # ① 链接方案
    rbox(ax, 0.4, 0.9, 4.6, 3.0, fc=TEAL_L, ec=TEAL)
    tx(ax, 2.7, 3.55, "① 链接方案", fs=12, bold=True, color=TEAL)
    rbox(ax, 0.65, 2.35, 1.5, 0.8, "索引块1", fc=TEAL_L, ec=TEAL, fs=10)
    arrow(ax, 2.2, 2.75, 2.65, 2.75, color=TEAL, lw=1.6)
    rbox(ax, 2.7, 2.35, 1.5, 0.8, "索引块2", fc=TEAL_L, ec=TEAL, fs=10)
    arrow(ax, 3.45, 3.15, 3.1, 3.15, color=TEAL, lw=1.6, text="…", fs=9)
    tx(ax, 2.7, 1.9, "索引块自己串成链（索引块间）", fs=9.4)
    tx(ax, 2.7, 1.2, "× 找第 i 块仍要顺着链找，慢\n√ 无需连续空间", fs=9.4)
    # ② 多层索引
    rbox(ax, 5.2, 0.9, 4.6, 3.0, fc=PURPLE_L, ec=PURPLE)
    tx(ax, 7.5, 3.55, "② 多层索引", fs=12, bold=True, color=PURPLE)
    rbox(ax, 5.45, 2.35, 1.4, 0.8, "一级\n索引", fc=PURPLE_L, ec=PURPLE, fs=9)
    arrow(ax, 6.9, 2.75, 7.3, 2.75, color=PURPLE, lw=1.6)
    rbox(ax, 7.35, 2.35, 1.4, 0.8, "二级\n索引", fc=PURPLE_L, ec=PURPLE, fs=9)
    arrow(ax, 8.8, 2.75, 9.2, 2.75, color=PURPLE, lw=1.6)
    rbox(ax, 9.25, 2.35, 1.1, 0.8, "数据", fc=GRAY_L, ec=GRAY, fs=9)
    tx(ax, 7.5, 1.9, "一级索引表指向二级索引表，逐层展开", fs=9.4)
    tx(ax, 7.5, 1.2, "√ 容量指数级增长  × 小文件也要逐层读，慢", fs=9.4)
    # ③ 混合索引
    rbox(ax, 10.0, 0.9, 4.6, 3.0, fc=PINK_L, ec=PINK)
    tx(ax, 12.3, 3.55, "③ 混合索引（UNIX）", fs=12, bold=True, color=PINK)
    rbox(ax, 10.3, 2.3, 1.6, 1.0, "inode\n直接+间接", fc=PINK_L, ec=PINK, fs=9)
    arrow(ax, 11.95, 2.8, 12.35, 2.8, color=PINK, lw=1.6)
    rbox(ax, 12.4, 2.3, 1.9, 1.0, "直接块 + 一/二/三\n级间接索引树", fc=AMBER_L, ec=AMBER, fs=8.6)
    tx(ax, 12.3, 1.85, "小文件直接寻址，大文件逐级展开", fs=9.4)
    tx(ax, 12.3, 1.2, "→ 详见下一节【UNIX 混合索引】大图", fs=9.4, bold=True)
    save(fig, FDIR + "ch4-05_physical_index.png")


def f06():
    fig, ax = new_fig(16, 10.8, (0, 16), (0, 10.8))
    title(ax, "UNIX 混合索引：inode 中的直接地址与多级间接索引",
          "块大小 4KB，块地址 4B → 每个索引块可装 1024 个块号；直接 10 块 + 一级 + 二级 + 三级间接", y=10.35)
    # ---------- inode 框
    rbox(ax, 0.4, 3.0, 4.7, 6.5, fc=AMBER_L, ec=AMBER)
    tx(ax, 2.75, 9.05, "磁盘 inode（逻辑索引结点）", fs=12, bold=True, color=AMBER)
    tx(ax, 2.75, 8.5, "地址项共 13 个：10 直接 + 3 间接", fs=9.8)
    for i in range(10):
        cx = 0.62 + (i % 5) * 0.9
        cy = 7.75 - (i // 5) * 0.62
        rect(ax, cx, cy, 0.8, 0.5, "D%d" % i, fc=AMBER_L, ec=AMBER, fs=8.8)
    tx(ax, 2.75, 6.9, "▲ 10 个直接地址（各指向 1 盘块）", fs=9.0, color=AMBER)
    for i, name in enumerate(["一级间接", "二级间接", "三级间接"]):
        cy = 5.85 - i * 0.6
        rect(ax, 0.62, cy, 1.35, 0.46, name, fc=AMBER_L, ec=AMBER, fs=9.6, lw=1.2)
        chip = ["→ 4MB", "→ 4GB", "→ 4TB"]
        rect(ax, 2.1, cy, 0.9, 0.46, "L%d" % (i + 1), fc=GRAY_L, ec=GRAY, fs=9.6)
        tx(ax, 3.32, cy + 0.23, chip[i], fs=9.0, color=INK, ha="left")
    tx(ax, 2.75, 3.55, "inode 常驻在磁盘 inode 表中；\n文件打开后进入内存。", fs=9.4)
    # ---------- 直接 10 块
    tx(ax, 6.0, 8.95, "① 直接地址区（10 块 = 40 KB）", fs=11.5, bold=True, color=BLUE)
    for i in range(5):
        rect(ax, 5.55 + i * 0.85, 7.75, 0.75, 0.75, "D%d" % i, fc=BLUE_L, ec=BLUE, fs=8.6)
    tx(ax, 9.7, 8.1, "…", fs=14, color=GRAY)
    rect(ax, 9.95, 7.75, 0.75, 0.75, "D9", fc=BLUE_L, ec=BLUE, fs=8.6)
    tx(ax, 11.3, 8.12, "每个直接地址项指向一个数据块（4KB）\n合计：10 × 4KB = 40 KB", fs=9.6)
    rect(ax, 5.55, 6.9, 13.55, 0.55, "", fc=BLUE_L, ec=BLUE, lw=1.2)
    tx(ax, 12.3, 7.17, "10 个直接地址 → 数据块；小文件（≤ 40KB）只需直接寻址，读数据 1 次访盘",
       fs=9.8, bold=True)
    arrow(ax, 2.62, 7.75, 5.5, 8.1, color=AMBER, lw=1.6, shrink=6)
    # ---------- 一级间接
    tx(ax, 6.0, 6.25, "② 一级间接（1 × 1024 块 = 4 MB）", fs=11.5, bold=True, color=GREEN)
    rbox(ax, 5.55, 5.05, 1.9, 0.9, "一级索引块\n(1024 项)", fc=GREEN_L, ec=GREEN, fs=8.8)
    arrow(ax, 7.5, 5.5, 8.0, 5.5, color=GREEN, lw=1.6, text="1024 项", fs=8.4)
    for i in range(4):
        rect(ax, 8.1 + i * 0.72, 5.05, 0.62, 0.9, "数据块", fc=GREEN_L, ec=GREEN, fs=7.2)
    tx(ax, 11.5, 5.5, "… 1024 块 ×4KB = 4 MB", fs=9.4, bold=True, color=GREEN, ha="left")
    arrow(ax, 3.02, 5.62, 5.4, 5.5, color=AMBER, lw=1.5, shrink=5)
    # ---------- 二级间接
    tx(ax, 6.0, 4.3, "③ 二级间接（1024 × 1024 块 = 4 GB）", fs=11.5, bold=True, color=PURPLE)
    x0 = 5.55
    rbox(ax, x0, 3.1, 1.7, 0.9, "一级\n索引块1024", fc=PURPLE_L, ec=PURPLE, fs=8.6)
    arrow(ax, x0 + 1.75, 3.55, x0 + 2.15, 3.55, color=PURPLE, lw=1.6, text="×1024", fs=8.4)
    x0 += 2.4
    rbox(ax, x0, 3.1, 1.7, 0.9, "二级\n索引块…", fc=PURPLE_L, ec=PURPLE, fs=8.6)
    arrow(ax, x0 + 1.75, 3.55, x0 + 2.15, 3.55, color=PURPLE, lw=1.6, text="×1024", fs=8.4)
    x0 += 2.4
    rbox(ax, x0, 3.1, 1.7, 0.9, "二级\n索引块…", fc=PURPLE_L, ec=PURPLE, fs=8.6)
    arrow(ax, x0 + 1.75, 3.55, x0 + 2.15, 3.55, color=PURPLE, lw=1.6, text="×1024", fs=8.4)
    rect(ax, x0 + 2.5, 3.1, 4.0, 0.9, "", fc=GRAY_L, ec=GRAY, lw=1.2)
    tx(ax, x0 + 4.5, 3.55, "每块二级索引又指向 1024 个数据块\n1024×1024×4KB = 4 GB", fs=9.4, bold=True)
    arrow(ax, 3.02, 3.3, 5.4, 3.55, color=AMBER, lw=1.5, shrink=5)
    # ---------- 三级间接
    tx(ax, 6.0, 2.45, "④ 三级间接（1024^3 块 = 4 TB）", fs=11.5, bold=True, color=RED)
    x0 = 5.55
    for i in range(3):
        rbox(ax, x0, 1.25, 1.6, 0.9, "索引块\n1024 项", fc=RED_L, ec=RED, fs=8.6)
        arrow(ax, x0 + 1.65, 1.7, x0 + 2.0, 1.7, color=RED, lw=1.5, text="×1024", fs=8.0)
        x0 += 2.25
    rect(ax, x0, 1.25, 4.55, 0.9, "", fc=GRAY_L, ec=GRAY, lw=1.2)
    tx(ax, x0 + 2.28, 1.7, "1024×1024×1024×4KB = 4 TB", fs=9.8, bold=True)
    arrow(ax, 3.02, 1.9, 5.4, 1.7, color=AMBER, lw=1.5, shrink=5)
    # ---------- 底部结论
    rect(ax, 0.4, 0.45, 15.2, 0.62, "", fc=AMBER_L, ec=AMBER, lw=1.4)
    tx(ax, 8.0, 0.76,
       "【结论】文件最大长度 = 40KB + 4MB + 4GB + 4TB；【访盘次数】读直接区块：1 次；一级间接区：2 次；二级间接区：3 次；三级间接区：4 次（假设索引块均未在内存）",
       fs=9.8, bold=True)
    save(fig, FDIR + "ch4-06_unix_mixed.png")
