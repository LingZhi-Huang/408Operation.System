# -*- coding: utf-8 -*-
"""第2章 进程与线程 · 全部插图绘制脚本（写作顺序：确认图片成功后再写正文）"""
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

FIG = "/Users/levi/IdeaProjects/操作系统/第2章_进程与线程/figures"

def t(ax, *a, **k): return O.tx(ax, *a, **k)
def bk(ax, *a, **k): return O.box(ax, *a, **k)
def rk(ax, *a, **k): return O.rbox(ax, *a, **k)
def rc(ax, *a, **k): return O.rect(ax, *a, **k)
def dm(ax, *a, **k): return O.diamond(ax, *a, **k)
def el(ax, *a, **k): return O.ellipse(ax, *a, **k)
def ci(ax, *a, **k): return O.circle(ax, *a, **k)
def al(ax, *a, **k): return O.arrow(ax, *a, **k)
def ln(ax, *a, **k): return O.line(ax, *a, **k)

def save_fig(fig, name):
    O.save(fig, f"{FIG}/{name}.png")

# ============ 通用小件 ============
def gantt_row(ax, x0, x1, y, h, segs, labels_below=True, axis=False):
    """segs: list of (label, start, length, color, fc)"""
    for label, st, ln_, ec, fc in segs:
        rc(ax, st, y, ln_, h, label, fc=fc, ec=ec, fs=10.5, bold=True, z=4)

def proc_colors():
    return [("P1", BLUE, BLUE_L), ("P2", GREEN, GREEN_L),
            ("P3", AMBER, AMBER_L), ("P4", PURPLE, PURPLE_L)]

# ============ ch2-00 本章知识框架导图 ============
def fig00():
    fig, ax = O.new_fig(11.6, 11.2, (0, 11.6), (0, 11.2))
    O.title(ax, "第2章 进程与线程 · 知识框架导图",
            "主线：程序如何变成“在CPU上跑动的进程”——描述它(2.1~2.5) → 管好它(2.6调度) → 协调它(2.7同步) → 防范它(2.8死锁)")
    bk(ax, 5.8, 9.6, 3.2, 0.8, "进程与线程", fc=PURPLE_L, ec=PURPLE, fs=16, bold=True)
    cols = [
        (1.15, BLUE,  "2.1 进程概念与组成", ["程序并发三特点", "进程实体=PCB+程序+数据", "PCB详解·进程特征"], ["间断性·失去封闭性·不可再现性"]),
        (3.50, GREEN, "2.2 状态与转换", ["五状态模型", "七状态+挂起", "状态转换判断"], ["中级调度=挂起管理"]),
        (5.85, AMBER, "2.3 进程控制", ["原语=原子操作", "创建·撤销原语", "阻塞·唤醒·切换"], ["关中断实现"]),
        (8.20, TEAL,  "2.4 进程通信", ["共享存储", "消息传递(信箱)", "管道(半双工)"], ["互斥+同步+阻塞"]),
        (10.55, PINK, "2.5 线程", ["线程引入与属性", "进程vs线程", "ULT与KLT映射"], ["一个阻塞全阻塞"]),
    ]
    for cx, c, head, kids, note in cols:
        bk(ax, cx, 8.35, 2.18, 0.78, head, fc=GRAY_L, ec=c, fs=11, bold=True, color=c)
        al(ax, 5.8, 9.18, cx, 8.76, lw=1.8, color=c)
        ys = [7.35, 6.4, 5.45]
        light = {BLUE: BLUE_L, GREEN: GREEN_L, AMBER: AMBER_L,
                 TEAL: TEAL_L, PINK: PINK_L}
        for i, k in enumerate(kids):
            bk(ax, cx, ys[i], 2.16, 0.72, k, fc=light[c], ec=c, fs=9.6)
            if i == 0:
                al(ax, cx, 7.94, cx, ys[i] + 0.40, lw=1.6, color=c)
            else:
                al(ax, cx, ys[i - 1] - 0.40, cx, ys[i] + 0.40, lw=1.6, color=c)
    al(ax, 5.8, 9.18, 5.8, 5.1, lw=1.6, color=GRAY, ls=":")
    bigs = [
        (2.0, AMBER, "2.6 处理机调度", ["三级调度(高/中/低)", "调度时机·方式·指标", "FCFS·SJF·HRRN·RR·优先级·MLFQ", "★甘特图计算大题"]),
        (5.9, RED,   "2.7 同步与互斥", ["临界区四个部分", "软件/硬件方法·Peterson", "信号量与PV原语", "生产者-消费者·读者写者·哲学家"]),
        (9.8, BLUE,  "2.8 死锁", ["四必要条件", "预防·避免(银行家)", "检测(RAG化简)+解除", "安全序列判断"]),
    ]
    for cx, c, head, kids in bigs:
        bk(ax, cx, 4.2, 3.6, 0.72, head, fc=GRAY_L, ec=c, fs=12, bold=True, color=c)
        al(ax, 5.8, 5.05, cx, 4.58, lw=1.6, color=c)
        for i, k in enumerate(kids):
            bk(ax, cx, 3.35 - i * 0.75, 3.58, 0.62, k, fc=GRAY_L, ec=c, fs=9.6,
               dashed=(i == 3))
    rk(ax, 0.35, 0.15, 10.9, 0.52,
       "考情：本章分值最重。选择题高频：状态转换·管道特性·线程属性·调度算法；大题高频：调度甘特图、PV代码(生产者消费者/读者写者/哲学家)、银行家算法安全序列。",
       fc=AMBER_L, ec=AMBER, fs=9.6)
    save_fig(fig, "ch2-00_chapter_map")

# ============ ch2-01 进程实体 ============
def fig01():
    fig, ax = O.new_fig(10.6, 6.4, (0, 10.6), (0, 6.4))
    O.title(ax, "进程实体：PCB + 程序段 + 数据段",
            "程序=静态的(躺在磁盘上的代码)；进程=动态的(程序的一次执行过程)")
    # 大容器
    rk(ax, 0.5, 1.9, 9.6, 3.3, "", fc="#F8FAFC", ec=INK, lw=2.2)
    t(ax, 5.3, 5.02, "进程实体（一个进程在系统里的全部“存在”）", fs=13, bold=True)
    # 三块
    bk(ax, 1.9, 3.15, 2.7, 1.5, "PCB\n进程控制块", fc=BLUE_L, ec=BLUE, fs=13, bold=True)
    t(ax, 1.9, 2.15, "常驻内存\n(进程存在的唯一标志)", fs=9.6, color=BLUE, bold=True)
    bk(ax, 5.3, 3.15, 2.7, 1.5, "程序段\n程序代码(指令)", fc=GREEN_L, ec=GREEN, fs=12, bold=True)
    t(ax, 5.3, 2.2, "可在内存，也可被换出到外存", fs=9.6, color=GREEN, bold=True)
    bk(ax, 8.7, 3.15, 2.5, 1.5, "数据段\n运行时数据\n(全局变量等)", fc=AMBER_L, ec=AMBER, fs=11, bold=True)
    t(ax, 8.75, 2.2, "也可被换出到外存", fs=9.6, color=AMBER, bold=True)
    al(ax, 3.3, 3.6, 3.9, 3.6, lw=1.4, color=GRAY)
    al(ax, 6.7, 3.6, 7.4, 3.6, lw=1.4, color=GRAY)
    # 底部
    rk(ax, 0.5, 0.35, 4.85, 1.15, "程序：静态的、可以多个进程共享同一程序段\n(如两个浏览器窗口=同一程序段的两个进程)",
       fc=GRAY_L, ec=GRAY, fs=9.6, color=INK)
    rk(ax, 5.6, 0.35, 4.5, 1.15, "进程：动态的、有生命周期\n(创建→就绪→运行→…→终止)\nPCB是进程定身的“灵魂”——进程不会没有PCB",
       fc=PINK_L, ec=PINK, fs=9.6, color=INK)
    save_fig(fig, "ch2-01_process_entity")

# ============ ch2-02 PCB 结构 ============
def fig02():
    fig, ax = O.new_fig(11.2, 7.8, (0, 11.2), (0, 7.8))
    O.title(ax, "进程控制块 PCB 的内容（四个分区）",
            "PCB 常驻内存、由 OS 内核维护；进程＝程序段＋数据段＋PCB，PCB 决定了一个进程“是谁”")
    cells = [
        (0.5, 4.85, 5.0, 1.45, "① 进程描述信息", BLUE, BLUE_L,
         "· 进程标识符 PID（唯一）\n· 用户标识符 UID\n· 家族关系：父/子进程指针"),
        (6.0, 4.85, 5.0, 1.45, "② 进程控制和管理信息", GREEN, GREEN_L,
         "· 当前状态(就绪/运行/阻塞…)\n· 优先级\n· 时间片、已运行时间、等待时间"),
        (0.5, 2.75, 5.0, 1.45, "③ 资源分配清单", AMBER, AMBER_L,
         "· 程序段指针、数据段指针\n· 已打开文件(文件描述符表)\n· 已分配的设备/资源"),
        (6.0, 2.75, 5.0, 1.45, "④ 处理机现场信息(CPU现场)", PURPLE, PURPLE_L,
         "· 通用寄存器组的值\n· 程序计数器 PC 的值\n· 程序状态字 PSW、栈指针"),
    ]
    for x, y, w, h, head, ec, fc, body in cells:
        rk(ax, x, y, w, h, "", fc=fc, ec=ec, lw=1.8)
        t(ax, x + 0.2, y + h - 0.28, head, fs=12, bold=True, color=ec, ha="left", z=4)
        t(ax, x + 0.22, y + h / 2 - 0.28, body, fs=10, ha="left", va="center", z=4, ls=1.6)
    rk(ax, 0.5, 1.05, 10.5, 1.5, "", fc=GRAY_L, ec=GRAY, fs=11, bold=True)
    t(ax, 2.42, 2.28, "PCB 的组织方式", fs=11, bold=True, color=INK)
    t(ax, 0.7, 1.85, "链表方式：同一状态的进程用指针串成队列（就绪队列、阻塞队列、终止队列）——教科书与真题默认", fs=9.8, ha="left")
    t(ax, 0.7, 1.42, "索引方式：按状态建一张索引表，表项指向 PCB 地址（效率更高）", fs=9.8, ha="left")
    save_fig(fig, "ch2-02_pcb_structure")

# ============ ch2-03 五状态模型 ============
def fig03():
    fig, ax = O.new_fig(11.4, 7.0, (0, 11.4), (0, 7.0))
    O.title(ax, "进程五状态模型",
            "六条边：每条边记住【触发原因】+【主动/被动】——主动：进程自己请求；被动：由OS/硬件决定")
    el(ax, 1.25, 4.75, 2.0, 1.05, "创建\n(创建原语)", fc=PINK_L, ec=PINK, fs=10.5)
    el(ax, 3.85, 4.75, 1.9, 1.05, "就绪", fc=GREEN_L, ec=GREEN, fs=12, bold=True)
    el(ax, 6.45, 4.75, 1.9, 1.05, "运行", fc=BLUE_L, ec=BLUE, fs=12, bold=True)
    el(ax, 10.0, 4.75, 1.9, 1.05, "终止", fc=RED_L, ec=RED, fs=12, bold=True)
    el(ax, 5.35, 2.0, 2.4, 1.05, "阻塞 (等待)", fc=AMBER_L, ec=AMBER, fs=12, bold=True)
    # 箭头（无文字，标签用 t 手工定位防重叠）
    al(ax, 2.25, 4.75, 2.88, 4.75, "", color=PINK, lw=2.2)
    t(ax, 2.55, 4.26, "①创建完成：分配资源、初始化PCB→放入就绪队列\n【被动·OS执行】", fs=9.0, color=PINK, bg="white")
    al(ax, 4.82, 4.75, 5.48, 4.75, "", color=GREEN, lw=2.2)
    t(ax, 5.15, 5.42, "②被调度选中·获得CPU\n【被动】", fs=9.3, color=GREEN, bg="white")
    al(ax, 5.48, 4.22, 4.82, 4.22, "", color=GREEN, lw=2.2)
    t(ax, 5.15, 3.78, "③时间片用完 / 被更高优先级抢占\n【被动·OS】", fs=9.0, color=GREEN, bg="white")
    al(ax, 7.42, 4.75, 9.0, 4.75, "", color=RED, lw=2.2)
    t(ax, 8.2, 5.42, "④正常结束 / 异常退出\n【主动或OS强制】", fs=9.3, color=RED, bg="white")
    al(ax, 6.3, 4.2, 5.72, 2.58, "", color=AMBER, lw=2.2)
    t(ax, 7.7, 3.35, "⑤请求I/O、等待事件\n【主动·进程自己】", fs=9.3, color=AMBER, bg="white")
    ln(ax, 4.2, 2.0, 3.85, 2.0, color=AMBER, lw=2.2)
    al(ax, 3.85, 2.0, 3.85, 4.2, "", color=AMBER, lw=2.2)
    t(ax, 2.4, 3.15, "⑥事件发生(如I/O完成、被V唤醒)\n【阻塞→就绪：被动】", fs=9.3, color=AMBER, bg="white")
    rk(ax, 0.35, 0.25, 5.2, 0.72, "提示：阻塞和就绪的唯一区别：\n有没有拿到CPU？→ 阻塞：事件未完成，即使空闲也不能运行",
       fc=PURPLE_L, ec=PURPLE, fs=9.6)
    rk(ax, 5.85, 0.25, 5.2, 0.72, "记法：只有“就绪→运行”能进入运行；\n只有“运行→就绪/阻塞/终止”能离开运行",
       fc=AMBER_L, ec=AMBER, fs=9.6)
    save_fig(fig, "ch2-03_five_states")

# ============ ch2-04 七状态模型 ============
def fig04():
    fig, ax = O.new_fig(11.6, 7.6, (0, 11.6), (0, 7.6))
    O.title(ax, "进程七状态模型（五状态 + 挂起suspend）",
            "挂起=进程被换出到外存(暂不参与调度)；由中级调度(挂起/激活原语)管理；“就绪挂起/阻塞挂起”按事件状态再细分")
    rk(ax, 0.3, 0.9, 5.3, 4.4, "", fc="#F0FDFA", ec=TEAL, lw=2.0)
    rk(ax, 6.1, 0.9, 5.2, 4.4, "", fc="#F5F3FF", ec=PURPLE, lw=2.0)
    t(ax, 0.55, 1.05, "内存（活跃）", fs=12, bold=True, color=TEAL, ha="left")
    t(ax, 6.35, 1.05, "外存（被挂起）", fs=12, bold=True, color=PURPLE, ha="left")
    # 顶部 新建/终止
    el(ax, 0.9, 6.15, 1.7, 0.75, "新建\n(创建)", fc=PINK_L, ec=PINK, fs=10)
    el(ax, 4.0, 6.15, 1.7, 0.75, "终止", fc=RED_L, ec=RED, fs=10.5, bold=True)
    # 状态
    el(ax, 1.5, 4.7, 1.7, 0.95, "活动就绪", fc=GREEN_L, ec=GREEN, fs=10.5, bold=True)
    el(ax, 4.0, 4.7, 2.0, 0.95, "运行", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
    el(ax, 2.2, 2.4, 2.3, 0.95, "活动阻塞", fc=AMBER_L, ec=AMBER, fs=10.5, bold=True)
    el(ax, 8.9, 3.5, 2.0, 0.95, "静止就绪", fc=GREEN_L, ec=PURPLE, fs=10.5, bold=True)
    el(ax, 8.9, 1.9, 2.3, 0.95, "静止阻塞", fc=AMBER_L, ec=PURPLE, fs=10.5, bold=True)
    # 基本转换
    al(ax, 1.15, 5.75, 1.35, 4.3, "", color=PINK, lw=1.9)
    t(ax, 2.05, 5.35, "①创建完成【被动】", fs=8.6, color=PINK, bg="white")
    al(ax, 2.4, 4.7, 2.95, 4.7, "", color=GREEN, lw=1.9)
    t(ax, 2.68, 5.12, "②被调度\n[被动]", fs=8.6, color=GREEN, bg="white", ls=1.2)
    al(ax, 2.95, 4.3, 2.4, 4.3, "", color=GREEN, lw=1.9)
    t(ax, 2.68, 3.88, "③时间片用完/抢占", fs=8.6, color=GREEN, bg="white")
    al(ax, 4.0, 5.18, 4.0, 5.72, "", color=RED, lw=1.9)
    t(ax, 4.62, 5.45, "④结束【主动】", fs=8.6, color=RED, bg="white", ha="left")
    al(ax, 3.55, 4.22, 2.5, 2.95, "", color=AMBER, lw=1.9)
    t(ax, 4.15, 3.45, "⑤等待事件【主动】", fs=8.6, color=AMBER, bg="white")
    al(ax, 1.7, 2.87, 1.42, 4.2, "", color=AMBER, lw=1.9)
    t(ax, 0.65, 3.45, "⑥事件发生【被动】", fs=8.6, color=AMBER, bg="white", ha="left")
    # 挂起/激活 就绪对
    al(ax, 2.4, 4.42, 8.05, 3.68, "", color=PURPLE, lw=1.9)
    t(ax, 5.85, 4.28, "⑦挂起(换出到外存)\n【中级调度】", fs=8.6, color=PURPLE, bg="white", ls=1.25)
    al(ax, 8.05, 3.32, 2.4, 4.18, "", color=PURPLE, lw=1.9, ls="--")
    t(ax, 4.9, 3.62, "⑧激活(换回内存)", fs=8.6, color=PURPLE, bg="white")
    # 挂起/激活 阻塞对
    al(ax, 3.35, 2.5, 7.7, 2.12, "", color=PURPLE, lw=1.9)
    t(ax, 5.55, 2.42, "⑨挂起(事件未完也换出)", fs=8.6, color=PURPLE, bg="white")
    al(ax, 7.7, 1.78, 3.35, 2.26, "", color=PURPLE, lw=1.9, ls="--")
    t(ax, 5.55, 1.72, "⑩激活→活动阻塞", fs=8.6, color=PURPLE, bg="white")
    # 静止阻塞 → 静止就绪
    al(ax, 8.9, 2.42, 8.9, 2.98, "", color=AMBER, lw=1.9)
    t(ax, 9.4, 2.7, "11。事件发生【被动】", fs=8.6, color=AMBER, bg="white", ha="left")
    # 新建→静止就绪(可选)
    al(ax, 1.3, 5.75, 8.3, 3.85, "", color=GRAY, lw=1.6, ls=":")
    t(ax, 4.9, 4.9, "创建即挂起(可选)", fs=8.6, color=GRAY, bg="white")
    rk(ax, 0.3, 0.25, 10.95, 0.55, "为什么引入挂起：①内存不足/负载太重(换出轻装)  ②父进程考察、调试子进程  ③调节系统负载均衡  ④断电恢复等故障处理",
       fc=AMBER_L, ec=AMBER, fs=9.4)
    save_fig(fig, "ch2-04_seven_states")

# ============ ch2-05 禁止的错误转换 ============
def fig05():
    fig, ax = O.new_fig(11.6, 7.2, (0, 11.6), (0, 7.2))
    O.title(ax, "状态转换·易错辨析（这些“捷径”都不存在）",
            "左边是“你以为可以”的箭头（×），右边是“为什么不行”")
    el(ax, 1.6, 3.9, 2.1, 1.0, "就绪", fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    el(ax, 4.3, 5.0, 1.9, 1.0, "运行", fc=BLUE_L, ec=BLUE, fs=11, bold=True)
    el(ax, 4.3, 2.7, 2.3, 1.0, "阻塞(等待)", fc=AMBER_L, ec=AMBER, fs=11, bold=True)
    el(ax, 8.0, 5.0, 1.9, 1.0, "终止", fc=RED_L, ec=RED, fs=11, bold=True)
    el(ax, 2.0, 6.3, 1.9, 0.9, "创建", fc=PINK_L, ec=PINK, fs=10.5)
    # 合法转换(浅色)
    al(ax, 2.1, 6.0, 1.7, 4.5, "创建→就绪(合法的)", color=GRAY, fs=8.6, dx=1.15, dy=0.12)
    al(ax, 2.75, 3.9, 3.3, 4.75, "就绪→运行\n(合法)", color=GRAY, fs=8.6, dx=-1.65, dy=0.1)
    al(ax, 4.3, 4.45, 4.3, 3.85, "", color=GRAY, both=True, lw=1.2)
    t(ax, 4.3, 4.12, "运行→就绪(合法)\n运行→阻塞(合法)", fs=8.6, color=GRAY, bg="white")
    # 错误箭头
    al(ax, 4.3, 3.3, 4.3, 4.4, "① 阻塞→运行 ?!", color=RED, fs=10, ls="--", lw=2.4, dx=2.2, dy=0.1, ms=20)
    t(ax, 3.15, 1.9, "×", fs=20, bold=True, color=RED)
    al(ax, 1.6, 4.5, 3.9, 4.9, "② 就绪→阻塞 ?!", color=RED, fs=10, ls="--", lw=2.4, dx=-2.35, dy=-0.5, ms=20)
    t(ax, 2.7, 5.55, "×", fs=20, bold=True, color=RED)
    al(ax, 4.3, 5.6, 1.9, 4.6, "③ 创建→运行 ?!", color=RED, fs=10, ls="--", lw=2.4, dx=-1.9, dy=-0.2, ms=20)
    t(ax, 3.0, 6.9, "×", fs=20, bold=True, color=RED)
    al(ax, 8.0, 4.4, 2.2, 4.2, "④ 终止→就绪 复活 ?!", color=RED, fs=10, ls="--", lw=2.4, dx=0.0, dy=-0.9, ms=20)
    t(ax, 6.3, 4.0, "×", fs=20, bold=True, color=RED)
    # 右侧解释
    rk(ax, 8.9, 0.4, 2.55, 6.3, "为什么这些转换不存在？", fc=RED_L, ec=RED, fs=11.5, bold=True)
    expl = [
        "① 阻塞→运行：阻塞进程「事件没等到」，即使CPU空闲也不能运行；必须等事件发生→就绪，再被调度",
        "② 就绪→阻塞：就绪进程没拿到CPU，不可能「正在请求I/O」；只有运行中的进程才能因等待转入阻塞",
        "③ 创建→运行：创建完成后先放入就绪队列排队等待调度，不能一步到位",
        "④ 终止→就绪/运行：进程终止后PCB被回收「死亡」，复活必须重新调用创建原语",
        "→ 记忆：从「运行」出发的转换最丰富（→就绪/→阻塞/→终止）；进入「运行」只有一条路(就绪→运行)",
    ]
    for i, e in enumerate(expl):
        t(ax, 9.05, 5.75 - i * 1.12, e, fs=9.2, ha="left", va="top", z=4, ls=1.45)
    save_fig(fig, "ch2-05_forbidden_transitions")

# ============ ch2-06 进程控制原语 ============
def fig06():
    fig, ax = O.new_fig(11.6, 8.8, (0, 11.6), (0, 8.8))
    O.title(ax, "五种进程控制原语：做什么、何时触发、改变什么状态",
            "原语=不可中断的原子操作（用关中断实现）；进程控制=用原语实施状态转换；一切切换都发生在核心态")
    data = [
        ("创建", PINK, PINK_L, "触发：\n终端登录 / 作业调度\n提供服务 / 应用请求",
         "① 申请空白PCB\n② 分配内存等资源\n③ 初始化PCB(装入程序)\n④ 插入就绪队列",
         "转换：创建 → 就绪\n易错：创建后是“就绪”而非“运行”"),
        ("撤销", RED, RED_L, "触发：\n正常结束 / 异常退出\n外界干预(强制终止)",
         "① 从PCB表删除\n② 递归撤销其全部子孙进程\n③ 归还资源, 回收PCB",
         "转换：运行/就绪/阻塞 → 终止\n易错：撤销父进程必须撤销子孙"),
        ("阻塞", AMBER, AMBER_L, "触发：\n运行中请求I/O\n或等待某事件(自己主动)",
         "① 保存现场\n② 改为阻塞态, 移出就绪队列\n③ 转入阻塞队列等事件",
         "转换：运行 → 阻塞(主动)\n易错：阻塞后CPU让给别人"),
        ("唤醒", GREEN, GREEN_L, "触发：\n事件发生(如I/O完成)\n被V唤醒(被动)",
         "① 从阻塞队列取出\n② 改为就绪态\n③ 插入就绪队列",
         "转换：阻塞 → 就绪(被动)\n易错：阻塞与唤醒必须成对出现"),
        ("切换(调度)", BLUE, BLUE_L, "触发：\n时间片用完 / 更高优先\n级到达 / 结束或阻塞",
         "① 保存原进程运行现场\n② 更新其PCB状态\n③ 选新进程, 恢复其现场",
         "转换：就绪 <-> 运行\n易错：切换一定发生在核心态"),
    ]
    x0, w, gap = 0.45, 2.1, 0.12
    for i, (name, ec, fc, trig, steps, conv) in enumerate(data):
        x = x0 + i * (w + gap)
        bk(ax, x + w / 2, 7.35, w, 0.75, name, fc=fc, ec=ec, fs=13, bold=True)
        t(ax, x + w / 2, 6.72, "触发时机", fs=10, bold=True, color=ec)
        rk(ax, x, 5.4, w, 1.12, trig.strip(), fc="#F8FAFC", ec=GRAY, fs=8.8, color=INK)
        t(ax, x + w / 2, 5.05, "执行步骤", fs=10, bold=True, color=ec)
        rk(ax, x, 3.35, w, 1.5, steps.strip(), fc=fc, ec=ec, fs=8.8, color=INK)
        t(ax, x + w / 2, 3.0, "状态变化", fs=10, bold=True, color=ec)
        rk(ax, x, 1.3, w, 1.28, conv.strip(), fc=AMBER_L, ec=AMBER, fs=8.8, color=INK)
    rk(ax, 0.45, 0.55, 10.92, 0.42, "以上五种原语都必须在核心态执行；原语用关中断保证原子性", fc=GRAY_L, ec=GRAY, fs=9.6)
    save_fig(fig, "ch2-06_process_primitives")

# ============ ch2-07 进程通信概览 ============
def fig07():
    fig, ax = O.new_fig(11.6, 7.8, (0, 11.6), (0, 7.8))
    O.title(ax, "进程通信的三种方式",
            "各进程地址空间相互独立——不能直接改对方的变量，必须借助OS提供的通信机制")
    # 1 共享存储
    rk(ax, 0.35, 3.5, 3.55, 3.0, "", fc=BLUE_L, ec=BLUE, fs=12.5, bold=True)
    t(ax, 2.125, 6.2, "① 共享存储", fs=12.5, bold=True, color=BLUE)
    bk(ax, 1.0, 5.3, 1.1, 0.9, "进程A", fc="#F8FAFC", ec=GRAY, fs=10)
    bk(ax, 3.15, 5.3, 1.1, 0.9, "进程B", fc="#F8FAFC", ec=GRAY, fs=10)
    rc(ax, 1.4, 4.35, 1.6, 0.8, "共享区\n(数据结构/存储区)", fc=AMBER_L, ec=AMBER, fs=8.2, lw=1.4)
    al(ax, 1.55, 4.87, 1.95, 4.68, "", color=GRAY, lw=1.2)
    al(ax, 2.75, 4.87, 2.35, 4.68, "", color=GRAY, lw=1.2)
    t(ax, 2.125, 3.85, "低级：基于数据结构共享\n—— 需OS辅助\n高级：基于存储区共享\n—— 直接读写、速度快", fs=8.4, ha="center", ls=1.42)
    # 2 消息传递
    rk(ax, 4.18, 3.5, 3.6, 3.0, "", fc=GREEN_L, ec=GREEN, fs=12.5, bold=True)
    t(ax, 5.98, 6.2, "② 消息传递", fs=12.5, bold=True, color=GREEN)
    bk(ax, 4.8, 5.3, 1.1, 0.9, "进程A", fc="#F8FAFC", ec=GRAY, fs=10)
    bk(ax, 6.95, 5.3, 1.1, 0.9, "进程B", fc="#F8FAFC", ec=GRAY, fs=10)
    bk(ax, 5.85, 6.0, 2.2, 0.55, "信箱(间接通信)", fc=PURPLE_L, ec=PURPLE, fs=8.6)
    bk(ax, 5.85, 4.5, 1.2, 0.75, "消息", fc=PINK_L, ec=PINK, fs=9.5, bold=True)
    al(ax, 5.0, 5.28, 5.35, 5.75, "", color=PURPLE, lw=1.2, ls=":")
    al(ax, 6.75, 5.28, 6.45, 5.75, "", color=PURPLE, lw=1.2, ls=":")
    al(ax, 5.3, 4.98, 5.62, 4.55, "A发消息", color=PINK, fs=8.2, lw=1.3)
    al(ax, 6.2, 4.55, 6.55, 4.98, "B收消息", color=PINK, fs=8.2, lw=1.3)
    t(ax, 5.95, 3.85, "直接通信：指名道姓(发到指定进程)\n间接通信：经信箱传递(中间实体)", fs=8.6, ha="center", ls=1.42)
    # 3 管道
    rk(ax, 8.05, 3.5, 3.25, 3.0, "", fc=AMBER_L, ec=AMBER, fs=12.5, bold=True)
    t(ax, 9.675, 6.2, "③ 管道", fs=12.5, bold=True, color=AMBER)
    bk(ax, 8.6, 5.3, 1.1, 0.9, "进程A", fc="#F8FAFC", ec=GRAY, fs=10)
    bk(ax, 10.4, 5.3, 1.1, 0.9, "进程B", fc="#F8FAFC", ec=GRAY, fs=10)
    rc(ax, 9.45, 4.35, 1.35, 0.75, "管道\n(缓冲区)", fc=TEAL_L, ec=TEAL, fs=8.6)
    al(ax, 9.15, 4.95, 9.72, 4.62, "", color=TEAL, lw=1.3)
    t(ax, 8.95, 4.85, "写", fs=8.6, color=TEAL, bold=True)
    al(ax, 10.4, 4.62, 10.1, 4.95, "", color=TEAL, lw=1.3)
    t(ax, 10.7, 4.85, "读", fs=8.6, color=TEAL, bold=True)
    t(ax, 9.675, 3.8, "半双工: 数据单向流动\n读走即删, 先来先走(FIFO)\n写满阻塞写者, 读空阻塞读者", fs=8.4, ha="center", ls=1.42)
    rk(ax, 0.35, 0.35, 10.95, 2.6, "", fc=GRAY_L, ec=GRAY, fs=12, bold=True)
    t(ax, 5.825, 2.72, "三者一句话记忆", fs=12, bold=True, color=INK)
    rows = [
        ("共享存储", "把钥匙给你，你自己开门进屋——快，但要自己保证互斥(锁)", BLUE),
        ("消息传递", "写信寄信——有中间人(OS)传递格式化的消息(消息头+正文)，安全但慢", GREEN),
        ("管道(也属于共享存储)", "接一根水管——一方在管口灌水(写)，一方在管口接水(读)；半双工，要双向就接两根管", AMBER),
    ]
    for i, (k, v, c) in enumerate(rows):
        yy = 2.25 - i * 0.65
        t(ax, 0.6, yy, k, fs=10, bold=True, color=c, ha="left")
        t(ax, 3.8, yy, v, fs=9.6, ha="left")
        ln(ax, 0.55, yy - 0.14, 0.55, yy + 0.16, color=c, lw=2.4)
    save_fig(fig, "ch2-07_ipc_overview")

# ============ ch2-08 管道 ============
def fig08():
    fig, ax = O.new_fig(11.6, 6.8, (0, 11.6), (0, 6.8))
    O.title(ax, "管道通信的原理与四个特性",
            "管道=内存中的固定大小缓冲区(特殊文件)，读端与写端分别由两个进程使用；本质是“生产者-消费者”")
    bk(ax, 1.5, 3.7, 2.0, 1.2, "写进程A\n(生产者)", fc=BLUE_L, ec=BLUE, fs=11, bold=True)
    bk(ax, 10.1, 3.7, 2.0, 1.2, "读进程B\n(消费者)", fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    # 管道
    rc(ax, 4.6, 2.9, 3.4, 2.2, "", fc=TEAL_L, ec=TEAL, lw=2.0)
    t(ax, 6.3, 4.8, "管道（固定大小缓冲区，如64KB）", fs=10.5, bold=True, color=TEAL)
    slots = ["已写", "已写", "已写（写满→写者阻塞）", "空", "空（读空→读者阻塞）", "空"]
    for i, s in enumerate(slots):
        col = TEAL if "已写" in s else "#FFFFFF"
        rc(ax, 4.75 + i * 0.52, 3.2, 0.45, 0.85, "", fc=col, ec=TEAL, lw=1.2)
        t(ax, 4.97 + i * 0.52, 2.75, str(i + 1), fs=8, color=TEAL, bold=True)
    al(ax, 3.55, 4.2, 4.55, 4.2, "write 写", color=BLUE, fs=10, lw=1.8)
    al(ax, 8.05, 4.2, 9.05, 4.2, "read 读", color=GREEN, fs=10, lw=1.8)
    al(ax, 4.6, 4.2, 3.7, 4.5, "", color=BLUE, lw=1.0)
    t(ax, 6.3, 2.55, "数据先进先出：从头读，读走即删（数据被“消费”后消失，不能回读）", fs=9.6)
    rk(ax, 0.35, 0.55, 10.95, 1.95, "", fc=AMBER_L, ec=AMBER, fs=12, bold=True)
    t(ax, 5.825, 2.3, "管道四大特性（逢考必出）", fs=12, bold=True, color=AMBER)
    feats = [
        "① 半双工：数据只能单向流动；要双向通信必须建立两根管道（A→B 一根，B→A 一根）",
        "② 写满阻塞写者：管道缓冲区满，写进程的write操作阻塞(等读者取走数据)",
        "③ 读空阻塞读者：管道缓冲区空，读进程的read操作阻塞(等写者写入数据)",
        "④ 互斥访问：读写双方对管道的访问必须互斥（管道是临界资源）——由OS保证",
    ]
    for i, f in enumerate(feats):
        t(ax, 0.6, 1.95 - i * 0.36, f, fs=9.6, ha="left")
    save_fig(fig, "ch2-08_pipe")

# ============ ch2-09 线程资源视图 ============
def fig09():
    fig, ax = O.new_fig(11.6, 7.8, (0, 11.6), (0, 7.8))
    O.title(ax, "线程的资源视图：同进程线程“共享什么、独有什么”",
            "进程=资源分配的基本单位(拥有地址空间等)；线程=CPU调度的基本单位(只保留一份“运行现场”)")
    rk(ax, 0.35, 1.6, 7.0, 4.9, "", fc="#F0FDFA", ec=TEAL, lw=2.2)
    t(ax, 3.85, 6.25, "进程 P（资源容器）", fs=13, bold=True, color=TEAL)
    rk(ax, 0.6, 4.2, 3.3, 1.85, "所有线程共享：", fc=TEAL_L, ec=TEAL, fs=11.5, bold=True)
    shared = ["· 地址空间(代码段/数据段/堆)", "· 全局变量", "· 已打开文件(文件描述符表)", "· 打开的设备、信号量等资源"]
    for i, s in enumerate(shared):
        t(ax, 0.75, 5.45 - i * 0.42, s, fs=9.8, ha="left")
    threads = [("线程1", 1.05), ("线程2", 3.15), ("线程3", 5.25)]
    for name, x in threads:
        bk(ax, x + 0.85, 2.5, 1.7, 1.35, "", fc=BLUE_L, ec=BLUE, lw=1.8)
        t(ax, x + 0.85, 3.55, name, fs=10.5, bold=True, color=BLUE)
        for i, s in enumerate(["线程ID", "程序计数器PC", "寄存器组", "栈"]):
            t(ax, x + 0.85, 3.1 - i * 0.22, s, fs=8.0, color=INK)
    t(ax, 3.85, 2.0, "三个线程“各自为政”的执行状态，但共用一段代码、一份全局数据", fs=9.4)
    rk(ax, 7.65, 1.6, 3.6, 4.9, "", fc=PURPLE_L, ec=PURPLE, fs=12, bold=True)
    t(ax, 9.45, 6.32, "线程独有的资源", fs=12, bold=True, color=PURPLE)
    own = [
        ("线程ID", "内核区分每个线程的编号"),
        ("PC程序计数器", "各自执行到哪一条指令"),
        ("寄存器组", "运算时各自的临时数据"),
        ("栈", "函数调用、局部变量——不能共享"),
    ]
    for i, (k, v) in enumerate(own):
        rk(ax, 7.85, 5.25 - i * 0.95, 3.2, 0.8, f"{k}\n{v}", fc="#FFFFFF", ec=PURPLE, fs=9.4)
    rk(ax, 0.35, 0.35, 10.9, 0.95, "升华：线程切换只换“现场”(PC/寄存器/栈等)，不换“房屋”(地址空间)——所以线程切换比进程切换开销小得多；同一进程线程间可直接用全局变量通信，无需IPC",
       fc=AMBER_L, ec=AMBER, fs=9.8)
    save_fig(fig, "ch2-09_thread_sharing")

# ============ ch2-10 线程映射 ============
def fig10():
    fig, ax = O.new_fig(11.7, 7.6, (0, 11.7), (0, 7.6))
    O.title(ax, "用户级线程ULT 与 内核级线程KLT：三种映射模型",
            "ULT：线程管理在用户态完成(对内核透明)；KLT：内核能感知并调度每个线程")
    panels = [
        ("多对一 Many-to-One", 1.95, ["ULT 用户级线程", 3], ["KLT 内核级线程", 1],
         "内核只看到1个线程：\n一个ULT阻塞→整个进程阻塞★\n切换在用户态(开销小)\n不能利用多核并行"),
        ("一对一 One-to-One", 5.85, ["ULT 用户级线程", 3], ["KLT 内核级线程", 3],
         "每个ULT对应一个KLT：\n一个阻塞不影响别的线程\n可多核并行(真正并行)\n切换要进核心态(开销大)\n如Windows、Linux"),
        ("多对多 Many-to-Many", 9.75, ["ULT 用户级线程", 4], ["KLT 内核级线程", 2],
         "m个ULT ≤ n个KLT：\n兼得多对一和一对一的优点\n内核调度KLT→并行与响应兼顾"),
    ]
    for name, cx, (lblu, nu), (lblk, nk), note in panels:
        rk(ax, cx - 1.7, 0.5, 3.4, 6.0, "", fc="#F8FAFC", ec=GRAY, lw=1.6)
        t(ax, cx, 6.3, name, fs=11.5, bold=True, color=INK)
        t(ax, cx, 5.75, lblu, fs=9.8, bold=True, color=BLUE)
        for i in range(nu):
            ci(ax, cx - (nu - 1) * 0.42 + i * 0.84, 5.2, 0.33, "T", fc=BLUE_L, ec=BLUE, fs=9)
        t(ax, cx, 4.55, lblk, fs=9.8, bold=True, color=TEAL)
        for i in range(nk):
            ci(ax, cx - (nk - 1) * 0.42 + i * 0.84, 4.0, 0.33, "K", fc=TEAL_L, ec=TEAL, fs=9)
        # 映射线
        for i in range(min(nu, nk)):
            ln(ax, cx - (nu - 1) * 0.42 + i * 0.84, 5.15, cx - (nk - 1) * 0.42 + i * 0.84, 4.05,
               color=GRAY, lw=1.4)
        rk(ax, cx - 1.55, 0.75, 3.1, 2.2, note, fc=AMBER_L, ec=AMBER, fs=9.4)
    rk(ax, 0.35, 0.25, 11.0, 0.42, "★考点：用户级线程模型中，“一个线程阻塞→整个进程被阻塞”的坑；以及“两级混合模型(用户层+LWP)”的推广",
       fc=RED_L, ec=RED, fs=9.4)
    save_fig(fig, "ch2-10_thread_mapping")

# ============ ch2-11 三级调度 ============
def fig11():
    fig, ax = O.new_fig(11.6, 7.6, (0, 11.6), (0, 7.6))
    O.title(ax, "处理机调度的三个层次",
            "高级调度≈从外存进内存；中级调度≈内存与外存之间(挂起/激活)；低级调度≈从就绪队列到CPU")
    # 主链
    rk(ax, 0.4, 4.7, 2.6, 1.1, "后备作业队列\n(外存)", fc=GRAY_L, ec=GRAY, fs=10)
    al(ax, 3.05, 5.25, 4.1, 5.25, "高级调度\n(作业调度)\n调入记忆·频率最低", color=BLUE, fs=8.8, dy=0.58)
    rk(ax, 4.15, 4.7, 2.7, 1.1, "就绪队列\n(内存)", fc=GREEN_L, ec=GREEN, fs=10)
    al(ax, 6.9, 5.25, 7.85, 5.25, "低级调度\n(进程调度)\n频率最高·真·调度", color=PINK, fs=8.8, dy=0.58)
    rk(ax, 7.9, 4.7, 3.3, 1.1, "CPU(处理机)", fc=PINK_L, ec=PINK, fs=12, bold=True)
    # 中级
    rk(ax, 4.15, 2.3, 2.7, 1.1, "就绪挂起/阻塞挂起\n(外存)", fc=PURPLE_L, ec=PURPLE, fs=9.4)
    rk(ax, 0.4, 2.3, 3.3, 1.1, "运行/活动就绪/活动阻塞\n(内存)", fc=AMBER_L, ec=AMBER, fs=9.4)
    al(ax, 2.0, 4.62, 2.0, 3.45, "", color=GRAY, lw=1.4, both=True)
    t(ax, 2.1, 4.05, "（程序段/数据段\n在内存·外存之间迁移）", fs=8.8, color=GRAY, ha="center")
    al(ax, 4.5, 3.45, 3.75, 3.45, "换出", color=PURPLE, fs=9.2, lw=1.8, dy=0.35, dx=0.5)
    al(ax, 6.6, 3.45, 5.55, 3.45, "挂起/激活(换入)\n【中级调度·内存调度】", color=PURPLE, fs=9.2, lw=1.8, dy=0.75, dx=0.2)
    ln(ax, 7.0, 3.45, 6.9, 3.45, color=PURPLE, lw=1.8)
    rk(ax, 0.4, 0.55, 5.2, 1.35, "只有低级调度真正把CPU分给进程\n(其余两者只管进程“进场/出场”)",
       fc=GREEN_L, ec=GREEN, fs=9.8)
    rk(ax, 5.95, 0.55, 5.25, 1.35, "触发频率：高级(低频·几分钟一次) ＜ 中级(可高可低) ＜ 低级(狂快·毫秒级)",
       fc=BLUE_L, ec=BLUE, fs=9.8)
    save_fig(fig, "ch2-11_scheduling_levels")

# ============ ch2-12 FCFS 与 SJF ============
def fig12():
    fig, ax = O.new_fig(11.6, 6.6, (0, 16), (0, 6.6))
    O.title(ax, "例题：FCFS 与 SJF（非抢占）甘特图",
            "P1(到达0, 服务7)  P2(到达2, 服务4)  P3(到达4, 服务1)  P4(到达5, 服务4)", fs=15)
    pc = proc_colors()
    # 到达标记
    for xt, lbl in [(2, "P2到达\nt=2"), (4, "P3到达\nt=4"), (5, "P4到达\nt=5")]:
        ln(ax, xt, 5.6, xt, 5.05, color=GRAY, lw=1.2, ls=":")
        t(ax, xt, 5.78, lbl, fs=8.8, color=GRAY, bold=True)
    # FCFS
    t(ax, 0.15, 4.72, "FCFS", fs=12, bold=True, color=BLUE, ha="left")
    rk(ax, 0.45, 4.35, 15.1, 0.72, "", fc=GRAY_L, ec=GRAY, lw=1.2)
    fcfs = [("P1", 0, 7, BLUE, BLUE_L), ("P2", 7, 4, GREEN, GREEN_L),
            ("P3", 11, 1, AMBER, AMBER_L), ("P4", 12, 4, PURPLE, PURPLE_L)]
    for name, st, ln_, ec, fc in fcfs:
        rc(ax, st, 4.35, ln_, 0.72, f"{name}" + (f"   服务{ln_}→完成{st + ln_}" if ln_ > 1.2 else ""),
           fc=fc, ec=ec, fs=9.6, bold=True)
    t(ax, 8.0, 4.0, "完成时刻: 7 / 11 / 12 / 16      周转时间: 7 / 9 / 8 / 11", fs=9.6, color=BLUE, bold=True)
    # SJF
    t(ax, 0.15, 3.3, "SJF", fs=12, bold=True, color=GREEN, ha="left")
    rk(ax, 0.45, 2.93, 15.1, 0.72, "", fc=GRAY_L, ec=GRAY, lw=1.2)
    sjf = [("P1", 0, 7, BLUE, BLUE_L), ("P3", 7, 1, AMBER, AMBER_L),
           ("P2", 8, 4, GREEN, GREEN_L), ("P4", 12, 4, PURPLE, PURPLE_L)]
    for name, st, ln_, ec, fc in sjf:
        rc(ax, st, 2.93, ln_, 0.72, f"{name}" + (f"   服务{ln_}→完成{st + ln_}" if ln_ > 1.2 else ""),
           fc=fc, ec=ec, fs=9.6, bold=True)
    t(ax, 8.0, 2.58, "完成时刻: 7 / 8 / 12 / 16      周转时间: 7 / 4 / 10 / 11", fs=9.6, color=GREEN, bold=True)
    # 轴
    for i in range(17):
        ln(ax, i, 2.1, i, 2.28, color="#C7CBD1", lw=1.0)
        t(ax, i, 1.72, str(i), fs=9, color=GRAY)
    ln(ax, 0, 2.1, 16, 2.1, color=INK, lw=1.6)
    t(ax, 16.2, 1.72, "t", fs=10, color=INK)
    # 比较
    rk(ax, 0.45, 0.25, 7.2, 1.15, "FCFS：P2/P3/P4 都排队等 P1(长作业先行)\n平均周转8.75  平均带权周转3.50",
       fc=BLUE_L, ec=BLUE, fs=9.6)
    rk(ax, 8.1, 0.25, 7.0, 1.15, "SJF：谁服务时间短谁先跑(P1等P3)，平均周转更优\n平均周转8.00  平均带权周转2.5625",
       fc=GREEN_L, ec=GREEN, fs=9.6)
    save_fig(fig, "ch2-12_gantt_fcfs_sjf")

# ============ ch2-13 HRRN 与 RR ============
def fig13():
    fig, ax = O.new_fig(11.6, 6.8, (0, 16), (0, 6.8))
    O.title(ax, "例题：HRRN 与 RR(q=1) 甘特图（同组数据）",
            "P1(0,7) P2(2,4) P3(4,1) P4(5,4)；RR约定：同一时刻先入队者在前(新到达进程先入队，被抢占进程后入队)", fs=13.5)
    # HRRN
    t(ax, 0.15, 5.55, "HRRN", fs=12, bold=True, color=AMBER, ha="left")
    hr = [("P1", 0, 7, BLUE, BLUE_L), ("P3", 7, 1, AMBER, AMBER_L),
          ("P2", 8, 4, GREEN, GREEN_L), ("P4", 12, 4, PURPLE, PURPLE_L)]
    rk(ax, 0.45, 4.85, 15.1, 0.72, "", fc=GRAY_L, ec=GRAY, lw=1.2)
    for name, st, ln_, ec, fc in hr:
        rc(ax, st, 4.85, ln_, 0.72, f"{name}", fc=fc, ec=ec, fs=9.6, bold=True)
    t(ax, 2.2, 4.5, "t=7时响应比: P2·9/4=2.25  P3·4/1=4.0  P4·6/4=1.5 → 选P3", fs=9.0, color=AMBER, ha="left")
    t(ax, 2.2, 4.2, "t=8时响应比: P2·10/4=2.5  P4·7/4=1.75 → 选P2", fs=9.0, color=AMBER, ha="left")
    # RR
    t(ax, 0.15, 3.55, "RR", fs=12, bold=True, color=RED, ha="left")
    rk(ax, 0.45, 2.85, 15.1, 0.72, "", fc=GRAY_L, ec=GRAY, lw=1.2)
    rr_seq = [("P1", 0), ("P1", 1), ("P2", 2), ("P1", 3), ("P2", 4), ("P3", 5),
              ("P1", 6), ("P4", 7), ("P2", 8), ("P1", 9), ("P4", 10), ("P2", 11),
              ("P1", 12), ("P4", 13), ("P1", 14), ("P4", 15)]
    cm = {"P1": BLUE, "P2": GREEN, "P3": AMBER, "P4": PURPLE}
    cl = {"P1": BLUE_L, "P2": GREEN_L, "P3": AMBER_L, "P4": PURPLE_L}
    for name, st in rr_seq:
        rc(ax, st, 2.85, 1.0, 0.72, name, fc=cl[name], ec=cm[name], fs=9, bold=True)
    t(ax, 0.2, 2.45, "每格=1个时间单位(时间片q=1)，共16格;  完成时刻: P3=6  P2=12  P1=15  P4=16", fs=9.2, color=RED, bold=True, ha="left")
    # 轴
    for i in range(17):
        ln(ax, i, 2.1, i, 2.28, color="#C7CBD1", lw=1.0)
        t(ax, i, 1.72, str(i), fs=9, color=GRAY)
    ln(ax, 0, 2.1, 16, 2.1, color=INK, lw=1.6)
    t(ax, 16.2, 1.72, "t", fs=10, color=INK)
    rk(ax, 0.45, 0.25, 7.2, 1.15, "HRRN: 与SJF调度结果相同(本例)\n平均周转8.00  平均带权周转2.5625",
       fc=AMBER_L, ec=AMBER, fs=9.6)
    rk(ax, 8.1, 0.25, 7.0, 1.15, "RR(q=1): 响应最快, 但长进程P1被频繁切换\n平均周转9.50  平均带权周转2.35",
       fc=RED, ec=RED, fs=9.6, color=INK)
    save_fig(fig, "ch2-13_gantt_hrrn_rr")

# ============ ch2-14 六算法对比 ============
def fig14():
    fig, ax = O.new_fig(11.9, 8.7, (0, 11.9), (0, 8.7))
    O.title(ax, "六种调度算法一览（小示意+一句话特征）",
            "按“谁先、谁短、谁比值高、轮流、谁重要、多级”六个思路记忆；每种算法的甘特图计算见前面的例题", fs=15)
    panels = [
        # (标题, 颜色, 示意段, 特征, 缺点)
        ("FCFS 先来先服务", BLUE, [("A", 0, 4, BLUE), ("B", 4, 2, GREEN), ("C", 6, 3, AMBER), ("D", 9, 2, PURPLE)],
         "按到达先后排队，不可剥夺；\n实现最简单、公平；但短作业吃亏", "对短作业不利；不抢占"),
        ("SJF 短作业优先", GREEN, [("A短", 6, 2, GREEN), ("C", 4, 3, AMBER), ("D", 2, 2, PURPLE), ("B长", 0, 4, BLUE)],
         "服务时间短者先运行(非抢占)；\n平均等待/平均周转最优(数学可证)", "需预知运行时间；长作业饥饿"),
        ("HRRN 高响应比优先", AMBER, [("A", 0, 4, BLUE), ("B", 4, 2, GREEN), ("C", 6, 3, AMBER), ("D", 9, 2, PURPLE)],
         "响应比=(等待+要求服务)/要求服务；\n兼顾FCFS的公平与SJF的高效", "每次调度要计算比值，小开销"),
        ("RR 时间片轮转", RED, [("A", 0, 1.2, BLUE), ("B", 1.2, 1.2, GREEN), ("C", 2.4, 1.2, AMBER), ("A", 3.6, 1.2, BLUE), ("B", 4.8, 1.2, GREEN), ("C", 6.0, 1.2, AMBER), ("A", 7.2, 1.2, BLUE)],
         "每个进程轮流运行一个时间片(抢占)；\n响应时间最短，交互式友好", "时间片太大→退化成FCFS；太小→切换开销大"),
        ("优先级调度", TEAL, [("P低", 0, 2.5, TEAL), ("低", 2.5, 1.0, BLUE), ("中", 3.5, 1.5, GREEN), ("高", 5.0, 1.5, AMBER), ("最高", 6.5, 1.5, PURPLE)],
         "优先级高者先运行(静态/动态)；\n抢占式: 高优先级可打断低优先级", "低优先级可能饥饿→用“老化”缓解"),
        ("多级反馈队列", PURPLE, [("Q1 t=1", 0, 1.4, PURPLE), ("Q2 t=2", 1.4, 2.0, BLUE), ("Q3 t=4", 3.4, 4.0, GREEN), ("Q3继续", 7.4, 2.4, AMBER)],
         "多队列+优先级递减+时间片倍增；\n用完降级、高层抢占低层(见下页)", "实现复杂；长任务被逐级下放"),
    ]
    for i, (name, c, segs, good, bad) in enumerate(panels):
        px = 0.35 + (i % 3) * 3.85
        py0 = 4.3 - (i // 3) * 3.7
        rk(ax, px, py0, 3.75, 3.7, "", fc="#F8FAFC", ec=c, lw=1.6)
        t(ax, px + 1.875, py0 + 3.35, name, fs=11, bold=True, color=c)
        rk(ax, px + 0.15, py0 + 1.3, 3.45, 0.85, "", fc=GRAY_L, ec=GRAY, lw=1.0)
        for lbl, st, ln_, cc in segs:
            rc(ax, px + 0.22 + st * 0.28, py0 + 1.32, ln_ * 0.28, 0.81, lbl, fc=GRAY_L, ec=cc, fs=7.6, bold=True, color=cc)
        t(ax, px + 1.875, py0 + 0.75, good + "\n" + bad, fs=7.9, ha="center", ls=1.5)
    rk(ax, 0.35, 0.06, 11.2, 0.48, "记忆口诀：F先到，S最短，H比长短，R轮流，P看重要，M层层降——前5种是“单队列型”，多级反馈队列是“多队列型”",
       fc=PURPLE_L, ec=PURPLE, fs=9.4)
    save_fig(fig, "ch2-14_scheduling_compare")

# ============ ch2-15 多级反馈队列 ============
def fig15():
    fig, ax = O.new_fig(11.6, 8.8, (0, 11.6), (0, 8.8))
    O.title(ax, "多级反馈队列 MLFQ 工作示意",
            "队列优先级从高到低，时间片从短到长；新进程进最高队列；用完时间片降级；高优先级队列非空时抢占低优先级")
    qs = [
        (6.9, 1, "Q1 最高优先级  时间片=1", BLUE, BLUE_L, "新进程P进入；被抢占回来；时间片用完→降级Q2"),
        (4.75, 2, "Q2  时间片=2", GREEN, GREEN_L, "Q1降级而来；时间片用完→再降级到Q3"),
        (2.6, 4, "Q3 最低优先级  时间片=4", AMBER, AMBER_L, "Q2降级而来；若一个时间片(4)用不完则重新排队"),
    ]
    for cy, q, lbl, ec, fc, dsc in qs:
        rk(ax, 0.4, cy - 0.75, 6.4, 1.5, "", fc=fc, ec=ec, lw=1.8)
        t(ax, 0.7, cy + 0.4, lbl, fs=11.5, bold=True, color=ec, ha="left")
        t(ax, 0.7, cy - 0.05, dsc, fs=8.8, ha="left", color=INK)
        for i in range(5):
            rc(ax, 0.7 + i * 1.1, cy - 0.75, 0.95, 0.48, "", fc="#FFFFFF", ec=ec, lw=1.0)
    rc(ax, 0.7, 6.15, 0.95, 0.48, "P(新)", fc=BLUE, ec=BLUE, fs=8.4, bold=True, color="white")
    rc(ax, 1.8, 6.15, 0.95, 0.48, "降级", fc=BLUE_L, ec=BLUE, fs=8.4, bold=True)
    # 降级箭头
    al(ax, 6.9, 6.15, 6.2, 5.5, "用完时间片→降级", color=BLUE, fs=8.6, lw=1.6, dx=0.75, dy=-0.35)
    al(ax, 6.9, 4.0, 6.2, 3.35, "用完时间片→降级", color=GREEN, fs=8.6, lw=1.6, dx=0.75, dy=-0.35)
    # CPU 与调度
    rk(ax, 9.6, 2.7, 1.9, 2.6, "CPU", fc=PINK_L, ec=PINK, fs=13, bold=True)
    al(ax, 7.0, 6.9, 9.5, 4.9, "", color=PINK, lw=1.6)
    t(ax, 8.2, 6.6, "① Q1非空先调度Q1", fs=8.4, color=PINK, bold=True, bg="white")
    al(ax, 7.0, 4.75, 9.5, 4.35, "", color=GRAY, lw=1.6)
    t(ax, 8.2, 5.1, "② Q1空→调度Q2", fs=8.4, color=GRAY, bold=True, bg="white")
    al(ax, 7.0, 2.6, 9.5, 3.35, "", color=GRAY, lw=1.6)
    t(ax, 8.2, 2.62, "③ Q1Q2都空→调度Q3", fs=8.4, color=GRAY, bold=True, bg="white")
    rk(ax, 9.6, 0.9, 1.9, 1.6, "", fc=RED_L, ec=RED, lw=1.6)
    t(ax, 9.75, 1.35, "抢占规则：\nQ1有新进程到达→\n立即打断正在运行的\nQ2/Q3进程，先调度Q1", fs=8.4, ha="left", ls=1.45)
    # 示例轨迹
    rk(ax, 0.4, 0.22, 9.0, 0.62, "一个进程的轨迹：P创建→进Q1(时间片1)；当用1片未完成→降级Q2(时间片2)；用2片仍未完成→降级Q3(时间片4)最终完成",
       fc=AMBER_L, ec=AMBER, fs=9.2)
    rk(ax, 0.4, 0.95, 9.0, 0.62, "优点：短作业在Q1快速完成(响应快)；长作业逐级下放、等待越久反而时间片越大，不会饿死；无需预知运行时间；兼顾响应时间与吞吐量",
       fc=GRAY_L, ec=GRAY, fs=9.2)
    save_fig(fig, "ch2-15_mlfq")

# ============ ch2-16 临界区四部分 ============
def fig16():
    fig, ax = O.new_fig(11.0, 7.6, (0, 11.0), (0, 7.6))
    O.title(ax, "临界区访问的四个部分",
            "临界资源=一次仅允许一个进程使用的资源(共享变量、共享缓冲区、打印机等)；访问它的代码段=临界区")
    parts = [
        ("进入区", "检查可否进入；若可以则“上锁”\n(设置标志)  —— 实现互斥的关键", BLUE, BLUE_L),
        ("临界区", "访问临界资源的那段代码\n(同一时刻只允许一个进程在此处)", RED, RED_L),
        ("退出区", "“开锁”(清除标志)\n释放资源给其他进程", GREEN, GREEN_L),
        ("剩余区", "其他无关代码\n(可以在任意时刻执行)", GRAY, GRAY_L),
    ]
    for i, (name, dsc, ec, fc) in enumerate(parts):
        y = 5.6 - i * 1.15
        bk(ax, 1.55, y, 1.75, 0.95, name, fc=fc, ec=ec, fs=12.5, bold=True)
        rk(ax, 2.65, y, 3.9, 0.95, dsc, fc="#FFFFFF", ec=ec, fs=9.6, color=INK)
        if i < 3:
            al(ax, 1.55, y - 0.42, 1.55, y - 0.78, "", color=GRAY, lw=1.2)
    t(ax, 1.05, 6.28, "进程A", fs=10, color=GRAY, bold=True, ha="center")
    # 右侧: 关系
    rk(ax, 6.9, 1.9, 3.85, 4.1, "", fc=AMBER_L, ec=AMBER, fs=12.5, bold=True)
    t(ax, 8.85, 5.72, "两种制约关系", fs=12.5, bold=True, color=AMBER)
    t(ax, 7.1, 4.95, "同步：\n直接制约——进程间有先后次序\n(如A放数据，B才能取数据)", fs=9.6, ha="left", ls=1.5)
    t(ax, 7.1, 3.9, "互斥：\n间接制约——竞争同一临界资源\n(如A、B都要用同一台打印机)", fs=9.6, ha="left", ls=1.5)
    t(ax, 7.1, 2.85, "互斥四原则：\n① 空闲让进 ② 忙则等待\n③ 有限等待 ④ 让权等待", fs=9.6, ha="left", ls=1.5, color=RED, bold=True)
    rk(ax, 6.9, 0.35, 3.85, 1.3, "注意：\n“同步”(时序)与“互斥”(排他)不同\n本章PV解题时二者都要用到",
       fc=GRAY_L, ec=GRAY, fs=9.2)
    save_fig(fig, "ch2-16_critical_section")

# ============ ch2-17 Peterson ============
def fig17():
    fig, ax = O.new_fig(11.4, 7.2, (0, 11.4), (0, 7.2))
    O.title(ax, "Peterson 算法：“主动争取 + 谦让 + 最后检查”",
            "满足：互斥、空闲让进、有限等待；不满足：让权等待(忙等) → 需要信号量改进")
    # 两列代码
    code0 = ['flag[0] = true;      // ①主动争取(把“我想进”写在门口)',
             'turn = 1;            // ②谦让：让给对方',
             'while(flag[1] && turn==1);  // ③检查',
             '// ——临界区—— 使用临界资源',
             'flag[0] = false;     // ④退出：撤销“我想进”']
    code1 = ['flag[1] = true;      // ①主动争取',
             'turn = 0;            // ②谦让：让给对方',
             'while(flag[0] && turn==0);  // ③检查',
             '// ——临界区—— 使用临界资源',
             'flag[1] = false;     // ④退出']
    rk(ax, 0.4, 1.35, 4.6, 4.85, "", fc=BLUE_L, ec=BLUE, lw=1.8)
    t(ax, 2.7, 5.95, "进程 P0", fs=12, bold=True, color=BLUE)
    for i, l in enumerate(code0):
        t(ax, 0.6, 5.35 - i * 0.88, l, fs=8.6, ha="left", z=4)
    rk(ax, 6.4, 1.35, 4.6, 4.85, "", fc=GREEN_L, ec=GREEN, lw=1.8)
    t(ax, 8.7, 5.95, "进程 P1", fs=12, bold=True, color=GREEN)
    for i, l in enumerate(code1):
        t(ax, 6.6, 5.35 - i * 0.88, l, fs=8.6, ha="left", z=4)
    # 中间文字
    t(ax, 5.5, 5.3, "turn\n后写者\n先通过", fs=9.2, bold=True, color=AMBER, ha="center", ls=1.4)
    t(ax, 5.5, 4.05, "两人同时\n“谦让”：\n谁最后写turn\n谁先检查通过", fs=8.8, color=AMBER, ha="center", ls=1.45)
    t(ax, 5.5, 2.35, "flag[i]=1\n“i 想进”\nwhile里检查\n对方的flag", fs=8.8, color=AMBER, ha="center", ls=1.35)
    rk(ax, 0.4, 0.25, 10.6, 0.9, "", fc=RED_L, ec=RED, lw=1.6)
    t(ax, 0.6, 0.78, "易错：两个进程都执行到 while 时，由于 turn 后写者胜出，一定只有一个通过检查——不存在同时进入临界区；但空转等待(忙等)浪费CPU", fs=9.2, ha="left")
    t(ax, 0.6, 0.42, "记忆：flag[]=各自意愿(是否想进)；turn=最后谁谦让(后写者让先)；顺序是“先写flag，再写turn”，顺序不能反", fs=9.2, ha="left", color=RED)
    save_fig(fig, "ch2-17_peterson")

# ============ ch2-18 信号量 PV ============
def fig18():
    fig, ax = O.new_fig(11.6, 7.4, (0, 11.6), (0, 7.4))
    O.title(ax, "记录型信号量：结构 + P/V 操作流程",
            "P原语=申请资源(减), V原语=释放资源(加)；都是不可中断的原子操作(关中断实现)，可有多个进程排队")
    # 左：结构
    rk(ax, 0.35, 3.3, 4.35, 3.5, "", fc=BLUE_L, ec=BLUE, fs=12, bold=True)
    t(ax, 2.525, 6.55, "记录型信号量 S 的结构", fs=12, bold=True, color=BLUE)
    rk(ax, 0.6, 5.2, 3.85, 1.0, "value（整型）", fc="#FFFFFF", ec=BLUE, fs=11, bold=True)
    t(ax, 2.53, 4.7, "value 含义：\n≥0：剩余可用资源数(空闲资源)\n<0 ：绝对值=正在等待的进程数", fs=9.4, ha="center", ls=1.5)
    rk(ax, 0.6, 3.55, 3.85, 0.95, "等待队列 L（指向阻塞的进程链表）", fc="#FFFFFF", ec=BLUE, fs=10.5)
    t(ax, 2.53, 3.42, "例：S=2 → 还有2个资源；S=0 → 无资源无人等；\nS=－3 → 3个进程排队等待", fs=9.0, ha="center", ls=1.5)
    # 右：流程
    # P
    rk(ax, 5.3, 4.7, 2.7, 2.1, "", fc=GREEN_L, ec=GREEN, lw=1.6)
    t(ax, 6.65, 6.6, "P(S) 申请/等待", fs=12, bold=True, color=GREEN)
    t(ax, 6.65, 6.1, "S.value = S.value - 1", fs=10.5, color=INK)
    dm(ax, 6.65, 5.15, 2.3, 0.85, "S.value < 0 ?", fc=AMBER_L, ec=AMBER, fs=10.5, bold=True)
    t(ax, 5.0, 5.0, "是\n(无资源可给)", fs=9, color=RED, ha="center")
    bk(ax, 5.15, 4.05, 2.0, 0.8, "阻塞进程\n放入等待队列L", fc=RED_L, ec=RED, fs=9.6, bold=True)
    t(ax, 8.3, 5.0, "否\n(拿到资源)", fs=9, color=GREEN, ha="center")
    bk(ax, 7.95, 4.05, 1.7, 0.8, "进程继续\n(获得资源)", fc=GREEN_L, ec=GREEN, fs=9.6, bold=True)
    al(ax, 6.65, 4.7, 6.2, 4.5, "", color=RED, lw=1.4)
    al(ax, 7.4, 5.15, 7.9, 5.15, "", color=GREEN, lw=1.4)
    al(ax, 5.25, 4.9, 5.15, 4.5, "", color=RED, lw=1.4)
    al(ax, 6.65, 4.5, 6.05, 4.5, "", color=RED, lw=1.4)
    ln(ax, 8.3, 5.15, 7.95, 5.15, color=GREEN, lw=1.4)
    # V
    rk(ax, 9.0, 4.7, 2.6, 2.1, "", fc=AMBER_L, ec=AMBER, lw=1.6)
    t(ax, 10.3, 6.6, "V(S) 释放/唤醒", fs=12, bold=True, color=AMBER)
    t(ax, 10.3, 6.1, "S.value = S.value + 1", fs=10.5, color=INK)
    dm(ax, 10.3, 5.15, 2.3, 0.85, "S.value ≤ 0 ?", fc=GREEN_L, ec=GREEN, fs=10.5, bold=True)
    t(ax, 8.85, 5.0, "是\n(有人在等)", fs=9, color=RED, ha="center")
    bk(ax, 8.8, 4.05, 2.1, 0.8, "唤醒等待队列中\n的1个进程", fc=RED_L, ec=RED, fs=9.6, bold=True)
    t(ax, 11.55, 5.0, "否\n(没人等)", fs=9, color=GREEN, ha="right")
    bk(ax, 10.85, 4.05, 1.75, 0.8, "进程继续", fc=GREEN_L, ec=GREEN, fs=9.6, bold=True)
    al(ax, 10.3, 4.7, 10.0, 4.5, "", color=RED, lw=1.4)
    al(ax, 11.05, 5.15, 11.35, 4.55, "", color=GREEN, lw=1.4)
    al(ax, 10.3, 4.5, 10.9, 4.5, "", color=RED, lw=1.4)
    rk(ax, 0.35, 0.4, 10.9, 2.45, "", fc=PURPLE_L, ec=PURPLE, fs=12, bold=True)
    t(ax, 5.8, 2.62, "三大用法（解题三板斧）", fs=12, bold=True, color=PURPLE)
    t(ax, 0.55, 1.7, "① 互斥信号量：初值1，各进程P…V成对环绕临界区 → 实现互斥(资源只有1份)", fs=9.8, ha="left")
    t(ax, 0.55, 1.28, "② 同步信号量：初值0，前V后P → 实现先后次序(有时效上的必然性：先者V，后者才能P通过)", fs=9.8, ha="left")
    t(ax, 0.55, 0.86, "③ 资源计数信号量：初值=N（N个同类资源）；S<0时|S|就是等的人数", fs=9.8, ha="left")
    t(ax, 0.55, 0.48, "易错：P/V必须成对；V可以由别的进程执行(唤醒者)。整型信号量while(S<=0)忙等→改进为记录型", fs=9.8, ha="left", color=RED, bold=True)
    save_fig(fig, "ch2-18_semaphore_pv")

# ============ ch2-19 前驱图 -> 信号量 ============
def fig19():
    fig, ax = O.new_fig(11.6, 8.0, (0, 11.6), (0, 8.0))
    O.title(ax, "前驱图 → 信号量实现：每条边 = 一个同步信号量",
            "模板：①每条有向边设一个初值为0的同步信号量  ②前驱进程在它的所有任务完成后V各边信号量  ③后继进程一开始依次P各入边信号量")
    # 左：前驱图
    bk(ax, 2.0, 6.3, 1.15, 0.85, "S1", fc=PINK_L, ec=PINK, fs=11, bold=True)
    bk(ax, 0.95, 4.5, 1.15, 0.85, "S2", fc=BLUE_L, ec=BLUE, fs=11, bold=True)
    bk(ax, 3.05, 4.5, 1.15, 0.85, "S3", fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    bk(ax, 2.0, 2.75, 1.15, 0.85, "S4", fc=AMBER_L, ec=AMBER, fs=11, bold=True)
    bk(ax, 2.0, 1.0, 1.15, 0.85, "S5", fc=PURPLE_L, ec=PURPLE, fs=11, bold=True)
    al(ax, 2.0, 6.25, 1.5, 5.4, "s12", color=GRAY, fs=8.6)
    al(ax, 2.0, 6.25, 2.55, 5.4, "s13", color=GRAY, fs=8.6)
    al(ax, 1.5, 4.45, 1.95, 3.65, "s24", color=GRAY, fs=8.6)
    al(ax, 2.55, 4.45, 2.1, 3.65, "s34", color=GRAY, fs=8.6)
    al(ax, 2.0, 2.7, 2.0, 1.9, "s45", color=GRAY, fs=8.6)
    rk(ax, 0.45, 0.25, 4.3, 0.6, "前驱图：S1先于S2、S3；S2、S3先于S4；S4先于S5",
       fc=GRAY_L, ec=GRAY, fs=9.0)
    # 右：代码
    rk(ax, 5.3, 0.4, 6.0, 6.4, "", fc="#F8FAFC", ec=GRAY, lw=1.6)
    t(ax, 8.3, 6.55, "信号量实现（对应位置标注）", fs=12, bold=True, color=INK)
    lines = [
        " semaphore s12=0, s13=0, s24=0, s34=0, s45=0;",
        "",
        " S1 \u2502 { S1;  V(s12); V(s13); }   // 完成任务才V(后V)",
        " S2 \u2502 { P(s12); S2;  V(s24); }   // 先P入边信号量(前P)",
        " S3 \u2502 { P(s13); S3;  V(s34); }",
        " S4 \u2502 { P(s24); P(s34); S4;  V(s45); }  // 两条入边→两个P",
        " S5 \u2502 { P(s45); S5; }",
        "",
        " 口诀：先P后执行，执行完再V；",
        " 入边几条P几个，出边几条V几个。",
    ]
    for i, l in enumerate(lines):
        t(ax, 5.5, 5.4 - i * 0.48, l, fs=9.6, ha="left", ls=1.3, color=INK if not l.startswith(" ") else INK)
    rk(ax, 5.3, 5.78, 6.0, 0.5, "提示：P会阻塞(等它前面的边都V过)；V让后继的P有机会通过", fc=AMBER_L, ec=AMBER, fs=9.4)
    save_fig(fig, "ch2-19_precedence_graph")

# ============ ch2-20 生产者-消费者 ============
def fig20():
    fig, ax = O.new_fig(11.6, 7.8, (0, 11.6), (0, 7.8))
    O.title(ax, "生产者-消费者问题（N个缓冲区）",
            "生产者往缓冲区放产品，消费者取产品；缓冲=临界资源；empty/full=同步信号量，mutex=互斥信号量")
    bk(ax, 1.6, 5.45, 2.2, 1.0, "生产者进程", fc=BLUE_L, ec=BLUE, fs=11, bold=True)
    rc(ax, 4.5, 5.05, 6.0, 1.7, "", fc=GRAY_L, ec=GRAY, lw=1.5)
    t(ax, 7.5, 6.55, "缓冲区（容量 N）", fs=11, bold=True)
    for i in range(8):
        rc(ax, 4.7 + i * 0.72, 5.25, 0.6, 0.95, f"B{i+1}", fc="#FFFFFF", ec=GRAY, fs=8.6)
    for i in range(3):
        rc(ax, 4.7 + i * 0.72, 5.25, 0.6, 0.95, "", fc=TEAL_L, ec=TEAL, lw=1.4)
    bk(ax, 10.3, 5.45, 1.15, 1.0, "消费者", fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    al(ax, 3.9, 5.95, 4.55, 5.95, "", color=BLUE, lw=1.6)
    t(ax, 3.7, 6.2, "P(empty) P(mutex) 放入", fs=8.8, color=BLUE, ha="center", bg="white")
    al(ax, 10.9, 5.95, 10.5, 5.95, "", color=GREEN, lw=1.6)
    t(ax, 9.3, 6.2, "V(mutex) V(full)", fs=8.8, color=GREEN, ha="center", bg="white")
    al(ax, 10.0, 4.85, 2.0, 4.85, "", color=GREEN, lw=1.2, ls=":")
    t(ax, 6.2, 4.72, "消费者：P(full) → P(mutex) → 取出 → V(mutex) → V(empty)", fs=9.2, color=GREEN, ha="center", bg="white")
    # 代码区
    rk(ax, 0.4, 1.05, 5.3, 3.5, "", fc=BLUE_L, ec=BLUE, fs=11.5, bold=True)
    t(ax, 3.05, 4.3, "生产者的代码（N缓冲版）", fs=11.5, bold=True, color=BLUE)
    codes = [
        "while(1){",
        "    P(empty);     // ①先P资源信号量: 要一个空位",
        "    P(mutex);     // ②再P互斥信号量: 独占缓冲区",
        "    把产品放进缓冲区;",
        "    V(mutex);     // ③V的顺序可以互换",
        "    V(full);      // ④通知消费者: 多了一个产品",
        "}",
    ]
    for i, c in enumerate(codes):
        t(ax, 0.6, 3.85 - i * 0.38, c, fs=9.2, ha="left", ls=1.2)
    t(ax, 0.6, 1.22, "消费者：P(full)→P(mutex)→取出→V(mutex)→V(empty)", fs=9.2, ha="left", color=GREEN)
    rk(ax, 5.95, 1.05, 5.35, 3.5, "", fc=RED_L, ec=RED, fs=12, bold=True)
    t(ax, 8.62, 4.3, "铁律（防死锁）", fs=12, bold=True, color=RED)
    t(ax, 6.15, 3.45, "先 P(资源信号量 empty/full)，再 P(互斥信号量 mutex)；\nV 的顺序随意。若颠倒：", fs=9.6, ha="left", ls=1.5)
    t(ax, 6.15, 2.45, "生产者 P(mutex) 后 卡在 P(empty)；\n消费者 P(full) 后 卡在 P(mutex)——\n双方互握对方所需要的“锁”→ 死锁！", fs=9.6, ha="left", ls=1.5, color=RED, bold=True)
    rk(ax, 0.4, 0.25, 10.9, 0.62, "单缓冲版：N=1，empty=1、full=0、mutex=1——仍然必须“先资源后互斥”；两个P的顺序是最大考点",
       fc=AMBER_L, ec=AMBER, fs=9.6)
    save_fig(fig, "ch2-20_producer_consumer")

# ============ ch2-21 读者-写者 ============
def fig21():
    fig, ax = O.new_fig(11.6, 7.8, (0, 11.6), (0, 7.8))
    O.title(ax, "读者-写者问题（读优先版）",
            "核心规则：读-读可并行；读-写互斥；写-写互斥。实现技巧：“第一个读者上锁、最后一个读者开锁”")
    # 左：示意
    rk(ax, 0.4, 3.7, 3.9, 3.0, "", fc=GRAY_L, ec=GRAY, fs=11.5, bold=True)
    t(ax, 2.35, 6.42, "访问示意", fs=11.5, bold=True, color=GRAY)
    rc(ax, 1.0, 3.95, 2.6, 1.0, "共享文件/数据库", fc=AMBER_L, ec=AMBER, fs=10.5, bold=True)
    for i, s in enumerate(["读1", "读k"]):
        ci(ax, 1.4 + i * 1.1, 5.45, 0.42, s, fc=GREEN_L, ec=GREEN, fs=9)
        al(ax, 1.4 + i * 1.1, 4.98, 2.1 + i * 0.5, 5.05, "", color=GREEN, lw=1.2)
    ci(ax, 3.6, 5.45, 0.42, "写", fc=RED_L, ec=RED, fs=9, bold=True)
    al(ax, 3.6, 4.98, 3.15, 5.05, "", color=RED, lw=1.2)
    t(ax, 0.6, 4.1, "读读可并 / 读写互斥 / 写写互斥", fs=9.4, ha="left", color=INK, bold=True)
    # 右：代码
    rk(ax, 4.65, 3.7, 6.65, 3.0, "", fc=GREEN_L, ec=GREEN, fs=11.5, bold=True)
    t(ax, 7.98, 6.48, "读优先：读者代码（count计数 + rw互斥）", fs=11.5, bold=True, color=GREEN)
    rcode = [
        "while(1){",
        "    P(rc_mutex);                  // 保护count",
        "    if(count == 0) P(rw);         // 第一个读者：锁住rw(锁文件)",
        "    count++;                      // 后来的读者：只加计数",
        "    V(rc_mutex);",
        "    读文件;                        // 读者之间可并行读",
        "    P(rc_mutex);",
        "    count--;",
        "    if(count == 0) V(rw);         // 最后一个读者：开锁",
        "    V(rc_mutex);",
        "}",
    ]
    for i, c in enumerate(rcode):
        t(ax, 4.85, 6.1 - i * 0.2, c, fs=8.8, ha="left", ls=1.1)
    rk(ax, 4.65, 0.75, 6.65, 2.35, "", fc=RED_L, ec=RED, fs=11.5, bold=True)
    t(ax, 7.98, 2.9, "写者代码：只有一个 rw", fs=11.5, bold=True, color=RED)
    wcode = [
        "while(1){",
        "    P(rw);            // 读、写互斥的关键",
        "    写文件;",
        "    V(rw);            // 写完必须释放，否则读者/其他写者饿死",
        "}",
        "信号量：rw=1, rc_mutex=1；整型 count=0",
    ]
    for i, c in enumerate(wcode):
        t(ax, 4.85, 2.35 - i * 0.26, c, fs=9.0, ha="left", ls=1.15)
    rk(ax, 0.4, 1.15, 3.9, 2.35, "", fc=PURPLE_L, ec=PURPLE, fs=11.5, bold=True)
    t(ax, 2.35, 3.25, "写优先思路（一句话）", fs=11.5, bold=True, color=PURPLE)
    t(ax, 0.6, 2.75, "再加一个信号量 w：\n写者先P(w)，读者进入前也先P(w)；只要有一个写者在等，新读者就被挡在外面，只能等现有读者读完",
       fs=9.0, ha="left", ls=1.4)
    t(ax, 0.6, 1.6, "易错：若没有 w，读者源源不断时，\n写者可能“饿死”(读优先的代价)。", fs=9.0, ha="left", ls=1.4, color=RED, bold=True)
    save_fig(fig, "ch2-21_readers_writers")

# ============ ch2-22 哲学家进餐 ============
def fig22():
    import math
    fig, ax = O.new_fig(11.6, 8.2, (0, 11.6), (0, 8.2))
    O.title(ax, "哲学家进餐问题",
            "5个哲学家共用一张圆桌，每人左右各一根筷子；每个哲学家：思考→拿起左筷→拿起右筷→进餐→放下（谁会死锁？）")
    cx, cy, R = 3.3, 5.05, 1.95
    ci(ax, cx, cy, 0.62, "圆\n桌", fc=AMBER_L, ec=AMBER, fs=11)
    ang = {i: (90 - i * 72) for i in range(5)}
    pos = {}
    for i in range(5):
        a = math.radians(ang[i])
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        pos[i] = (x, y)
        ci(ax, x, y, 0.5, f"P{i}", fc=BLUE_L, ec=BLUE, fs=10, bold=True)
    # 筷子：在每两个哲学家之间的弧中点，垂直半径方向
    for i in range(5):
        a0 = math.radians(ang[i]); a1 = math.radians(ang[(i + 1) % 5])
        am = (a0 + a1) / 2
        xr, yr = cx + 1.25 * math.cos(am), cy + 1.25 * math.sin(am)
        dxr, dyr = math.cos(am + math.pi / 2), math.sin(am + math.pi / 2)
        ln(ax, xr - 0.28 * dxr, yr - 0.28 * dyr, xr + 0.28 * dxr, yr + 0.28 * dyr,
           color=PURPLE, lw=3.2)
        t(ax, xr + dxr * 0.5, yr + dyr * 0.5, f"筷{i+1}", fs=9, color=PURPLE, bold=True)
    # 死锁推演
    rk(ax, 6.7, 4.35, 4.6, 2.75, "", fc=RED_L, ec=RED, lw=1.8)
    t(ax, 9.0, 6.85, "死锁推演（经典的“每人先拿左筷”）", fs=11.5, bold=True, color=RED)
    t(ax, 6.85, 6.25, "P0拿筷1、P1拿筷2、P2拿筷3、P3拿筷4、\nP4拿筷5 → 每人各占一根，都等着拿另一根\n→ 谁也不让谁 → 循环等待 → 死锁！",
       fs=9.4, ha="left", ls=1.5)
    t(ax, 6.85, 5.0, "四个条件同时满足：互斥(一根筷子一人用)、\n不剥夺(没人能抢)、请求并保持(占着左手等右手)、\n循环等待(五个人围成一圈)", fs=9.4, ha="left", ls=1.5)
    # 三种解法
    sols = [
        ("解法① 最多4人同时进餐", BLUE, BLUE_L,
         "semaphore num = 4;\nP(num); P(左); P(右); 吃;\nV(左); V(右); V(num);\n破坏了“循环等待”形成的条件\n(总有一个人能先吃完)"),
        ("解法② 奇数先左、偶数先右", GREEN, GREEN_L,
         "i为偶数: 先P(右筷) 再P(左筷)\ni为奇数: 先P(左筷) 再P(右筷)\n破坏“循环等待”：\n0、2先抢右→1、3先抢左,\n顺序不一致, 环被打断"),
        ("解法③ 一次性申请两根", AMBER, AMBER_L,
         "用互斥信号量包住“拿左+拿右”\n(或管程/AND-型信号量):\nP(mutex); P(左); P(右); V(mutex);\n等待时不握有筷子:破坏“请求并保持”\n代价:拿筷子被串行化, 效率下降"),
    ]
    for i, (name, ec, fc, dsc) in enumerate(sols):
        x = 0.4 + i * 3.72
        rk(ax, x, 0.35, 3.5, 2.75, "", fc=fc, ec=ec, lw=1.8)
        t(ax, x + 1.75, 2.85, name, fs=10, bold=True, color=ec)
        t(ax, x + 0.2, 2.5, dsc, fs=8.8, ha="left", va="top", ls=1.5)
    save_fig(fig, "ch2-22_philosophers")

# ============ ch2-23 管程 ============
def fig23():
    fig, ax = O.new_fig(11.6, 8.2, (0, 11.6), (0, 8.2))
    O.title(ax, "管程（Monitor）的结构与特点",
            "管程=共享数据结构 + 一组操作过程 + 初始化代码；互斥由编译器自动保证，程序员不用写P/V锁细节")
    # 外部等待队列
    rk(ax, 0.4, 3.8, 1.7, 2.6, "进程调用\n请求进入\n(入口等待队列)", fc=GRAY_L, ec=GRAY, fs=9.6)
    # 管程主体
    rk(ax, 2.5, 1.15, 5.6, 5.9, "", fc=PURPLE_L, ec=PURPLE, lw=2.2)
    t(ax, 5.3, 6.7, "管程 Monitor", fs=13, bold=True, color=PURPLE)
    rk(ax, 2.8, 5.05, 5.0, 0.9, "共享数据结构（如缓冲区队列）", fc="#FFFFFF", ec=PURPLE, fs=10.5, lw=1.4)
    rk(ax, 2.8, 3.9, 5.0, 0.95, "初始化代码（一次性执行）", fc="#FFFFFF", ec=PURPLE, fs=10.5, lw=1.4)
    rk(ax, 2.8, 1.55, 5.0, 1.75, "操作过程（函数）：\n生产() / 消费() / …\n同一时刻只有一个进程能进入",
       fc=BLUE_L, ec=BLUE, fs=10.5)
    # 条件变量
    rk(ax, 0.4, 0.3, 5.5, 0.75, "", fc=AMBER_L, ec=AMBER, fs=9.6)
    t(ax, 3.15, 0.9, "条件变量 x, y（每个条件变量有自己的等待队列）", fs=9.6, ha="center")
    t(ax, 3.15, 0.5, "x.wait()：释放管程并挂起到自己的队列      x.signal()：唤醒该队列中的1个进程", fs=8.4, ha="center")
    # 右侧特点
    rk(ax, 8.4, 0.6, 2.95, 6.45, "", fc=GREEN_L, ec=GREEN, fs=12, bold=True)
    t(ax, 8.6, 6.7, "基本特性", fs=12, bold=True, color=GREEN, ha="left")
    feats = [6.15, 5.45, 4.75]
    txt = [
        "① 一次仅允许一个进程进入管程(自动互斥)",
        "② 进入管程必须“排队”(入口等待队列)",
        "③ 条件变量没有值，只有等待队列",
    ]
    for y, s in zip(feats, txt):
        t(ax, 8.6, y, s, fs=9.2, ha="left", ls=1.5)
    t(ax, 8.6, 4.15, "④ 与信号量区别：", fs=9.2, ha="left", ls=1.5)
    t(ax, 8.6, 3.9, "管程=封装好的类，编译层面", fs=9.2, ha="left", ls=1.5)
    t(ax, 8.6, 3.65, "保证互斥；信号量=P/V分散", fs=9.2, ha="left", ls=1.5)
    t(ax, 8.6, 3.4, "在代码中，易出错。", fs=9.2, ha="left", ls=1.5)
    t(ax, 8.6, 2.5, "⑤ 管程内部可以用条件变量\n实现同步(一次唤醒1个/广播)", fs=9.2, ha="left", ls=1.5)
    t(ax, 8.6, 1.5, "对比记忆：信号量同步=分散的\nP/V(灵活但易错)；管程同步=\n封装的对象(安全但受限)", fs=9.2, ha="left", ls=1.5)
    save_fig(fig, "ch2-23_monitor")

# ============ ch2-24 死锁四条件 ============
def fig24():
    fig, ax = O.new_fig(11.6, 7.8, (0, 11.6), (0, 7.8))
    O.title(ax, "死锁四个必要条件 + 三种处理策略",
            "四条件必须同时满足才可能死锁(缺一不可)；其中“循环等待”是必要不充分——需与安全判断(银行家)结合")
    conds = [
        ("① 互斥", "资源一次只能分配给一个进程使用",
         "比喻：一台打印机同时只能打印一个任务", AMBER, AMBER_L),
        ("② 不剥夺", "进程已获得的资源，用完之前不能被强行夺走，只能主动释放",
         "比喻：你手里的奶茶，别人不能抢走", BLUE, BLUE_L),
        ("③ 请求并保持", "进程拿着已获得的资源，又去申请新资源(边等边占) ",
         "比喻：左手拿A，右手又伸向B", GREEN, GREEN_L),
        ("④ 循环等待", "每个进程都等着下一个进程手里的资源，(资源分配图成环)",
         "比喻：四人围圈，每人拿住前一个的钥匙", RED, RED_L),
    ]
    for i, (name, k, m, ec, fc) in enumerate(conds):
        x = 0.4 + (i % 2) * 5.4
        y = 4.55 - (i // 2) * 2.35
        rk(ax, x, y, 5.2, 2.1, "", fc=fc, ec=ec, lw=1.8)
        t(ax, x + 0.25, y + 1.8, name, fs=13, bold=True, color=ec, ha="left")
        t(ax, x + 0.25, y + 1.12, k, fs=9.6, ha="left", ls=1.45)
        t(ax, x + 0.25, y + 0.42, m, fs=9.0, ha="left", ls=1.4, color=GRAY)
    # 处理策略
    rk(ax, 0.4, 0.3, 10.85, 2.0, "", fc="#F8FAFC", ec=GRAY, lw=1.6)
    t(ax, 0.55, 2.12, "死锁处理策略（四选一）", fs=12, bold=True, color=INK, ha="left")
    hts = [
        ("预防", "破坏四条件之一：一次性分配\n(破坏请求保持)/可剥夺/顺序分配\n互斥难破坏→SPOOLing改造",
         "静态方法, 资源利用率低", PURPLE, PURPLE_L),
        ("避免", "银行家算法：分配前判断\n是否处于安全状态\n安全序列存在等价于安全",
         "动态方法, 需知最大需求", BLUE, BLUE_L),
        ("检测+解除", "资源分配图化简(死锁定理)\n→撤销进程/资源剥夺/回退",
         "事后处理, 开销大", RED, RED_L),
        ("鸵鸟策略", "系统不处理，交给用户重启\n(死锁概率极低时最经济)",
         "最简单, 有风险", AMBER, AMBER_L),
    ]
    for i, (k, v1, v2, ec, fc) in enumerate(hts):
        x = 0.75 + i * 2.63
        rk(ax, x, 0.45, 2.45, 1.5, "", fc=fc, ec=ec, lw=1.6)
        t(ax, x + 1.225, 1.75, k, fs=11, bold=True, color=ec)
        t(ax, x + 1.225, 1.13, v1, fs=8.0, ha="center", ls=1.4)
        t(ax, x + 1.225, 0.6, v2, fs=8.0, ha="center", ls=1.3, color=GRAY)
    save_fig(fig, "ch2-24_deadlock_conditions")

# ============ ch2-25 资源分配图 ============
def fig25():
    fig, ax = O.new_fig(11.6, 7.6, (0, 11.6), (0, 7.6))
    O.title(ax, "资源分配图与化简（死锁检测）",
            "圆圈=进程；方框=资源类(框内圆点=资源实例)；请求边：进程→资源类；分配边：资源实例→进程")
    # 资源框
    def res(x, y, n, name):
        rk(ax, x, y, 1.9, 0.72, "", fc="#FFFFFF", ec=AMBER, lw=1.6)
        t(ax, x - 0.12, y + 0.36, name, fs=10, bold=True, color=AMBER, ha="right")
        for i in range(n):
            ci(ax, x + 1.9 * (i + 1) / (n + 1), y + 0.36, 0.16, "", fc=AMBER_L, ec=AMBER, lw=1.2)
    res(0.5, 5.45, 2, "R1(2个)")
    res(0.5, 3.75, 1, "R2(1个)")
    res(0.5, 2.05, 1, "R3(1个)")
    ci(ax, 3.7, 5.8, 0.55, "P1", fc=BLUE_L, ec=BLUE, fs=11, bold=True)
    ci(ax, 4.9, 4.3, 0.55, "P2", fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    ci(ax, 3.7, 2.7, 0.55, "P3", fc=PINK_L, ec=PINK, fs=11, bold=True)
    # 边
    al(ax, 1.85, 5.81, 3.1, 5.81, "分配边 R1→P1", color=AMBER, fs=8.4, dy=0.55)
    al(ax, 3.55, 5.25, 2.5, 4.5, "请求边 P1→R2", color=BLUE, fs=8.4, dx=0.5, dy=0.68)
    al(ax, 1.5, 4.11, 4.3, 4.28, "分配边 R2→P2", color=AMBER, fs=8.4, dy=0.46)
    al(ax, 4.65, 3.9, 2.5, 2.6, "请求边 P2→R3", color=GREEN, fs=8.4, dx=0.42, dy=0.5)
    al(ax, 1.5, 2.45, 3.1, 2.68, "分配边 R3→P3", color=AMBER, fs=8.4, dy=0.44)
    al(ax, 3.55, 3.25, 2.4, 5.6, "请求边 P3→R1", color=PINK, fs=8.4, dx=-0.1, dy=1.34)
    t(ax, 1.45, 5.1, "R1共2个实例：1个分给P1,\n还有1个空闲 → P3有戏", fs=8.8, color=INK, ha="center", bg="white")
    # 化简
    rk(ax, 7.4, 3.35, 3.9, 3.3, "", fc=GREEN_L, ec=GREEN, lw=1.8)
    t(ax, 7.55, 6.45, "化简步骤（手工逐点消除）", fs=11, bold=True, color=GREEN, ha="left")
    steps = [
        "① P3 请求 R1：R1有1个空闲实例→P3可满足→P3完成，收回R3的实例(释放)",
        "② 收回R3→P2请求R3满足→P2完成，收回R2的实例(释放)",
        "③ 收回R2→P1请求R2满足→P1完成",
        "④ 全部进程均可完成→图可完全化简\n  → 系统无死锁(尽管图中有一个环!)",
    ]
    for i, s in enumerate(steps):
        t(ax, 7.55, 6.02 - i * 0.72, s, fs=9.0, ha="left", ls=1.4)
    rk(ax, 7.4, 0.8, 3.9, 2.35, "", fc=RED_L, ec=RED, lw=1.8)
    t(ax, 7.55, 2.92, "死锁定理", fs=11, bold=True, color=RED, ha="left")
    thm = [
        "① 系统死锁 等价于 资源分配图不可完全化简",
        "② 单实例资源：图中有环 等价于 死锁",
        "③ 多实例资源：有环 不一定 死锁(本例)",
        "④ 图中无环 → 一定没有死锁",
    ]
    for i, s in enumerate(thm):
        t(ax, 7.55, 2.52 - i * 0.44, s, fs=9.2, ha="left", ls=1.35)
    save_fig(fig, "ch2-25_rag")

# ============ ch2-26 银行家算法 ============
def fig26():
    fig, ax = O.new_fig(11.9, 8.6, (0, 11.9), (0, 8.6))
    O.title(ax, "银行家算法 · 完整例题",
            "系统5进程P0~P4、3类资源A/B/C；Available=(3,3,2)；Need = Max - Allocation；安全性检查找安全序列", fs=14.5)
    def matrix(x, y, title, rows, head, color):
        t(ax, x + 1.1, y + 0.62, title, fs=10.5, bold=True, color=color, ha="center")
        for j, h in enumerate(head):
            rc(ax, x + j * 0.72, y, 0.72, 0.42, h, fc=GRAY_L, ec=GRAY, fs=8.4, bold=True)
        for i, r in enumerate(rows):
            rc(ax, x - 0.9, y - (i + 1) * 0.42, 0.9, 0.42, r[0], fc=GRAY_L, ec=GRAY, fs=8.4)
            for j, v in enumerate(r[1]):
                rc(ax, x + j * 0.72, y - (i + 1) * 0.42, 0.72, 0.42, str(v), fc="#FFFFFF", ec=GRAY, fs=8.4)
    head = ["A", "B", "C"]
    maxr = [("P0", [7, 5, 3]), ("P1", [3, 2, 2]), ("P2", [9, 0, 2]), ("P3", [2, 2, 2]), ("P4", [4, 3, 3])]
    allo = [("P0", [0, 1, 0]), ("P1", [2, 0, 0]), ("P2", [3, 0, 2]), ("P3", [2, 1, 1]), ("P4", [0, 0, 2])]
    need = [("P0", [7, 4, 3]), ("P1", [1, 2, 2]), ("P2", [6, 0, 0]), ("P3", [0, 1, 1]), ("P4", [4, 3, 1])]
    matrix(1.15, 5.85, "Max 最大需求", maxr, head, BLUE)
    matrix(4.45, 5.85, "Allocation 已分配", allo, head, GREEN)
    matrix(7.75, 5.85, "Need 尚需", need, head, AMBER)
    t(ax, 5.8, 6.95, "Need = Max - Allocation（逐位相减，如 P1: (3,2,2)-(2,0,0)=(1,2,2)）",
      fs=9.0, color=AMBER, ha="center", bg="white")
    # Available
    rk(ax, 10.35, 5.2, 1.35, 1.35, "", fc="#FFFFFF", ec=PINK, lw=1.8)
    t(ax, 11.02, 6.35, "Available", fs=8.8, bold=True, color=PINK)
    t(ax, 11.02, 5.9, "(3,3,2)", fs=11, bold=True, color=PINK)
    t(ax, 11.02, 5.48, "空闲资源", fs=8.2, color=GRAY)
    al(ax, 10.05, 6.0, 10.3, 6.0, "", color=PINK, lw=1.4)
    # 安全性检查
    rk(ax, 0.4, 0.4, 6.9, 3.3, "", fc=GREEN_L, ec=GREEN, lw=1.8)
    t(ax, 0.6, 3.5, "安全性检查（逐步验算）", fs=11.5, bold=True, color=GREEN, ha="left")
    lines = [
        "t=0 Available=(3,3,2)  检查谁的Need≤Available?",
        "  P1 (1,2,2)≤(3,3,2) √ → 分配并回收Alloc → (5,3,2)",
        "  P3 (0,1,1)≤(5,3,2) √ → 回收Alloc → (7,4,3)",
        "  P4 (4,3,1)≤(7,4,3) √ → 回收Alloc → (7,4,5)",
        "  P0 (7,4,3)≤(7,4,5) √ → 回收Alloc → (7,5,5)",
        "  P2 (6,0,0)≤(7,5,5) √ → 回收Alloc → (10,5,7)",
        "→ 安全序列 <P1,P3,P4,P0,P2>  系统安全,可分配!",
    ]
    for i, l in enumerate(lines):
        t(ax, 0.6, 3.08 - i * 0.36, l, fs=9.2, ha="left", ls=1.25)
    t(ax, 0.6, 0.62, "注: 能找到安全序列→安全状态(必不死锁); 找不到→不安全(未必死锁)", fs=9.0, ha="left", color=RED, bold=True)
    # 第二问
    rk(ax, 7.6, 0.4, 4.1, 3.3, "", fc=AMBER_L, ec=AMBER, lw=1.8)
    t(ax, 7.75, 3.5, "第二问：P1请求(1,0,2)？", fs=11, bold=True, color=AMBER, ha="left")
    q = [
        "① Request≤Need? (1,0,2)≤(1,2,2) √",
        "② Request≤Available? (1,0,2)≤(3,3,2) √",
        "③ 试探分配（先假设给它）：",
        "   Available'=(3,3,2)-(1,0,2)=(2,3,0)",
        "   Alloc'(P1)=(2,0,0)+(1,0,2)=(3,0,2)",
        "   Need'(P1)=(1,2,2)-(1,0,2)=(0,2,0)",
        "④ 再安全性检查: P1(0,2,0)≤(2,3,0)√→(5,3,2)",
        "   →(7,4,3)→(7,4,5)→(7,5,5)→(10,5,7)",
        "结论: 存在安全序列<P1,P3,P4,P0,P2> → 可以分配!",
    ]
    for i, l in enumerate(q):
        t(ax, 7.75, 3.15 - i * 0.28, l, fs=8.8, ha="left", ls=1.2)
    save_fig(fig, "ch2-26_bankers")

# ============ 主程序 ============
if __name__ == "__main__":
    funcs = [fig00, fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08,
             fig09, fig10, fig11, fig12, fig13, fig14, fig15, fig16, fig17,
             fig18, fig19, fig20, fig21, fig22, fig23, fig24, fig25, fig26]
    for f in funcs:
        f()
    print("ALL FIGURES DONE:", len(funcs))
