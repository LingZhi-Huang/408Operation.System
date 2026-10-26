# -*- coding: utf-8 -*-
"""生成第0章学习地图的插图：全书知识地图 + 学习路线"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L, GRAY, GRAY_L)

FIGDIR = "/Users/levi/IdeaProjects/操作系统/第0章_学习地图/figures"

# ============ 图1：全书知识地图 ============
fig, ax = osfig.new_fig(15, 11.2, xlim=(0, 15), ylim=(0, 11.2))
osfig.title(ax, "考研408《操作系统》全书知识地图",
            sub="五大模块 · 一条主线：让多道程序安全、高效、共享地使用计算机资源", fs=19)

# 第1章 总纲（顶部）
osfig.rbox(ax, 0.7, 8.9, 13.6, 1.1, "", fc=BLUE_L, ec=BLUE)
osfig.tx(ax, 7.5, 9.68, "第1章 操作系统概述 · 总纲（概念+判断为主）", fs=14.5, bold=True)
osfig.tx(ax, 7.5, 9.05,
         "为什么需要OS → 四大特征(并发/共享/虚拟/异步) → 发展历程 → 两类指令与核心态\n→ 中断与异常 → 系统调用 → 体系结构 → 引导与虚拟机",
         fs=11, color=INK, ls=1.5)

# 中部四条主线
rows = [
    ("第2章 进程与线程", "CPU资源 · 分值最高", PURPLE, PURPLE_L,
     "进程与PCB → 状态转换(五/七) → 控制原语 → 通信 → 线程\n→ 调度算法(计算) → 同步互斥PV(大题) → 死锁/银行家算法"),
    ("第3章 内存管理", "内存资源 · 计算最多", GREEN, GREEN_L,
     "装入链接 → 覆盖交换 → 连续分配(四算法) → 分页/分段/段页式\n→ 地址变换+TLB(计算) → 虚拟内存 → 置换算法 → 抖动"),
    ("第4章 文件管理", "磁盘资源 · 细节最多", AMBER, AMBER_L,
     "文件概念 → 逻辑结构 → 物理结构(连续/FAT/索引/UNIX混合)\n→ 目录与inode → 硬软链接 → 空闲管理(位图/成组链接) → 磁盘调度"),
    ("第5章 输入/输出管理", "设备资源 · 概念为主", TEAL, TEAL_L,
     "设备分类 → 控制器与编址 → 四种I/O控制方式(程序/中断/DMA/通道)\n→ I/O软件四层(归属判断) → 缓冲区(计算) → SPOOLing → LUT"),
]
for i, (name, sub, ec, fc, content) in enumerate(rows):
    y = 7.2 - i * 1.55
    osfig.rbox(ax, 0.7, y, 3.5, 1.32, "", fc=fc, ec=ec)
    osfig.tx(ax, 2.45, y + 0.9, name, fs=14, bold=True)
    osfig.tx(ax, 2.45, y + 0.4, sub, fs=10.5, color=ec)
    osfig.rbox(ax, 4.3, y, 10.0, 1.32, "", fc="white", ec=ec, lw=1.6)
    osfig.tx(ax, 9.3, y + 0.66, content, fs=10.5, ls=1.55)

# 底部方法论
osfig.rbox(ax, 0.7, 0.15, 13.6, 1.45, "", fc=GRAY_L, ec=GRAY)
osfig.tx(ax, 7.5, 1.32, "贯穿全书的 3 条方法论（每一章都问这三个问题）", fs=13, bold=True)
osfig.tx(ax, 7.5, 0.82,
         "① 谁分配？→ 管理主体(OS内核)与客体(进程/文件/设备)     ② 怎么分？→ 策略(连续/离散、静态/动态)与数据结构(表/链/栈/队列)\n"
         "③ 安全吗？→ 同步互斥与死锁(第2章) · 越界与保护(第3章) · 空闲与坏块(第4章) · 独占与共享(第5章)",
         fs=10.5, ls=1.6)
osfig.save(fig, FIGDIR + "/ch0-01_whole_book_map.png")

# ============ 图2：三轮复习路线 ============
fig, ax = osfig.new_fig(14, 7.5, xlim=(0, 14), ylim=(0, 7.5))
osfig.title(ax, "三轮复习路线（建议 9 个月 / 3 个月 / 1 个月）",
            sub="每轮结束用「章末自测题」检验，错题回馈到对应小节", fs=16)

rows2 = [
    ("第一轮\n打地基", BLUE, BLUE_L,
     "逐章精读：先比喻后定义，看懂每张图，亲手算每道例题。\n本阶段不追求速度，追求「每个知识点的来龙去脉」。",
     "产出：每章思维导图 + 例题本（含演算过程）"),
    ("第二轮\n刷真题", GREEN, GREEN_L,
     "按章刷 2009-2025 年 408 真题与王道大题，死磕三类大题：\nPV 代码、调度/置换/磁盘调度计算、地址变换。",
     "产出：易错题清单（≥50 道）"),
    ("第三轮\n冲刺背记", AMBER, AMBER_L,
     "只看每章末的「高频考点清单 + 易错点清单 + 全章对比表」；\n每天限时做 2 道大题保持手感。",
     "产出：考前 7 天只看目录 + 对比表 + 易错点"),
]
for i, (name, ec, fc, desc, out) in enumerate(rows2):
    y = 4.75 - i * 1.85
    osfig.rbox(ax, 1.0, y, 2.7, 1.55, name, fc=fc, ec=ec, bold=True, fs=14, ls=1.4)
    osfig.rbox(ax, 3.9, y + 0.35, 9.1, 1.2, "", fc="white", ec=ec, lw=1.6)
    osfig.tx(ax, 8.45, y + 1.08, desc, fs=10.5, ls=1.5)
    osfig.tx(ax, 8.45, y + 0.55, out, fs=10, color=ec)
    if i < 2:
        osfig.arrow(ax, 2.35, y + 0.22, 2.35, y + 0.02, color=GRAY, lw=1.8)

osfig.rbox(ax, 1.0, 0.25, 12.0, 0.95, "", fc=RED_L, ec=RED)
osfig.tx(ax, 7.0, 0.72,
         "最重要的一句话：教材是「会」的入口，动手算才是「做对」的唯一途径——每章的例题与自测题请务必先自己写一遍再对答案。",
         fs=11.5, bold=True)
osfig.save(fig, FIGDIR + "/ch0-02_study_route.png")
print("done")
