# -*- coding: utf-8 -*-
"""第1章 扩写新增插图（ch1-16 ~ ch1-25）。运行：python3 draw_figures_extra.py"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L, GRAY, GRAY_L,
                   PINK, PINK_L)

FIG = "/Users/levi/IdeaProjects/操作系统/第1章_操作系统概述/figures/"
F = lambda n: FIG + n


# ---------- ch1-16 三种接口 ----------
def f16():
    fig, ax = osfig.new_fig(12, 5.6, xlim=(0, 12), ylim=(0, 5.6))
    osfig.title(ax, "操作系统向用户提供的三种接口",
                sub="命令行给「打字的人」，GUI 给「点鼠标的人」，系统调用给「写程序的人」", fs=16)
    cols = [
        (0.6, "命令接口（CLI）", BLUE, BLUE_L,
         "联机命令接口：交互式终端\n输入一条命令 → 立即执行\n如 ls / dir、cd\n\n脱机命令接口：批处理作业\n控制语言 JCL",
         "使用者：普通用户/运维\n[用户态为主，命令解释器执行]"),
        (4.4, "图形用户接口（GUI）", GREEN, GREEN_L,
         "窗口 / 图标 / 菜单 / 指针\n双击图标 = 发出命令\n如 macOS Finder、Windows 桌面\n\n本质仍是调用系统功能",
         "使用者：普通用户\n[用户态，界面进程代为请求服务]"),
        (8.2, "程序接口（系统调用）", AMBER, AMBER_L,
         "由一组系统调用组成\n只允许「程序」使用\n如 fork() / read() / write()\n\n是用户程序获得 OS 服务的\n唯一合法通道",
         "使用者：程序员（程序）\n[陷入核心态执行，最重要的考点]"),
    ]
    for x, name, ec, fc, body, tag in cols:
        osfig.rbox(ax, x, 1.0, 3.2, 3.9, "", fc=fc, ec=ec)
        osfig.tx(ax, x + 1.6, 4.55, name, fs=13, bold=True, color=ec)
        osfig.tx(ax, x + 1.6, 3.15, body, fs=10.5, ls=1.55)
        osfig.tx(ax, x + 1.6, 1.42, tag, fs=9.5, color=ec, bold=True)
    osfig.tx(ax, 6, 0.5, "【考点】命令接口和 GUI 是给「用户」的，程序接口（系统调用）是给「程序」的——判断题常考",
             fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch1-16_three_interfaces.png"))


# ---------- ch1-17 单道 vs 多道内存布局 ----------
def f17():
    fig, ax = osfig.new_fig(12, 6.2, xlim=(0, 12), ylim=(0, 6.2))
    osfig.title(ax, "单道批处理 vs 多道批处理：内存里住着谁", fs=16)
    osfig.tx(ax, 3, 5.35, "① 单道：一次只有一道作业", fs=13, bold=True, color=BLUE)
    osfig.rect(ax, 1.8, 4.35, 2.4, 0.55, "操作系统", fc=GRAY_L, ec=GRAY, fs=11, bold=True)
    osfig.rect(ax, 1.8, 2.35, 2.4, 1.9, "作业 A\n(独占全部资源)", fc=BLUE_L, ec=BLUE, fs=11.5, bold=True)
    osfig.rect(ax, 1.8, 1.35, 2.4, 0.9, "空闲（也用不了）", fc="white", ec=GRAY, fs=10)
    osfig.tx(ax, 3, 0.85, "A 做 I/O 时 CPU 干等 → 利用率低", fs=10.5, color=RED)
    osfig.tx(ax, 9, 5.35, "② 多道：内存同时驻留多道", fs=13, bold=True, color=GREEN)
    osfig.rect(ax, 7.8, 4.35, 2.4, 0.55, "操作系统", fc=GRAY_L, ec=GRAY, fs=11, bold=True)
    osfig.rect(ax, 7.8, 3.75, 2.4, 0.52, "作业 A", fc=BLUE_L, ec=BLUE, fs=11, bold=True)
    osfig.rect(ax, 7.8, 3.15, 2.4, 0.52, "作业 B", fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    osfig.rect(ax, 7.8, 2.55, 2.4, 0.52, "作业 C", fc=PURPLE_L, ec=PURPLE, fs=11, bold=True)
    osfig.tx(ax, 9, 1.95, "宏观并行：A 用 CPU 时，B 在 I/O", fs=10.5, color=GREEN)
    osfig.tx(ax, 9, 1.5, "微观串行：单 CPU 任一时刻只跑一道", fs=10.5, color=AMBER)
    osfig.tx(ax, 9, 1.0, "特点：多道 / 宏观并行 / 微观串行", fs=10.5, bold=True, color=INK)
    osfig.tx(ax, 6, 0.42, "【考点】「多道」指内存中同时存放多道程序，与「并行处理（多CPU）」不是一回事",
             fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch1-17_single_vs_multi_memory.png"))


# ---------- ch1-18 分时时间轴 ----------
def f18():
    fig, ax = osfig.new_fig(12, 5.2, xlim=(0, 12), ylim=(0, 5.2))
    osfig.title(ax, "分时系统：时间片轮转（q = 10ms，3 个终端）",
                sub="每个用户都感觉「整台机器只为我服务」——因为 10ms 内必轮到我一次", fs=15)
    seq = [("A", BLUE, BLUE_L), ("B", GREEN, GREEN_L), ("C", PURPLE, PURPLE_L)]
    x0, w = 1.2, 1.9
    for i, (name, ec, fc) in enumerate(seq):
        osfig.rect(ax, x0 + i * w, 3.0, w, 1.1, name + " 的 10ms", fc=fc, ec=ec, fs=12, bold=True)
    for i in range(4):
        osfig.tx(ax, x0 + i * w, 2.6, str(i * 10), fs=10, color=GRAY)
    osfig.tx(ax, x0 + 3 * w + 0.45, 3.55, "…", fs=20, bold=True)
    osfig.tx(ax, x0 + 3 * w + 0.45, 3.0, "循环", fs=10, color=GRAY)
    osfig.tx(ax, 6, 4.6, "第 1 轮：A → B → C    第 2 轮：A → B → C    ……", fs=12, bold=True, color=INK)
    osfig.tx(ax, 6, 1.7, "响应时间的估算：最坏情况 = 用户数 × 时间片", fs=12, bold=True, color=BLUE)
    osfig.tx(ax, 6, 1.15, "例：20 个终端、时间片 100ms → 某用户最坏要等 20×100ms = 2s 才轮到", fs=11.5, color=INK)
    osfig.tx(ax, 6, 0.6, "时间片越小响应越快，但切换开销占比越大 → 时间片要「适中」", fs=11, color=RED)
    osfig.save(fig, F("ch1-18_timeshare_timeline.png"))


# ---------- ch1-19 实时系统 ----------
def f19():
    fig, ax = osfig.new_fig(12, 5.4, xlim=(0, 12), ylim=(0, 5.4))
    osfig.title(ax, "实时系统：必须在期限（Deadline）内完成",
                sub="首要目标是「及时」与「可靠」，吞吐量、周转时间都是次要目标", fs=15)
    osfig.rbox(ax, 0.7, 1.2, 5.0, 3.5, "", fc=RED_L, ec=RED)
    osfig.tx(ax, 3.2, 4.3, "硬实时：错过期限 = 灾难", fs=13.5, bold=True, color=RED)
    osfig.tx(ax, 3.2, 3.35, "汽车安全气囊控制器：碰撞后必须在几毫秒内弹出", fs=11)
    osfig.tx(ax, 3.2, 2.8, "导弹飞行控制、工业过程控制、心脏起搏器", fs=11)
    osfig.tx(ax, 3.2, 2.0, "要求：绝对不能迟", fs=11.5, bold=True, color=RED)
    osfig.tx(ax, 3.2, 1.55, "设计取向：牺牲吞吐，保证确定性", fs=10.5, color=GRAY)
    osfig.rbox(ax, 6.3, 1.2, 5.0, 3.5, "", fc=AMBER_L, ec=AMBER)
    osfig.tx(ax, 8.8, 4.3, "软实时：偶尔超时可以容忍", fs=13.5, bold=True, color=AMBER)
    osfig.tx(ax, 8.8, 3.35, "视频播放：偶尔丢一帧只是卡一下", fs=11)
    osfig.tx(ax, 8.8, 2.8, "订票网站响应、股票行情推送", fs=11)
    osfig.tx(ax, 8.8, 2.0, "要求：大多数时候要及时", fs=11.5, bold=True, color=AMBER)
    osfig.tx(ax, 8.8, 1.55, "设计取向：统计意义上的及时", fs=10.5, color=GRAY)
    osfig.tx(ax, 6, 0.55, "【考点】实时系统「可靠性 > 性能 > 灵活性/交互性」；与分时系统对比：不强调「公平轮转」，强调「按紧急程度抢占」",
             fs=10.5, color=RED, bold=True)
    osfig.save(fig, F("ch1-19_realtime_systems.png"))


# ---------- ch1-20 特权指令判定 ----------
def f20():
    fig, ax = osfig.new_fig(12, 7.6, xlim=(0, 12), ylim=(0, 7.6))
    osfig.title(ax, "专项训练：逐条判定特权指令",
                sub="口诀：凡是「动硬件、动系统关键数据、影响别人」的指令都是特权指令", fs=14.5)
    rows = [
        ("启动 I/O 的指令（如启动 DMA）", "[特权]", "直接控制设备，用户乱用会冲掉别人数据", RED, RED_L),
        ("设置时钟的指令（置时钟初值）", "[特权]", "时钟归内核管，改了会扰乱时间片与调度", RED, RED_L),
        ("把 PSW 置为核心态（修改状态标志）", "[特权]", "若用户能改，就能自己进核心态 = 安全机制失效", RED, RED_L),
        ("清空 / 整块改写内存", "[特权]", "可能清到别人（甚至内核）的内存", RED, RED_L),
        ("修改页表基址寄存器（PTBR）", "[特权]", "页表是地址翻译的根，改了能访问任意物理地址", RED, RED_L),
        ("屏蔽 / 开放中断的指令", "[特权]", "关中断是原语实现的基础，只允许内核用", RED, RED_L),
        ("读取时钟的指令", "[非特权]", "读时间不改变系统状态，普通程序也要用", GREEN, GREEN_L),
        ("普通算术 / 逻辑运算（加、移位等）", "[非特权]", "只在用户自己的寄存器/内存里操作", GREEN, GREEN_L),
    ]
    y = 6.5
    for name, tag, reason, ec, fc in rows:
        osfig.rbox(ax, 0.6, y - 0.62, 5.4, 0.52, name, fc="white", ec=INK, fs=11, lw=1.2)
        osfig.rbox(ax, 6.1, y - 0.62, 1.15, 0.52, tag, fc=fc, ec=ec, fs=10.5, bold=True, lw=1.2)
        osfig.tx(ax, 8.9, y - 0.36, reason, fs=10, color=INK, ha="left")
        y -= 0.72
    osfig.tx(ax, 6, 0.35, "记忆：读一般无害（非特权）；写系统状态必特权。存内存数据本身非特权，但「清整块内存」是特权。",
             fs=11, color=BLUE, bold=True)
    osfig.save(fig, F("ch1-20_privileged_check.png"))


# ---------- ch1-21 态切换全景 ----------
def f21():
    fig, ax = osfig.new_fig(12, 5.8, xlim=(0, 12), ylim=(0, 5.8))
    osfig.title(ax, "用户态 与 核心态：切换不对称",
                sub="进去有三个门，出来只有一条路（且必须由内核程序亲自走）", fs=15)
    osfig.rbox(ax, 1.2, 2.3, 3.4, 1.9, "用户态（目态）\n\n跑应用程序", fc=BLUE_L, ec=BLUE, fs=12, bold=True, ls=1.6)
    osfig.rbox(ax, 7.4, 2.3, 3.4, 1.9, "核心态（管态）\n\n跑内核程序", fc=RED_L, ec=RED, fs=12, bold=True, ls=1.6)
    osfig.arrow(ax, 4.6, 3.9, 7.4, 3.6, "硬件中断机制自动切换", color=RED, fs=10.5, dy=0.3)
    osfig.tx(ax, 3.1, 4.75, "① 系统调用陷入", fs=10, color=BLUE, bold=True)
    osfig.tx(ax, 3.1, 4.42, "② 异常（内中断）", fs=10, color=AMBER, bold=True)
    osfig.tx(ax, 3.1, 4.09, "③ 外中断到达", fs=10, color=GREEN, bold=True)
    osfig.arrow(ax, 7.4, 2.75, 4.6, 2.75, "内核程序执行修改 PSW 的特权指令返回（如 iret）", color=BLUE, fs=10.5, dy=-0.32)
    osfig.tx(ax, 6, 1.35, "【易错】应用「主动要服务」走 trap；系统「主动打断」走中断。两种切换都不是应用程序自己完成的。",
             fs=11, color=RED, bold=True)
    osfig.tx(ax, 6, 0.85, "【考点】用户态→核心态的唯一途径 = 中断（广义：含陷入与异常）；核心态→用户态 = 执行特权指令",
             fs=11, color=BLUE)
    osfig.save(fig, F("ch1-21_mode_switch.png"))


# ---------- ch1-22 中断判定 ----------
def f22():
    fig, ax = osfig.new_fig(12, 7.8, xlim=(0, 12), ylim=(0, 7.8))
    osfig.title(ax, "专项训练：内中断 or 外中断？十连判",
                sub="两步判定法：第1步 与当前指令有关吗？有关→内中断；无关→外中断", fs=14.5)
    rows = [
        ("除零 / 运算溢出", "内", "就是当前这条算术指令引起的", PINK),
        ("缺页（访问的页不在内存）", "内", "当前访存指令引起，可恢复后重执行", PINK),
        ("地址越界 / 非法操作码", "内", "当前指令本身非法", PINK),
        ("陷入 trap（系统调用）", "内", "当前这条陷入指令「故意」引发", PINK),
        ("程序严重错误引发的终止 abort", "内", "内核直接终止该进程", PINK),
        ("时钟中断（时间片到）", "外", "时钟芯片发信号，与当前指令无关", TEAL),
        ("键盘输入 / Ctrl-C", "外", "外设/人工干预，与当前指令无关", TEAL),
        ("磁盘 I/O 完成中断", "外", "设备就绪信号，与当前指令无关", TEAL),
    ]
    y = 6.9
    for name, tag, reason, c in rows:
        osfig.rbox(ax, 0.6, y - 0.58, 5.2, 0.5, name, fc="white", ec=INK, fs=11, lw=1.2)
        osfig.rbox(ax, 5.9, y - 0.58, 0.95, 0.5, tag + "中断",
                   fc=(PINK_L if tag == "内" else TEAL_L), ec=c, fs=10.5, bold=True, lw=1.2)
        osfig.tx(ax, 8.8, y - 0.33, reason, fs=10, color=INK, ha="left")
        y -= 0.66
    osfig.tx(ax, 6, 1.15, "补充理解：内中断=异常（CPU 自己撞上的）；外中断=狭义中断（别人敲的门）。",
             fs=11.5, bold=True, color=BLUE)
    osfig.tx(ax, 6, 0.62, "【易错】缺页是「内中断」不是 I/O 中断——它由当前指令触发，只是处理时要去做 I/O。",
             fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch1-22_interrupt_judge.png"))


# ---------- ch1-23 printf 调用链 ----------
def f23():
    fig, ax = osfig.new_fig(11, 7.4, xlim=(0, 11), ylim=(0, 7.4))
    osfig.title(ax, "printf 的完整旅程：从库函数到硬件",
                sub="库函数在用户态干活，只有陷入内核那一刻才「升态」", fs=15)
    layers = [
        ("应用程序：printf(\"hi\")", "用户态", BLUE, BLUE_L),
        ("C 库函数 printf：拼好格式串 → 调用 write()", "用户态", BLUE, BLUE_L),
        ("write()：装好参数，执行陷入指令 trap", "用户态→触发", AMBER, AMBER_L),
        ("内核 sys_write：检查参数、缓冲处理", "核心态", RED, RED_L),
        ("设备驱动程序：写控制器寄存器，启动 I/O", "核心态", RED, RED_L),
        ("硬件控制器：把数据送到显示器", "硬件", GRAY, GRAY_L),
    ]
    y = 6.3
    for i, (name, tag, ec, fc) in enumerate(layers):
        osfig.rbox(ax, 1.2, y - 0.52, 5.6, 0.72, name, fc=fc, ec=ec, fs=10.5, bold=True, lw=1.6)
        osfig.rbox(ax, 7.1, y - 0.42, 1.55, 0.5, tag, fc="white", ec=ec, fs=9.5, bold=True, lw=1.4)
        if i < len(layers) - 1:
            osfig.arrow(ax, 4.0, y - 0.52, 4.0, y - 0.88, color=INK, lw=1.6, ms=12)
        y -= 1.06
    osfig.tx(ax, 4.6, 0.42, "库函数不是系统调用：它在用户态包装了系统调用", fs=10, color=BLUE)
    osfig.tx(ax, 5.5, 0.05, "【易错】引发系统调用的陷入指令在用户态执行；系统调用服务例程在核心态执行。",
             fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch1-23_libcall_chain.png"))


# ---------- ch1-24 微内核开销 ----------
def f24():
    fig, ax = osfig.new_fig(12, 6.0, xlim=(0, 12), ylim=(0, 6.0))
    osfig.title(ax, "微内核为什么「慢」：一次读文件的往返之旅",
                sub="功能被搬到用户态服务进程后，每用一次服务都要「进出内核 + 传消息」", fs=15)
    osfig.tx(ax, 3.1, 5.15, "微内核：客户-服务器式消息往返", fs=12.5, bold=True, color=PURPLE)
    osfig.rbox(ax, 0.8, 3.9, 4.6, 0.62, "用户进程（请求读文件）", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
    osfig.rbox(ax, 0.8, 3.0, 4.6, 0.62, "内核（只管消息转发/调度）", fc=PURPLE_L, ec=PURPLE, fs=10.5, bold=True)
    osfig.rbox(ax, 0.8, 2.1, 4.6, 0.62, "文件服务进程（用户态）", fc=GREEN_L, ec=GREEN, fs=10.5, bold=True)
    osfig.rbox(ax, 0.8, 1.2, 4.6, 0.62, "设备驱动进程（用户态）", fc=AMBER_L, ec=AMBER, fs=10.5, bold=True)
    osfig.arrow(ax, 5.4, 4.2, 5.4, 3.3, color=INK, lw=1.6, ms=12)
    osfig.arrow(ax, 5.4, 3.0, 5.4, 2.4, color=INK, lw=1.6, ms=12)
    osfig.arrow(ax, 5.4, 2.1, 5.4, 1.5, color=INK, lw=1.6, ms=12)
    osfig.tx(ax, 3.1, 0.7, "来回消息传递 + 多次态切换", fs=10.5, color=RED, bold=True)
    osfig.tx(ax, 9.0, 5.15, "大内核：一次陷入全搞定", fs=12.5, bold=True, color=BLUE)
    osfig.rbox(ax, 6.7, 3.55, 4.6, 1.15, "内核（文件系统/驱动\n全是内核函数调用）", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True, ls=1.5)
    osfig.rbox(ax, 6.7, 2.35, 4.6, 0.62, "用户进程（请求读文件）", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
    osfig.arrow(ax, 9.0, 3.55, 9.0, 3.0, "一次陷入/一次返回", color=INK, lw=1.8, fs=10, ms=12)
    osfig.tx(ax, 9.0, 1.7, "普通函数调用，开销小", fs=10.5, color=GREEN, bold=True)
    osfig.tx(ax, 6, 0.85, "【考点】微内核优点：可靠性/稳定性高、便于扩展维护；缺点：性能低（频繁切换态+消息传递）。",
             fs=11, color=RED, bold=True)
    osfig.tx(ax, 6, 0.4, "典型的微内核功能清单：进程调度、基本进程通信、中断处理、时钟管理（只留最基本功能）。",
             fs=11, color=BLUE)
    osfig.save(fig, F("ch1-24_microkernel_cost.png"))


# ---------- ch1-25 引导磁盘布局 ----------
def f25():
    fig, ax = osfig.new_fig(12, 6.4, xlim=(0, 12), ylim=(0, 6.4))
    osfig.title(ax, "操作系统引导：磁盘视角与 CPU 视角对照",
                sub="CPU 一步步「按图索骥」地从磁盘把内核搬进内存", fs=15)
    osfig.tx(ax, 3.2, 5.55, "磁盘上的「开机户口本」", fs=12.5, bold=True, color=AMBER)
    osfig.rect(ax, 0.8, 4.45, 1.9, 0.85, "MBR\n0号扇区", fc=AMBER_L, ec=AMBER, fs=10.5, bold=True)
    osfig.tx(ax, 1.75, 4.02, "= 磁盘引导程序 + 分区表", fs=9.5, color=GRAY)
    osfig.rect(ax, 3.0, 4.45, 1.9, 0.85, "PBR\n活动分区首扇区", fc=GREEN_L, ec=GREEN, fs=10, bold=True)
    osfig.tx(ax, 3.95, 4.02, "= 分区引导记录", fs=9.5, color=GRAY)
    osfig.rect(ax, 5.2, 4.45, 1.9, 0.85, "启动管理器", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
    osfig.rect(ax, 7.4, 4.45, 1.9, 0.85, "OS 内核映像", fc=RED_L, ec=RED, fs=10.5, bold=True)
    osfig.tx(ax, 3.2, 3.45, "CPU 的执行流", fs=12.5, bold=True, color=BLUE)
    steps = [
        "加电 → 硬件自动执行 ROM 中 BIOS",
        "BIOS 硬件自检（加电自检）→ 读 MBR 至内存并执行",
        "MBR 的磁盘引导程序找活动分区 → 读 PBR 并执行",
        "PBR 读入启动管理器 → 它再装入 OS 内核",
        "内核初始化（装驱动、建初始进程…）→ 登录界面",
    ]
    y = 2.95
    for i, s in enumerate(steps):
        osfig.circle(ax, 1.15, y, 0.24, str(i + 1), fc=BLUE_L, ec=BLUE, fs=10.5)
        osfig.tx(ax, 3.9, y, s, fs=11, ha="left")
        if i < len(steps) - 1:
            osfig.line(ax, 1.15, y - 0.24, 1.15, y - 0.5, color=GRAY, lw=1.4)
        y -= 0.56
    osfig.tx(ax, 6, 0.42, "【考点】MBR 在磁盘 0 号扇区；OS 内核最终被加载到 RAM；BIOS 固化在 ROM 中。",
             fs=11.5, color=RED, bold=True)
    osfig.save(fig, F("ch1-25_boot_disk_layout.png"))


if __name__ == "__main__":
    f16(); f17(); f18(); f19(); f20(); f21(); f22(); f23(); f24(); f25()
    print("all extras done")
