# -*- coding: utf-8 -*-
"""第0章 扩写新增插图（ch0-03、ch0-04）。"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L, GRAY, GRAY_L)

FIG = "/Users/levi/IdeaProjects/操作系统/第0章_学习地图/figures/"


def f03():
    fig, ax = osfig.new_fig(13, 6.2, xlim=(0, 13), ylim=(0, 6.2))
    osfig.title(ax, "408 操作系统 35 分怎么分布：把力气花在刀刃上",
                sub="选择题约 22 分（11 题 × 2 分）+ 综合应用大题约 13 分（2~3 道）", fs=17)
    # 左：选择题分布
    osfig.tx(ax, 3.3, 5.1, "选择题 22 分的来源（估算）", fs=13, bold=True, color=BLUE)
    bars = [("进程/调度/同步/死锁", 7, BLUE), ("内存/虚拟页", 5, GREEN), ("文件/磁盘", 4, AMBER), ("I/O与概述", 6, TEAL)]
    y = 4.45
    for name, n, c in bars:
        osfig.tx(ax, 0.7, y + 0.05, name, fs=10.5, ha="left", color=INK)
        osfig.rect(ax, 4.1, y - 0.12, n * 0.42, 0.4, "", fc=(BLUE_L if c == BLUE else GREEN_L if c == GREEN else AMBER_L if c == AMBER else TEAL_L), ec=c, lw=1.6)
        osfig.tx(ax, 4.15 + n * 0.42 + 0.2, y + 0.08, "约 " + str(n) + " 分", fs=10, ha="left", color=c, bold=True)
        y -= 0.8
    # 右：大题分布
    osfig.rbox(ax, 7.6, 1.4, 4.9, 3.7, "", fc=RED_L, ec=RED)
    osfig.tx(ax, 10.05, 4.6, "综合大题 13 分的主战场", fs=13, bold=True, color=RED)
    osfig.tx(ax, 10.05, 3.6, "① PV 信号量题（6~8 分）\n    生产者消费者 / 读者写者变体\n② 调度或置换计算题（4~6 分）\n    甘特图 / 缺页率 / 磁盘调度\n③ 偶发：地址变换 / 银行家 / 文件系统", fs=11, ls=1.9)
    osfig.tx(ax, 10.05, 2.05, "结论：第2章几乎必出一道大题，", fs=11, bold=True, color=INK)
    osfig.tx(ax, 10.05, 1.65, "第3/4章轮流出一道——先吃第2章！", fs=11, bold=True, color=RED)
    osfig.tx(ax, 6.5, 0.6, "【使用建议】每轮复习前先看这张图自问：这一章的「分数密度」我配得上花的时间吗？", fs=11.5, color=GRAY)
    osfig.save(fig, FIG + "ch0-03_exam_distribution.png")


def f04():
    fig, ax = osfig.new_fig(13, 5.6, xlim=(0, 13), ylim=(0, 5.6))
    osfig.title(ax, "每 90 分钟一个学习闭环：看图 → 读文 → 动手算 → 自测",
                sub="只看不算 = 白学。每个小节都建议按这个循环走一遍", fs=17)
    steps = [
        ("1. 看框架图", "本节开头先看图\n带着问题读正文", BLUE),
        ("2. 精读正文", "先比喻后定义\n考点/易错随手勾", GREEN),
        ("3. 动手算例题", "盖住答案自己写\n调度/置换/地址变换必亲手", AMBER),
        ("4. 做自测题", "每章末 10 道限时做\n错题标记", RED),
        ("5. 错题回看", "回到对应小节+图\n弄懂再往下走", PURPLE),
    ]
    xs = [1.5, 4.0, 6.5, 9.0, 11.5]
    for (name, desc, c), x in zip(steps, xs):
        osfig.circle(ax, x, 3.9, 0.42, name.split(".")[0], fc="white", ec=c, fs=13, bold=True, lw=2.2)
        osfig.tx(ax, x, 2.95, name.split(". ")[1], fs=12.5, bold=True, color=c)
        osfig.tx(ax, x, 2.25, desc, fs=9.5, color=GRAY, ls=1.4)
        if x < 11.4:
            osfig.arrow(ax, x + 0.55, 3.9, x + 1.9, 3.9, "", color=GRAY, lw=1.8)
    osfig.arrow(ax, 11.5, 1.45, 1.5, 1.45, "下一小节循环往复；每章末整体复盘一遍", color=TEAL, fs=11, both=True, dy=-0.22, ls=":")
    osfig.rbox(ax, 1.5, 0.6, 10.0, 0.95, "", fc=RED_L, ec=RED)
    osfig.tx(ax, 6.5, 1.07, "铁律：一道例题「看懂」的时间 ≤ 3 分钟，但「独立做对」带来的分数增长是看懂的 5 倍以上。",
             fs=12, bold=True)
    osfig.save(fig, FIG + "ch0-04_daily_loop.png")


if __name__ == "__main__":
    f03(); f04()
    print("ch0 extras done")
