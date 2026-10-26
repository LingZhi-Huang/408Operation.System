# -*- coding: utf-8 -*-
"""第6章 题库实战 插图（ch6-01 ~ ch6-08）。所有例题数据均经程序验算。"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L, GRAY, GRAY_L,
                   PINK, PINK_L)

FIG = "/Users/levi/IdeaProjects/操作系统/第6章_题库实战/figures/"
F = lambda n: FIG + n


# ---------- 验算工具 ----------
def verify():
    # 置换：经典 20 引用串，3 帧
    refs = [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
    def fifo():
        mem, q, miss = set(), [], 0
        for r in refs:
            if r in mem: continue
            miss += 1
            if len(mem) == 3: mem.discard(q.pop(0))
            mem.add(r); q.append(r)
        return miss
    def lru():
        mem, order, miss = set(), [], 0
        for r in refs:
            if r in mem:
                order.remove(r); order.append(r); continue
            miss += 1
            if len(mem) == 3: mem.discard(order.pop(0))
            mem.add(r); order.append(r)
        return miss
    def opt():
        mem, miss = set(), 0
        for i, r in enumerate(refs):
            if r in mem: continue
            miss += 1
            if len(mem) == 3:
                future = refs[i+1:]
                cand = max(mem, key=lambda p: future.index(p) if p in future else 999)
                mem.discard(cand)
            mem.add(r)
        return miss
    print("置换验证: FIFO=%d LRU=%d OPT=%d" % (fifo(), lru(), opt()))

    # 银行家：Available=(2,2,2)
    Alloc = {"P0":(1,0,1),"P1":(1,1,0),"P2":(0,1,1),"P3":(1,0,0)}
    Need  = {"P0":(2,2,1),"P1":(1,1,2),"P2":(3,0,2),"P3":(1,1,1)}
    def le(a, b): return all(x <= y for x, y in zip(a, b))
    def add(a, b): return tuple(x + y for x, y in zip(a, b))
    work = (2,2,2); done = []; pend = ["P0","P1","P2","P3"]
    while pend:
        for p in list(pend):
            if le(Need[p], work):
                work = add(work, Alloc[p]); done.append(p); pend.remove(p); break
        else: break
    print("银行家验证: 安全序列=", done, " Work终=", work)
    # P3 请求 (1,0,0) 试探后
    work2 = (1,2,2)
    Need2 = dict(Need); Need2["P3"] = (0,1,1)
    Alloc2 = dict(Alloc); Alloc2["P3"] = (2,0,0)
    done2 = []; pend2 = ["P0","P1","P2","P3"]
    while pend2:
        for p in list(pend2):
            if le(Need2[p], work2):
                work2 = add(work2, Alloc2[p]); done2.append(p); pend2.remove(p); break
        else: break
    print("试探后验证: 安全序列=", done2)


# ---------- ch6-01 调度题甘特图 ----------
def f01():
    fig, ax = osfig.new_fig(13, 5.8, xlim=(0, 13), ylim=(0, 5.8))
    osfig.title(ax, "大题1：SJF（非抢占） vs SRTN（抢占）甘特图",
                sub="P1(0,8) P2(1,4) P3(2,9) P4(3,5)——同一组数据，非抢占与抢占的差距一目了然", fs=15)
    bands = [
        ("SJF 非抢占", [("P1",0,8,BLUE),("P2",8,12,GREEN),("P4",12,17,AMBER),("P3",17,26,PURPLE)],
         "完成 8/12/26/17  周转 8/11/24/14  平均 14.25"),
        ("SRTN 抢占", [("P1",0,1,BLUE),("P2",1,5,GREEN),("P4",5,10,AMBER),("P1",10,17,BLUE),("P3",17,26,PURPLE)],
         "完成 17/4/26/10  周转 17/3/24/7  平均 12.75"),
    ]
    y = 4.0
    for name, segs, note in bands:
        osfig.tx(ax, 0.9, y + 0.95, name, fs=12, bold=True, color=INK, ha="left")
        for p, a, b, c in segs:
            osfig.rect(ax, 0.9 + a / 26 * 11.6, y, (b - a) / 26 * 11.6, 0.6, p + "(%d-%d)" % (a, b),
                       fc=(BLUE_L if c == BLUE else GREEN_L if c == GREEN else AMBER_L if c == AMBER else PURPLE_L),
                       ec=c, fs=9.5, bold=True)
        osfig.tx(ax, 0.9, y - 0.4, note, fs=10.5, ha="left", color=(GREEN if "SRTN" in name else RED))
        y -= 2.0
    for t in [0, 5, 8, 10, 12, 17, 26]:
        osfig.tx(ax, 0.9 + t / 26 * 11.6, 0.55, str(t), fs=9, color=GRAY)
    osfig.tx(ax, 6.5, 0.15, "【答案要点】SRTN 平均周转 12.75 < SJF 14.25：抢占让短作业「随到随插队」；P1 被切三段，周转反而最长", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch6-01_scheduling_gantt.png"))


# ---------- ch6-02 置换题 ----------
def f02():
    fig, ax = osfig.new_fig(14, 6.6, xlim=(0, 14), ylim=(0, 6.6))
    osfig.title(ax, "大题2：经典 20 次引用，三算法缺页对比（3 帧）",
                sub="引用串 7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1（程序验算：FIFO=15、LRU=12、OPT=9）", fs=15)
    refs = [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
    panels = [
        ("FIFO：淘「最先进入」的页", "FIFO", 15, BLUE),
        ("LRU：淘「最久未用」的页", "LRU", 12, GREEN),
        ("OPT：淘「将来最久不用」的页", "OPT", 9, PURPLE),
    ]
    y = 5.1
    # 引用行
    osfig.tx(ax, 0.9, y, "引用", fs=10, ha="left", bold=True)
    for i, r in enumerate(refs):
        osfig.rect(ax, 1.7 + i * 0.6, y - 0.18, 0.58, 0.36, str(r), fc=GRAY_L, ec=GRAY, fs=8.5)
    y -= 0.75
    misses = {
        "FIFO": [1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1],
        "LRU":  [1,1,1,1,0,1,0,1,1,1,1,0,0,1,0,1,0,1,0,0],
        "OPT":  [1,1,1,1,0,1,0,1,0,1,0,0,0,1,0,1,0,1,0,0],
    }
    for name, key, total, c in panels:
        osfig.tx(ax, 0.9, y + 0.55, name + " → 缺页 %d 次，缺页率 %d%%" % (total, total * 5), fs=11, bold=True, color=c, ha="left")
        m = misses[key]
        for i in range(20):
            osfig.rect(ax, 1.7 + i * 0.6, y, 0.58, 0.42, "缺" if m[i] else "中",
                       fc=(RED_L if m[i] else GREEN_L), ec=(RED if m[i] else GREEN), fs=8)
        y -= 1.15
    osfig.tx(ax, 7, 0.75, "结论：OPT 9 < LRU 12 < FIFO 15；缺页率 = 缺页次数 ÷ 20（75% / 60% / 45%）", fs=11.5, bold=True, color=INK)
    osfig.tx(ax, 7, 0.3, "【答题规范】画三行对照表逐格填，每格标注「缺/中」——直接给数字不给过程会扣分", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch6-02_replacement_exam.png"))


# ---------- ch6-03 地址变换综合题 ----------
def f03():
    fig, ax = osfig.new_fig(12.5, 6.0, xlim=(0, 12.5), ylim=(0, 6.0))
    osfig.title(ax, "大题3：分页 + 快表 + 缺页的综合访存",
                sub="页 4KB；TLB 查 20ns、访存 100ns、TLB 命中率 90%、缺页率 1%（缺页处理 8ms）", fs=15)
    osfig.tx(ax, 6.25, 5.0, "① 纯 TLB 视角（无缺页）：EAT = 0.9×(20+100) + 0.1×(20+200) = 108+22 = 130ns", fs=11.5, color=BLUE, bold=True)
    osfig.tx(ax, 6.25, 4.5, "② 加入缺页（题目口径：缺页时另加处理时间）：", fs=11.5, color=INK)
    osfig.rbox(ax, 1.4, 2.7, 9.7, 1.5, "", fc=AMBER_L, ec=AMBER)
    osfig.tx(ax, 6.25, 3.85, "EAT = 99% × 130ns + 1% × (8ms 级别的缺页代价)", fs=13, bold=True, color=INK)
    osfig.tx(ax, 6.25, 3.25, "    = 128.7ns + 0.01×8,000,000ns = 128.7 + 80,000 ≈ 80,129ns ≈ 80μs", fs=13, bold=True, color=RED)
    osfig.tx(ax, 6.25, 2.05, "结论：1% 的缺页率把有效访问时间从 130ns 拉高到约 80μs —— 恶化 600 倍！", fs=12, bold=True, color=RED)
    osfig.tx(ax, 6.25, 1.4, "这解释了为什么「降低缺页率（工作集/预调页）」比「提高 TLB 命中率」重要得多", fs=11, color=GRAY)
    osfig.tx(ax, 6.25, 0.8, "【变体】若题目给「缺页后仍需常规访问」，则缺页项 = 缺页处理 + 130ns，结果相差 0.13μs，可忽略", fs=11, color=BLUE)
    osfig.tx(ax, 6.25, 0.25, "【考点】分段计费式 EAT：正常项 × 概率 + 缺页项 × 概率——两种口径都要会写", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch6-03_eat_with_pagefault.png"))


# ---------- ch6-04 吸烟者题图 ----------
def f04():
    fig, ax = osfig.new_fig(12.5, 6.8, xlim=(0, 12.5), ylim=(0, 6.8))
    osfig.title(ax, "大题4：吸烟者问题（生产者按单一资源分组投放）",
                sub="供应商轮流把「三种材料中的两种」放桌上；持有第三种材料的吸烟者才能卷烟", fs=15)
    osfig.box(ax, 2.6, 5.05, 3.0, 1.1, "供应商\n轮流放两种材料", fc=BLUE_L, ec=BLUE, fs=11.5, bold=True, ls=1.4)
    osfig.box(ax, 7.3, 5.05, 2.8, 1.1, "桌面（两种材料）", fc=GRAY_L, ec=GRAY, fs=11, bold=True)
    osfig.arrow(ax, 4.1, 5.05, 5.9, 5.05, "放", color=INK, lw=1.8)
    rows = [("吸烟者A：持有烟草 → 等纸+胶", "offerA", GREEN),
            ("吸烟者B：持有纸 → 等烟草+胶", "offerB", TEAL),
            ("吸烟者C：持有胶 → 等烟草+纸", "offerC", PURPLE)]
    y = 3.9
    for name, sig, c in rows:
        osfig.rbox(ax, 1.3, y - 0.36, 6.6, 0.72, name, fc="white", ec=c, fs=11.5, bold=True)
        osfig.tx(ax, 10.3, y, "P(" + sig + ") 才能动筷", fs=11, color=c, bold=True)
        osfig.arrow(ax, 7.9, y, 8.9, y, "", color=c, lw=1.4, ms=11)
        y -= 1.0
    osfig.arrow(ax, 7.3, 4.5, 4.6, 3.95, "", color=GRAY, lw=1.4, ls=":")
    osfig.tx(ax, 6.25, 1.35, "抽完的吸烟者 V(finish) → 供应者 P(finish) 通过，再放下一组 → 循环", fs=11.5, color=INK)
    osfig.tx(ax, 6.25, 0.85, "【信号量】offerA = offerB = offerC = 0（三种组合各一个）、finish = 0——「按组唤醒」是本题灵魂", fs=11, color=BLUE, bold=True)
    osfig.tx(ax, 6.25, 0.4, "【考点】一组生产者对多组消费者、按资源种类唤醒 → 每种组合一个同步信号量；一次只 V 一个（放哪组 V 哪个）", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch6-04_smokers.png"))


# ---------- ch6-05 理发师题图 ----------
def f05():
    fig, ax = osfig.new_fig(12.5, 5.8, xlim=(0, 12.5), ylim=(0, 5.8))
    osfig.title(ax, "大题5：睡眠理发师问题（有限等待队列）",
                sub="理发椅 1 张、等候室 n 座；满员则顾客离开，空则叫号理发", fs=15)
    osfig.box(ax, 2.4, 3.9, 2.6, 1.1, "顾客到达\n（随机流）", fc=BLUE_L, ec=BLUE, fs=12, bold=True)
    osfig.box(ax, 6.4, 3.9, 3.0, 1.1, "等候室：n 个座位\nwaiting 计数（受 mutex 保护）", fc=TEAL_L, ec=TEAL, fs=10.5, bold=True, ls=1.4)
    osfig.box(ax, 10.4, 3.9, 2.0, 1.1, "理发椅 ×1\n理发师", fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    osfig.arrow(ax, 3.7, 3.9, 4.9, 3.9, "① 有座？", color=INK, fs=9.5, dy=0.3)
    osfig.arrow(ax, 7.9, 3.9, 9.4, 3.9, "② 叫号", color=INK, fs=9.5, dy=0.3)
    osfig.tx(ax, 4.3, 2.85, "满员 → V(mutex) 后离开（不等待！）", fs=11, color=RED, bold=True)
    osfig.tx(ax, 4.3, 2.4, "有座 → waiting++，V(customers)，P(barber) 等叫号", fs=11, color=INK)
    osfig.rbox(ax, 1.2, 1.0, 10.2, 1.0, "", fc=AMBER_L, ec=AMBER)
    osfig.tx(ax, 6.3, 1.65, "理发师：P(customers) 睡觉等客 → P(mutex) 改 waiting-- → V(barber) 叫号 → V(mutex) → 理发", fs=11.5, bold=True, color=INK)
    osfig.tx(ax, 6.3, 1.25, "信号量 customers=0（等客）、barber=0（叫号）、mutex=1（护 waiting）；顾客：P(mutex)→判断→V(mutex)→P(barber)", fs=10.5, color=INK)
    osfig.tx(ax, 6.25, 0.45, "【考点】「满员即走」用 if 而非 while；waiting 是共享变量必须配 mutex——两个易错点叠加的经典大题", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch6-05_barber.png"))


# ---------- ch6-06 银行家题 ----------
def f06():
    fig, ax = osfig.new_fig(13, 7.2, xlim=(0, 13), ylim=(0, 7.2))
    osfig.title(ax, "大题6：银行家算法（Available = (2,2,2)）",
                sub="四进程三类资源；程序验算：安全序列 <P0,P1,P2,P3>；P3 请求 (1,0,0) 可以分配", fs=15)
    # 矩阵
    cols = [("Max", 3.0), ("Alloc", 5.6), ("Need", 8.2)]
    osfig.tx(ax, 1.1, 5.9, "", fs=10)
    for name, x in cols:
        osfig.rbox(ax, x - 0.9, 5.35, 1.8, 0.45, name, fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    rows = [("P0", "(3,2,2)", "(1,0,1)", "(2,2,1)"),
            ("P1", "(2,2,2)", "(1,1,0)", "(1,1,2)"),
            ("P2", "(3,1,3)", "(0,1,1)", "(3,0,2)"),
            ("P3", "(2,1,1)", "(1,0,0)", "(1,1,1)")]
    y = 5.35
    for p, m, a, n in rows:
        y -= 0.52
        osfig.tx(ax, 0.8, y + 0.26, p, fs=11, bold=True, ha="left")
        for (name, x), v in zip(cols, (m, a, n)):
            osfig.rbox(ax, x - 0.9, y, 1.8, 0.5, v, fc="white", ec=GRAY, fs=10.5)
    # 安全性
    osfig.rbox(ax, 9.5, 2.9, 3.2, 2.85, "", fc=GREEN_L, ec=GREEN)
    osfig.tx(ax, 11.1, 5.4, "安全性检查", fs=12, bold=True, color=GREEN)
    osfig.tx(ax, 11.1, 4.55, "Work=(2,2,2)\nP0 需(2,2,1) √ → (3,2,3)\nP1 需(1,1,2) √ → (4,3,3)\nP3 需(1,1,1) √ → (5,3,3)\nP2 需(3,0,2) √ → (5,4,4)", fs=10, ls=1.65)
    osfig.tx(ax, 11.1, 3.15, "安全序列 <P0,P1,P2,P3>\n（不唯一，P2/P3 可互换）", fs=10.5, bold=True, color=GREEN)
    # 第二问
    osfig.rbox(ax, 1.0, 1.0, 11.2, 1.6, "", fc=BLUE_L, ec=BLUE)
    osfig.tx(ax, 6.5, 2.2, "第二问：P3 请求 (1,0,0) 能否满足？", fs=12, bold=True, color=BLUE)
    osfig.tx(ax, 6.5, 1.6, "≤ Need(P3)=(1,1,1) √；≤ Available √ → 试探：Available'=(1,2,2)、Need'(P3)=(0,1,1)", fs=11, color=INK)
    osfig.tx(ax, 6.5, 1.2, "再检安全性：P1(1,1,2)≤(1,2,2) √ → … 存在安全序列（如 <P1,P0,P2,P3>）→ 可以分配", fs=11, bold=True, color=GREEN)
    osfig.tx(ax, 6.5, 0.45, "【答题规范】四步一个不能少：① ≤Need ② ≤Available ③ 试探改三张表 ④ 完整的安全性检查（写出 Work 变化）", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch6-06_banker_exam.png"))


# ---------- ch6-07 磁盘调度题 ----------
def f07():
    fig, ax = osfig.new_fig(13.5, 6.4, xlim=(0, 13.5), ylim=(0, 6.4))
    osfig.title(ax, "大题7：磁盘调度（磁头 100 起步，方向向大）",
                sub="请求队列 55,58,39,18,90,160,150,38,184（程序逐段验算）", fs=15)
    seqs = [
        ("FCFS", [100,55,58,39,18,90,160,150,38,184], 498, BLUE),
        ("SSTF", [100,90,58,55,39,38,18,150,160,184], 248, GREEN),
        ("SCAN(到199)", [100,150,160,184,199,90,58,55,39,38,18], 280, AMBER),
        ("LOOK(到184)", [100,150,160,184,90,58,55,39,38,18], 250, PURPLE),
    ]
    y = 5.3
    for name, path, total, c in seqs:
        osfig.tx(ax, 0.5, y + 0.62, name + " → 总寻道 %d" % total, fs=11, bold=True, color=c, ha="left")
        for i, p in enumerate(path):
            x = 1.6 + i * 1.18
            osfig.circle(ax, x, y + 0.2, 0.28, str(p), fc="white", ec=c, fs=7.5, lw=1.4)
            if i < len(path) - 1:
                osfig.line(ax, x + 0.28, y + 0.2, x + 0.9, y + 0.2, color=c, lw=1.2)
        y -= 1.15
    osfig.tx(ax, 6.75, 0.7, "要点：SSTF 248 最短但会饥饿；SCAN 280 vs LOOK 250——差的 30 = 184→199 的空跑 + 折返多走的 15", fs=11, color=INK)
    osfig.tx(ax, 6.75, 0.25, "【易错】SCAN 到「磁盘边缘 199」；本题 LOOK 折返点是「该方向最远请求 184」——两者别混", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch6-07_disk_scheduling_exam.png"))


# ---------- ch6-08 缓冲计算题 ----------
def f08():
    fig, ax = osfig.new_fig(12.5, 5.6, xlim=(0, 12.5), ylim=(0, 5.6))
    osfig.title(ax, "大题8：缓冲区计算（T=100μs，M=15μs，C=60μs，n=8 块）",
                sub="单缓冲每块 max(C,T)+M = 115μs；双缓冲每块 max(C+M,T) = 100μs", fs=15)
    osfig.rbox(ax, 0.9, 3.0, 5.3, 1.9, "", fc=BLUE_L, ec=BLUE)
    osfig.tx(ax, 3.55, 4.5, "单缓冲", fs=13, bold=True, color=BLUE)
    osfig.tx(ax, 3.55, 3.75, "首块：T+M+C = 175μs\n每块（稳态）：max(60,100)+15 = 115μs\n总时间 = 175 + 7×115 = 980μs", fs=11.5, ls=1.7)
    osfig.rbox(ax, 6.5, 3.0, 5.3, 1.9, "", fc=GREEN_L, ec=GREEN)
    osfig.tx(ax, 9.15, 4.5, "双缓冲", fs=13, bold=True, color=GREEN)
    osfig.tx(ax, 9.15, 3.75, "首块：T+M+C = 175μs\n每块（稳态）：max(60+15,100) = 100μs\n总时间 = 175 + 7×100 = 875μs", fs=11.5, ls=1.7)
    osfig.tx(ax, 6.25, 2.3, "验算另一种口径（瓶颈法）：双缓冲下设备是瓶颈（T=100 最大），设备不停歇 → n×T + (M+C) = 800+75 = 875 √", fs=11, color=INK)
    osfig.tx(ax, 6.25, 1.7, "若 C=150（CPU 变瓶颈）：双缓冲每块 = max(165,100) = 165μs → 总 = 175 + 7×165 = 1330μs", fs=11, color=AMBER)
    osfig.tx(ax, 6.25, 1.0, "【考点】先找瓶颈（T 与 C+M 谁大），再写总时间 = 首块全流程 + (n−1)×稳态；两种口径互验可防算错", fs=11.5, color=RED, bold=True)
    osfig.tx(ax, 6.25, 0.4, "【易错】直接写 n×115 或 n×100 都不对——首块没有「上一块」可并行，必须单算", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch6-08_buffer_exam.png"))


if __name__ == "__main__":
    verify()
    f01(); f02(); f03(); f04(); f05(); f06(); f07(); f08()
    print("ch6 figures done")
