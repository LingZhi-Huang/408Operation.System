# -*- coding: utf-8 -*-
"""第2章 扩写新增插图（ch2-27 ~ ch2-38）。运行：python3 draw_figures_extra.py"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L, GRAY, GRAY_L,
                   PINK, PINK_L)

FIG = "/Users/levi/IdeaProjects/操作系统/第2章_进程与线程/figures/"
F = lambda n: FIG + n


# ---------- ch2-27 程序 vs 进程 ----------
def f27():
    fig, ax = osfig.new_fig(12, 6.0, xlim=(0, 12), ylim=(0, 6.0))
    osfig.title(ax, "程序 vs 进程：菜谱 vs 正在炒的那盘菜",
                sub="程序是静态的指令文件；进程是程序的一次动态执行过程，一个程序可对应多个进程", fs=15)
    # 左：程序
    osfig.tx(ax, 3.0, 5.1, "程序（静态）", fs=13, bold=True, color=GRAY)
    osfig.rbox(ax, 1.2, 3.3, 3.6, 1.4, "微信.exe\n\n（代码 + 初始数据）", fc=GRAY_L, ec=GRAY, fs=12, bold=True, ls=1.6)
    osfig.tx(ax, 3.0, 2.7, "躺在磁盘上，永远不变", fs=10.5, color=GRAY)
    osfig.tx(ax, 3.0, 2.25, "永久的：可长期保存", fs=10.5, color=GRAY)
    osfig.tx(ax, 3.0, 1.8, "无并发概念、无状态", fs=10.5, color=GRAY)
    # 右：进程
    osfig.tx(ax, 9.0, 5.1, "进程（动态）：同一程序 × 3", fs=13, bold=True, color=BLUE)
    names = [("微信进程#1\n(和妈聊天)", BLUE_L, BLUE, 7.2), ("微信进程#2\n(摸鱼群)", GREEN_L, GREEN, 8.7), ("微信进程#3\n(视频号)", PURPLE_L, PURPLE, 10.2)]
    for label, fc, ec, x in names:
        osfig.rbox(ax, x, 3.0, 1.5, 1.7, label, fc=fc, ec=ec, fs=9, bold=True, ls=1.3)
        osfig.tx(ax, x + 0.75, 4.85, "PCB", fs=9, bold=True, color=ec)
        osfig.rect(ax, x + 0.15, 4.72, 1.2, 0.22, "", fc="white", ec=ec, lw=1.1)
    osfig.tx(ax, 9.0, 2.45, "在内存里「活」着：有生命周期、有状态", fs=10.5, color=INK)
    osfig.tx(ax, 9.0, 2.0, "暂时的：创建→运行→消亡", fs=10.5, color=INK)
    osfig.tx(ax, 9.0, 1.55, "可并发、会走走停停（异步）", fs=10.5, color=INK)
    osfig.tx(ax, 6, 0.85, "对应关系：一个程序可对应多个进程（如上）；一个进程也可至少对应一个程序（进程里可再调别的程序）", fs=11, color=BLUE, bold=True)
    osfig.tx(ax, 6, 0.4, "【易错】「进程 = 程序 + PCB + 数据」说的是进程实体；「进程是程序的一次执行」说的是动态过程——两层说法都对，考点在区别", fs=10, color=RED, bold=True)
    osfig.save(fig, F("ch2-27_prog_vs_process.png"))


# ---------- ch2-28 状态转换序列例题 ----------
def f28():
    fig, ax = osfig.new_fig(13, 6.4, xlim=(0, 13), ylim=(0, 6.4))
    osfig.title(ax, "专项训练：给事件序列写状态变化（进程 P 的一生）",
                sub="做题模板：每发生一个事件，只检查「谁变、变成什么」，一次只动一条边", fs=15)
    states = [
        ("创建", GRAY, GRAY_L, 0.9), ("就绪", BLUE, BLUE_L, 2.85), ("运行", GREEN, GREEN_L, 4.8),
        ("阻塞", RED, RED_L, 6.75), ("就绪", BLUE, BLUE_L, 8.7), ("运行", GREEN, GREEN_L, 10.65), ("终止", PURPLE, PURPLE_L, 12.35),
    ]
    y = 4.0
    for name, ec, fc, x in states:
        w = 1.35 if x < 12 else 1.2
        osfig.box(ax, x + w / 2, y, w, 1.0, name, fc=fc, ec=ec, fs=13, bold=True)
    links = [(2.25, 2.85, "创建完成"), (4.2, 4.8, "被调度"), (6.15, 6.75, "请求打印"), (8.1, 8.7, "打印完成"), (10.05, 10.65, "再次调度"), (12.0, 12.35, "执行完毕")]
    for x1, x2, label in links:
        osfig.arrow(ax, x1, y, x2, y, "", color=INK, lw=1.8, ms=13)
        osfig.tx(ax, (x1 + x2) / 2, y + 0.35, label, fs=9.5, color=GRAY)
    rows = [
        ("t1 用户双击 P 的图标", "空 → 创建态", "创建原语：申请 PCB、分配资源"),
        ("t2 创建工作完成", "创建 → 就绪", "进入就绪队列排队等 CPU"),
        ("t3 被调度程序选中", "就绪 → 运行", "获得 CPU；注意不是「运行→就绪」"),
        ("t4 P 执行 print 语句", "运行 → 阻塞", "主动调用阻塞原语等 I/O（主动行为）"),
        ("t5 打印机打印完成", "阻塞 → 就绪", "I/O 中断触发唤醒原语（被动行为）"),
        ("t6 再次被调度", "就绪 → 运行", "从断点继续执行"),
        ("t7 程序执行 exit", "运行 → 终止", "撤销原语：回收资源、删 PCB"),
    ]
    osfig.tx(ax, 6.5, 2.95, "事件序列与状态推导（先自己写，再看右列）", fs=12, bold=True, color=INK)
    yy = 2.5
    for evt, trans, note in rows:
        osfig.tx(ax, 0.7, yy, evt, fs=10, ha="left", color=INK)
        osfig.tx(ax, 5.9, yy, trans, fs=10, ha="left", color=BLUE, bold=True)
        osfig.tx(ax, 8.4, yy, note, fs=9.5, ha="left", color=GRAY)
        yy -= 0.34
    osfig.tx(ax, 6.5, 0.28, "【易错】t4 是「运行→阻塞」（P 主动要 I/O）；若题目说「时间片到」才是「运行→就绪」——分清主动与被动", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch2-28_state_sequence_example.png"))


# ---------- ch2-29 就绪队列与阻塞队列 ----------
def f29():
    fig, ax = osfig.new_fig(13, 6.2, xlim=(0, 13), ylim=(0, 6.2))
    osfig.title(ax, "就绪队列与阻塞队列：进程排队的全景图",
                sub="就绪队列排的是「CPU」这一种资源；阻塞队列按「等的事件」分组，排队的人互不相干", fs=15)
    # CPU
    osfig.box(ax, 1.8, 4.4, 2.0, 1.1, "CPU", fc=GREEN_L, ec=GREEN, fs=15, bold=True)
    # 就绪队列
    osfig.tx(ax, 7.3, 5.5, "就绪队列（等 CPU）", fs=12, bold=True, color=BLUE)
    osfig.rect(ax, 4.6, 4.05, 5.6, 0.9, "", fc=BLUE_L, ec=BLUE, lw=1.8)
    for i, (nm, ec) in enumerate([("P1", BLUE), ("P2", TEAL), ("P6", PURPLE), ("P7", AMBER)]):
        osfig.circle(ax, 5.3 + i * 1.3, 4.5, 0.34, nm, fc="white", ec=ec, fs=11)
    osfig.arrow(ax, 4.5, 4.5, 2.9, 4.4, "调度：选一个上 CPU", color=GREEN, fs=10, dy=0.25)
    osfig.arrow(ax, 1.8, 3.85, 4.5, 3.3, "时间片到/被抢占 → 排回就绪队尾", color=BLUE, fs=10, dy=-0.15)
    # 阻塞队列组
    osfig.tx(ax, 7.3, 3.0, "阻塞队列（按等的事件分组）", fs=12, bold=True, color=RED)
    groups = [("等磁盘的队列", ["P3"], 0.9), ("等键盘的队列", ["P4", "P8"], 4.6), ("等打印机的队列", ["P5"], 8.9)]
    for title, members, x in groups:
        osfig.rbox(ax, x, 1.45, 3.2, 1.25, "", fc=RED_L, ec=RED)
        osfig.tx(ax, x + 1.6, 2.42, title, fs=10.5, bold=True, color=RED)
        for j, nm in enumerate(members):
            osfig.circle(ax, x + 1.0 + j * 1.1, 1.85, 0.3, nm, fc="white", ec=RED, fs=10.5)
    osfig.arrow(ax, 4.4, 3.55, 4.0, 2.7, "P 主动请求 I/O", color=RED, fs=10, dx=-0.5)
    osfig.arrow(ax, 2.0, 1.2, 4.4, 3.2, "I/O 完成（中断）→ 唤醒 → 回就绪队列", color=TEAL, fs=10, dx=1.2, dy=-0.3)
    osfig.tx(ax, 6.5, 0.55, "【考点】就绪队列里的进程「只差 CPU」；阻塞队列里的进程「差的是别的事件」，给它 CPU 也没用——所以不存在「阻塞→运行」", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch2-29_ready_block_queues.png"))


# ---------- ch2-30 直接/间接通信 ----------
def f30():
    fig, ax = osfig.new_fig(12, 5.6, xlim=(0, 12), ylim=(0, 5.6))
    osfig.title(ax, "消息传递：直接通信 vs 间接通信",
                sub="直接=报出对方名字点对点送；间接=通过共享的「信箱」中转（解耦收发双方）", fs=15)
    # 直接
    osfig.tx(ax, 3.2, 4.75, "① 直接通信：send(P2, msg)", fs=12.5, bold=True, color=BLUE)
    osfig.circle(ax, 1.7, 3.3, 0.6, "P1", fc=BLUE_L, ec=BLUE, fs=13)
    osfig.circle(ax, 4.7, 3.3, 0.6, "P2", fc=GREEN_L, ec=GREEN, fs=13)
    osfig.arrow(ax, 2.4, 3.3, 4.0, 3.3, "消息信封：\n接收进程的 ID + 正文", color=INK, fs=9.5, both=True, dy=0.55)
    osfig.tx(ax, 3.2, 2.15, "收发双方必须显式写明对方的标识符", fs=10.5, color=INK)
    osfig.tx(ax, 3.2, 1.7, "耦合紧：改一方，另一方也要改", fs=10.5, color=GRAY)
    # 间接
    osfig.tx(ax, 9.0, 4.75, "② 间接通信：信箱 mailbox", fs=12.5, bold=True, color=PURPLE)
    osfig.circle(ax, 7.4, 3.3, 0.6, "P1", fc=BLUE_L, ec=BLUE, fs=13)
    osfig.circle(ax, 10.6, 3.3, 0.6, "P2", fc=GREEN_L, ec=GREEN, fs=13)
    osfig.box(ax, 9.0, 3.3, 1.7, 1.1, "信箱\nM", fc=PURPLE_L, ec=PURPLE, fs=12, bold=True)
    osfig.arrow(ax, 8.05, 3.5, 8.15, 3.5, "", color=INK, lw=1.8)
    osfig.tx(ax, 7.75, 3.85, "send(M,msg)", fs=9, color=BLUE)
    osfig.arrow(ax, 9.75, 3.5, 9.95, 3.5, "", color=INK, lw=1.8)
    osfig.tx(ax, 10.35, 3.85, "receive(M)", fs=9, color=GREEN)
    osfig.tx(ax, 9.0, 2.15, "双方只认信箱，不认人：接收者可是多个", fs=10.5, color=INK)
    osfig.tx(ax, 9.0, 1.7, "耦合松：支持多对多、易于扩展", fs=10.5, color=GRAY)
    osfig.tx(ax, 6, 0.75, "【考点】信箱通信属于「间接」消息传递；「直接通信需要知道对方名字」判断题常考", fs=11, color=RED, bold=True)
    osfig.tx(ax, 6, 0.3, "注意：无论直接还是间接，消息传递都需要内核提供收发原语（send/receive），是「高级通信」方式", fs=10, color=BLUE)
    osfig.save(fig, F("ch2-30_ipc_direct_indirect.png"))


# ---------- ch2-31 ULT vs KLT 切换 ----------
def f31():
    fig, ax = osfig.new_fig(12.5, 6.4, xlim=(0, 12.5), ylim=(0, 6.4))
    osfig.title(ax, "用户级线程 vs 内核级线程：切换发生在哪里？",
                sub="ULT 切换不进内核（快，但一阻全阻）；KLT 切换要进内核（慢一点，可真并行）", fs=15)
    # 左 ULT
    osfig.tx(ax, 3.1, 5.55, "用户级线程（ULT）", fs=13, bold=True, color=BLUE)
    osfig.rbox(ax, 0.7, 3.1, 4.8, 2.1, "", fc=BLUE_L, ec=BLUE)
    osfig.tx(ax, 3.1, 4.95, "进程 P（内核只看见它）", fs=11, bold=True, color=BLUE)
    for i, nm in enumerate(["T1", "T2", "T3"]):
        osfig.circle(ax, 1.7 + i * 1.5, 3.95, 0.42, nm, fc="white", ec=BLUE, fs=11)
    osfig.rbox(ax, 0.7, 1.7, 4.8, 0.9, "内核（把 P 当成调度单位）", fc=GRAY_L, ec=GRAY, fs=11, bold=True)
    osfig.arrow(ax, 2.2, 3.1, 2.2, 2.62, "", color=INK, lw=1.5)
    osfig.tx(ax, 3.1, 0.95, "T1→T2 切换：线程库代码完成，全程用户态", fs=10.5, color=GREEN, bold=True)
    osfig.tx(ax, 3.1, 0.5, "坑：T1 阻塞（如等 I/O）→ 内核把整个 P 挂起", fs=10.5, color=RED, bold=True)
    # 右 KLT
    osfig.tx(ax, 9.4, 5.55, "内核级线程（KLT）", fs=13, bold=True, color=PURPLE)
    osfig.rbox(ax, 7.0, 3.1, 4.8, 2.1, "", fc=PURPLE_L, ec=PURPLE)
    osfig.tx(ax, 9.4, 4.95, "进程 P", fs=11, bold=True, color=PURPLE)
    for i, nm in enumerate(["T1", "T2", "T3"]):
        osfig.circle(ax, 8.0 + i * 1.5, 3.95, 0.42, nm, fc="white", ec=PURPLE, fs=11)
    osfig.rbox(ax, 7.0, 1.7, 4.8, 0.9, "内核（直接调度每个 T）", fc=RED_L, ec=RED, fs=11, bold=True)
    osfig.arrow(ax, 8.6, 3.1, 8.6, 2.62, "", color=INK, lw=1.5)
    osfig.arrow(ax, 10.2, 2.62, 10.2, 3.1, "", color=INK, lw=1.5)
    osfig.tx(ax, 9.4, 0.95, "T1→T2 切换：陷入内核，内核完成调度切换", fs=10.5, color=AMBER, bold=True)
    osfig.tx(ax, 9.4, 0.5, "好：T1 阻塞，内核可调度 T2/T3，甚至另一核", fs=10.5, color=GREEN, bold=True)
    osfig.tx(ax, 6.25, 0.12, "【考点】ULT 切换可在无内核介入下完成（不需要态切换）；KLT 的切换与进程切换一样需要进核心态", fs=10.5, color=RED, bold=True)
    osfig.save(fig, F("ch2-31_ult_klt_switch.png"))


# ---------- ch2-32 RR 完整时间轴 ----------
def f32():
    fig, ax = osfig.new_fig(12.5, 9.9, xlim=(0, 12.5), ylim=(0, 9.9))
    osfig.title(ax, "时间片轮转 RR（q=1）完整推演：每个 1ms 的就绪队列快照",
                sub="P1(0,7) P2(2,4) P3(4,1) P4(5,4)；约定：同一时刻「新到达先入队，被抢占的后入队」", fs=15)
    # 甘特带
    runs = [("P1", BLUE, BLUE_L), ("P1", BLUE, BLUE_L), ("P2", GREEN, GREEN_L), ("P1", BLUE, BLUE_L),
            ("P2", GREEN, GREEN_L), ("P3", AMBER, AMBER_L), ("P1", BLUE, BLUE_L), ("P4", PURPLE, PURPLE_L),
            ("P2", GREEN, GREEN_L), ("P1", BLUE, BLUE_L), ("P4", PURPLE, PURPLE_L), ("P2", GREEN, GREEN_L),
            ("P1", BLUE, BLUE_L), ("P4", PURPLE, PURPLE_L), ("P1", BLUE, BLUE_L), ("P4", PURPLE, PURPLE_L)]
    x0, w = 3.4, 0.54
    for i, (nm, ec, fc) in enumerate(runs):
        osfig.rect(ax, x0 + i * w, 8.05, w, 0.6, nm, fc=fc, ec=ec, fs=9, bold=True)
    for i in range(0, 17, 2):
        osfig.tx(ax, x0 + i * w, 7.78, str(i), fs=8.5, color=GRAY)
    # 表格
    rows = [
        ("0-1", "P1", "[P1]", "P1 运行1ms后被抢占，重新入队尾"),
        ("1-2", "P1", "[P1]", "队列里只有它，接着跑"),
        ("2-3", "P2", "[P2, P1]", "t=2：P2到达先入队，P1被抢占后入队"),
        ("3-4", "P1", "[P1, P2]", "P1跑完1ms回队尾，排到P2后面"),
        ("4-5", "P2", "[P2, P3, P1]", "t=4：P3到达先入队，P1被抢占后入队"),
        ("5-6", "P3", "[P3, P1, P4, P2]", "t=5：P4到达先入队，P2被抢占后入队"),
        ("6-7", "P1", "[P1, P4, P2]", "P3只需1ms，在5-6完成（完成时刻6）"),
        ("7-8", "P4", "[P4, P2, P1]", ""),
        ("8-9", "P2", "[P2, P1, P4]", ""),
        ("9-10", "P1", "[P1, P4, P2]", ""),
        ("10-11", "P4", "[P4, P2, P1]", ""),
        ("11-12", "P2", "[P2, P1, P4]", "P2最后1ms，完成（完成时刻12）"),
        ("12-13", "P1", "[P1, P4]", "只剩两个，轮流跑"),
        ("13-14", "P4", "[P4, P1]", ""),
        ("14-15", "P1", "[P1, P4]", "P1完成（完成时刻15）"),
        ("15-16", "P4", "[P4]", "P4完成（完成时刻16）"),
    ]
    # 表头
    osfig.rect(ax, 0.7, 7.35, 1.1, 0.5, "时间", fc=GRAY_L, ec=GRAY, fs=10, bold=True)
    osfig.rect(ax, 1.8, 7.35, 1.0, 0.5, "CPU", fc=GRAY_L, ec=GRAY, fs=10, bold=True)
    osfig.rect(ax, 2.8, 7.35, 4.2, 0.5, "该 1ms 结束时的就绪队列", fc=GRAY_L, ec=GRAY, fs=10, bold=True)
    osfig.rect(ax, 7.0, 7.35, 5.0, 0.5, "事件/说明", fc=GRAY_L, ec=GRAY, fs=10, bold=True)
    y = 7.35
    colors = {"P1": BLUE_L, "P2": GREEN_L, "P3": AMBER_L, "P4": PURPLE_L}
    ecolors = {"P1": BLUE, "P2": GREEN, "P3": AMBER, "P4": PURPLE}
    for t, cpu, queue, note in rows:
        y -= 0.42
        osfig.rect(ax, 0.7, y, 1.1, 0.42, t, fc="white", ec=GRAY, fs=9.5)
        osfig.rect(ax, 1.8, y, 1.0, 0.42, cpu, fc=colors[cpu], ec=ecolors[cpu], fs=9.5, bold=True)
        osfig.rect(ax, 2.8, y, 4.2, 0.42, queue, fc="white", ec=GRAY, fs=9)
        osfig.rect(ax, 7.0, y, 5.0, 0.42, note, fc="white", ec=GRAY, fs=8.5)
    osfig.tx(ax, 6.25, 0.35, "结果：完成时刻 P1=15、P2=12、P3=6、P4=16；周转时间 15/10/2/11；带权周转 ≈2.14/2.5/2/2.75",
             fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch2-32_rr_full_timeline.png"))


# ---------- ch2-33 TSL 与 Swap ----------
def f33():
    fig, ax = osfig.new_fig(12.5, 6.2, xlim=(0, 12.5), ylim=(0, 6.2))
    osfig.title(ax, "硬件同步方法：TSL 与 Swap 为什么不会「中间被打断」",
                sub="关键：上锁+检查用一条（不可分割的）指令完成，软件法的「检查、上锁分离」漏洞被硬件堵死", fs=14.5)
    # TSL 面板
    osfig.rbox(ax, 0.7, 1.3, 5.5, 4.3, "", fc=BLUE_L, ec=BLUE)
    osfig.tx(ax, 3.45, 5.15, "TSL 指令（Test and Set Lock）", fs=12.5, bold=True, color=BLUE)
    osfig.rbox(ax, 1.1, 3.7, 4.7, 1.1, "TSL RX, LOCK：\n  (RX) = (LOCK)   // 读旧值\n  (LOCK) = 1      // 立刻上锁", fc="white", ec=BLUE, fs=10.5, bold=True, ls=1.6)
    osfig.tx(ax, 3.45, 3.05, "硬件保证这两步一条指令内完成", fs=10.5, color=RED, bold=True)
    osfig.tx(ax, 3.45, 2.5, "之后：if (RX == 0) 进临界区；else 自旋重试", fs=10.5, color=INK)
    osfig.tx(ax, 3.45, 1.85, "附加手段：封锁总线，其他核插不进来", fs=10.5, color=INK)
    # Swap 面板
    osfig.rbox(ax, 6.4, 1.3, 5.5, 4.3, "", fc=GREEN_L, ec=GREEN)
    osfig.tx(ax, 9.15, 5.15, "Swap / XCHG 指令（交换）", fs=12.5, bold=True, color=GREEN)
    osfig.rbox(ax, 6.8, 3.7, 4.7, 1.1, "Swap(A, B)：\n  临时 = (A); (A) = (B); (B) = 临时\n// 一步完成内存两单元交换", fc="white", ec=GREEN, fs=10.5, bold=True, ls=1.6)
    osfig.tx(ax, 9.15, 3.05, "用法：把 old=1 换进 LOCK，看换出的旧值", fs=10.5, color=INK)
    osfig.tx(ax, 9.15, 2.5, "换出 0 → 说明原来没锁 → 进临界区", fs=10.5, color=GREEN)
    osfig.tx(ax, 9.15, 1.95, "换出 1 → 已被别人锁 → 自旋重试", fs=10.5, color=RED)
    osfig.tx(ax, 6.25, 0.7, "【对比软件方法】双标志先检查法错在「检查」和「上锁」是两条指令、中间可被打断；", fs=10.5, color=INK)
    osfig.tx(ax, 6.25, 0.28, "TSL/Swap 把两件事焊成一条原子指令——这就是「硬件方法」的全部秘密", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch2-33_hardware_sync.png"))


# ---------- ch2-34 信号量 value 追踪 ----------
def f34():
    fig, ax = osfig.new_fig(12.5, 7.4, xlim=(0, 12.5), ylim=(0, 7.4))
    osfig.title(ax, "手把手算信号量：S 初值 = 2 时的每一步变化",
                sub="口诀：P 减 V 增；S>0 表示还剩几份资源，S<0 绝对值 = 排队等待的进程数", fs=15)
    steps = [
        ("0", "初始", "2", "—", "两份资源空闲"),
        ("1", "P1 执行 P(S)", "1", "空", "P1 拿走一份"),
        ("2", "P2 执行 P(S)", "0", "空", "P2 拿走最后一份"),
        ("3", "P3 执行 P(S)", "-1", "[P3]", "没资源了，P3 进等待队列阻塞"),
        ("4", "P4 执行 P(S)", "-2", "[P3, P4]", "P4 也阻塞；|S|=2 = 等待数"),
        ("5", "P1 用完执行 V(S)", "-1", "[P4]", "P1 归还一份，唤醒队首 P3"),
        ("6", "P3 执行 P(S)", "-2", "[P3, P4]", "P3 拿到刚归还的资源又立刻用掉？——不对：P3 被唤醒后重新参与调度，P(S) 是它被调度后才执行"),
        ("7", "P2 执行 V(S)", "-1", "[P3]", "P2 归还一份，唤醒 P4"),
    ]
    # 表头
    osfig.rect(ax, 0.7, 6.35, 0.8, 0.5, "步", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 1.5, 6.35, 2.6, 0.5, "操作", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 4.1, 6.35, 1.1, 0.5, "S 值", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 5.2, 6.35, 1.9, 0.5, "等待队列", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 7.1, 6.35, 5.0, 0.5, "解释", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    y = 6.35
    for no, op, sv, q, note in steps:
        y -= 0.62
        osfig.rect(ax, 0.7, y, 0.8, 0.62, no, fc="white", ec=GRAY, fs=10)
        osfig.rect(ax, 1.5, y, 2.6, 0.62, op, fc=BLUE_L, ec=BLUE, fs=9.5, bold=True)
        val_color = GREEN_L if int(sv) >= 0 else RED_L
        osfig.rect(ax, 4.1, y, 1.1, 0.62, sv, fc=val_color, ec=(GREEN if int(sv) >= 0 else RED), fs=10.5, bold=True)
        osfig.rect(ax, 5.2, y, 1.9, 0.62, q, fc="white", ec=GRAY, fs=9)
        osfig.rect(ax, 7.1, y, 5.0, 0.62, note, fc="white", ec=GRAY, fs=8)
    osfig.tx(ax, 6.25, 0.55, "【考点】给出操作序列求 S 的最终值与等待进程数——就是顺着这张表一步步推", fs=11, color=RED, bold=True)
    osfig.tx(ax, 6.25, 0.15, "S 的物理意义再强调：S>0 = 还剩 S 份资源；S=0 = 都被占用但没人等；S<0 = 超发，|S| 个进程在排队", fs=10, color=BLUE)
    osfig.save(fig, F("ch2-34_semaphore_trace.png"))


# ---------- ch2-35 写优先 ----------
def f35():
    fig, ax = osfig.new_fig(12.5, 7.0, xlim=(0, 12.5), ylim=(0, 7.0))
    osfig.title(ax, "读者-写者问题：读优先的「饿死写者」与写优先补丁",
                sub="读优先版里，只要读者一个接一个，写者永远挤不进去——加一把「w 闸门」解决", fs=14.5)
    # 左：读优先问题
    osfig.rbox(ax, 0.6, 1.5, 5.4, 4.7, "", fc=RED_L, ec=RED)
    osfig.tx(ax, 3.3, 5.75, "读优先版的问题", fs=12.5, bold=True, color=RED)
    osfig.tx(ax, 3.3, 5.0, "t1 读者A到 → rc=1，锁 rw，开始读\n\n"
                          "t2 读者B到 → rc=2，直接读\n\n"
                          "t3 写者W到 → 卡在 P(rw) 上\n\n"
                          "t4 读者C到 → rc=3，直接读\n\n"
                          "t5 读者D到 → ……\n\n"
                          "只要读者不断流，rw 永远不释放",
              fs=10.5, ls=1.75, color=INK)
    osfig.tx(ax, 3.3, 1.85, "W 被「饿死」", fs=12, bold=True, color=RED)
    # 右：写优先
    osfig.rbox(ax, 6.5, 1.5, 5.4, 4.7, "", fc=GREEN_L, ec=GREEN)
    osfig.tx(ax, 9.2, 5.75, "写优先（读写公平法）补丁", fs=12.5, bold=True, color=GREEN)
    osfig.rbox(ax, 6.9, 3.0, 4.6, 2.3, "writer {            \n"
                                      "  while(true){\n"
                                      "    P(w);   // 闸门：写者把门\n"
                                      "    P(rw);  // 独占访问\n"
                                      "    写;\n"
                                      "    V(rw); V(w); }\n"
                                      "}  // 读者进入区也要先 P(w)",
              fc="white", ec=GREEN, fs=9.5, bold=True, ls=1.45)
    osfig.tx(ax, 9.2, 2.35, "效果：写者 W 到达后在 P(w) 排队，", fs=10, color=INK)
    osfig.tx(ax, 9.2, 2.0, "后续读者被 W 挡在 w 上——W 不再饿死", fs=10, color=INK)
    osfig.tx(ax, 9.2, 1.65, "代价：并发读的吞吐略降（读写公平）", fs=10, color=GRAY)
    osfig.tx(ax, 6.25, 0.75, "【考点】三个信号量各司其职：rw=读写互斥；rc_mutex=保护 rc 计数；w=让写者「插队占门」", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch2-35_writer_priority.png"))


# ---------- ch2-36 不安全 ≠ 死锁 ----------
def f36():
    fig, ax = osfig.new_fig(12.5, 6.4, xlim=(0, 12.5), ylim=(0, 6.4))
    osfig.title(ax, "反例澄清：不安全状态 ≠ 死锁",
                sub="安全序列找不到 = 「可能」死锁；真死锁还要看进程实际是否申请到最大需求", fs=15)
    # 数据
    osfig.tx(ax, 6.25, 5.35, "单类资源 R，共 10 个；Available = 10-9 = 1", fs=12, bold=True, color=INK)
    cols = [("进程", 2.2), ("Allocation 已分", 4.6), ("Max 最大需求", 7.2), ("Need 尚需", 9.6)]
    for name, x in cols:
        osfig.rbox(ax, x - 1.1, 4.45, 2.2, 0.5, name, fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    rows = [("P1", "5", "10", "5"), ("P2", "2", "4", "2"), ("P3", "2", "9", "7")]
    y = 3.95
    for p, a, m, n in rows:
        for (name, x), v in zip(cols, (p, a, m, n)):
            osfig.rbox(ax, x - 1.1, y, 2.2, 0.45, v, fc="white", ec=GRAY, fs=10.5, bold=(name == "进程"))
        y -= 0.5
    # 结论
    osfig.rbox(ax, 0.7, 1.35, 5.4, 1.45, "", fc=AMBER_L, ec=AMBER)
    osfig.tx(ax, 3.4, 2.45, "安全性检查：Available=1", fs=11.5, bold=True, color=AMBER)
    osfig.tx(ax, 3.4, 1.95, "P1 需 5 > 1；P2 需 2 > 1；P3 需 7 > 1\n找不到任何安全序列 → 不安全状态", fs=10.5, color=INK, ls=1.5)
    osfig.rbox(ax, 6.4, 1.35, 5.4, 1.45, "", fc=GREEN_L, ec=GREEN)
    osfig.tx(ax, 9.1, 2.45, "但此刻并没有死锁", fs=11.5, bold=True, color=GREEN)
    osfig.tx(ax, 9.1, 1.95, "若 P2 实际只要再要 1 个（没用到 Max=4），\n用完归还 2 个 → 系统照常推进，无人死锁", fs=10.5, color=INK, ls=1.5)
    osfig.tx(ax, 6.25, 0.6, "【必背】安全状态必无死锁；不安全状态只是「有死锁的风险」——银行家算法是「事前避险」，不是「已经出事」", fs=11.5, color=RED, bold=True)
    osfig.save(fig, F("ch2-36_unsafe_no_deadlock.png"))


# ---------- ch2-37 资源分配图化简例题 ----------
def f37():
    fig, ax = osfig.new_fig(13, 6.8, xlim=(0, 13), ylim=(0, 6.8))
    osfig.title(ax, "死锁检测：资源分配图化简两例",
                sub="化简法：找一个「请求都能被满足」的进程，抹掉它的边、回收资源，反复化简", fs=15)
    # 左：可完全化简
    osfig.tx(ax, 3.2, 6.0, "例 1：可以完全化简 → 无死锁", fs=12.5, bold=True, color=GREEN)
    osfig.circle(ax, 1.5, 4.6, 0.45, "P3", fc="white", ec=GREEN, fs=12, bold=True)
    osfig.box(ax, 3.6, 4.6, 0.75, 0.75, "R3", fc=AMBER_L, ec=AMBER, fs=10, bold=True)
    osfig.circle(ax, 5.4, 4.6, 0.45, "P4", fc="white", ec=BLUE, fs=12, bold=True)
    osfig.circle(ax, 3.6, 5.65, 0.2, "", fc=AMBER, ec=AMBER)
    osfig.tx(ax, 1.75, 4.95, "无请求边", fs=9, color=GRAY)
    osfig.arrow(ax, 3.22, 4.6, 1.95, 4.6, "分配边", color=AMBER, fs=8.5, dy=0.22)
    osfig.arrow(ax, 5.0, 4.35, 4.0, 4.15, "请求边：P4 要 R3", color=BLUE, fs=8.5, dy=-0.3)
    osfig.tx(ax, 3.2, 3.3, "第1步：P3 请求为空 → 非孤立不阻塞\n     抹掉 P3 全部边，R3 空出一个资源\n第2步：P4 的请求被满足 → 同样化简\n两进程都可完成 → 可完全化简", fs=10, color=INK, ls=1.6, bg=GREEN_L)
    # 右：不可完全化简
    osfig.tx(ax, 9.7, 6.0, "例 2：卡住 → 有死锁", fs=12.5, bold=True, color=RED)
    osfig.circle(ax, 8.4, 4.8, 0.45, "P5", fc="white", ec=RED, fs=12, bold=True)
    osfig.circle(ax, 11.0, 4.8, 0.45, "P6", fc="white", ec=RED, fs=12, bold=True)
    osfig.box(ax, 9.7, 5.6, 0.75, 0.7, "R1", fc=AMBER_L, ec=AMBER, fs=10, bold=True)
    osfig.box(ax, 9.7, 3.9, 0.75, 0.7, "R2", fc=AMBER_L, ec=AMBER, fs=10, bold=True)
    osfig.circle(ax, 9.7, 5.6, 0.14, "", fc=AMBER, ec=AMBER)
    osfig.circle(ax, 9.7, 3.9, 0.14, "", fc=AMBER, ec=AMBER)
    osfig.arrow(ax, 9.32, 5.6, 8.75, 5.1, "", color=AMBER, lw=1.6)
    osfig.arrow(ax, 8.75, 4.5, 9.32, 4.05, "", color=BLUE, lw=1.6)
    osfig.arrow(ax, 10.62, 5.45, 10.08, 5.75, "", color=BLUE, lw=1.6)
    osfig.arrow(ax, 10.08, 4.15, 10.62, 3.6, "", color=AMBER, lw=1.6)
    osfig.tx(ax, 8.35, 5.35, "持R1", fs=8.5, color=AMBER)
    osfig.tx(ax, 8.55, 4.3, "要R2", fs=8.5, color=BLUE)
    osfig.tx(ax, 11.15, 5.5, "要R1", fs=8.5, color=BLUE)
    osfig.tx(ax, 10.95, 3.75, "持R2", fs=8.5, color=AMBER)
    osfig.tx(ax, 9.7, 3.3, "P5 等 P6 手里的 R2，P6 等 P5 手里的 R1\n两进程都阻塞 → 谁的边都抹不掉\n剩余子图不可化简 → 死锁（死锁定理）", fs=10, color=INK, ls=1.6, bg=RED_L)
    osfig.tx(ax, 6.5, 1.0, "化简口诀：找「要的都给得起」的进程 → 消边回收 → 循环直到无人可化简", fs=11.5, color=BLUE, bold=True)
    osfig.tx(ax, 6.5, 0.45, "【死锁定理】系统处于死锁态 ⇔ 资源分配图不可完全化简；化简后还连着边的进程 = 死锁进程", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch2-37_rag_simplify_example.png"))


# ---------- ch2-38 死锁 vs 饥饿 ----------
def f38():
    fig, ax = osfig.new_fig(12.5, 6.0, xlim=(0, 12.5), ylim=(0, 6.0))
    osfig.title(ax, "死锁 vs 饥饿：都是「等不到」，病根完全不同",
                sub="死锁=互相等、集体卡死；饥饿=排不上队、但系统整体仍在推进", fs=15)
    # 左：死锁
    osfig.tx(ax, 3.2, 5.2, "死锁：互相等待，全员冻结", fs=13, bold=True, color=RED)
    osfig.circle(ax, 1.8, 4.0, 0.5, "P1", fc="white", ec=RED, fs=12, bold=True)
    osfig.circle(ax, 4.6, 4.0, 0.5, "P2", fc="white", ec=RED, fs=12, bold=True)
    osfig.box(ax, 3.2, 4.9, 0.7, 0.65, "R1", fc=GRAY_L, ec=GRAY, fs=10, bold=True)
    osfig.box(ax, 3.2, 3.1, 0.7, 0.65, "R2", fc=GRAY_L, ec=GRAY, fs=10, bold=True)
    osfig.tx(ax, 2.45, 4.55, "持R1", fs=9, color=GRAY)
    osfig.tx(ax, 3.95, 4.55, "要R2", fs=9, color=RED)
    osfig.tx(ax, 3.95, 3.55, "持R2", fs=9, color=GRAY)
    osfig.tx(ax, 2.45, 3.55, "要R1", fs=9, color=RED)
    osfig.rect(ax, 0.9, 2.0, 4.6, 0.55, "P1: 卡住…卡住…卡住…", fc=RED_L, ec=RED, fs=10)
    osfig.rect(ax, 0.9, 1.35, 4.6, 0.55, "P2: 卡住…卡住…卡住…", fc=RED_L, ec=RED, fs=10)
    osfig.tx(ax, 3.2, 0.75, "循环等待形成 → 系统这一角「死机」", fs=10.5, color=RED, bold=True)
    # 右：饥饿
    osfig.tx(ax, 9.3, 5.2, "饥饿：抢不过别人，系统仍在跑", fs=13, bold=True, color=AMBER)
    osfig.tx(ax, 9.3, 4.55, "打印机排队（优先级调度）", fs=10.5, color=INK)
    rows = [("P1(高优先级)", "打印 打印 打印", GREEN), ("P2(中优先级)", "打印 打印 打印", TEAL), ("P3(低优先级)", "等…等…等…永远排不上", RED)]
    y = 4.0
    for name, act, c in rows:
        osfig.rbox(ax, 7.0, y, 2.2, 0.5, name, fc="white", ec=c, fs=9.5, bold=True)
        osfig.rbox(ax, 9.2, y, 2.7, 0.5, act, fc=(GREEN_L if c != RED else RED_L), ec=c, fs=9.5)
        y -= 0.62
    osfig.tx(ax, 9.3, 1.7, "P1、P2 正常推进（系统没卡死），", fs=10.5, color=INK)
    osfig.tx(ax, 9.3, 1.3, "但 P3 长期得不到服务 → 饥饿", fs=10.5, color=RED, bold=True)
    osfig.tx(ax, 6.25, 0.5, "【对比】死锁的双方都在「等对方」；饥饿的受害者只是在「排队规则」下永远轮不到——SJF 让长作业饥饿、读优先让写者饥饿", fs=10.5, color=BLUE, bold=True)
    osfig.save(fig, F("ch2-38_deadlock_vs_starvation.png"))


if __name__ == "__main__":
    f27(); f28(); f29(); f30(); f31(); f32(); f33(); f34(); f35(); f36(); f37(); f38()
    print("ch2 extras done")
