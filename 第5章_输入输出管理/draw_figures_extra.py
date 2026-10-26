# -*- coding: utf-8 -*-
"""第5章 扩写新增插图（ch5-14 ~ ch5-23）。运行：python3 draw_figures_extra.py"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L, GRAY, GRAY_L,
                   PINK, PINK_L)

FIG = "/Users/levi/IdeaProjects/操作系统/第5章_输入输出管理/figures/"
F = lambda n: FIG + n


# ---------- ch5-14 块/字符设备对比 ----------
def f14():
    fig, ax = osfig.new_fig(12, 5.6, xlim=(0, 12), ylim=(0, 5.6))
    osfig.title(ax, "块设备 vs 字符设备：一图分清",
                sub="块设备按「块」寻址可随机读；字符设备按字符流顺序传输、不可寻址", fs=15)
    osfig.rbox(ax, 0.8, 1.3, 5.0, 3.5, "", fc=BLUE_L, ec=BLUE)
    osfig.tx(ax, 3.3, 4.4, "块设备（Block）", fs=13, bold=True, color=BLUE)
    osfig.tx(ax, 3.3, 3.55, "信息交换单位：数据块\n传输速率较高、可寻址\n（能直接定位第 n 块）\n典型：磁盘、SSD、U盘", fs=11.5, ls=1.7)
    osfig.tx(ax, 3.3, 2.0, "访问方式：随机存取", fs=11.5, bold=True, color=INK)
    osfig.tx(ax, 3.3, 1.55, "常用缓冲 + DMA 提高性能", fs=10.5, color=GRAY)
    osfig.rbox(ax, 6.2, 1.3, 5.0, 3.5, "", fc=TEAL_L, ec=TEAL)
    osfig.tx(ax, 8.7, 4.4, "字符设备（Character）", fs=13, bold=True, color=TEAL)
    osfig.tx(ax, 8.7, 3.55, "信息交换单位：字符（字节流）\n传输速率较低、不可寻址\n（只能顺序读）\n典型：键盘、打印机、串口、鼠标", fs=11.5, ls=1.7)
    osfig.tx(ax, 8.7, 2.0, "访问方式：顺序存取", fs=11.5, bold=True, color=INK)
    osfig.tx(ax, 8.7, 1.55, "常采用中断驱动方式", fs=10.5, color=GRAY)
    osfig.tx(ax, 6, 0.7, "【考点】「磁盘是块设备、键盘是字符设备」配对题常考；「字符设备不可寻址所以只能顺序访问」判断", fs=11, color=RED, bold=True)
    osfig.tx(ax, 6, 0.25, "【延伸】网络设备（网卡）是第三类，走 socket 接口，不属于块/字符两分法", fs=10.5, color=GRAY)
    osfig.save(fig, F("ch5-14_block_char_devices.png"))


# ---------- ch5-15 程序直接控制 ----------
def f15():
    fig, ax = osfig.new_fig(12, 5.8, xlim=(0, 12), ylim=(0, 5.8))
    osfig.title(ax, "程序直接控制（轮询）：最原始的 I/O 方式",
                sub="CPU 反复读状态寄存器问「好了吗？」——设备慢，CPU 全程陪跑", fs=15)
    osfig.box(ax, 2.2, 3.6, 2.4, 1.1, "CPU", fc=BLUE_L, ec=BLUE, fs=14, bold=True)
    osfig.box(ax, 6.4, 3.6, 2.6, 1.1, "设备控制器\n状态寄存器", fc=AMBER_L, ec=AMBER, fs=11, bold=True)
    osfig.box(ax, 10.1, 3.6, 2.0, 1.1, "I/O 设备", fc=GRAY_L, ec=GRAY, fs=13, bold=True)
    osfig.arrow(ax, 3.4, 3.95, 5.1, 3.95, "① 读状态", color=BLUE, fs=10, dy=0.22)
    osfig.arrow(ax, 7.7, 3.95, 9.1, 3.95, "", color=GRAY, lw=1.6)
    osfig.tx(ax, 8.4, 4.3, "② 状态", fs=10, color=GRAY)
    osfig.arrow(ax, 3.4, 3.2, 5.1, 3.2, "③ 忙→继续问", color=RED, fs=10, dy=-0.25, ls=":")
    osfig.tx(ax, 2.2, 2.3, "循环：读状态 → 忙？→ 是：再读（原地打转）", fs=11.5, color=RED)
    osfig.tx(ax, 2.2, 1.8, "                     → 否：传一个字 → 继续", fs=11.5, color=INK)
    osfig.tx(ax, 6, 0.9, "代价：CPU 与设备完全串行——键盘敲 1 个字的时间够 CPU 空转几百万条指令", fs=11.5, color=RED, bold=True)
    osfig.tx(ax, 6, 0.4, "【考点】轮询方式中 CPU 与 I/O 设备「串行」工作；这个串行正是中断方式要解决的痛点", fs=11, color=RED)
    osfig.save(fig, F("ch5-15_polling_flow.png"))


# ---------- ch5-16 中断驱动流程 ----------
def f16():
    fig, ax = osfig.new_fig(12, 5.8, xlim=(0, 12), ylim=(0, 5.8))
    osfig.title(ax, "中断驱动方式：设备主动报告，CPU 不再陪跑",
                sub="CPU 发出启动命令后去干别的；设备准备好（或传完一个字）才中断 CPU 一次", fs=15)
    steps = [
        ("① CPU 发出读命令", "启动设备后立即转去执行其他进程", BLUE),
        ("② 设备自行准备/传送", "CPU 与设备并行工作", GREEN),
        ("③ 一个字准备好 → 中断", "设备控制器向 CPU 发中断信号", AMBER),
        ("④ CPU 保存现场 → 处理中断", "把字从控制器搬走，再发下一次读命令", RED),
        ("⑤ 恢复现场 → 回到原进程", "继续被中断的进程，等下一次中断", PURPLE),
    ]
    y = 4.55
    for i, (t, d, c) in enumerate(steps):
        osfig.circle(ax, 1.3, y, 0.32, str(i + 1), fc="white", ec=c, fs=11, bold=True, lw=2)
        osfig.tx(ax, 4.6, y, t, fs=12, bold=True, color=c, ha="left")
        osfig.tx(ax, 9.2, y, d, fs=10.5, color=GRAY, ha="left")
        if i < len(steps) - 1:
            osfig.line(ax, 1.3, y - 0.32, 1.3, y - 0.72, color=GRAY, lw=1.5)
        y -= 1.0
    osfig.tx(ax, 6, 0.42, "【考点】中断驱动按「字」传输：每传一个字就打断 CPU 一次——传一块数据要中断成百上千次，仍太碎 → DMA 登场", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch5-16_interrupt_io_flow.png"))


# ---------- ch5-17 通道方式 ----------
def f17():
    fig, ax = osfig.new_fig(12, 5.8, xlim=(0, 12), ylim=(0, 5.8))
    osfig.title(ax, "通道方式：请了一个「代驾 CPU」",
                sub="通道是弱化的专用处理器：CPU 委托一份「通道程序」，它自己搬完一整批数据才回来报告", fs=15)
    osfig.box(ax, 2.2, 4.2, 2.6, 1.0, "CPU\n（发启动指令后去干别的）", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True, ls=1.4)
    osfig.box(ax, 6.3, 4.2, 2.8, 1.0, "通道（能执行通道程序）", fc=PURPLE_L, ec=PURPLE, fs=11, bold=True)
    osfig.box(ax, 10.0, 4.2, 2.0, 1.0, "设备控制器", fc=AMBER_L, ec=AMBER, fs=10.5, bold=True)
    osfig.arrow(ax, 3.5, 4.2, 4.9, 4.2, "① 启动指令\n+通道程序入口", color=BLUE, fs=9, dy=0.42)
    osfig.arrow(ax, 7.7, 4.2, 9.0, 4.2, "", color=GRAY, lw=1.6)
    osfig.box(ax, 6.3, 2.2, 2.8, 0.9, "内存", fc=GREEN_L, ec=GREEN, fs=12, bold=True)
    osfig.arrow(ax, 7.4, 3.75, 7.0, 2.65, "② 数据直达内存\n（不经 CPU）", color=GREEN, fs=9.5, dx=0.55)
    osfig.arrow(ax, 5.0, 3.75, 5.4, 2.65, "", color=GRAY, lw=1.4)
    osfig.arrow(ax, 4.9, 1.9, 3.6, 3.7, "③ 全部传完 → 一次中断", color=RED, fs=10.5, dx=-0.4, dy=-0.5)
    osfig.tx(ax, 6, 1.0, "层级链：CPU → 通道 → 控制器 → 设备（一级管一级）；通道程序在内存中，由通道自己取指执行", fs=11, color=INK)
    osfig.tx(ax, 6, 0.45, "【考点】通道中断 ≠ 设备中断：通道是「一批数据全部完成」才向 CPU 报告一次；CPU 干预次数最少", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch5-17_channel_flow.png"))


# ---------- ch5-18 printf 逐层 ----------
def f18():
    fig, ax = osfig.new_fig(12, 5.8, xlim=(0, 12), ylim=(0, 5.8))
    osfig.title(ax, "一次 printf 的逐层下行（I/O 软件四层实战）",
                sub="printf → 库函数格式化 → write 系统调用 → 设备独立性软件 → 驱动 → 中断善后", fs=15)
    layers = [
        ("用户层 I/O 软件", "C 库 printf：格式化字符串（用户态）", BLUE, BLUE_L),
        ("设备独立性软件", "write 系统调用进入：检查参数、缓冲、命名映射（核心态）", GREEN, GREEN_L),
        ("设备驱动程序", "把「写 n 字节」翻译成写打印机控制器寄存器的命令", AMBER, AMBER_L),
        ("中断处理程序", "打印完成后：保存现场→取状态→恢复现场，唤醒等待进程", RED, RED_L),
        ("硬件", "控制器驱动打印机出纸", GRAY, GRAY_L),
    ]
    y = 4.6
    for i, (name, desc, c, fc) in enumerate(layers):
        osfig.rbox(ax, 0.8, y - 0.35, 2.6, 0.8, name, fc=fc, ec=c, fs=11, bold=True)
        osfig.tx(ax, 4.0, y + 0.05, desc, fs=10.5, ha="left", color=INK)
        if i < len(layers) - 1:
            osfig.arrow(ax, 2.1, y - 0.35, 2.1, y - 0.9, "", color=INK, lw=1.6, ms=12)
        y -= 1.08
    osfig.tx(ax, 6, 0.5, "【考点】每一层的职责边界就是考题：格式化在用户层；缓冲与命名映射在设备独立性软件；", fs=10.5, color=RED, bold=True)
    osfig.tx(ax, 6, 0.08, "写寄存器在驱动层；「保存/恢复现场」在中断处理层——归属判断每年必考", fs=10.5, color=RED, bold=True)
    osfig.save(fig, F("ch5-18_io_layers_example.png"))


# ---------- ch5-19 n块单缓冲时间轴 ----------
def f19():
    fig, ax = osfig.new_fig(12.5, 6.0, xlim=(0, 12.5), ylim=(0, 6.0))
    osfig.title(ax, "单缓冲连续处理 n 块：流水时间轴推导",
                sub="T=设备填缓冲，M=缓冲→工作区传送，C=CPU处理；稳态每块耗时 max(C,T)+M", fs=14.5)
    # 前两块的时间轴
    lanes = [("设备T", BLUE, [(0, 120), (140, 260), (280, 400)]),
             ("传送M", AMBER, [(120, 140), (260, 280), (400, 420)]),
             ("CPU C", GREEN, [(140, 220), (280, 360), (420, 500)])]
    y = 4.4
    for name, c, spans in lanes:
        osfig.tx(ax, 0.7, y + 0.18, name, fs=10.5, ha="left", color=INK)
        for (a, b) in spans:
            osfig.rect(ax, 2.2 + a / 500 * 9.0, y, (b - a) / 500 * 9.0, 0.42, "", fc=(BLUE_L if c == BLUE else AMBER_L if c == AMBER else GREEN_L), ec=c, lw=1.4)
        y -= 0.85
    for t in [0, 120, 140, 260, 280, 400, 500]:
        osfig.tx(ax, 2.2 + t / 500 * 9.0, 1.95, str(t), fs=8.5, color=GRAY)
    osfig.tx(ax, 6.25, 1.35, "第 1 块：T + M + C = 120+20+80 = 220μs（流水还没转起来）", fs=11, color=INK)
    osfig.tx(ax, 6.25, 0.9, "第 2 块起进入稳态：每块 max(C,T) + M = max(80,120)+20 = 140μs", fs=11.5, bold=True, color=RED)
    osfig.tx(ax, 6.25, 0.45, "总时间 = T + M + C + (n−1)×max(C,T)+M？——警惕！正确式：首块 T+M+C，其后每块 max(C,T)+M", fs=10.5, color=BLUE)
    osfig.save(fig, F("ch5-19_buffer_n_blocks.png"))


# ---------- ch5-20 双缓冲时间轴 ----------
def f20():
    fig, ax = osfig.new_fig(12.5, 5.6, xlim=(0, 12.5), ylim=(0, 5.6))
    osfig.title(ax, "双缓冲为什么更快：填另一个缓冲与处理并行",
                sub="设备往缓冲2 填数时，CPU 正处理来自缓冲1 的数据——两条流水线咬合", fs=14.5)
    lanes = [("设备T", BLUE, [(0, 120), (140, 260), (280, 400), (420, 540)]),
             ("传送M", AMBER, [(120, 140), (260, 280), (400, 420), (540, 560)]),
             ("CPU C", GREEN, [(120, 200), (260, 340), (400, 480), (540, 620)])]
    y = 3.9
    for name, c, spans in lanes:
        osfig.tx(ax, 0.7, y + 0.18, name, fs=10.5, ha="left", color=INK)
        for (a, b) in spans:
            osfig.rect(ax, 2.2 + a / 620 * 9.3, y, (b - a) / 620 * 9.3, 0.42, "", fc=(BLUE_L if c == BLUE else AMBER_L if c == AMBER else GREEN_L), ec=c, lw=1.4)
        y -= 0.85
    for t in [0, 120, 200, 260, 340, 400, 480, 540, 620]:
        osfig.tx(ax, 2.2 + t / 620 * 9.3, 1.85, str(t), fs=8.5, color=GRAY)
    osfig.tx(ax, 6.25, 1.25, "每块耗时 max(C+M, T) = max(80+20, 120) = 120μs（本例恰好 T 是瓶颈，设备不停歇）", fs=11.5, bold=True, color=RED)
    osfig.tx(ax, 6.25, 0.7, "对比单缓冲 140μs/块 → 双缓冲提速约 17%；若 C+M < T，瓶颈在设备：双缓冲让设备「连续满速」工作", fs=11, color=INK)
    osfig.tx(ax, 6.25, 0.25, "【考点】双缓冲公式 max(C+M, T)；两台机器通信时双缓冲可全双工", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch5-20_double_buffer_timeline.png"))


# ---------- ch5-21 安全/不安全分配 ----------
def f21():
    fig, ax = osfig.new_fig(12, 5.6, xlim=(0, 12), ylim=(0, 5.6))
    osfig.title(ax, "设备分配中的安全方式 vs 不安全方式",
                sub="安全=发出 I/O 就阻塞（不会死锁但串行）；不安全=继续运行申请更多设备（高效但可能死锁）", fs=14.5)
    # 安全
    osfig.rbox(ax, 0.8, 1.3, 5.0, 3.4, "", fc=GREEN_L, ec=GREEN)
    osfig.tx(ax, 3.3, 4.35, "安全分配方式", fs=13, bold=True, color=GREEN)
    osfig.tx(ax, 3.3, 3.4, "进程发出 I/O 请求后\n立即进入阻塞态，\n重新调度其他进程", fs=11.5, ls=1.7)
    osfig.tx(ax, 3.3, 2.25, "请求并保持被破坏 → 不会死锁", fs=11, bold=True, color=GREEN)
    osfig.tx(ax, 3.3, 1.7, "缺点：一个进程同时只能用一台设备，效率低", fs=10.5, color=GRAY)
    # 不安全
    osfig.rbox(ax, 6.2, 1.3, 5.0, 3.4, "", fc=RED_L, ec=RED)
    osfig.tx(ax, 8.7, 4.35, "不安全分配方式", fs=13, bold=True, color=RED)
    osfig.tx(ax, 8.7, 3.4, "发出 I/O 请求后继续运行，\n还能再申请别的设备，\n需要时才阻塞", fs=11.5, ls=1.7)
    osfig.tx(ax, 8.7, 2.25, "优点：设备利用率高、推进快", fs=11, bold=True, color=AMBER)
    osfig.tx(ax, 8.7, 1.7, "风险：多个设备互相等待 → 可能死锁", fs=10.5, color=RED)
    osfig.tx(ax, 6, 0.7, "【考点】「安全分配方式破坏了请求并保持条件」对；「不安全分配方式一定会死锁」错（是「可能」）", fs=11, color=RED, bold=True)
    osfig.tx(ax, 6, 0.25, "【关联】这就是第2章死锁四条件里「请求并保持」在设备分配上的具体化", fs=10.5, color=GRAY)
    osfig.save(fig, F("ch5-21_safety_alloc.png"))


# ---------- ch5-22 SPOOLing 时间轴 ----------
def f22():
    fig, ax = osfig.new_fig(12.5, 5.6, xlim=(0, 12.5), ylim=(0, 5.6))
    osfig.title(ax, "SPOOLing 打印排队时间轴：三个进程「同时」打印的真相",
                sub="用户进程瞬间「拿到」打印机（其实拿到的是输出井里的盘块）；物理打印逐份排队", fs=14.5)
    lanes = [
        ("用户进程1", BLUE, [(0, 20)]),
        ("用户进程2", TEAL, [(30, 50)]),
        ("用户进程3", PURPLE, [(60, 80)]),
        ("输出进程+打印机", GREEN, [(100, 260), (260, 420), (420, 580)]),
    ]
    y = 4.1
    for name, c, spans in lanes:
        osfig.tx(ax, 0.7, y + 0.15, name, fs=10.5, ha="left", color=INK)
        for (a, b) in spans:
            osfig.rect(ax, 2.6 + a / 580 * 8.8, y, (b - a) / 580 * 8.8, 0.44, "", fc=(BLUE_L if c == BLUE else TEAL_L if c == TEAL else PURPLE_L if c == PURPLE else GREEN_L), ec=c, lw=1.4)
        y -= 0.75
    for t in [0, 100, 260, 420, 580]:
        osfig.tx(ax, 2.6 + t / 580 * 8.8, 1.75, str(t), fs=8.5, color=GRAY)
    osfig.tx(ax, 6.25, 1.2, "0~80μs：三个进程都「申请成功」——各自把数据写进输出井的不同盘块（逻辑上各占一台「虚拟打印机」）", fs=10.5, color=INK)
    osfig.tx(ax, 6.25, 0.75, "100μs 起：输出进程按队列逐份真打印——物理打印机任何时刻只服务一个任务（独占设备本性未变）", fs=10.5, color=RED)
    osfig.tx(ax, 6.25, 0.3, "【考点】SPOOLing 把「独占设备」改造成「共享设备」靠的是：磁盘排队 + 输出进程代劳；代价是占用磁盘与内存", fs=10.5, color=RED, bold=True)
    osfig.save(fig, F("ch5-22_spooling_print_timeline.png"))


# ---------- ch5-23 LUT 与重定向 ----------
def f23():
    fig, ax = osfig.new_fig(12, 5.4, xlim=(0, 12), ylim=(0, 5.4))
    osfig.title(ax, "设备独立性：逻辑设备名 → 物理设备名 的翻译官 LUT",
                sub="程序只说「往打印机上打印」，具体是哪台打印机，由 LUT 查表决定——换设备不用改程序", fs=14.5)
    # LUT 表
    osfig.tx(ax, 2.4, 4.55, "逻辑设备表 LUT", fs=12, bold=True, color=BLUE)
    osfig.rect(ax, 0.9, 3.85, 1.9, 0.5, "逻辑设备名", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 2.8, 3.85, 1.9, 0.5, "物理设备名", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 4.7, 3.85, 1.9, 0.5, "驱动入口", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    lut = [("printer", "LPTR_3楼", "驱动A"), ("disk", "SDA_2", "驱动B")]
    y = 3.85
    for a, b, c in lut:
        y -= 0.55
        osfig.rect(ax, 0.9, y, 1.9, 0.55, a, fc=BLUE_L, ec=BLUE, fs=10.5)
        osfig.rect(ax, 2.8, y, 1.9, 0.55, b, fc="white", ec=GRAY, fs=10)
        osfig.rect(ax, 4.7, y, 1.9, 0.55, c, fc="white", ec=GRAY, fs=10)
    # 两种设置
    osfig.tx(ax, 9.0, 4.55, "LUT 的两种设置方式", fs=12, bold=True, color=AMBER)
    osfig.tx(ax, 9.0, 3.9, "① 全系统一张 LUT：\n   单用户系统，简单", fs=11, color=INK, ls=1.5)
    osfig.tx(ax, 9.0, 2.95, "② 每用户一张 LUT：\n   多用户系统，各用各的\n   逻辑名互不冲突", fs=11, color=INK, ls=1.5)
    osfig.tx(ax, 6, 1.6, "I/O 重定向：把逻辑设备名临时指向别处（如把「打印」重定向为「写入文件」），程序一行不改", fs=11, color=TEAL)
    osfig.tx(ax, 6, 0.9, "设备独立性两大好处：① 用户程序与物理设备解耦（可移植）；② 便于设备分配与故障切换", fs=11, color=INK)
    osfig.tx(ax, 6, 0.35, "【考点】「逻辑设备名是用户程序中使用的、暂不指定物理设备的名」——定义判断题", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch5-23_lut_redirect.png"))


if __name__ == "__main__":
    f14(); f15(); f16(); f17(); f18(); f19(); f20(); f21(); f22(); f23()
    print("ch5 extras done")
