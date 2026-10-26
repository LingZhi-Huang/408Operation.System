# -*- coding: utf-8 -*-
"""第4章 扩写新增插图（ch4-18 ~ ch4-28）。运行：python3 draw_figures_extra.py"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (INK, BLUE, BLUE_L, GREEN, GREEN_L, AMBER, AMBER_L,
                   RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L, GRAY, GRAY_L,
                   PINK, PINK_L)

FIG = "/Users/levi/IdeaProjects/操作系统/第4章_文件管理/figures/"
F = lambda n: FIG + n


# ---------- ch4-18 打开文件表 ----------
def f18():
    fig, ax = osfig.new_fig(12.5, 6.2, xlim=(0, 12.5), ylim=(0, 6.2))
    osfig.title(ax, "open() 的内幕：两级打开文件表与 fd",
                sub="打开=把 FCB 从磁盘调入内存打开文件表；以后读写只凭 fd 编号，不再重复检索目录", fs=15)
    # 进程
    osfig.rbox(ax, 0.7, 3.4, 2.6, 1.4, "进程 A\n\nfd 表：\n0→标准输入\n3→fd 槽", fc=BLUE_L, ec=BLUE, fs=10.5, bold=True, ls=1.5)
    # 系统级表
    osfig.rbox(ax, 4.6, 2.7, 3.6, 2.8, "", fc=GREEN_L, ec=GREEN)
    osfig.tx(ax, 6.4, 5.1, "系统级打开文件表（全系统一张）", fs=11.5, bold=True, color=GREEN)
    osfig.tx(ax, 6.4, 4.3, "条目：FCB 副本（读写指针、\n共享计数、访问权限…）\n——《notes.txt》\n——《photo.jpg》", fs=10, ls=1.6)
    osfig.tx(ax, 6.4, 3.05, "引用计数：几个进程打开它", fs=9.5, color=GRAY)
    # FCB/inode
    osfig.rbox(ax, 9.5, 2.7, 2.3, 2.8, "", fc=AMBER_L, ec=AMBER)
    osfig.tx(ax, 10.65, 5.1, "磁盘上的 FCB", fs=11.5, bold=True, color=AMBER)
    osfig.tx(ax, 10.65, 3.9, "位置、大小、\n属主、权限、\n时间戳、块指针", fs=10.5, ls=1.8)
    osfig.arrow(ax, 3.3, 4.3, 4.6, 4.3, "open(\"notes.txt\") 返回 fd=3", color=BLUE, fs=9.5, dy=-0.3)
    osfig.arrow(ax, 8.2, 4.3, 9.5, 4.3, "首次打开时复制", color=AMBER, fs=9.5, dy=0.28)
    osfig.tx(ax, 6.25, 1.7, "为什么要 open？——检索目录（按名找 FCB）很慢，一次检索多次使用；close 使计数-1，归 0 才真正关闭", fs=11, color=INK)
    osfig.tx(ax, 6.25, 1.1, "父子进程 fork 后共享打开文件表条目 → 引用计数再 +1；一方读会移动共享的读写指针", fs=10.5, color=GRAY)
    osfig.tx(ax, 6.25, 0.55, "【考点】read/write 只需要 fd（编号）；「打开文件表在内存」判断题常考", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch4-18_open_file_tables.png"))


# ---------- ch4-19 索引文件查找例 ----------
def f19():
    fig, ax = osfig.new_fig(12, 5.8, xlim=(0, 12), ylim=(0, 5.8))
    osfig.title(ax, "索引文件：变长记录也能「随机」查找",
                sub="为变长记录文件建一张索引表（按关键字排序）→ 顺序查找变二分查找", fs=15)
    # 记录文件
    osfig.tx(ax, 2.2, 4.95, "主文件（变长记录）", fs=12, bold=True, color=GRAY)
    recs = ["张伟 1000字", "李娜 300字", "王强 800字", "赵敏 200字"]
    y = 4.3
    for r in recs:
        osfig.rect(ax, 0.9, y, 2.6, 0.5, r, fc=GRAY_L, ec=GRAY, fs=10)
        y -= 0.62
    # 索引表
    osfig.tx(ax, 6.4, 4.95, "索引表（按姓名排序，定长项）", fs=12, bold=True, color=BLUE)
    idx = [("李娜", 1), ("王强", 3), ("张伟", 0), ("赵敏", 4)]
    y = 4.3
    for name, ptr in idx:
        osfig.rect(ax, 5.1, y, 1.3, 0.5, name, fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
        osfig.rect(ax, 6.4, y, 1.3, 0.5, "指针→" + str(ptr), fc="white", ec=BLUE, fs=9.5)
        y -= 0.62
    osfig.arrow(ax, 5.75, 4.3, 2.2, 4.3, "", color=BLUE, lw=1.4, ms=10)
    osfig.tx(ax, 6, 1.4, "查找「王强」：主文件顺序找要 3 次比较；索引表二分只需 2 次；10^6 条记录 → 50 次 vs 20 次", fs=11, color=INK)
    osfig.tx(ax, 6, 0.8, "索引表本身定长有序 → 可整表装入内存快速查找", fs=11, color=GRAY)
    osfig.tx(ax, 6, 0.3, "【考点】索引文件解决的是「变长记录的快速检索」；索引顺序文件再进一步：分组 √N 查找", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch4-19_index_file_access.png"))


# ---------- ch4-20 多层索引计算 ----------
def f20():
    fig, ax = osfig.new_fig(12.5, 6.0, xlim=(0, 12.5), ylim=(0, 6.0))
    osfig.title(ax, "多层索引的算账模板（块 4KB、地址 4B）",
                sub="每块可存 4KB/4B = 1024 个地址；每上一层，可寻址大小 ×1024", fs=15)
    levels = [
        ("单级索引", "1 个索引块", "1024 × 4KB = 4MB", "读数据：2 次访盘（索引块+数据块）"),
        ("两级索引", "1 + 1024 个索引块", "1024 × 1024 × 4KB = 4GB", "读数据：3 次访盘"),
        ("三级索引", "1 + 1024 + 1024^2 个索引块", "1024^3 × 4KB = 4TB", "读数据：4 次访盘"),
    ]
    y = 4.9
    for name, blocks, cap, cost in levels:
        y -= 1.35
        osfig.rbox(ax, 0.7, y, 2.2, 1.15, name, fc=BLUE_L, ec=BLUE, fs=12, bold=True)
        osfig.tx(ax, 4.3, y + 0.85, blocks, fs=11, ha="left", color=INK)
        osfig.tx(ax, 4.3, y + 0.35, "可寻址：" + cap, fs=11.5, ha="left", color=GREEN, bold=True)
        osfig.tx(ax, 4.3, y - 0.1, cost, fs=10.5, ha="left", color=RED)
    osfig.tx(ax, 6.25, 1.05, "通用公式：N 级索引可寻址 = (块大小/地址大小)^N × 块大小；访盘次数 = N + 1", fs=11.5, bold=True, color=BLUE)
    osfig.tx(ax, 6.25, 0.5, "【易错】「最大的文件」要问清「是否含直接地址」——UNIX 混合索引最大 = 直接10块+一级+二级+三级", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch4-20_multilevel_index_calc.png"))


# ---------- ch4-21 FAT 查表示例 ----------
def f21():
    fig, ax = osfig.new_fig(12.5, 6.6, xlim=(0, 12.5), ylim=(0, 6.6))
    osfig.title(ax, "显式链接（FAT）：读第 i 块为什么只需 1 次访盘",
                sub="FAT 整表驻内存：链是「纸上」的，查 k 个逻辑块只在内存表里跳 k 次，最后 1 次读盘取数", fs=15)
    # FAT 表
    osfig.tx(ax, 2.4, 5.35, "FAT（常驻内存）", fs=12, bold=True, color=BLUE)
    fat = [("2", "5"), ("3", "(EOF)"), ("5", "7"), ("7", "3")]
    y = 4.25
    osfig.rect(ax, 0.9, 4.75, 1.2, 0.5, "块号", fc=GRAY_L, ec=GRAY, fs=10, bold=True)
    osfig.rect(ax, 2.1, 4.75, 1.2, 0.5, "下一块", fc=GRAY_L, ec=GRAY, fs=10, bold=True)
    for cur, nxt in fat:
        y -= 0.55
        osfig.rect(ax, 0.9, y, 1.2, 0.55, cur, fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
        osfig.rect(ax, 2.1, y, 1.2, 0.55, nxt, fc="white", ec=BLUE, fs=10.5)
    # 磁盘
    osfig.tx(ax, 9.3, 5.35, "磁盘上的数据块", fs=12, bold=True, color=TEAL)
    disks = ["块2", "块5", "块7", "块3"]
    for i, d in enumerate(disks):
        osfig.rect(ax, 7.9 + i * 1.15, 4.0, 1.05, 0.7, d, fc=TEAL_L, ec=TEAL, fs=10.5, bold=True)
    osfig.arrow(ax, 8.4, 3.9, 9.5, 3.9, "", color=TEAL, lw=1.4, ls=":")
    osfig.tx(ax, 6.25, 2.7, "读文件第 3 块（逻辑）的完整过程：", fs=12, bold=True, color=INK)
    osfig.tx(ax, 6.25, 2.15, "① 查 FAT：块2 → 块5 → 块7（内存里跳 3 次，0 次访盘）", fs=11, color=INK)
    osfig.tx(ax, 6.25, 1.7, "② 按块7 的物理地址直接读盘 1 次 → 拿到数据", fs=11, color=INK)
    osfig.tx(ax, 6.25, 1.15, "对比隐式链接：指针藏在块里，要真的把块2、块5 逐个读盘才能找到块7 → 4 次访盘", fs=11, color=RED)
    osfig.tx(ax, 6.25, 0.5, "【考点】FAT 代价 = 占内存空间；换来 = 「随机访问任一块只需 1 次访盘」", fs=11.5, color=RED, bold=True)
    osfig.save(fig, F("ch4-21_fat_walkthrough.png"))


# ---------- ch4-22 目录树路径 ----------
def f22():
    fig, ax = osfig.new_fig(12, 5.6, xlim=(0, 12), ylim=(0, 5.6))
    osfig.title(ax, "树形目录：绝对路径 vs 相对路径",
                sub="绝对路径从根 / 出发；相对路径从「当前目录」出发——改的是检索的起点，不改变树结构", fs=15)
    # 树
    osfig.box(ax, 2.2, 4.6, 1.2, 0.6, "root /", fc=GRAY_L, ec=GRAY, fs=11, bold=True)
    osfig.box(ax, 1.0, 3.4, 1.2, 0.6, "usr", fc=BLUE_L, ec=BLUE, fs=11, bold=True)
    osfig.box(ax, 3.4, 3.4, 1.2, 0.6, "home", fc=BLUE_L, ec=BLUE, fs=11, bold=True)
    osfig.box(ax, 2.9, 2.2, 1.2, 0.6, "levi", fc=GREEN_L, ec=GREEN, fs=11, bold=True)
    osfig.box(ax, 4.7, 2.2, 1.3, 0.6, "notes.md", fc=AMBER_L, ec=AMBER, fs=10, bold=True)
    osfig.line(ax, 2.0, 4.3, 1.3, 3.7, color=GRAY, lw=1.5)
    osfig.line(ax, 2.5, 4.3, 3.3, 3.7, color=GRAY, lw=1.5)
    osfig.line(ax, 3.1, 3.1, 3.2, 2.5, color=GRAY, lw=1.5)
    osfig.line(ax, 3.7, 3.1, 4.9, 2.5, color=GRAY, lw=1.5)
    # 路径对照
    osfig.tx(ax, 8.6, 4.5, "绝对路径（从根开始）：", fs=12, bold=True, color=BLUE)
    osfig.tx(ax, 8.6, 4.0, "  /home/levi/notes.md", fs=12, color=INK)
    osfig.tx(ax, 8.6, 3.3, "若当前目录 = /home/levi：", fs=12, bold=True, color=GREEN)
    osfig.tx(ax, 8.6, 2.8, "  相对路径 = notes.md", fs=12, color=INK)
    osfig.tx(ax, 8.6, 2.3, "  上级 = .. （/home）", fs=12, color=INK)
    osfig.tx(ax, 6, 1.3, "路径检索 = 逐级查目录文件：先查 home 目录的 FCB → 读入 → 查 levi → 再读入 → 查 notes.md", fs=11, color=INK)
    osfig.tx(ax, 6, 0.7, "【考点】「设置当前目录可加快检索」对；「相对路径必须从根目录开始」错", fs=11, color=RED, bold=True)
    osfig.tx(ax, 6, 0.2, "【延伸】每次目录检索都可能读盘一次 → 引入 inode 减少目录项体积，让一个磁盘块装更多目录项", fs=10.5, color=GRAY)
    osfig.save(fig, F("ch4-22_dir_tree_paths.png"))


# ---------- ch4-23 ACL ----------
def f23():
    fig, ax = osfig.new_fig(12.5, 5.8, xlim=(0, 12.5), ylim=(0, 5.8))
    osfig.title(ax, "文件保护：从访问控制矩阵到 ACL 与能力表",
                sub="矩阵最直观但太稀疏；按「列」存=ACL（每个文件一份），按「行」存=能力表（每个用户一份）", fs=14.5)
    # 矩阵
    rows = ["张三", "李四", "访客"]
    cols = ["fileA", "fileB"]
    vals = [["读写", "读"], ["读", "读写"], ["-", "读"]]
    osfig.rect(ax, 0.9, 4.5, 1.4, 0.5, "", fc=GRAY_L, ec=GRAY)
    osfig.rect(ax, 2.3, 4.5, 1.6, 0.5, "fileA", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 3.9, 4.5, 1.6, 0.5, "fileB", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    y = 4.5
    for i, r in enumerate(rows):
        y -= 0.55
        osfig.rect(ax, 0.9, y, 1.4, 0.55, r, fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
        osfig.rect(ax, 2.3, y, 1.6, 0.55, vals[i][0], fc="white", ec=GRAY, fs=10.5)
        osfig.rect(ax, 3.9, y, 1.6, 0.55, vals[i][1], fc="white", ec=GRAY, fs=10.5)
    osfig.tx(ax, 3.2, 2.6, "访问控制矩阵", fs=11.5, bold=True, color=INK)
    # ACL
    osfig.rbox(ax, 6.2, 2.9, 2.8, 2.1, "", fc=BLUE_L, ec=BLUE)
    osfig.tx(ax, 7.6, 4.65, "ACL（按列存）", fs=11.5, bold=True, color=BLUE)
    osfig.tx(ax, 7.6, 3.75, "挂在 fileA 上：\n张三:读写\n李四:读\n访客:无", fs=10.5, ls=1.7)
    # 能力表
    osfig.rbox(ax, 9.5, 2.9, 2.4, 2.1, "", fc=GREEN_L, ec=GREEN)
    osfig.tx(ax, 10.7, 4.65, "能力表（按行存）", fs=11.5, bold=True, color=GREEN)
    osfig.tx(ax, 10.7, 3.75, "张三随身带：\nfileA:读写\nfileB:读", fs=10.5, ls=1.7)
    osfig.tx(ax, 6.25, 1.7, "ACL：看「某个文件谁能动」很方便（按对象管）；能力表：看「某个人能动什么」很方便（按主体管）", fs=11, color=INK)
    osfig.tx(ax, 6.25, 1.1, "Linux 的 rwx 权限位 = 简化的 ACL（按 属主/属组/其他人 三类各给 rwx）", fs=11, color=TEAL)
    osfig.tx(ax, 6.25, 0.45, "【考点】「能力表按用户（行）存储」判断题常考；口诀：列=ACL 挂文件，行=能力跟人走", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch4-23_acl_matrix.png"))


# ---------- ch4-24 空闲表与空闲链 ----------
def f24():
    fig, ax = osfig.new_fig(12.5, 5.6, xlim=(0, 12.5), ylim=(0, 5.6))
    osfig.title(ax, "空闲表法 与 空闲链表法：连续分配时代的管理器",
                sub="空闲表=记「起始块号+长度」的区段表；空闲链=把空闲块（或空闲区）用指针串起来", fs=15)
    # 空闲表
    osfig.tx(ax, 3.0, 4.95, "空闲表法（配合连续分配）", fs=12.5, bold=True, color=BLUE)
    osfig.rect(ax, 0.9, 4.25, 1.7, 0.5, "起始块号", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 2.6, 4.25, 1.7, 0.5, "空闲块数", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    data = [("3", "5"), ("12", "8"), ("30", "20")]
    y = 4.25
    for a, b in data:
        y -= 0.55
        osfig.rect(ax, 0.9, y, 1.7, 0.55, a, fc=BLUE_L, ec=BLUE, fs=10.5)
        osfig.rect(ax, 2.6, y, 1.7, 0.55, b, fc=BLUE_L, ec=BLUE, fs=10.5)
    osfig.tx(ax, 2.5, 2.3, "分配算法同动态分区：\n首次/最佳适应", fs=10.5, color=INK)
    osfig.tx(ax, 2.5, 1.55, "回收要合并相邻空闲区", fs=10.5, color=RED)
    # 空闲链
    osfig.tx(ax, 9.3, 4.95, "空闲链表法", fs=12.5, bold=True, color=GREEN)
    chain = [("盘块链\n一块一节点", TEAL), ("盘区链\n一区一节点", GREEN)]
    for i, (t, c) in enumerate(chain):
        osfig.rbox(ax, 6.6 + i * 2.8, 3.3, 2.6, 1.2, t, fc=TEAL_L if i == 0 else GREEN_L, ec=c, fs=10.5, bold=True, ls=1.5)
    osfig.tx(ax, 9.3, 2.5, "分配 = 摘链；回收 = 插链（盘区链也要合并相邻区）", fs=10.5, color=INK)
    osfig.tx(ax, 9.3, 2.0, "优点：实现简单；缺点：不能随机访问、链太长", fs=10.5, color=GRAY)
    osfig.tx(ax, 6.25, 1.0, "对比位示图：位图用一个 bit 表示一个块的状态——可随机查、占空间小，是现代文件系统的主流", fs=11, color=BLUE, bold=True)
    osfig.tx(ax, 6.25, 0.4, "【考点】空闲表法用于「连续分配方案」；位示图/成组链接用于「离散分配方案」——搭配关系要记牢", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch4-24_free_table_chain.png"))


# ---------- ch4-25 位图练习 ----------
def f25():
    fig, ax = osfig.new_fig(12.5, 5.4, xlim=(0, 12.5), ylim=(0, 5.4))
    osfig.title(ax, "专项训练：位示图互算（字长 32 位，从 0 编号）",
                sub="公式：盘块号 b = 字号 i × 32 + 位号 j；反推：i = b div 32，j = b mod 32", fs=14.5)
    cases = [
        ("b = 25", "i = 25 div 32 = 0", "j = 25", "(0 号字, 25 位)"),
        ("b = 65", "i = 65 div 32 = 2", "j = 1", "(2 号字, 1 位)"),
        ("b = 100", "i = 100 div 32 = 3", "j = 4", "(3 号字, 4 位)"),
        ("(i=5, j=30)", "b = 5×32 + 30 = 190", "—", "反向同样一步"),
    ]
    osfig.rect(ax, 0.7, 4.2, 2.2, 0.5, "已知", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 2.9, 4.2, 3.0, 0.5, "求字号 i", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 5.9, 4.2, 2.2, 0.5, "求位号 j", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 8.1, 4.2, 3.3, 0.5, "结论", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    y = 4.2
    for known, i, j, con in cases:
        y -= 0.6
        osfig.rect(ax, 0.7, y, 2.2, 0.6, known, fc=BLUE_L, ec=BLUE, fs=10.5, bold=True)
        osfig.rect(ax, 2.9, y, 3.0, 0.6, i, fc="white", ec=GRAY, fs=10.5)
        osfig.rect(ax, 5.9, y, 2.2, 0.6, j, fc="white", ec=GRAY, fs=10.5)
        osfig.rect(ax, 8.1, y, 3.3, 0.6, con, fc=GREEN_L, ec=GREEN, fs=10.5, bold=True)
    osfig.tx(ax, 6.25, 1.3, "警惕三个坑：① 从 0 编号（不是 1）；② 「字」是 32 位的一行；③ 有的教材位示图按行优先排列——公式一样，行=字号", fs=11, color=INK)
    osfig.tx(ax, 6.25, 0.65, "变体：若题目给「每字 16 位」→ 把 32 全部换成 16，套路不变", fs=11, color=TEAL)
    osfig.tx(ax, 6.25, 0.15, "【考点】位示图法适合离散分配；0/1 谁代表空闲要看题目约定（常见 0=空闲）", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch4-25_bitmap_exercises.png"))


# ---------- ch4-26 SCAN vs LOOK ----------
def f26():
    fig, ax = osfig.new_fig(12.5, 6.8, xlim=(0, 12.5), ylim=(0, 6.8))
    osfig.title(ax, "SCAN vs LOOK：差的就是「要不要跑到磁盘边缘」",
                sub="同数据（起点 53，请求 98,183,37,122,14,124,65,67，方向：向大）：SCAN=331，LOOK=299", fs=14.5)
    # SCAN 面板
    osfig.tx(ax, 3.2, 5.15, "SCAN（电梯）：扫到 199 才折返", fs=12, bold=True, color=BLUE)
    pts_scan = [53, 65, 67, 98, 122, 124, 183, 199, 37, 14]
    for i, p in enumerate(pts_scan):
        y = 4.5 - i * 0.38
        osfig.rect(ax, 1.0 + p / 199 * 3.2, y, 0.28, 0.24, "", fc=BLUE_L, ec=BLUE)
        osfig.tx(ax, 0.55, y + 0.12, str(p), fs=8, color=GRAY, ha="left")
        if i < len(pts_scan) - 1:
            osfig.line(ax, 1.0 + pts_scan[i + 1] / 199 * 3.2 + 0.14, y - 0.14 + 0.12, 1.0 + p / 199 * 3.2 + 0.14, y + 0.12, color=BLUE, lw=1.2)
    osfig.tx(ax, 3.2, 1.15, "SCAN 在 183 之后仍扫到边缘 199：白走 16 道", fs=10.5, color=RED)
    # LOOK 面板
    osfig.tx(ax, 9.3, 5.15, "LOOK：到最远请求 183 即折返", fs=12, bold=True, color=GREEN)
    pts_look = [53, 65, 67, 98, 122, 124, 183, 37, 14]
    for i, p in enumerate(pts_look):
        y = 4.5 - i * 0.38
        osfig.rect(ax, 7.1 + p / 199 * 3.2, y, 0.28, 0.24, "", fc=GREEN_L, ec=GREEN)
        osfig.tx(ax, 6.65, y + 0.12, str(p), fs=8, color=GRAY, ha="left")
        if i < len(pts_look) - 1:
            osfig.line(ax, 7.1 + pts_look[i + 1] / 199 * 3.2 + 0.14, y - 0.14 + 0.12, 7.1 + p / 199 * 3.2 + 0.14, y + 0.12, color=GREEN, lw=1.2)
    osfig.tx(ax, 9.3, 1.15, "LOOK 到 183 就折返：省 16 道 → 总寻道 299", fs=10.5, color=GREEN)
    osfig.tx(ax, 6.25, 0.6, "【考点】SCAN「到边缘」= 对新请求更公平（中途方向的请求总要被扫到）；LOOK「到最远请求」= 更省；C-SCAN 之于 C-LOOK 同理（382 vs 322）", fs=10.5, color=RED, bold=True)
    osfig.save(fig, F("ch4-26_scan_look_diff.png"))


# ---------- ch4-27 格式化 ----------
def f27():
    fig, ax = osfig.new_fig(12, 5.4, xlim=(0, 12), ylim=(0, 5.4))
    osfig.title(ax, "磁盘的两级格式化：低级格式化 与 逻辑格式化",
                sub="低级=物理「划地皮」；逻辑=搭「管理班子」（根目录、空闲管理结构）", fs=15)
    # 低级
    osfig.rbox(ax, 0.8, 1.4, 5.0, 3.3, "", fc=BLUE_L, ec=BLUE)
    osfig.tx(ax, 3.3, 4.35, "低级格式化（物理/分区前）", fs=12.5, bold=True, color=BLUE)
    osfig.tx(ax, 3.3, 3.4, "把每个磁道划分成扇区；\n每个扇区 = 头部 P 域 + 数据 512B + 尾部 V 域\n（P/V 存扇区校验与控制信息）", fs=11, ls=1.7)
    osfig.tx(ax, 3.3, 2.2, "通常出厂前完成；用户一般不做", fs=10.5, color=GRAY)
    osfig.tx(ax, 3.3, 1.75, "坏块检测与标记也在此阶段处理", fs=10.5, color=GRAY)
    # 逻辑
    osfig.rbox(ax, 6.2, 1.4, 5.0, 3.3, "", fc=GREEN_L, ec=GREEN)
    osfig.tx(ax, 8.7, 4.35, "逻辑格式化（高级/建文件系统）", fs=12.5, bold=True, color=GREEN)
    osfig.tx(ax, 8.7, 3.4, "初始化文件系统的管理数据：\n空闲空间管理结构（位图/FAT…）\n空闲分区表、根目录", fs=11, ls=1.7)
    osfig.tx(ax, 8.7, 2.2, "我们日常「格式化D盘」就是这一级", fs=10.5, color=GRAY)
    osfig.tx(ax, 8.7, 1.75, "装 OS 前 / 换文件系统（NTFS↔ext4）时做", fs=10.5, color=GRAY)
    osfig.tx(ax, 6, 0.7, "顺序：低级格式化 → 分区 → 逻辑格式化 → 装 OS", fs=12, bold=True, color=INK)
    osfig.tx(ax, 6, 0.25, "【考点】「逻辑格式化会建立根目录与空闲管理结构」对；「低级格式化建立根目录」错", fs=11, color=RED, bold=True)
    osfig.save(fig, F("ch4-27_format_levels.png"))


# ---------- ch4-28 UNIX 区间计算练习 ----------
def f28():
    fig, ax = osfig.new_fig(12.5, 6.2, xlim=(0, 12.5), ylim=(0, 6.2))
    osfig.title(ax, "UNIX 混合索引专项：给偏移量，算访盘次数",
                sub="块 4KB、地址 4B（每索引块 1024 项）；inode 已在内存；直接 10 块 = 40KB", fs=14.5)
    # 区间表
    zones = [
        ("0 ~ 40KB", "直接地址(0~9)", "1 次（直接读数据块）", GREEN),
        ("40KB ~ 4MB+40KB", "一级间接", "2 次（读一级索引块+数据块）", BLUE),
        ("~ 4GB+...", "二级间接", "3 次（读二级+一级索引块+数据块）", AMBER),
        ("~ 4TB+...", "三级间接", "4 次", RED),
    ]
    osfig.rect(ax, 0.7, 4.9, 2.6, 0.5, "文件偏移区间", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 3.3, 4.9, 2.6, 0.5, "落在哪个区", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    osfig.rect(ax, 5.9, 4.9, 5.6, 0.5, "读这一块需要访盘", fc=GRAY_L, ec=GRAY, fs=10.5, bold=True)
    y = 4.9
    for zone, reg, cost, c in zones:
        y -= 0.72
        osfig.rect(ax, 0.7, y, 2.6, 0.72, zone, fc="white", ec=GRAY, fs=10)
        osfig.rect(ax, 3.3, y, 2.6, 0.72, reg, fc="white", ec=c, fs=10, bold=True)
        osfig.rect(ax, 5.9, y, 5.6, 0.72, cost, fc="white", ec=c, fs=10)
    osfig.tx(ax, 6.25, 1.55, "例：偏移 = 5000 字节 → 5000 div 4096 = 1（第 1 个逻辑块）< 10 → 直接地址 → 访盘 1 次", fs=11, color=INK)
    osfig.tx(ax, 6.25, 1.0, "例：偏移 = 5MB → 5MB/4KB = 1280 号逻辑块；1280 ≥ 10 → 一级间接区（块号 1280-10=1270 < 1024）→ 访盘 2 次", fs=11, color=INK)
    osfig.tx(ax, 6.25, 0.45, "【易错】① 先换算成「逻辑块号」再判断区间；② 减掉直接块的 10 块；③ 若题目说索引块也要先从盘读入且未缓存，才计入次数", fs=10.5, color=RED, bold=True)
    osfig.save(fig, F("ch4-28_unix_index_calc.png"))


if __name__ == "__main__":
    f18(); f19(); f20(); f21(); f22(); f23(); f24(); f25(); f26(); f27(); f28()
    print("ch4 extras done")
