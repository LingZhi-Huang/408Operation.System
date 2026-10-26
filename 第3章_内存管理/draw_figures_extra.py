# -*- coding: utf-8 -*-
"""第3章 扩写新增插图（ch3-20 ~ ch3-30）。运行：python3 draw_figures_extra.py"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L, GRAY, GRAY_L,
                   PINK, PINK_L)

FIG = "/Users/levi/IdeaProjects/操作系统/第3章_内存管理/figures/"
F = lambda n: FIG + n


# ---------- ch3-20 动态重定位例 ----------
def f20():
    fig, ax = osfig.new_fig(12, 5.8, xlim=(0, 12), ylim=(0, 5.8))
    osfig.title(ax, "动态重定位：一条加法完成地址翻译",
                sub="物理地址 = 重定位寄存器（装入起始地址）+ 逻辑地址 —— 译码在访存前由硬件实时完成", fs=15)
    osfig.rbox(ax, 0.8, 3.4, 3.2, 1.3, "进程的逻辑地址空间\n（从 0 开始编址）", fc=BLUE_L, ec=BLUE, fs=11, bold=True, ls=1.5)
    osfig.tx(ax, 2.4, 2.95, "逻辑地址 2500", fs=11, bold=True, color=BLUE)
    osfig.rbox(ax, 4.7, 3.4, 2.6, 1.3, "重定位寄存器\n（基址 = 10000）", fc=AMBER_L, ec=AMBER, fs=11, bold=True, ls=1.5)
    osfig.box(ax, 9.0, 4.05, 2.2, 0.9, "+ 加法器", fc=GREEN_L, ec=GREEN, fs=12, bold=True)
    osfig.rbox(ax, 7.9, 1.9, 3.4, 1.2, "物理内存\n物理地址 = 10000 + 2500 = 12500", fc=GREEN_L, ec=GREEN, fs=11, bold=True, ls=1.5)
    osfig.arrow(ax, 4.0, 4.05, 4.7, 4.05, "", color=INK, lw=1.8)
    osfig.arrow(ax, 7.3, 4.05, 7.9, 4.05, "", color=INK, lw=1.8)
    osfig.arrow(ax, 9.6, 3.6, 9.6, 3.15, "", color=INK, lw=1.8)
    osfig.tx(ax, 6, 1.15, "好处：程序在内存里「搬家」后，只需改一次重定位寄存器，程序本身一个字节都不用动", fs=11.5, color=GREEN, bold=True)
    osfig.tx(ax, 6, 0.65, "对比：静态重定位在装入时一次性算死地址，之后不能再移动；动态重定位是「运行时随时可搬」", fs=11, color=GRAY)
    osfig.tx(ax, 6, 0.2, "【考点】动态重定位 = 紧凑技术的前提 = 离散分配（分页/分段）的基础", fs=11.5, color=RED, bold=True)
    osfig.save(fig, F("ch3-20_dynamic_reloc_example.png"))


# ---------- ch3-21 分区分配逐步例 ----------
def f21():
    fig, ax = osfig.new_fig(12.5, 6.6, xlim=(0, 12.5), ylim=(0, 6.6))
    osfig.title(ax, "首次适应（FF）手算示范：空闲区链的三次变化",
                sub="空闲区 100K/500K/200K/300K/600K；请求 212K → 417K → 112K；每次都从链首找第一个够大的", fs=14.5)
    # 三个阶段
    stages = [
        ("初始", [100, 500, 200, 300, 600], []),
        ("分配 212K 后", [100, 288, 200, 300, 600], [(500, "212K")]),
        ("再分配 417K 后", [100, 288, 200, 300, 183], [(500, "212K"), (288, "417K")]),
        ("再分配 112K 后", [100, 176, 200, 300, 183], [(500, "212K"), (288, "417K"), (288, "112K")]),
    ]
    y = 5.5
    for name, free, allocs in stages:
        y -= 1.25
        osfig.tx(ax, 1.35, y + 0.55, name, fs=11, bold=True, color=BLUE, ha="left")
        x = 2.6
        for i, sz in enumerate(free):
            if sz > 0:
                osfig.rect(ax, x, y, sz / 600 * 8.0, 0.55, str(sz) + "K", fc=GREEN_L, ec=GREEN, fs=9.5, bold=True)
            x += sz / 600 * 8.0
        for start, label in allocs:
            osfig.rect(ax, 2.6 + start / 600 * 8.0, y + 0.58, (112 if label == "212K" else 417 if label == "417K" else 112) / 600 * 8.0, 0.28, label, fc=BLUE_L, ec=BLUE, fs=8)
    osfig.tx(ax, 6.25, 0.95, "要点：FF 从链首顺序找「第一个 ≥ 请求」的空闲区；212K 进 500K 区后该区裂成「212K（已用）+ 288K（剩）」", fs=10.5, color=INK)
    osfig.tx(ax, 6.25, 0.5, "追问：若改用最佳适应（BF）？—— 212K 会进 300K 区（剩 88K 碎片）；BF「挑最小够用」但会留下大量用不了的小碎块", fs=10.5, color=AMBER)
    osfig.tx(ax, 6.25, 0.12, "【易错】分配后剩 0 的空闲区要从链中删除；回收时若与相邻空闲区前后贴着，必须合并", fs=10.5, color=RED, bold=True)
    osfig.save(fig, F("ch3-21_partition_calc_walkthrough.png"))


# ---------- ch3-22 地址拆分练习 ----------
def f22():
    fig, ax = osfig.new_fig(12.5, 6.2, xlim=(0, 12.5), ylim=(0, 6.2))
    osfig.title(ax, "专项训练：逻辑地址拆分（页大小 1KB = 2^10）",
                sub="十进制法：页号 = A ÷ L 取整，页内偏移 = A mod L；二进制法：低 10 位是偏移，其余是页号", fs=14.5)
    cases = [
        ("2500", "2500 = 2×1024 + 452", "页号 2，偏移 452", "0000 1001 1100 0100 → 高6位=2，低10位=452"),
        ("3456", "3456 = 3×1024 + 384", "页号 3，偏移 384", "0000 1101 1000 0000 → 高6位=3，低10位=384"),
        ("8910", "8910 = 8×1024 + 718", "页号 8，偏移 718", "0010 0010 1100 1110 → 高6位=8，低10位=718"),
    ]
    y = 5.0
    for addr, dec, result, _bin in cases:
        osfig.rbox(ax, 0.7, y - 0.6, 1.3, 0.75, addr, fc=GRAY_L, ec=GRAY, fs=13, bold=True)
        osfig.tx(ax, 4.3, y - 0.22, "十进制：" + dec, fs=11.5, ha="left", color=INK)
        osfig.tx(ax, 8.8, y - 0.22, result, fs=11.5, ha="left", color=GREEN, bold=True)
        y -= 1.0
    osfig.tx(ax, 6.25, 1.7, "再拼物理地址：物理地址 = 页框号 × 1024 + 页内偏移（例如页号2 → 页框6，则物理地址 = 6×1024+452 = 6596）", fs=11.5, color=BLUE, bold=True)
    osfig.tx(ax, 6.25, 1.1, "二进制视角更快：页大小 1KB → 低 10 位固定是页内偏移，逻辑地址直接「掰两半」", fs=11, color=INK)
    osfig.tx(ax, 6.25, 0.6, "页大小 4KB（2^12）→ 低 12 位是偏移；页大小 2KB（2^11）→ 低 11 位是偏移", fs=11, color=TEAL)
    osfig.tx(ax, 6.25, 0.15, "【易错】页内偏移位数 = log2(页大小)，由页大小唯一决定；地址总位数 − 偏移位数 = 页号位数", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch3-22_page_split_examples.png"))


# ---------- ch3-23 TLB 时序 ----------
def f23():
    fig, ax = osfig.new_fig(12.5, 5.8, xlim=(0, 12.5), ylim=(0, 5.8))
    osfig.title(ax, "TLB 命中 vs 未命中：一次访存的两种时间线",
                sub="t = 查 TLB 时间，m = 访存一次的时间；EAT = h(t+m) + (1-h)(t+2m)", fs=15)
    # 命中
    osfig.tx(ax, 3.2, 4.9, "命中（h = 90%）", fs=12.5, bold=True, color=GREEN)
    osfig.rect(ax, 0.9, 3.75, 1.5, 0.6, "查TLB", fc=TEAL_L, ec=TEAL, fs=10.5, bold=True)
    osfig.rect(ax, 2.4, 3.75, 2.6, 0.6, "按页框号访存取数", fc=GREEN_L, ec=GREEN, fs=10.5, bold=True)
    osfig.tx(ax, 3.7, 3.15, "耗时 t + m = 20+100 = 120ns", fs=11, color=GREEN, bold=True)
    # 未命中
    osfig.tx(ax, 9.3, 4.9, "未命中（1-h = 10%）", fs=12.5, bold=True, color=RED)
    osfig.rect(ax, 7.0, 3.75, 1.5, 0.6, "查TLB", fc=TEAL_L, ec=TEAL, fs=10.5, bold=True)
    osfig.rect(ax, 8.5, 3.75, 2.0, 0.6, "查内存页表", fc=AMBER_L, ec=AMBER, fs=10.5, bold=True)
    osfig.rect(ax, 10.5, 3.75, 2.2, 0.6, "再访存取数", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
    osfig.tx(ax, 9.3, 3.15, "耗时 t + m + m = 20+100+100 = 220ns", fs=11, color=RED, bold=True)
    osfig.rbox(ax, 0.9, 1.15, 5.2, 1.45, "", fc=GRAY_L, ec=GRAY)
    osfig.tx(ax, 3.5, 2.25, "EAT = 0.9×120 + 0.1×220", fs=13, bold=True, color=INK)
    osfig.tx(ax, 3.5, 1.6, "    = 108 + 22 = 130ns", fs=13, bold=True, color=RED)
    osfig.rbox(ax, 6.4, 1.15, 5.3, 1.45, "", fc=BLUE_L, ec=BLUE)
    osfig.tx(ax, 9.05, 2.25, "对比：无 TLB 时每次都要 2 次访存", fs=11.5, bold=True, color=BLUE)
    osfig.tx(ax, 9.05, 1.6, "即 200ns/次 —— TLB 让访问提速约 35%", fs=11.5, color=INK)
    osfig.tx(ax, 6.25, 0.45, "【易错】两级页表 + TLB 未命中时 = t + m + m（查页表两次？——TLB 未命中按「查一级、查二级」算 m+m，再取数再一次，按题设为准）", fs=10.5, color=RED)
    osfig.save(fig, F("ch3-23_tlb_hit_miss_time.png"))


# ---------- ch3-24 多级页表位数练习 ----------
def f24():
    fig, ax = osfig.new_fig(12.5, 6.0, xlim=(0, 12.5), ylim=(0, 6.0))
    osfig.title(ax, "专项训练：两级页表的位数拆分（3 组参数）",
                sub="公式：页内偏移位数 = log2(页大小)；剩余位数 = 页表项大小的位数比（每级平分或按题设拆）", fs=14.5)
    rows = [
        ("32 位地址 / 4KB 页 / 每项 4B", "偏移 12 位", "剩 20 位 → 一级 10 + 二级 10（4KB/4B=1024 项=10 位）", "无 TLB 访存 3 次（一级表+二级表+取数）"),
        ("32 位地址 / 4KB 页 / 每项 8B", "偏移 12 位", "剩 20 位，每项 8B → 每张表 512 项 = 9 位 → 拆成 10+10? 不行——需按 9 的倍数拆 → 一级/二级各 10 位的方案不成立", "改为 3 级（10+10+... 按题设）——常见变体"),
        ("48 位地址 / 4KB 页 / 每项 8B", "偏移 12 位", "剩 36 位，每张表 512 项 = 9 位/级 → 4 级页表（9×4=36）", "无 TLB 访存 5 次"),
    ]
    osfig.rect(ax, 0.7, 5.0, 3.6, 0.55, "题设", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 4.3, 5.0, 1.6, 0.55, "偏移位数", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 5.9, 5.0, 4.3, 0.55, "页号位数拆分", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 10.2, 5.0, 2.0, 0.55, "无TLB访存", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    y = 5.0
    for t, a, b, c in rows:
        y -= 1.25
        osfig.rbox(ax, 0.7, y, 3.6, 1.2, t, fc=BLUE_L, ec=BLUE, fs=10, bold=True, ls=1.4)
        osfig.rbox(ax, 4.3, y, 1.6, 1.2, a, fc="white", ec=GRAY, fs=10.5)
        osfig.rbox(ax, 5.9, y, 4.3, 1.2, b, fc="white", ec=GRAY, fs=8.5, ls=1.35)
        osfig.rbox(ax, 10.2, y, 2.0, 1.2, c, fc=GREEN_L, ec=GREEN, fs=9, ls=1.35)
    osfig.tx(ax, 6.25, 0.75, "解题套路：先切偏移 → 剩下位数 ÷ 每级位数（每级位数 = log2(页大小/页表项大小)）", fs=11.5, color=BLUE, bold=True)
    osfig.tx(ax, 6.25, 0.3, "【考点】N 级页表无 TLB 时：访存次数 = N + 1；顶级页表只能有一个且常驻内存", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch3-24_multilevel_bits.png"))


# ---------- ch3-25 分段共享 ----------
def f25():
    fig, ax = osfig.new_fig(12, 5.8, xlim=(0, 12), ylim=(0, 5.8))
    osfig.title(ax, "分段的天赋：按逻辑单位共享与保护",
                sub="编辑器只有一份代码，N 个进程各有一份「数据段」——共享靠段表指向同一个物理段", fs=15)
    # 进程A
    osfig.tx(ax, 2.4, 4.95, "进程 A 的段表", fs=12, bold=True, color=BLUE)
    osfig.rect(ax, 0.9, 3.5, 3.0, 0.55, "段0 代码段 → 基址5000", fc=BLUE_L, ec=BLUE, fs=10, bold=True)
    osfig.rect(ax, 0.9, 2.85, 3.0, 0.55, "段1 数据段 → 基址9000", fc=GRAY_L, ec=GRAY, fs=10)
    # 进程B
    osfig.tx(ax, 9.6, 4.95, "进程 B 的段表", fs=12, bold=True, color=PURPLE)
    osfig.rect(ax, 8.1, 3.5, 3.0, 0.55, "段0 代码段 → 基址5000", fc=PURPLE_L, ec=PURPLE, fs=10, bold=True)
    osfig.rect(ax, 8.1, 2.85, 3.0, 0.55, "段1 数据段 → 基址11000", fc=GRAY_L, ec=GRAY, fs=10)
    # 共享段
    osfig.rbox(ax, 4.3, 3.35, 3.4, 0.85, "物理内存 5000 号起：\n「文本编辑器」共享代码段", fc=GREEN_L, ec=GREEN, fs=10.5, bold=True, ls=1.4)
    osfig.arrow(ax, 3.9, 3.77, 4.3, 3.77, "", color=BLUE, lw=1.8)
    osfig.arrow(ax, 8.1, 3.77, 7.7, 3.77, "", color=PURPLE, lw=1.8)
    osfig.tx(ax, 6, 1.9, "为什么分段能轻松共享、分页却别扭？", fs=12.5, bold=True, color=INK)
    osfig.tx(ax, 6, 1.3, "分段按「完整逻辑单位」划分：一段 = 一个模块，天然对齐共享需求；", fs=11, color=INK)
    osfig.tx(ax, 6, 0.85, "分页按「固定大小」机械切分：一段代码可能横跨好几页，共享粒度碎、管理别扭", fs=11, color=INK)
    osfig.tx(ax, 6, 0.35, "【考点】「可重入代码（纯代码）」= 不能修改的代码，才能被多进程共享；各自配私有数据区", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch3-25_segment_share.png"))


# ---------- ch3-26 虚拟内存容量例 ----------
def f26():
    fig, ax = osfig.new_fig(12, 5.6, xlim=(0, 12), ylim=(0, 5.6))
    osfig.title(ax, "虚拟内存的最大容量与实际容量",
                sub="最大容量由「地址结构」决定：2^地址位数；实际可用 ≤ min(2^位数, 内存+外存)", fs=15)
    osfig.tx(ax, 3.2, 4.6, "例 1：32 位系统、4GB 内存 + 1TB 磁盘", fs=12.5, bold=True, color=BLUE)
    osfig.tx(ax, 3.2, 3.9, "虚拟地址空间最大 = 2^32 = 4GB", fs=11.5, color=INK)
    osfig.tx(ax, 3.2, 3.4, "哪怕磁盘有 1TB，虚拟内存也最多 4GB", fs=11.5, color=RED, bold=True)
    osfig.tx(ax, 3.2, 2.9, "——地址就 32 根线，编不出更多号", fs=11, color=GRAY)
    osfig.tx(ax, 9.0, 4.6, "例 2：64 位系统、8GB 内存 + 512GB 磁盘", fs=12.5, bold=True, color=TEAL)
    osfig.tx(ax, 9.0, 3.9, "2^64 = 16EB，实际受物理限制", fs=11.5, color=INK)
    osfig.tx(ax, 9.0, 3.4, "虚拟内存实际最大 = 8GB + 512GB", fs=11.5, color=GREEN, bold=True)
    osfig.tx(ax, 9.0, 2.9, "——此时瓶颈是内外存之和", fs=11, color=GRAY)
    osfig.rbox(ax, 0.9, 1.0, 10.2, 1.35, "", fc=AMBER_L, ec=AMBER)
    osfig.tx(ax, 6, 2.05, "结论（两条都要会）：最大虚拟内存 = 2^地址位数；实际能开的 = min(2^地址位数, 内存容量 + 外存容量)", fs=12, bold=True, color=INK)
    osfig.tx(ax, 6, 1.35, "【易错】「虚拟内存容量 = min(...)」填空题常把两个取反——先想「地址编几号」再想「仓库有多大」", fs=11, color=RED)
    osfig.save(fig, F("ch3-26_vm_capacity_example.png"))


# ---------- ch3-27 LRU 栈式性质 ----------
def f27():
    fig, ax = osfig.new_fig(12.5, 6.0, xlim=(0, 12.5), ylim=(0, 6.0))
    osfig.title(ax, "LRU 的「栈式算法」性质：k 帧内容 ⊆ k+1 帧内容",
                sub="访问序列 4,3,2,1,4,3,5：比较 3 帧与 4 帧的 LRU 逐时刻内容——帧多绝不缺页变多", fs=14.5)
    seq = ["4", "3", "2", "1", "4", "3", "5"]
    # 3帧
    osfig.tx(ax, 3.2, 5.15, "3 帧 LRU", fs=12, bold=True, color=BLUE)
    x0 = 1.4
    for i, p in enumerate(seq):
        osfig.tx(ax, x0 + i * 1.55, 4.75, p, fs=11, bold=True, color=GRAY)
        stack3 = {"4": ["4"], "3": ["4", "3"], "2": ["4", "3", "2"], "1": ["1", "3", "2"],
                  "4x": None, "3x": None, "5": None}
        pass
    # 直接画每列
    cols3 = [["4"], ["4", "3"], ["4", "3", "2"], ["1", "3", "2"], ["1", "4", "2"] , ["1", "4", "3"], ["5", "4", "3"]]
    hits3 = [False, False, False, False, True, True, False]
    for i, col in enumerate(cols3):
        for j, v in enumerate(col):
            c = GREEN_L if (j == len(col) - 1 and hits3[i]) else BLUE_L
            e = GREEN if (j == len(col) - 1 and hits3[i]) else BLUE
            osfig.rect(ax, x0 + i * 1.55, 3.55 + j * 0.42, 0.6, 0.4, v, fc=c, ec=e, fs=9.5)
    # 4帧
    osfig.tx(ax, 9.3, 5.15, "4 帧 LRU", fs=12, bold=True, color=PURPLE)
    x1 = 7.5
    cols4 = [["4"], ["4", "3"], ["4", "3", "2"], ["1", "3", "2", "4"], ["1", "3", "2", "4"], ["1", "3", "2", "4"] , ["5", "1", "3", "2"]]
    hits4 = [False, False, False, False, True, True, False]
    for i, col in enumerate(cols4):
        osfig.tx(ax, x1 + i * 0.9, 4.75, seq[i], fs=11, bold=True, color=GRAY)
        for j, v in enumerate(col):
            c = GREEN_L if (j == len(col) - 1 and False) else PURPLE_L
            e = GREEN if (j == len(col) - 1 and False) else PURPLE
            osfig.rect(ax, x1 + i * 0.9, 3.1 + j * 0.42, 0.62, 0.4, v, fc=c, ec=e, fs=9.5)
    osfig.tx(ax, 3.2, 2.55, "帧数 3→4，每列内容只多不少（栈式包含）", fs=11, color=GREEN, bold=True)
    osfig.tx(ax, 6.25, 1.75, "推论：LRU（与 OPT）帧数越多缺页越少 → 不可能发生 Belady 异常", fs=12, bold=True, color=INK)
    osfig.tx(ax, 6.25, 1.1, "FIFO 无此性质：3 帧 9 次缺页，4 帧反而 10 次（Belady 异常）", fs=11.5, color=RED)
    osfig.tx(ax, 6.25, 0.5, "【考点】「栈式算法」定义：k 帧时内存页集合 ⊆ k+1 帧时集合；LRU/OPT 是，FIFO 不是", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch3-27_lru_stack_property.png"))


# ---------- ch3-28 改进CLOCK实例 ----------
def f28():
    fig, ax = osfig.new_fig(12.5, 6.4, xlim=(0, 12.5), ylim=(0, 6.4))
    osfig.title(ax, "改进 CLOCK 的一轮扫描实例",
                sub="优先级：(A=0,M=0) 最好 → (0,1) 次之 → (1,0) → (1,1)；目标：少写回、快淘汰", fs=15)
    # 环上的 6 个页框
    import math
    frames = [("页5", 0, 1), ("页9", 1, 1), ("页2", 0, 1), ("页7", 0, 0), ("页3", 1, 0), ("页1", 0, 0)]
    cx, cy, r = 6.25, 3.3, 1.9
    pos = []
    for i in range(6):
        ang = math.pi / 2 + i * math.pi / 3
        x, y = cx + r * math.cos(ang), cy + r * math.sin(ang)
        pos.append((x, y))
    for i, (pg, a, m) in enumerate(frames):
        x, y = pos[i]
        color = GREEN_L if (a == 0 and m == 0) else (AMBER_L if a == 0 else GRAY_L)
        ec = GREEN if (a == 0 and m == 0) else (AMBER if a == 0 else GRAY)
        osfig.circle(ax, x, y, 0.62, pg + "\n(" + str(a) + "," + str(m) + ")", fc=color, ec=ec, fs=10, bold=True, lw=2)
    osfig.tx(ax, cx, cy, "指针", fs=11, bold=True, color=RED)
    osfig.arrow(ax, cx + 0.45, cy + 0.15, 5.7, 4.55, "", color=RED, lw=2.2, ms=18)
    # 步骤
    steps = [
        "第 1 轮：指针扫一圈找 (0,0) → 命中页7？无空闲则直接选它淘汰（最佳候选）",
        "若第 1 轮全miss：第 2 轮找 (0,1)——途中顺手把扫过的 A 位清 0（不置换）",
        "若第 2 轮仍无：回到 (0,0) 必然有了（上一轮清出来的）；再不行才轮到 (1,x)",
    ]
    y = 1.35
    for s in steps:
        osfig.tx(ax, 6.25, y, s, fs=10.5, color=INK)
        y -= 0.42
    osfig.tx(ax, 6.25, 0.3, "【考点】为什么偏爱 M=0？——淘汰「没改过的页」不用写回磁盘，省一次慢速 I/O；「先清 A 再扫」给页面第二次机会", fs=10.5, color=RED, bold=True)
    osfig.save(fig, F("ch3-28_clock_rounds.png"))


# ---------- ch3-29 工作集例 ----------
def f29():
    fig, ax = osfig.new_fig(12.5, 5.6, xlim=(0, 12.5), ylim=(0, 5.6))
    osfig.title(ax, "工作集：最近 Δ 次访问用到的页的集合",
                sub="访问串 2,6,1,5,6,2,1,2,5,6，Δ=4：滑动窗口逐时刻算工作集", fs=15)
    seq = ["2", "6", "1", "5", "6", "2", "1", "2", "5", "6"]
    windows = [
        ("2,6,1,5", "{2,6,1,5}"),
        ("6,1,5,6", "{1,5,6}"),
        ("1,5,6,2", "{1,2,5,6}"),
        ("5,6,2,1", "{1,2,5,6}"),
    ]
    x0 = 0.9
    for i, p in enumerate(seq):
        osfig.circle(ax, x0 + i * 1.15, 4.3, 0.42, p, fc=BLUE_L, ec=BLUE, fs=12, bold=True)
    osfig.tx(ax, 6.25, 3.35, "滑动窗口（Δ=4）逐时刻的工作集：", fs=12, bold=True, color=INK)
    y = 2.75
    for w, ws in windows:
        osfig.tx(ax, 4.0, y, "最近 4 次: " + w, fs=11, color=GRAY, ha="left")
        osfig.tx(ax, 8.2, y, "工作集 = " + ws, fs=11.5, color=GREEN, bold=True, ha="left")
        y -= 0.5
    osfig.tx(ax, 6.25, 1.0, "用途：给进程的常驻集 ≥ 工作集，才不会频繁缺页（抖动）", fs=11.5, bold=True, color=BLUE)
    osfig.tx(ax, 6.25, 0.45, "【考点】工作集是「时间 × 页集合」的动态概念；多道程序度过高 → 各进程工作集装不下 → 抖动 → 挂起部分进程", fs=10.5, color=RED, bold=True)
    osfig.save(fig, F("ch3-29_workingset_example.png"))


# ---------- ch3-30 局部 vs 全局置换 ----------
def f30():
    fig, ax = osfig.new_fig(12.5, 5.8, xlim=(0, 12.5), ylim=(0, 5.8))
    osfig.title(ax, "局部置换 vs 全局置换：缺页时「换谁」",
                sub="局部=只在自己分到的帧里挑替死鬼；全局=可以抢别人（别的进程）的帧", fs=15)
    # 局部
    osfig.tx(ax, 3.2, 4.95, "局部置换", fs=13, bold=True, color=BLUE)
    osfig.rect(ax, 0.9, 3.6, 4.6, 0.9, "进程 P 的帧池（固定 3 帧）", fc=BLUE_L, ec=BLUE, fs=11, bold=True)
    osfig.rect(ax, 0.9, 2.8, 4.6, 0.55, "缺页 → 在这 3 帧里选一页换出", fc="white", ec=BLUE, fs=10.5)
    osfig.tx(ax, 3.2, 2.3, "P 缺页再频繁，也动不了别人的帧", fs=10.5, color=GRAY)
    osfig.tx(ax, 3.2, 1.85, "缺点：帧太少时怎么换都缺（被动挨打）", fs=10.5, color=RED)
    # 全局
    osfig.tx(ax, 9.3, 4.95, "全局置换", fs=13, bold=True, color=PURPLE)
    osfig.rect(ax, 7.0, 3.6, 4.6, 0.9, "整个系统的帧池", fc=PURPLE_L, ec=PURPLE, fs=11, bold=True)
    osfig.rect(ax, 7.0, 2.8, 4.6, 0.55, "缺页 → 可换出任何进程的页", fc="white", ec=PURPLE, fs=10.5)
    osfig.tx(ax, 9.3, 2.3, "优点：谁顺手换谁，系统总缺页率低", fs=10.5, color=GREEN)
    osfig.tx(ax, 9.3, 1.85, "缺点：P 的缺页率受别人影响（不可控）", fs=10.5, color=AMBER)
    osfig.tx(ax, 6.25, 1.0, "【考点】固定分配 + 局部置换 / 可变分配 + 全局置换 / 可变分配 + 局部置换（缺页频繁时多给几帧）——「固定 + 全局」无意义（全局必然可变）", fs=10.5, color=RED, bold=True)
    osfig.tx(ax, 6.25, 0.45, "【易错】「全局置换比局部置换好」不绝对——实时/安全场景更需要「我的缺页率我自己可控」（局部）", fs=10.5, color=AMBER)
    osfig.save(fig, F("ch3-30_local_vs_global.png"))


if __name__ == "__main__":
    f20(); f21(); f22(); f23(); f24(); f25(); f26(); f27(); f28(); f29(); f30()
    print("ch3 extras done")
