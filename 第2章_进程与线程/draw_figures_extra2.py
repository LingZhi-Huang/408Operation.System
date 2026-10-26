# -*- coding: utf-8 -*-
"""第2章补充插图：吸烟者问题、理发师问题（ch2-39、ch2-40）。"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L, GRAY, GRAY_L)

FIG = "/Users/levi/IdeaProjects/操作系统/第2章_进程与线程/figures/"


def f39():
    fig, ax = osfig.new_fig(12.5, 5.8, xlim=(0, 12.5), ylim=(0, 5.8))
    osfig.title(ax, "吸烟者问题：一种「按资源分组」的生产者-消费者",
                sub="供应者轮流把三种材料中的两种放上桌；持有第三种材料的人才能卷烟抽", fs=15)
    osfig.box(ax, 2.3, 3.7, 2.9, 1.15, "供应者\n轮流放两种材料", fc=BLUE_L, ec=BLUE, fs=11.5, bold=True, ls=1.4)
    osfig.box(ax, 6.3, 3.7, 2.2, 1.15, "桌面\n(两种材料)", fc=GRAY_L, ec=GRAY, fs=11, bold=True)
    osfig.arrow(ax, 3.75, 3.7, 5.2, 3.7, "放", color=INK, lw=1.8)
    groups = [("吸烟者A：有烟草\n等「纸+胶」→ P(offerA)", GREEN, 1.6),
              ("吸烟者B：有纸\n等「烟草+胶」→ P(offerB)", TEAL, 4.9),
              ("吸烟者C：有胶\n等「烟草+纸」→ P(offerC)", PURPLE, 8.2)]
    for name, c, x in groups:
        osfig.rbox(ax, x - 1.5, 1.35, 3.0, 1.3, name, fc="white", ec=c, fs=10.5, bold=True, ls=1.4)
        osfig.arrow(ax, 6.0, 3.1, x, 2.7, "", color=c, lw=1.5)
    osfig.tx(ax, 6.25, 0.75, "抽完的吸烟者 V(finish) → 供应者 P(finish) 通过，再放下两种 → 循环", fs=11.5, color=INK)
    osfig.tx(ax, 6.25, 0.3, "【信号量】offerA=offerB=offerC=0（三种组合各一个）、finish=0——「按组唤醒」是本题的灵魂", fs=11, color=RED, bold=True)
    osfig.save(fig, FIG + "ch2-39_smokers.png")


def f40():
    fig, ax = osfig.new_fig(12.5, 5.8, xlim=(0, 12.5), ylim=(0, 5.8))
    osfig.title(ax, "睡眠理发师问题：有限的等待队列（满员即走）",
                sub="理发椅 1 张 + 等候室 n 座；有空位才排队，满员顾客直接离开", fs=15)
    osfig.box(ax, 2.0, 4.0, 2.2, 1.05, "顾客到达", fc=BLUE_L, ec=BLUE, fs=12, bold=True)
    osfig.box(ax, 6.3, 4.0, 3.4, 1.05, "等候室（n 座）\nwaiting 计数 ∈ [0, n]", fc=TEAL_L, ec=TEAL, fs=11, bold=True, ls=1.4)
    osfig.box(ax, 10.4, 4.0, 2.0, 1.05, "理发椅 ×1\n理发师", fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    osfig.arrow(ax, 3.1, 4.0, 4.6, 4.0, "①有座？", color=INK, fs=9.5, dy=0.28)
    osfig.arrow(ax, 8.0, 4.0, 9.4, 4.0, "②叫号", color=INK, fs=9.5, dy=0.28)
    osfig.tx(ax, 4.4, 3.0, "满员：V(mutex) 后直接离开（不排队、不阻塞在等椅子上）", fs=11, color=RED, bold=True)
    osfig.tx(ax, 4.4, 2.55, "有座：waiting++ → V(customers) → V(mutex) → P(barber) 等叫号 → 理发", fs=11, color=INK)
    osfig.rbox(ax, 1.0, 0.95, 10.5, 1.05, "", fc=AMBER_L, ec=AMBER)
    osfig.tx(ax, 6.25, 1.62, "理发师：P(customers)（没客就睡）→ P(mutex) → waiting-- → V(barber) → V(mutex) → 理发", fs=11.5, bold=True, color=INK)
    osfig.tx(ax, 6.25, 1.2, "信号量：customers=0（有无顾客）、barber=0（叫号）、mutex=1（护 waiting）", fs=11, color=INK)
    osfig.tx(ax, 6.25, 0.4, "【两个易错】① 满员判断在 mutex 内、用 if；② waiting 是共享变量，改它必须持锁——漏一个就错", fs=11, color=RED, bold=True)
    osfig.save(fig, FIG + "ch2-40_barber.png")


if __name__ == "__main__":
    f39(); f40()
    print("ch2 extras2 done")
