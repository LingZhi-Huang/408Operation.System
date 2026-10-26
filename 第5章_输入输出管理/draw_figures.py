# -*- coding: utf-8 -*-
"""第5章 输入/输出(I/O)管理 —— 全部插图绘制脚本（唯一脚本）。
用法：python3 第5章_输入输出管理/draw_figures.py
依赖：/Users/levi/IdeaProjects/操作系统/osfig.py（只import，不修改）
"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
import matplotlib.pyplot as plt
from osfig import (new_fig, title, tx, rbox, box, rect, diamond, ellipse,
                   circle, arrow, line, save,
                   INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L,
                   GRAY, GRAY_L, PINK, PINK_L, YELLOW)

OUT = "/Users/levi/IdeaProjects/操作系统/第5章_输入输出管理/figures"


# ============================================================ 00 知识框架导图
def fig00():
    fig, ax = new_fig(15, 9.8, xlim=(0, 15), ylim=(0, 9.8))
    title(ax, "第5章 输入/输出(I/O)管理 · 知识框架导图",
          sub="主线：CPU 干预越来越少、设备与 CPU 并行度越来越高；软件层越来越厚、分工越来越细")

    box(ax, 7.5, 7.95, 6.8, 1.0, "第5章　输入/输出(I/O)管理",
        fc=BLUE_L, ec=BLUE, fs=15, bold=True)

    # 三个栏目头
    hdr = [("Ⅰ　I/O硬件基础", 2.4, BLUE),
           ("Ⅱ　控制方式与层次 ★重点", 7.5, PURPLE),
           ("Ⅲ　缓冲·分配·共享 ★重点", 12.6, GREEN)]
    for s, x, c in hdr:
        box(ax, x, 6.3, 4.6, 0.7, s, fc="white", ec=c, fs=12, bold=True)
        arrow(ax, 7.5, 7.45, x, 6.66, color=c, lw=1.8)

    # 栏目Ⅰ：两个叶子
    box(ax, 2.4, 4.85, 4.1, 1.5, "5.1 I/O设备概述\n分类：使用特性/传输速率/信息交换单位\n块设备 vs 字符设备",
        fc=BLUE_L, ec=BLUE, fs=10)
    box(ax, 2.4, 3.05, 4.1, 1.5, "5.2 I/O控制器\n三类寄存器：数据/状态/控制\n编址：内存映射 vs 独立编址",
        fc=BLUE_L, ec=BLUE, fs=10)
    tx(ax, 2.4, 2.15, "【考点】给设备判断类别", fs=10, color=BLUE, bold=True)

    # 栏目Ⅱ：三个叶子
    box(ax, 7.5, 5.15, 4.1, 1.45, "5.3 I/O控制方式 ★必考\n①程序直接控制②中断驱动\n③DMA④通道",
        fc=PURPLE_L, ec=PURPLE, fs=10)
    box(ax, 7.5, 3.5, 4.1, 1.45, "5.4 I/O软件层次 ★必考\n四层：用户/设备独立性/驱动/中断\n【考点】功能归属判断",
        fc=PURPLE_L, ec=PURPLE, fs=10)
    box(ax, 7.5, 1.85, 4.1, 1.45, "5.5 应用程序I/O接口\n块/字符/网络设备接口\n阻塞 vs 非阻塞",
        fc=PURPLE_L, ec=PURPLE, fs=10)

    # 栏目Ⅲ：四个叶子
    box(ax, 12.6, 5.5, 4.1, 1.35, "5.6 缓冲区管理 ★必考(计算)\n单/双/循环缓冲、缓冲池\nT/M/C 时间轴推演",
        fc=GREEN_L, ec=GREEN, fs=10)
    box(ax, 12.6, 4.1, 4.1, 1.2, "5.7 设备分配\nSDT→DCT→COCT→CHCT\n安全 vs 不安全分配",
        fc=GREEN_L, ec=GREEN, fs=10)
    box(ax, 12.6, 2.75, 4.1, 1.2, "5.8 SPOOLing ★必考\n输入井/输出井/缓冲/进程\n独占设备→共享设备",
        fc=GREEN_L, ec=GREEN, fs=10)
    box(ax, 12.6, 1.45, 4.1, 1.15, "5.9 设备独立性 & LUT\n逻辑设备表、I/O重定向",
        fc=GREEN_L, ec=GREEN, fs=10)

    rbox(ax, 0.5, 0.12, 14.0, 0.85,
         "全书一条线：设备(五花八门的交通工具) → 控制器(站点) → 缓冲(中转仓) → 层次软件(分工部门) → SPOOLing(把独占变共享)",
         fc=AMBER_L, ec=AMBER, fs=11)
    save(fig, f"{OUT}/ch5-00_chapter_map.png")


# ============================================================ 01 设备分类
def fig01():
    fig, ax = new_fig(15, 9.3, xlim=(0, 15), ylim=(0, 9.3))
    title(ax, "I/O设备分类：三种视角",
          sub="视角一按使用特性｜视角二按传输速率｜视角三按信息交换单位（408高频考点）")

    # ---------- 视角一：按使用特性 ----------
    tx(ax, 0.9, 7.35, "①按\n使用\n特性", fs=11, color=BLUE, bold=True)
    items = [
        ("人机交互设备", "键盘、鼠标、显示器、打印机",
         "人与机器交换信息；速度慢，\n常采用中断驱动方式", BLUE),
        ("存储设备", "磁盘、光盘、磁带、U盘",
         "机器内部保存大量数据；\n速度快，可寻址（块设备）", TEAL),
        ("网络通信设备", "网卡、调制解调器、蓝牙",
         "设备与设备之间通信；\n中速，常以帧/包为单位", PURPLE),
    ]
    for i, (name, ex, feat, c) in enumerate(items):
        x = 2.9 + i * 4.4
        rbox(ax, x, 6.05, 4.0, 1.95, "", fc="white", ec=c, lw=2.0)
        tx(ax, x + 2.0, 7.78, name, fs=12, bold=True, color=c)
        tx(ax, x + 2.0, 7.15, "例：" + ex, fs=10.5, color=INK)
        tx(ax, x + 2.0, 6.5, feat, fs=10, color=GRAY)

    # ---------- 视角二：按传输速率 ----------
    tx(ax, 0.9, 4.55, "②按\n传输\n速率", fs=11, color=TEAL, bold=True)
    spd = [
        ("低速设备", "键盘、鼠标、打印机、语音输入", "每秒几个字节～几百字节", AMBER),
        ("中速设备", "激光打印机、网卡、终端", "每秒几千～几万字节", GREEN),
        ("高速设备", "磁盘、光盘、SSD", "每秒几十万～几百万字节", RED),
    ]
    for i, (name, ex, sp, c) in enumerate(spd):
        x = 2.9 + i * 4.4
        rbox(ax, x, 3.85, 4.0, 1.35, "", fc="white", ec=c, lw=2.0)
        tx(ax, x + 2.0, 4.95, name, fs=12, bold=True, color=c)
        tx(ax, x + 2.0, 4.35, ex, fs=10, color=INK)
        tx(ax, x + 2.0, 3.98, sp, fs=10, color=AMBER if c is AMBER else GRAY)
    tx(ax, 12.7, 5.55, "速率不等的原因：\n机械运动慢于电子信号", fs=9.5, color=GRAY)

    # ---------- 视角三：按信息交换单位 ----------
    tx(ax, 0.9, 1.9, "③按\n信息交\n换单位", fs=11, color=GREEN, bold=True)
    rbox(ax, 2.6, 0.85, 5.9, 2.5, "", fc=GREEN_L, ec=GREEN, lw=2.0)
    tx(ax, 5.55, 3.08, "块设备（成块传输）", fs=12.5, bold=True, color=GREEN)
    tx(ax, 5.55, 2.5, "例：磁盘、光盘、磁带\n传输单位：一块（被读/写的一个数据块）\n特点：可寻址（按块号随机访问）；速度较快\n常结合 DMA 方式（成块传送，一次中断）", fs=10)
    rbox(ax, 9.0, 0.85, 5.9, 2.5, "", fc=PURPLE_L, ec=PURPLE, lw=2.0)
    tx(ax, 11.95, 3.08, "字符设备（按字符传输）", fs=12.5, bold=True, color=PURPLE)
    tx(ax, 11.95, 2.5, "例：键盘、鼠标、打印机、终端\n传输单位：一个字符（字节）\n特点：不可寻址（只能顺序读入）；速度较慢\n常采用中断驱动方式", fs=10)

    rbox(ax, 0.3, 0.06, 14.4, 0.55,
         "【记忆口诀】块设备＝能按“块号”满盘乱跑（可寻址）；字符设备＝只能一个字符一个字符“排队进站”",
         fc=AMBER_L, ec=AMBER, fs=10.5)
    save(fig, f"{OUT}/ch5-01_io_classification.png")


# ============================================================ 02 设备控制器
def fig02():
    fig, ax = new_fig(15, 10.3, xlim=(0, 15), ylim=(0, 10.3))
    title(ax, "I/O控制器（设备控制器）：CPU 与设备之间的“翻译官”",
          sub="组成：三类寄存器 + 设备控制逻辑 + 与CPU接口/与设备接口 ｜ 端口编址：内存映射I/O vs 独立编址")

    # ---------- 上方：组成与链路 ----------
    box(ax, 2.3, 6.6, 3.0, 1.9, "CPU\n（只通过总线访问控制器，\n不直接操作设备）",
        fc=BLUE_L, ec=BLUE, fs=10.5)
    box(ax, 4.55, 7.9, 1.9, 0.55, "与CPU接口", fc=GRAY_L, ec=GRAY, fs=9.5)
    arrow(ax, 3.8, 6.6, 4.9, 6.6, both=True, color=INK, lw=2.0,
          text="系统总线：地址/数据/控制", dy=0.22, fs=9.5)

    # 设备控制器主体
    rbox(ax, 5.0, 4.75, 6.7, 3.55, "", fc="white", ec=INK, lw=2.2)
    tx(ax, 8.35, 8.0, "设备控制器（I/O控制器）", fs=13, bold=True)
    regs = [("数据寄存器\nDR", "暂存 CPU 与设备\n交换的数据", BLUE),
            ("状态寄存器\nSR", "记录设备状态：\n忙/就绪/出错", AMBER),
            ("控制寄存器\nCR", "存放命令与参数：\n读/写/定位/地址…", PURPLE)]
    for i, (name, desc, c) in enumerate(regs):
        x = 5.75 + i * 2.65
        rbox(ax, x, 6.0, 2.3, 1.5, "", fc="white", ec=c, lw=2.0)
        tx(ax, x + 1.15, 7.28, name, fs=11, bold=True, color=c)
        tx(ax, x + 1.15, 6.5, desc, fs=9.5, color=INK)
    rbox(ax, 5.55, 4.95, 5.6, 0.85, "设备控制逻辑：解释命令、控制设备完成操作、\n把设备状态翻译成状态寄存器里的位",
         fc=GRAY_L, ec=GRAY, fs=10)

    box(ax, 11.9, 7.9, 1.85, 0.55, "与设备接口", fc=GRAY_L, ec=GRAY, fs=9.5)
    arrow(ax, 11.7, 6.6, 12.6, 6.6, both=True, color=INK, lw=2.0,
          text="设备接口信号线：\n数据/状态/命令", dy=0.22, fs=9.5)
    box(ax, 13.6, 6.6, 2.35, 1.6, "设备\n（机械部件+电子部件）\n例：打印机/磁盘",
        fc=TEAL_L, ec=TEAL, fs=10.5)
    tx(ax, 7.5, 4.35, "（控制器的作用：①隔离CPU与电子/机械细节 ②缓冲数据、暂存状态 ③实现数据格式转换）",
       fs=10, color=GRAY)

    # ---------- 中部：三类寄存器说明表 ----------
    tbl_y = 4.0
    rect(ax, 1.2, tbl_y, 13.2, 0.55, "寄存器      作用描述（谁读写）", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    rows = [("数据寄存器DR（缓冲）", "临时存放设备与 CPU 之间交换的数据（一个字/一块）；CPU 写DR=送数据给设备，读DR=取数据", BLUE_L),
            ("状态寄存器SR", "存放设备当前状态：设备忙/就绪、传输完毕、有无错误（校验错/格式错）等若干状态位", AMBER_L),
            ("控制寄存器CR（命令）", "存放 CPU 下发的命令字与参数：读/写/定位、传送的块号与长度等（命令与参数常分寄存器或分字段）", PURPLE_L)]
    for i, (n, d, c) in enumerate(rows):
        y = tbl_y - 0.78 * (i + 1)
        rect(ax, 1.2, y, 3.4, 0.72, n, fc=c, ec=GRAY, fs=10, bold=True)
        rect(ax, 4.6, y, 8.0, 0.72, d, fc="white", ec=GRAY, fs=9.5)

    # ---------- 下方：两种编址方式对比 ----------
    rbox(ax, 0.55, 0.25, 6.9, 2.2, "", fc=BLUE_L, ec=BLUE, lw=2.0)
    tx(ax, 4.0, 2.2, "内存映射I/O（统一编址）", fs=12, bold=True, color=BLUE)
    tx(ax, 4.0, 1.72, "思路：I/O 端口与内存单元编入同一地址空间\n访问：用普通内存指令（如 MOV）即可读写端口\n优点：无需专门I/O指令，指令集简单，编程灵活\n缺点：占用内存地址空间，内存被“挤占”", fs=9.5)
    tx(ax, 4.0, 1.15, "例：ARM、MIPS、多数单片机", fs=10, color=GRAY)

    rbox(ax, 7.8, 0.25, 6.9, 2.2, "", fc=PURPLE_L, ec=PURPLE, lw=2.0)
    tx(ax, 11.25, 2.2, "独立编址（端口单独编址）", fs=12, bold=True, color=PURPLE)
    tx(ax, 11.25, 1.72, "思路：I/O 端口地址空间与内存地址空间相互独立\n访问：需专门指令 IN/OUT 读写端口\n优点：不占用内存地址空间，独立指令更安全\n缺点：需专门指令，指令集复杂，需额外地址线", fs=9.5)
    tx(ax, 11.25, 1.15, "例：x86 的 IN / OUT 指令", fs=10, color=GRAY)

    save(fig, f"{OUT}/ch5-02_device_controller.png")


# ============================================================ 03 四种I/O控制方式
def fig03():
    fig, ax = new_fig(15, 11.2, xlim=(0, 15), ylim=(0, 11.2))
    title(ax, "I/O控制方式演进：CPU 越来越“闲”，设备越来越“独立”",
          sub="四种方式对比（CPU干预程度递减）：①程序直接控制 → ②中断驱动 → ③DMA → ④通道")

    X0, X1 = 2.75, 14.2
    LX0, LX1 = 2.0, 2.62        # 泳道标签

    def panel(top, name, summ, cpu_segs, dev_segs, dev_name, note=""):
        tx(ax, X0, top - 0.20, name, fs=11.5, bold=True, ha="left")
        tx(ax, X1, top - 0.20, summ, fs=9, color=GRAY, ha="right")
        # CPU 泳道
        rect(ax, LX0, top - 0.76, 0.62, 0.44, "CPU", fc=GRAY_L, ec=GRAY, fs=8.5, bold=True)
        for x0, w, fc, ec, lab in cpu_segs:
            rect(ax, X0 + x0, top - 0.74, w, 0.42, lab, fc=fc, ec=ec, fs=9)
        # 设备/DMA/通道 泳道
        rect(ax, LX0, top - 1.58, 0.62, 0.44, dev_name, fc=GRAY_L, ec=GRAY, fs=8.5, bold=True)
        for x0, w, fc, ec, lab in dev_segs:
            rect(ax, X0 + x0, top - 1.56, w, 0.42, lab, fc=fc, ec=ec, fs=9)
        if note:
            tx(ax, X0, top - 1.90, note, fs=8.5, color=GRAY, ha="left")

    # ① 程序直接控制（轮询忙等）: 每字CPU全程参与
    panel(10.1, "① 程序直接控制（轮询忙等）", "CPU干预：每字全程参与，且忙等占死CPU",
          [(0.0, 11.45, RED_L, RED, "忙等循环：读状态寄存器 → 判断“就绪？” → 未就绪再读 → 就绪后由CPU搬运一个字（全程串行）")],
          [(0.0, 3.7, BLUE_L, BLUE, "设备工作:字1"), (3.9, 3.7, BLUE_L, BLUE, "设备工作:字2"), (7.8, 3.7, BLUE_L, BLUE, "设备工作:字3")],
          "设备", note="CPU反复查询状态位，其余时间无任何事可做")

    # ② 中断驱动：每字一次中断
    panel(8.2, "② 中断驱动", "CPU干预：每个字传输完成时被“打断”一次",
          [(0.0, 2.3, GREEN_L, GREEN, "做其他任务"), (2.4, 1.0, RED_L, RED, "处理字1"),
           (3.45, 1.5, GREEN_L, GREEN, "做其他任务"), (5.0, 1.0, RED_L, RED, "处理字2"),
           (6.05, 1.5, GREEN_L, GREEN, "做其他任务"), (7.6, 1.0, RED_L, RED, "处理字3"),
           (8.65, 1.45, GREEN_L, GREEN, "做其他任务"), (10.15, 1.0, RED_L, RED, "处理字4")],
          [(0.0, 2.3, BLUE_L, BLUE, "传字1"), (2.6, 2.3, BLUE_L, BLUE, "传字2"),
           (5.2, 2.3, BLUE_L, BLUE, "传字3"), (7.8, 2.3, BLUE_L, BLUE, "传字4"),
           (10.4, 1.05, BLUE_L, BLUE, "…")],
          "设备", note="每传完一字 → 中断 → CPU处理该字：中断次数=字数n，保存/恢复现场开销大")
    for i, x0 in enumerate([2.3, 4.9, 7.5, 10.1]):
        arrow(ax, X0 + x0 - 0.06, 8.2 - 1.44, X0 + x0 + 0.05, 8.2 - 0.52,
              color=AMBER, lw=1.3, ms=10)

    # ③ DMA：一块一次中断
    panel(6.3, "③ DMA（直接内存存取）", "CPU干预：初始化 + 整块传完善后，各一次",
          [(0.0, 8.6, GREEN_L, GREEN, "做其他任务（数据完全不经过CPU）"), (8.9, 2.4, RED_L, RED, "中断处理(整块)")],
          [(0.0, 8.6, AMBER_L, AMBER, "DMA搬运一整块（n个字）：设备→内存 直接传送")],
          "DMA", note="传完一整块才中断一次；中断次数=块数")
    arrow(ax, X0 + 8.6, 6.3 - 1.44, X0 + 8.92, 6.3 - 0.52, color=TEAL, lw=1.6,
          text="整块完成→中断一次", dy=0.1, fs=8.5, tc=TEAL)

    # ④ 通道：一批一次中断
    panel(4.4, "④ 通道（I/O处理机）", "CPU干预：初始化通道程序 + 一批数据完成时，各一次",
          [(0.0, 9.9, GREEN_L, GREEN, "做其他任务"), (10.2, 1.3, RED_L, RED, "中断(一批完成)")],
          [(0.0, 9.9, PURPLE_L, PURPLE, "通道执行“通道程序”：把一批数据（多块）读入内存 / 从内存输出")],
          "通道", note="通道＝“弱弱CPU”：自己取指执行通道程序；CPU干预最少")
    arrow(ax, X0 + 9.9, 4.4 - 1.44, X0 + 10.22, 4.4 - 0.52, color=PURPLE, lw=1.6,
          text="一批完成→中断一次", dy=0.1, fs=8.5, tc=PURPLE)

    # 底部结论
    rbox(ax, 0.3, 0.3, 14.4, 1.9, "", fc=BLUE_L, ec=BLUE)
    tx(ax, 7.5, 1.95, "四种方式内核思想：把“搬运数据”这件苦差事从 CPU 肩上一点点卸下来", fs=12.5, bold=True, color=BLUE)
    tx(ax, 7.5, 0.7, "①轮询：CPU全程亲力亲为 → ②中断：设备“喊一声”，CPU只处理一个字符 → ③DMA：设备→内存直达，CPU只干头尾 → ④通道：连一级级初始化都交给通道程序，CPU只委托一次、结账一次",
       fs=10, color=INK)
    save(fig, f"{OUT}/ch5-03_io_control_methods.png")


# ============================================================ 04 DMA流程
def fig04():
    fig, ax = new_fig(15, 9.7, xlim=(0, 15), ylim=(0, 9.7))
    title(ax, "DMA方式：设备与内存直接“握手”，CPU只当“交接员”",
          sub="四寄存器：CR命令/状态、MAR内存地址、DC数据计数、DR数据缓冲 ｜ 传完一整块才中断CPU一次")

    box(ax, 2.6, 7.0, 3.5, 1.7, "CPU\n①初始化：写入命令/地址/长度\n⑤接收中断：善后处理",
        fc=BLUE_L, ec=BLUE, fs=10)
    box(ax, 2.7, 2.5, 3.4, 2.1, "内存\n\n数据区\n（整块数据直接落地，\n不经过CPU）",
        fc=GREEN_L, ec=GREEN, fs=10)

    # DMA控制器主体
    rbox(ax, 6.3, 1.35, 6.3, 6.85, "", fc="white", ec=TEAL, lw=2.2)
    tx(ax, 9.45, 7.9, "DMA控制器", fs=13, bold=True, color=TEAL)
    tx(ax, 9.45, 7.42, "（代替CPU执行“搬整块”的小工）", fs=9.5, color=GRAY)

    rbox(ax, 6.55, 5.75, 2.75, 1.35, "", fc=AMBER_L, ec=AMBER)
    tx(ax, 7.925, 6.85, "CR 命令/状态寄存器", fs=10.5, bold=True, color=AMBER)
    tx(ax, 7.925, 6.25, "存放命令(读/写)\n与状态", fs=9)
    rbox(ax, 9.6, 5.75, 2.75, 1.35, "", fc=PURPLE_L, ec=PURPLE)
    tx(ax, 10.975, 6.85, "MAR 内存地址寄存器", fs=10.5, bold=True, color=PURPLE)
    tx(ax, 10.975, 6.25, "存放所读写内存\ndata起始地址", fs=9)
    rbox(ax, 6.55, 4.15, 2.75, 1.35, "", fc=AMBER_L, ec=AMBER)
    tx(ax, 7.925, 5.25, "DC 数据计数器", fs=10.5, bold=True, color=AMBER)
    tx(ax, 7.925, 4.65, "存放剩余字数；\n每传一字减1", fs=9)
    rbox(ax, 9.6, 4.15, 2.75, 1.35, "", fc=BLUE_L, ec=BLUE)
    tx(ax, 10.975, 5.25, "DR 数据寄存器(缓冲)", fs=10.5, bold=True, color=BLUE)
    tx(ax, 10.975, 4.65, "暂存设备与内存\n正在传的字", fs=9)

    rbox(ax, 6.6, 1.95, 5.75, 1.9, "", fc=TEAL_L, ec=TEAL)
    tx(ax, 9.475, 3.6, "数据通道（关键！）", fs=11, bold=True, color=TEAL)
    tx(ax, 9.475, 2.9, "设备 → DR → 内存：每传一个字，\nMAR自动+1、DC自动-1；字字相连",
       fs=9.5, color=INK)

    # 设备
    box(ax, 13.9, 4.9, 2.0, 2.3, "设备\n（磁盘等）", fc=TEAL_L, ec=TEAL, fs=11)
    arrow(ax, 12.62, 4.9, 12.85, 4.9, both=True, color=TEAL, lw=2.2,
          text="② 按字传送", dy=0.24, fs=9.5)
    arrow(ax, 8.2, 4.15, 4.4, 3.55, color=TEAL, lw=2.6,
          text="③ 整块数据直达内存（根本不用CPU）", dy=0.35, fs=9.5, tc=TEAL)
    arrow(ax, 8.3, 8.2, 4.4, 7.8, color=AMBER, lw=1.8, ls="--",
          text="④ 一块传完（DC=0）→ 向CPU发中断", dy=-0.1, fs=9.5, tc=AMBER)
    arrow(ax, 4.35, 6.45, 6.25, 6.35, color=INK, lw=1.6, ls="--",
          text="① 初始化：写入CR命令/MAR首址/DC字数", dy=-0.45, fs=9, tc=INK)

    rbox(ax, 0.35, 0.16, 14.3, 0.95, "", fc=AMBER_L, ec=AMBER)
    tx(ax, 7.5, 0.86, "【易错】整块传送期间 CPU 不做任何搬运，但“初始化”与“结束时善后”仍由 CPU 完成 —— 两者缺一不可", fs=10.5, bold=True, color=AMBER)
    tx(ax, 7.5, 0.45, "读出：设备 → DR → 内存；写入：内存 → DR → 设备｜数据流全程绕过 CPU 的寄存器；CPU 与 DMA 控制器争用内存总线时才需“周期挪用”协调",
       fs=9.5, color=INK)
    save(fig, f"{OUT}/ch5-04_dma_flow.png")


# ============================================================ 05 中断驱动 vs DMA
def fig05():
    fig, ax = new_fig(15, 9.8, xlim=(0, 15), ylim=(0, 9.8))
    title(ax, "中断驱动 vs DMA：每个字一次中断 vs 整块一次中断",
          sub="核心差异：①谁在搬运数据 ②什么时候打断CPU ③一次中断能“管”多少数据")

    # ---------- 左：中断驱动 ----------
    tx(ax, 3.6, 8.45, "中断驱动：按“字”中断", fs=13, bold=True, color=AMBER)
    rect(ax, 0.5, 7.75, 0.7, 0.5, "CPU", fc=GRAY_L, ec=GRAY, fs=9, bold=True)
    cx = 1.3
    rect(ax, cx, 7.8, 0.9, 0.35, "任务A", fc=GREEN_L, ec=GREEN, fs=8.5)
    rect(ax, cx + 0.95, 7.8, 0.8, 0.35, "处理字1", fc=RED_L, ec=RED, fs=8.5)
    rect(ax, cx + 1.8, 7.8, 0.9, 0.35, "任务A", fc=GREEN_L, ec=GREEN, fs=8.5)
    rect(ax, cx + 2.75, 7.8, 0.8, 0.35, "处理字2", fc=RED_L, ec=RED, fs=8.5)
    rect(ax, cx + 3.6, 7.8, 1.4, 0.35, "任务A…", fc=GREEN_L, ec=GREEN, fs=8.5)
    rect(ax, 0.5, 6.9, 0.7, 0.5, "设备", fc=GRAY_L, ec=GRAY, fs=9, bold=True)
    rect(ax, cx, 6.95, 1.55, 0.35, "传字1", fc=BLUE_L, ec=BLUE, fs=9.5)
    rect(ax, cx + 1.6, 6.95, 1.55, 0.35, "传字2", fc=BLUE_L, ec=BLUE, fs=9.5)
    rect(ax, cx + 3.2, 6.95, 1.55, 0.35, "传字3", fc=BLUE_L, ec=BLUE, fs=9.5)
    for (a, b) in [(cx + 1.55, cx + 1.6), (cx + 3.15, cx + 3.2)]:
        arrow(ax, a, 6.95, b + 0.15, 7.8, color=AMBER, lw=1.3, ms=11, text="中断", dy=0.12, fs=8)
    tx(ax, 3.6, 6.2, "每传一个字就要中断一次！\n中断次数 = 字数 n\nCPU 反复保存/恢复现场，开销大",
       fs=10, color=AMBER, ha="left")

    # ---------- 右：DMA ----------
    tx(ax, 11.3, 8.45, "DMA：按“块”中断", fs=13, bold=True, color=TEAL)
    rect(ax, 8.2, 7.75, 0.7, 0.5, "CPU", fc=GRAY_L, ec=GRAY, fs=9, bold=True)
    rect(ax, 9.0, 7.8, 5.3, 0.35, "做其他任务（数据不经过CPU）", fc=GREEN_L, ec=GREEN, fs=9.5)
    rect(ax, 14.35, 7.8, 0.55, 0.35, "", fc=RED_L, ec=RED)
    rect(ax, 8.2, 6.9, 0.7, 0.5, "DMA", fc=GRAY_L, ec=GRAY, fs=9, bold=True)
    rect(ax, 9.0, 6.95, 5.35, 0.35, "DMA搬运：一整块（n个字）", fc=AMBER_L, ec=AMBER, fs=9.5)
    arrow(ax, 14.4, 6.95, 14.45, 7.8, color=TEAL, lw=1.6, text="整块完成\n一次中断", dy=0.1, fs=8.5)
    tx(ax, 11.3, 6.2, "n个字只中断一次！\n中断次数 = 块数 n/块长，\n几乎可以忽略",
       fs=10, color=TEAL, ha="left")

    # ---------- 底部：对比表 ----------
    rect(ax, 0.5, 4.1, 14.0, 0.55, "对比项          中断驱动方式                                       DMA方式",
         fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    info = [("数据传输单位", "一个字符（字/字节）", "一个块", BLUE),
            ("谁在搬运数据", "CPU：中断后亲自搬字入内存", "DMA控制器：自动搬完一整块（设备与内存）", TEAL),
            ("中断频率", "每传一个字中断一次（频繁）", "每传完一整块才中断一次（很少）", AMBER),
            ("CPU干预时机", "每个字传完时：保存现场→搬运→恢复现场", "仅两次：①初始化参数 ②整块完成后善后", RED),
            ("CPU与设备并行度", "较高：可并行，但打断太频繁", "最高：整块传送期间 CPU 完全不参与I/O", GREEN),
            ("典型适用", "低速字符设备：键盘、打印机、终端", "高速块设备：磁盘、光盘、SSD", PURPLE)]
    for i, (a, b, c, col) in enumerate(info):
        y = 4.1 - 0.75 * (i + 1)
        rect(ax, 0.5, y, 3.0, 0.7, a, fc="white", ec=GRAY, fs=10, bold=True)
        rect(ax, 3.5, y, 3.1, 0.7, b, fc=AMBER_L, ec=GRAY, fs=10)
        rect(ax, 6.6, y, 7.9, 0.7, c, fc="white", ec=GRAY, fs=10)
    save(fig, f"{OUT}/ch5-05_interrupt_vs_dma.png")


# ============================================================ 06 I/O软件四层结构
def fig06():
    fig, ax = new_fig(15, 10.7, xlim=(0, 15), ylim=(0, 10.7))
    title(ax, "I/O软件层次结构：从“用户说一句话”到“设备动一下”",
          sub="越往上越接近用户、越“抽象”；越往下越接近硬件、越“具体”。右侧为各层职责与向上接口")

    layers = [
        ("用户层I/O软件", BLUE, BLUE_L, "用户接口 + 库函数(printf/scanf) + SPOOLing 的用户态进程",
         "向上接口：系统调用 read/write/print"),
        ("设备独立性软件", GREEN, GREEN_L, "设备命名与保护、逻辑设备名→物理设备名映射、缓冲管理、设备分配与回收、差错处理",
         "向上接口：设备无关(不区分具体设备)的系统调用"),
        ("设备驱动程序", AMBER, AMBER_L, "唯一懂硬件控制器的层：把抽象命令翻译成寄存器读写（设CR/SR，读写DR）、检查设备状态、启动设备",
         "向上接口：面向设备的统一命令接口"),
        ("中断处理程序", RED, RED_L, "保存现场→识别中断来源→处理I/O完成事件→唤醒等待进程→恢复现场",
         "向上接口：中断向量（硬件中断的入口）"),
        ("硬件（控制器+设备）", GRAY, GRAY_L, "设备控制器执行真正I/O操作；完成后向CPU发中断",
         "向上接口：中断请求线"),
    ]
    ys = [8.85, 7.55, 6.25, 4.95, 3.65]
    for (name, ec, fc, duty, iface), y in zip(layers, ys):
        box(ax, 3.7, y, 4.9, 1.05, "", fc=fc, ec=ec, lw=2.2)
        tx(ax, 3.7, y + 0.24, name, fs=12, bold=True, color=ec)
        rbox(ax, 6.75, y - 0.53, 7.9, 1.06, "", fc="white", ec=ec, lw=1.6)
        tx(ax, 10.7, y + 0.22, name + " —— 职责", fs=10.5, bold=True, color=ec)
        tx(ax, 10.7, y - 0.24, duty, fs=9.5, color=INK)
        tx(ax, 10.7, y - 0.42, iface, fs=9, color=GRAY)

    # 下行箭头（发请求）
    arrow(ax, 3.7, 8.32, 3.7, 8.08, text="系统调用", dx=1.15, dy=0.12, fs=9, color=BLUE, lw=1.6)
    arrow(ax, 3.7, 7.02, 3.7, 6.78, text="设备无关I/O(缓冲/分配)", dx=1.15, dy=0.12, fs=9, color=GREEN, lw=1.6)
    arrow(ax, 3.7, 5.72, 3.7, 5.48, text="I/O命令(翻译后)", dx=1.15, dy=0.12, fs=9, color=AMBER, lw=1.6)
    arrow(ax, 3.7, 4.42, 3.7, 4.18, text="启动设备/等待中断", dx=1.15, dy=0.12, fs=9, color=GRAY, lw=1.6)

    # 上行中断路径（虚线，从硬件层回到中断处理层）
    arrow(ax, 2.15, 3.13, 2.15, 4.42, color=RED, lw=1.8, ls="--",
          text="设备工作完成 → 控制器请求中断（自下而上）", dy=0.62, dx=-0.4, fs=9, tc=RED)

    # 左侧步骤编号
    for i, y in enumerate(ys):
        circle(ax, 0.55, y, 0.34, str(i + 1), fc="white", ec=INK, fs=10)
    tx(ax, 0.55, 2.2, "步骤", fs=9, color=GRAY)

    rbox(ax, 0.4, 0.16, 14.2, 1.75, "", fc=AMBER_L, ec=AMBER)
    tx(ax, 7.5, 1.66, "以“用户读取磁盘一个数据块”为例，请求层层下行、完成信号回到最底层软件：", fs=11, bold=True, color=AMBER)
    steps = ["① 用户进程调用 read(fd, buf, n)：\n进入用户层I/O软件(库函数)",
             "② 设备独立性软件：\n查权限→LUT逻辑名转物理名→\n分配设备与缓冲",
             "③ 设备驱动程序：\n把“读1块”翻译成：CR设命令，\nMAR设地址，DC设字数，启动设备",
             "④ 控制器+DMA：\n设备→内存直传整块；\n传完→中断请求",
             "⑤ 中断处理程序：\n保存现场→识别中断→\n唤醒等待进程→返回用户态"]
    for i, s in enumerate(steps):
        x = 1.0 + i * 2.82
        rbox(ax, x, 0.3, 2.55, 1.15, "", fc="white", ec=AMBER, lw=1.4)
        tx(ax, x + 1.275, 0.875, s, fs=8.5, color=INK)
        if i < 4:
            arrow(ax, x + 2.6, 0.875, x + 2.78, 0.875, color=INK, lw=1.2, ms=10)
    save(fig, f"{OUT}/ch5-06_io_layers.png")


# ============================================================ 07 各层功能归属
def fig07():
    fig, ax = new_fig(15, 9.9, xlim=(0, 15), ylim=(0, 9.9))
    title(ax, "功能归属图：每个“工作”到底归哪一层？",
          sub="同一张图彻底搞定408判断题：“××功能属于哪一层？”（先把左边四层记牢，再看右边功能框“对号入座”）")

    layers = [
        ("用户层I/O软件", BLUE, BLUE_L, [
            "printf/scanf 等库函数", "SPOOLing 用户态进程", "read/write 用户入口(系统调用)"],
         ),
        ("设备独立性软件", GREEN, GREEN_L, [
            "设备命名与保护", "逻辑设备名→物理名映射", "缓冲管理",
            "设备分配与回收", "差错处理(通用)", "设备独立性/透明性"],
         ),
        ("设备驱动程序", AMBER, AMBER_L, [
            "设置设备寄存器值(CR/SR/DR)", "抽象命令→硬件操作", "检查设备状态", "启动设备/控制传送"],
         ),
        ("中断处理程序", RED, RED_L, [
            "保存现场", "识别中断来源", "I/O完成善后(唤醒)", "恢复现场"],
         ),
    ]
    ys = [8.0, 6.2, 4.4, 2.6]
    for (name, ec, fc, chips), y in zip(layers, ys):
        box(ax, 1.95, y, 2.9, 1.3, "", fc=fc, ec=ec, lw=2.2)
        tx(ax, 1.95, y + 0.28, name, fs=11.5, bold=True, color=ec)
        rect(ax, 3.6, y - 0.62, 11.1, 1.24, "", fc=GRAY_L, ec="white")
        n = len(chips)
        if n <= 5:
            w = 2.05
            xs = [3.85 + i * (w + 0.12) for i in range(n)]
        else:
            w = 1.72
            xs = [3.85 + i * (w + 0.1) for i in range(n)]
        for s, x in zip(chips, xs):
            rbox(ax, x, y - 0.48, w, 0.96, s, fc="white", ec=ec, lw=1.5, fs=9)

    rbox(ax, 0.35, 0.3, 14.3, 1.55, "", fc=BLUE_L, ec=BLUE)
    tx(ax, 7.5, 1.62, "【真题风格·判断归属】你只需记住三个“铁律”：",
       fs=11.5, bold=True, color=BLUE)
    marks = [
        ("“设置设备寄存器值”\n= 设备驱动程序层", True),
        ("“缓冲管理、设备分配”\n= 设备独立性软件层", True),
        ("“逻辑设备名→物理名”\n= 设备独立性软件层", True),
        ("“设备分配与回收”\n= 设备驱动程序层", False),
    ]
    for i, (s, ok) in enumerate(marks):
        x = 0.8 + i * 3.6
        rbox(ax, x, 0.45, 3.3, 0.95, "", fc=GREEN_L if ok else RED_L,
             ec=GREEN if ok else RED, lw=1.6)
        tx(ax, x + 1.65, 1.08, "√" if ok else "×", fs=13, bold=True,
           color=GREEN if ok else RED)
        tx(ax, x + 1.65, 0.62, s, fs=8.5, color=INK)
    save(fig, f"{OUT}/ch5-07_layer_functions.png")


# ============================================================ 08 单缓冲与双缓冲
def fig08():
    fig, ax = new_fig(15, 11.2, xlim=(0, 15), ylim=(0, 11.2))
    title(ax, "单缓冲与双缓冲：T / M / C 三个阶段的时间轴",
          sub="T：设备向缓冲区灌注数据；M：缓冲区→工作区（用户区）拷贝；C：CPU对工作区数据加工处理（示意图：T=2.4宽，M=0.4宽，C=1.6宽）")

    def lane_label(y, s):
        box(ax, 1.0, y, 1.5, 0.42, s, fc=GRAY_L, ec=GRAY, fs=9, bold=True)

    # ---------------- A 单缓冲：结构与时间轴 ----------------
    tx(ax, 0.45, 9.82, "A", fs=15, bold=True, color=BLUE)
    tx(ax, 0.95, 9.82, "单缓冲：一次只准备一块数据", fs=12.2, bold=True, color=BLUE)
    box(ax, 3.3, 9.18, 2.2, 0.85, "设备", fc=TEAL_L, ec=TEAL, fs=11)
    box(ax, 6.4, 9.18, 2.4, 0.85, "缓冲区 (1个)", fc=BLUE_L, ec=BLUE, fs=10)
    box(ax, 9.8, 9.18, 2.4, 0.85, "工作区(用户区)", fc=AMBER_L, ec=AMBER, fs=10)
    box(ax, 13.2, 9.18, 2.6, 0.85, "CPU加工处理", fc=GREEN_L, ec=GREEN, fs=10)
    arrow(ax, 4.4, 9.18, 5.15, 9.18, text="填缓冲 T", dy=0.2, fs=9.5, color=TEAL)
    arrow(ax, 7.6, 9.18, 8.55, 9.18, text="拷贝 M", dy=0.2, fs=9.5, color=BLUE)
    arrow(ax, 11.0, 9.18, 11.85, 9.18, text="处理 C", dy=0.2, fs=9.5, color=AMBER)
    tx(ax, 13.9, 8.62, "【约束】设备灌下一块\n要等 M 完成后才能开始；\n只有一个缓冲可替换", fs=8.5, color=GRAY, ha="right")

    # 单缓冲真实时间轴（T=2.4, M=0.4, C=1.6；X0=2.6）
    X0, TW, MW, CW = 2.6, 2.4, 0.4, 1.6
    lane_label(8.1, "设备(T)")
    lane_label(7.3, "拷贝(M)")
    lane_label(6.5, "CPU(C)")
    segs = [("T1", 0.0, "T"), ("M1", TW, "M"), ("C1", TW + MW, "C"),
            ("T2", TW + MW, "T"), ("M2", 2 * TW + MW, "M"), ("C2", 2 * TW + 2 * MW, "C"),
            ("T3", 2 * TW + 2 * MW, "T"), ("M3", 3 * TW + 2 * MW, "M"), ("C3", 3 * TW + 3 * MW, "C")]
    colors = {"T": (TEAL_L, TEAL), "M": (BLUE_L, BLUE), "C": (GREEN_L, GREEN)}
    ys = {"T": 7.85, "M": 7.05, "C": 6.25}
    for name, x0, k in segs:
        fc, ec = colors[k]
        rect(ax, X0 + x0, ys[k], TW if k == "T" else (MW if k == "M" else CW), 0.46,
             name, fc=fc, ec=ec, fs=9)
    # 首块与周期标注
    line(ax, X0, 6.2, X0, 8.34, color=RED, lw=1.0, ls=":")
    line(ax, X0 + TW + MW, 6.2, X0 + TW + MW, 8.34, color=RED, lw=1.0, ls=":")
    tx(ax, X0 + 0.9, 8.45, "首块：T+M+C", fs=8.5, color=RED)
    line(ax, X0 + TW + MW, 6.2, X0 + 2 * TW + MW, 6.2, color=AMBER, lw=2.0)
    tx(ax, X0 + 4.2, 6.1, "← 稳态周期 = max(C,T)+M = 2.4+0.4 →", fs=8.5, color=AMBER)
    tx(ax, X0 + 9.3, 7.6, "T2 要等 M1 结束才能开灌；但 C1 与 T2 已并行", fs=8.5, color=GRAY)

    # ---------------- B 双缓冲：结构与时间轴 ----------------
    tx(ax, 0.45, 5.0, "B", fs=15, bold=True, color=GREEN)
    tx(ax, 0.95, 5.0, "双缓冲：两个缓冲区轮换接力", fs=12.2, bold=True, color=GREEN)
    box(ax, 3.3, 4.35, 2.0, 0.8, "设备", fc=TEAL_L, ec=TEAL, fs=11)
    box(ax, 6.4, 4.7, 2.1, 0.62, "缓冲1", fc=BLUE_L, ec=BLUE, fs=9.5, bold=True)
    box(ax, 6.4, 3.92, 2.1, 0.62, "缓冲2", fc=BLUE_L, ec=BLUE, fs=9.5, bold=True)
    box(ax, 9.8, 4.35, 2.1, 0.8, "工作区", fc=AMBER_L, ec=AMBER, fs=10)
    box(ax, 13.2, 4.35, 2.4, 0.8, "CPU加工", fc=GREEN_L, ec=GREEN, fs=10)
    arrow(ax, 4.3, 4.35, 5.3, 4.35, text="T(交替)", dy=0.22, fs=9.5, color=TEAL)
    arrow(ax, 7.45, 4.35, 8.7, 4.35, text="M", dy=0.22, fs=9.5, color=BLUE)
    arrow(ax, 10.85, 4.35, 11.95, 4.35, text="C", dy=0.22, fs=9.5, color=AMBER)
    tx(ax, 13.9, 3.8, "设备灌入缓冲1时，\nCPU可处理缓冲2的数据\n——两缓冲交替接力", fs=8.5, color=GRAY)

    lane_label(2.95, "设备(T)")
    lane_label(2.15, "拷贝(M)")
    lane_label(1.35, "CPU(C)")
    segs = [("T1(→B1)", 0.0, "T"), ("M1", TW, "M"), ("C1", TW + MW, "C"),
            ("T2(→B2)", TW, "T"), ("M2", 2 * TW, "M"), ("C2", 2 * TW + MW, "C"),
            ("T3(→B1)", 2 * TW, "T"), ("M3", 3 * TW, "M"), ("C3", 3 * TW + MW, "C")]
    ysB = {"T": 2.7, "M": 1.9, "C": 1.1}
    for name, x0, k in segs:
        fc, ec = colors[k]
        rect(ax, X0 + x0, ysB[k], TW if k == "T" else (MW if k == "M" else CW), 0.46,
             name, fc=fc, ec=ec, fs=8.5)
    line(ax, X0 + TW + MW, 1.0, X0 + 2 * TW + MW, 1.0, color=AMBER, lw=2.0)
    tx(ax, X0 + 4.0, 0.9, "← 稳态周期 = max(C+M,T) = max(2.0,2.4) = 2.4 →", fs=8.5, color=AMBER)
    tx(ax, X0 + 6.9, 2.5, "T2 在设备空闲后立即开始（不需要等 C1）", fs=8.5, color=GRAY)

    rbox(ax, 0.35, 0.12, 14.3, 0.55,
         "结论：单缓冲每块 max(C,T)+M；双缓冲每块 max(C+M,T)。双缓冲迫使设备与CPU“错峰生产”，吞吐更高（本图为示意图，定量计算见 ch5-10 例题）",
         fc=GRAY_L, ec=GRAY, fs=10)
    save(fig, f"{OUT}/ch5-08_single_double_buffer.png")


# ============================================================ 09 循环缓冲 与 缓冲池
def fig09():
    fig, ax = new_fig(15, 10.6, xlim=(0, 15), ylim=(0, 10.6))
    title(ax, "循环缓冲（in/out双指针）与 缓冲池（三队列+四工作缓冲）",
          sub="循环缓冲：一个生产者+一个消费者轮流接力；缓冲池：多设备多进程统一调度缓冲空间")

    # ---------------- 上半：循环缓冲 ----------------
    tx(ax, 0.4, 9.55, "循环缓冲", fs=13.5, bold=True, color=BLUE)
    tx(ax, 0.4, 8.75, "多个缓冲区首尾相接成环，输入进程与计算进程共用，\n以 in / out 两个指针协调读写：", fs=9.5, color=GRAY, ha="left")
    cx, cy = 5.0, 6.9
    pos = [(-2.9, 0.9), (2.9, 0.9), (2.9, -0.9), (-2.9, -0.9)]   # 左上 右上 右下 左下
    bx, by = [], []
    for i, (dx, dy) in enumerate(pos):
        x, y = cx + dx, cy + dy
        box(ax, x, y, 2.0, 0.95, f"缓冲{i}", fc="white", ec=BLUE, fs=10.5, bold=True)
        bx.append(x); by.append(y)
    # 环形箭头：左上→右上→右下→左下→左上
    arrow(ax, bx[0] + 1.05, by[0], bx[1] - 1.05, by[1], color=BLUE, lw=1.7, ms=14)
    arrow(ax, bx[1], by[1] - 0.52 - 0.05, bx[2], by[2] + 0.52 + 0.05, color=BLUE, lw=1.7, ms=14)
    arrow(ax, bx[2] - 1.05, by[2], bx[3] + 1.05, by[3], color=BLUE, lw=1.7, ms=14)
    arrow(ax, bx[3], by[3] + 0.52 + 0.05, bx[0], by[0] - 0.52 - 0.05, color=BLUE, lw=1.7, ms=14)
    tx(ax, cx, cy, "in 写入 → in 前进\nout 读出 → out 前进\nin==out：全空或全满", fs=9.5, color=INK)
    arrow(ax, 1.4, 8.55, 7.0, 8.55, color=AMBER, lw=2.0, ls="--",
          text="in 指针方向（写）", dy=0.2, dx=1.6, fs=8.5, tc=AMBER)
    arrow(ax, 8.6, 5.25, 2.0, 5.25, color=GREEN, lw=2.0, ls="--",
          text="out 指针方向（读）", dy=-0.22, dx=-1.6, fs=8.5, tc=GREEN)
    rbox(ax, 9.7, 5.45, 5.1, 3.5, "", fc=BLUE_L, ec=BLUE)
    tx(ax, 12.25, 8.7, "使用规则", fs=11.5, bold=True, color=BLUE)
    tx(ax, 12.25, 7.55, "in 落后于 out：有数据可取；\nin 追上 out：缓冲区已满，\n输入进程等待（同步）；\nout 追上 in：缓冲区已空，\n计算进程等待。", fs=9.5, ha="left", color=INK)
    tx(ax, 12.25, 6.0, "循环缓冲适合场景：\n单输入进程(生产者)+\n单计算进程(消费者)\n“一对一”接力", fs=9, ha="left", color=GRAY)
    tx(ax, 0.4, 4.72, "（缓冲0 → 缓冲1 → 缓冲2 → 缓冲3 → 回到缓冲0，循环使用）", fs=9.5, color=GRAY, ha="left")

    # ---------------- 下半：缓冲池 ----------------
    tx(ax, 0.4, 4.12, "缓冲池", fs=13.5, bold=True, color=GREEN)
    tx(ax, 0.4, 3.6, "系统统一管理一批缓冲区：三种队列 + 四种工作缓冲；“角色”从队列借空缓冲、装入数据、还回队列：",
       fs=9.5, color=GRAY, ha="left")
    circle(ax, 11.6, 4.05, 0.78, "emq\n空缓冲队列", fc=GRAY_L, ec=GRAY, fs=8.5)
    circle(ax, 4.7, 1.5, 0.78, "inq\n输入队列", fc=BLUE_L, ec=BLUE, fs=8.5)
    circle(ax, 12.3, 1.5, 0.78, "outq\n输出队列", fc=PURPLE_L, ec=PURPLE, fs=8.5)
    items = [("输入设备", 1.0, TEAL_L, TEAL), ("收容输入", 2.9, BLUE_L, BLUE),
             ("提取输入", 6.6, GREEN_L, GREEN), ("计算进程", 8.5, AMBER_L, AMBER),
             ("收容输出", 10.4, PURPLE_L, PURPLE), ("提取输出", 13.95, RED_L, RED)]
    for name, x, fc, ec in items:
        box(ax, x, 1.5, 1.4, 0.95, name, fc=fc, ec=ec, fs=8.5, bold=True)
    for a, b in [(1.72, 2.18), (3.62, 3.92), (5.42, 5.88), (7.32, 7.78), (9.22, 9.68), (11.12, 11.5)]:
        arrow(ax, a, 1.5, b, 1.5, color=INK, lw=1.3, ms=10)
    tx(ax, 13.95, 2.4, "→ 送往输出设备(打印机等)", fs=8.5, color=GRAY)
    # emq 与 收容输入/收容输出 双向借用
    arrow(ax, 10.9, 3.3, 3.55, 1.85, color=GRAY, lw=1.4, ls="--",
          text="取空缓冲", dy=0.28, fs=8.5, tc=GRAY)
    arrow(ax, 3.4, 1.1, 10.7, 3.3, color=GRAY, lw=1.4, ls="--",
          text="用完归还", dy=-0.3, dx=0.4, fs=8.5, tc=GRAY)
    arrow(ax, 11.1, 3.28, 10.0, 2.05, color=GRAY, lw=1.4, ls="--",
          text="取空缓冲", dy=0.22, fs=8.5, tc=GRAY)
    arrow(ax, 10.4, 1.05, 11.2, 3.28, color=GRAY, lw=1.4, ls="--",
          text="用完归还", dy=-0.26, fs=8.5, tc=GRAY)
    tx(ax, 7.5, 0.55, "四种工作缓冲（角色）＝ 收容输入 / 提取输入 / 收容输出 / 提取输出 —— 缓冲本身只有“空/满”两种状态，靠排队与角色切换完成数据流动",
       fs=9.5, color=GRAY)
    save(fig, f"{OUT}/ch5-09_circular_buffer.png")


# ============================================================ 10 缓冲计算例题时间轴
def fig10():
    fig, ax = new_fig(15, 10.7, xlim=(0, 15), ylim=(0, 10.7))
    title(ax, "缓冲计算例题：T=120μs、M=20μs、C=80μs，处理n=10块",
          sub="先把时间轴一块一块“排出来”，再总结公式 —— 首块与末块的“边界效应”是丢分点")

    def X(t):                       # 时间μs → 图x坐标
        return 2.2 + t * 12.4 / 1560.0

    def lane(y, s, color=GRAY):
        box(ax, 1.0, y, 1.1, 0.5, s, fc=GRAY_L, ec=color, fs=9, bold=True)

    def tick(y, xmax_us):
        line(ax, 2.2, y, X(xmax_us), y, color=INK, lw=1.6)
        for t in range(0, xmax_us + 1, 200):
            ax.plot([X(t), X(t)], [y, y - 0.1], color=INK, lw=1.0)
            tx(ax, X(t), y - 0.26, f"{t}", fs=8, color=GRAY)
        tx(ax, X(xmax_us) + 0.25, y, "μs", fs=8, color=GRAY)

    def draw_blocks(t_starts, m_starts, yT, yM, yC, mtag=True, big=False):
        for i in range(10):
            rect(ax, X(t_starts[i]), yT, X(t_starts[i] + 120) - X(t_starts[i]), 0.5,
                 f"T{i+1}", fc=TEAL_L, ec=TEAL, fs=8.5)
            xm = X(m_starts[i]); wm = X(m_starts[i] + 20) - X(m_starts[i])
            if mtag:
                rect(ax, xm, yM, wm, 0.5, "", fc=BLUE_L, ec=BLUE)
                tx(ax, xm + wm / 2, yM + 0.28, f"M{i+1}", fs=6.8, rotation=90)
            else:
                rect(ax, xm, yM, wm, 0.5, "", fc=BLUE_L, ec=BLUE)
            rect(ax, X(m_starts[i] + 20), yC, X(m_starts[i] + 100) - X(m_starts[i] + 20), 0.5,
                 f"C{i+1}", fc=GREEN_L, ec=GREEN, fs=8.5)

    # ================= 单缓冲 =================
    tx(ax, 0.4, 9.55, "① 单缓冲", fs=12.5, bold=True, color=BLUE, ha="left")
    tx(ax, 3.0, 9.55, "每块 = max(C,T)+M = max(80,120)+20 = 140μs； 总时间 = T+(n-1)×140+M+C = 120+9×140+100 = 1480μs",
       fs=10, color=BLUE, ha="left")
    lane(8.6, "设备T"), lane(7.5, "拷贝M"), lane(6.4, "CPU_C")
    t_starts, m_starts = [], []
    buf_free, dev_free, work_free = 0, 0, 0
    for i in range(10):
        ts = max(dev_free, buf_free)
        t_starts.append(ts)
        ms = max(ts + 120, work_free)
        m_starts.append(ms)
        dev_free = ts + 120
        buf_free = ms + 20
        work_free = ms + 20 + 80
    draw_blocks(t_starts, m_starts, 8.35, 7.25, 6.15)
    TX = [s + 120 for s in t_starts]
    tick(5.75, 1520)
    line(ax, X(220), 6.1, X(220), 8.9, color=RED, lw=1.2, ls="--")
    line(ax, X(1480), 6.1, X(1480), 8.9, color=RED, lw=1.4)
    line(ax, X(140), 8.92, X(280), 8.92, color=AMBER, lw=2.0)
    tx(ax, 0.3, 9.08, "首块 0→220μs：T+M+C 全无重叠", fs=8.5, color=RED, ha="left")
    tx(ax, X(210), 9.08, "稳态周期 = 140μs", fs=8.5, color=AMBER)
    tx(ax, 14.7, 9.08, "末块 C10：1400→1480μs", fs=8.5, color=RED, ha="right")
    tx(ax, X(1480) + 0.7, 7.5, "总时间 = 1480μs", fs=10, bold=True, color=RED)

    # ================= 双缓冲 =================
    tx(ax, 0.4, 4.7, "② 双缓冲", fs=12.5, bold=True, color=GREEN, ha="left")
    tx(ax, 3.0, 4.7, "每块 = max(C+M,T) = max(100,120) = 120μs； 总时间 = T+(n-1)×120+M+C = 120+9×120+100 = 1300μs",
       fs=10, color=GREEN, ha="left")
    lane(3.55, "设备T"), lane(2.45, "拷贝M"), lane(1.35, "CPU_C")
    t_starts, m_starts = [], []
    bfree = [0, 0]
    dev_free, work_free = 0, 0
    for i in range(10):
        buf = i % 2
        ts = max(dev_free, bfree[buf])
        t_starts.append(ts)
        ms = max(ts + 120, work_free)
        m_starts.append(ms)
        dev_free = ts + 120
        bfree[buf] = ms + 20
        work_free = ms + 20 + 80
    # 画两层缓冲表明交替入缓冲1/2
    for i in range(10):
        buf = "1" if i % 2 == 0 else "2"
        rect(ax, X(t_starts[i]), 3.3, X(t_starts[i] + 120) - X(t_starts[i]), 0.5,
             f"T{i+1}(入B{buf})", fc=TEAL_L, ec=TEAL, fs=7.5)
        xm = X(m_starts[i]); wm = X(m_starts[i] + 20) - X(m_starts[i])
        rect(ax, xm, 2.2, wm, 0.5, "", fc=BLUE_L, ec=BLUE)
        tx(ax, xm + wm / 2, 2.48, f"M{i+1}", fs=6.8, rotation=90)
        rect(ax, X(m_starts[i] + 20), 1.1, X(m_starts[i] + 100) - X(m_starts[i] + 20), 0.5,
             f"C{i+1}", fc=GREEN_L, ec=GREEN, fs=8.5)
    tick(0.7, 1520)
    line(ax, X(1200), 1.05, X(1200), 3.85, color=RED, lw=1.2, ls="--")
    line(ax, X(1300), 1.05, X(1300), 3.85, color=RED, lw=1.4)
    tx(ax, 0.3, 4.2, "T1/T2 几乎无缝衔接：两缓冲轮流接货", fs=8.5, color=RED, ha="left")
    tx(ax, X(600), 4.2, "稳态周期 = 120μs", fs=8.5, color=AMBER)
    tx(ax, 14.7, 4.2, "末块 M10+C10：1200→1300μs", fs=8.5, color=RED, ha="right")
    tx(ax, X(1300) + 0.7, 2.3, "总时间 = 1300μs", fs=10, bold=True, color=RED)

    rbox(ax, 0.35, 0.1, 14.3, 0.55,
         "【推演要点】①单缓冲只有一个缓冲区：第i+1次输入T最早只能在第i次拷贝M结束后开始；②首块(0→220μs)：T+M+C全无重叠；③稳态周期=max(C,T)+M=140μs；④末块C10没人与它并行，还要再+80μs",
         fc=AMBER_L, ec=AMBER, fs=9.5)
    save(fig, f"{OUT}/ch5-10_buffer_calc.png")


# ============================================================ 11 设备分配：数据结构与流程
def fig11():
    fig, ax = new_fig(15, 10.6, xlim=(0, 15), ylim=(0, 10.6))
    title(ax, "设备分配：四级数据结构 + 分配流程 + 安全性",
          sub="SDT(系统设备表) → DCT(设备控制表) → COCT(控制器控制表) → CHCT(通道控制表)：从“逻辑”到“物理”层层落实")

    # ------------- 上层：四级数据结构 -------------
    boxes = [
        ("进程", ["以逻辑设备名", "提出I/O请求"], 1.5, 2.4, GRAY, GRAY_L),
        ("SDT\n系统设备表", ["登记所有设备类", "→每条DCT入口"], 4.3, 2.8, BLUE, BLUE_L),
        ("DCT\n设备控制表", ["设备类型/标识/地址", "忙闲状态、等待队列", "→COCT入口"], 7.5, 2.9, GREEN, GREEN_L),
        ("COCT\n控制器控制表", ["控制器标识/状态", "请求队列", "→CHCT入口"], 10.6, 2.7, AMBER, AMBER_L),
        ("CHCT\n通道控制表", ["通道标识/状态", "请求队列", "(无通道时省略)"], 13.4, 2.5, PURPLE, PURPLE_L),
    ]
    for name, desc, x, w, ec, fc in boxes:
        rbox(ax, x - w / 2, 7.6, w, 1.85, "", fc=fc, ec=ec, lw=2.2)
        tx(ax, x, 9.2, name, fs=10.5, bold=True, color=ec)
        for i, d in enumerate(desc):
            tx(ax, x, 8.7 - i * 0.34, d, fs=9, color=INK)
    arrow(ax, 2.7, 8.55, 2.9, 8.55, color=GRAY, lw=1.8)
    arrow(ax, 5.7, 8.55, 6.05, 8.55, text="指向/申请", dy=0.22, fs=8.5, color=BLUE)
    arrow(ax, 8.95, 8.55, 9.25, 8.55, text="指向/申请", dy=0.22, fs=8.5, color=GREEN)
    arrow(ax, 11.95, 8.55, 12.15, 8.55, text="指向/申请", dy=0.22, fs=8.5, color=AMBER)
    tx(ax, 7.5, 7.32, "查找链：SDT（系统有哪类设备、谁管）→ DCT（哪个具体设备空闲）→ COCT（哪个控制器空闲）→ CHCT（哪条通道空闲）",
       fs=9.5, color=GRAY)

    # ------------- 中部：六步分配流程（横向）+ 失败分支 -------------
    chips = [
        ("① 进程按逻辑设备名\n提出I/O请求", BLUE),
        ("② 查SDT→定位DCT\n检查忙闲/独占性", GREEN),
        ("③ 设备空闲?", AMBER),
        ("④ 申请COCT\n再申请CHCT", AMBER),
        ("⑤ 控制器与通道\n都空闲?", AMBER),
        ("⑥ 分配成功：\n置忙+建LUT映射", GREEN),
    ]
    xs = [1.3, 3.75, 6.2, 8.65, 11.1, 13.55]
    for (s, c), x in zip(chips, xs):
        rbox(ax, x - 1.0, 5.65, 2.0, 0.95, "", fc="white", ec=c, lw=2.0)
        tx(ax, x, 6.12, s, fs=8.5, bold=True, color=c)
    for i in range(5):
        arrow(ax, xs[i] + 1.03, 6.12, xs[i + 1] - 1.03, 6.12,
              color=(GREEN if i in (2, 4) else INK), lw=1.5, ms=10)
    arrow(ax, 6.2, 5.62, 6.2, 4.73, color=RED, lw=1.6, ls="--", text="否", dy=-0.14, fs=9, tc=RED)
    arrow(ax, 11.1, 5.62, 11.1, 4.73, color=RED, lw=1.6, ls="--", text="否", dy=-0.14, fs=9, tc=RED)
    rbox(ax, 0.6, 3.95, 13.9, 0.75, "", fc=RED_L, ec=RED)
    tx(ax, 7.55, 4.62, "③⑤ 失败分支（否）：进程挂入【设备】或【控制器/通道】的等待队列并阻塞 —— 等待队列分别存放在 DCT / COCT / CHCT 中；空闲后唤醒队首继续分配",
       fs=9.5, color=RED)
    rbox(ax, 0.6, 3.05, 13.9, 0.75, "", fc=GRAY_L, ec=GRAY)
    tx(ax, 7.55, 3.72, "释放：I/O完成 → 设备发出中断 → 中断处理程序善后 → 逐级释放（通道→控制器→设备置空闲）→ 唤醒下一个等待者 | 分配中途失败时：已拿到的需回收、没拿到的继续等待",
       fs=9.5, color=INK)

    # ------------- 底部：不安全分配 vs 安全分配 -------------
    rbox(ax, 0.45, 0.4, 7.0, 2.35, "", fc=GREEN_L, ec=GREEN, lw=2.2)
    tx(ax, 3.95, 2.52, "安全分配方式：请求后立即阻塞", fs=12, bold=True, color=GREEN)
    for i, d in enumerate(["进程发出I/O请求后立即阻塞，直到I/O完成才被唤醒；",
                           "一次只能申请一台设备 → 破坏死锁四条件中的“请求并保持”；",
                           "缺点：CPU与设备串行工作，利用率低、吞吐低；",
                           "适用：低速独占设备（打印机、键盘等）"]):
        tx(ax, 3.95, 2.05 - i * 0.4, d, fs=9.5, ha="left", color=INK)
    rbox(ax, 7.75, 0.4, 6.9, 2.35, "", fc=AMBER_L, ec=AMBER, lw=2.2)
    tx(ax, 11.2, 2.52, "不安全分配方式：请求后仍可运行", fs=12, bold=True, color=AMBER)
    for i, d in enumerate(["进程发出I/O请求后继续运行，需要时可继续申请其他设备；",
                           "优点：充分利用CPU与设备并行，效率高；",
                           "缺点：可能死锁 → 需配合死锁检测/预防/避免；",
                           "适用：高速设备、系统整体性能优先的场景"]):
        tx(ax, 11.2, 2.05 - i * 0.4, d, fs=9.5, ha="left", color=INK)
    save(fig, f"{OUT}/ch5-11_device_tables.png")


# ============================================================ 12 SPOOLing
def fig12():
    fig, ax = new_fig(15, 10.5, xlim=(0, 15), ylim=(0, 10.5))
    title(ax, "SPOOLing（假脱机）系统结构：一台打印机，人人“独占”",
          sub="以共享打印机为例：用户进程像独占一台打印机，实际由“井+缓冲+管理进程”排队办理 —— 独占设备被改造成共享设备")

    # ---------- 打印路径（上行） ----------
    box(ax, 1.35, 8.3, 2.6, 1.15, "用户进程（多个）\n提出打印请求", fc=BLUE_L, ec=BLUE, fs=10)
    box(ax, 8.1, 8.3, 2.4, 1.15, "输出井\n(磁盘上预留区)", fc=GREEN_L, ec=GREEN, fs=10)
    box(ax, 11.0, 8.3, 2.1, 1.15, "输出缓冲区\n(内存)", fc=AMBER_L, ec=AMBER, fs=10)
    box(ax, 13.8, 8.3, 2.2, 1.15, "打印机\n(独占设备)", fc=TEAL_L, ec=TEAL, fs=10)
    circle(ax, 2.5, 6.35, 0.75, "请求\n队列", fc=GRAY_L, ec=GRAY, fs=9.5)
    rbox(ax, 4.15, 5.55, 3.5, 1.5, "", fc="white", ec=PURPLE, lw=2.2, dashed=False)
    box(ax, 5.9, 6.3, 2.9, 1.0, "输出进程\n(管理打印)", fc=PURPLE_L, ec=PURPLE, fs=10)
    tx(ax, 5.9, 5.02, "井管理程序", fs=9.5, bold=True, color=PURPLE)

    arrow(ax, 1.6, 7.72, 2.2, 6.85, color=INK, lw=1.6, text="②登记打印请求", dy=-0.14, fs=8.5)
    arrow(ax, 2.65, 8.35, 6.85, 8.35, color=GREEN, lw=2.0,
          text="①把打印数据先写入输出井（不是真打印机！）", dy=0.24, fs=9)
    arrow(ax, 3.25, 6.35, 4.4, 6.35, color=INK, lw=1.6, text="③取请求", dy=0.22, fs=8.5)
    arrow(ax, 5.9, 6.8, 7.35, 7.75, color=GREEN, lw=1.8, text="④按队列从输出井读出", dy=0.3, dx=0.3, fs=8.5, tc=GREEN)
    arrow(ax, 7.35, 6.35, 9.9, 7.9, color=AMBER, lw=1.8, text="⑤送入输出缓冲区", dy=0.32, dx=-0.2, fs=8.5, tc=AMBER)
    arrow(ax, 12.1, 8.35, 12.65, 8.35, color=TEAL, lw=2.0,
          text="⑥打印机按排队顺序逐块打印", dy=-0.55, dx=0.4, fs=8.5, tc=TEAL)
    tx(ax, 0.95, 5.9, "【核心】用户以为\n打印机归自己用：\n其实是“写完就排队”", fs=9, color=GRAY)

    # ---------- 输入路径（下行） ----------
    box(ax, 1.1, 2.75, 2.1, 1.1, "输入设备\n(读卡机等)", fc=TEAL_L, ec=TEAL, fs=9.5)
    box(ax, 3.75, 2.75, 2.1, 1.1, "输入缓冲区\n(内存)", fc=AMBER_L, ec=AMBER, fs=9.5)
    box(ax, 6.0, 2.75, 2.1, 1.1, "输入进程\n(井管理)", fc=PURPLE_L, ec=PURPLE, fs=9.5)
    box(ax, 8.8, 2.75, 2.3, 1.1, "输入井\n(磁盘上预留区)", fc=GREEN_L, ec=GREEN, fs=9.5)
    box(ax, 11.6, 2.75, 2.4, 1.1, "用户进程\n(读“虚拟设备”)", fc=BLUE_L, ec=BLUE, fs=9.5)
    arrow(ax, 2.2, 2.75, 2.65, 2.75, color=INK, lw=1.5)
    arrow(ax, 4.85, 2.75, 4.9, 2.75, color=INK, lw=1.5)
    arrow(ax, 7.1, 2.75, 7.6, 2.75, color=GREEN, lw=1.6, text="写入\n输入井", dy=0.22, fs=8.5, tc=GREEN)
    arrow(ax, 9.98, 2.95, 12.6, 8.0, color=BLUE, lw=1.8, ls="--",
          text="用户进程像读普通文件一样从输入井读取（虚线=逻辑读）", dy=0.5, dx=-0.6, fs=8.5, tc=BLUE)

    # ---------- 底部结论 ----------
    rbox(ax, 0.4, 0.45, 14.2, 1.6, "", fc=BLUE_L, ec=BLUE)
    tx(ax, 7.5, 1.85, "SPOOLing系统的完整组成：输入井/输出井（磁盘） + 输入/输出缓冲区（内存） + 输入/输出进程（内存常驻） + 井管理程序",
       fs=10.5, bold=True, color=BLUE)
    tx(ax, 7.5, 0.75, "两大作用：①把独占设备改造成共享设备（逻辑上独占、物理上排队共享）②缓和CPU与设备速度矛盾、提高CPU与设备的并行度。"
                      "【考点】多进程“同时打印”≠ 真同时：打印机仍分时工作；SPOOLing以磁盘空间为代价，且占用管理进程与缓冲",
       fs=9.5, color=INK)
    save(fig, f"{OUT}/ch5-12_spooling.png")


# ============================================================ 13 逻辑设备表LUT
def fig13():
    fig, ax = new_fig(15, 8.7, xlim=(0, 15), ylim=(0, 8.7))
    title(ax, "设备独立性 & 逻辑设备表 LUT & I/O重定向",
          sub="逻辑设备名（用户起的名）→ LUT 查表 → 物理设备名（系统安排的真实设备）")

    # ---------- 概念链 ----------
    box(ax, 1.9, 7.35, 3.1, 0.95, "应用程序：\n“我要用 打印机 ”", fc=BLUE_L, ec=BLUE, fs=10)
    box(ax, 7.3, 7.35, 3.0, 0.95, "LUT：逻辑设备表\n(逻辑名→物理名)", fc=GREEN_L, ec=GREEN, fs=10)
    box(ax, 12.9, 7.35, 3.5, 0.95, "物理设备名→查SDT/DCT\n→ 实际设备（如LPT1）", fc=AMBER_L, ec=AMBER, fs=9.5)
    arrow(ax, 3.45, 7.35, 5.75, 7.35, color=GREEN, lw=2.0, text="逻辑设备名", dy=0.22, fs=9.5, tc=GREEN)
    arrow(ax, 8.8, 7.35, 11.1, 7.35, color=AMBER, lw=2.0, text="物理设备名", dy=0.22, fs=9.5, tc=AMBER)

    # ---------- 两种设置方式 ----------
    rbox(ax, 0.5, 3.55, 7.0, 3.15, "", fc="white", ec=GREEN, lw=2.0)
    tx(ax, 4.0, 6.45, "方式A：全系统一张LUT（全局表）", fs=12, bold=True, color=GREEN)
    rect(ax, 0.85, 5.4, 6.3, 0.5, "逻辑设备名         物理设备名", fc=GREEN_L, ec=GREEN, fs=9.5, bold=True)
    rowsA = [("打印机", "打印机1(LPT1)"), ("键盘", "键盘0(KB0)"), ("显示器", "终端1") ]
    for i, (a, b) in enumerate(rowsA):
        y = 5.4 - 0.5 * (i + 1)
        rect(ax, 0.85, y, 3.15, 0.5, a, fc="white", ec=GREEN, fs=9.5)
        rect(ax, 4.0, y, 3.15, 0.5, b, fc="white", ec=GREEN, fs=9.5)
    tx(ax, 4.0, 3.68, "特点：全系统公用；逻辑设备名全局唯一；\n系统只需一张表；但换给不同用户的设备不灵活", fs=9, color=INK)

    rbox(ax, 7.9, 3.55, 6.8, 3.15, "", fc="white", ec=PURPLE, lw=2.0)
    tx(ax, 11.3, 6.45, "方式B：每用户一张LUT（按进程建）", fs=12, bold=True, color=PURPLE)
    rect(ax, 8.25, 5.4, 6.1, 0.5, "用户A: 逻辑名→物理名    |  用户B: 逻辑名→物理名", fc=PURPLE_L, ec=PURPLE, fs=8.5, bold=True)
    rowsB = [("打印机→打印机1", "打印机→打印机5"), ("键盘→键盘0", "键盘→键盘2")]
    for i, (a, b) in enumerate(rowsB):
        y = 5.4 - 0.5 * (i + 1)
        rect(ax, 8.25, y, 3.05, 0.5, "A: " + a, fc="white", ec=PURPLE, fs=9)
        rect(ax, 11.3, y, 3.05, 0.5, "B: " + b, fc="white", ec=PURPLE, fs=9)
    tx(ax, 11.3, 3.82, "特点：每个用户可有自己的逻辑设备名；\n“打印机”对不同用户可映射到不同设备；灵活，但表多占空间", fs=9, color=INK)

    # ---------- I/O 重定向 ----------
    rbox(ax, 0.5, 0.45, 14.2, 2.75, "", fc=AMBER_L, ec=AMBER)
    tx(ax, 7.6, 2.95, "I/O重定向：不动代码，只改“映射” —— 重定向的本质就是修改LUT！", fs=12, bold=True, color=AMBER)
    tx(ax, 7.6, 2.2, "例：shell 命令  ls > data.txt —— 程序里写的是“标准输出(显示器)”，修改过的逻辑设备表把“标准输出”→映射到文件 data.txt（或\n另一台设备/打印机），于是输出全进了文件。程序本身一行没改，这就是设备独立性的好处。", fs=9.5, ha="left", color=INK)
    tx(ax, 7.6, 1.15, "【考点】设备独立性优点：①应用程序独立于物理设备（更换设备不改程序/不需重编译）；②便于设备增删与共享；③系统能灵活分配、合理调度设备。",
       fs=10, color=INK)
    save(fig, f"{OUT}/ch5-13_lut.png")


# ============================================================ 主入口
if __name__ == "__main__":
    for f in [fig00, fig01, fig02, fig03, fig04, fig05, fig06, fig07,
              fig08, fig09, fig10, fig11, fig12, fig13]:
        f()
    print("=== 第5章 全部插图生成完毕 ===")




