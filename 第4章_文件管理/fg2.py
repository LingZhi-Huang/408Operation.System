# -*- coding: utf-8 -*-
"""第4章 插图 第二部分：ch4-07 ~ ch4-12"""
import sys
sys.path.insert(0, "/Users/levi/IdeaProjects/操作系统")
import osfig
from osfig import (new_fig, rbox, box, rect, diamond, ellipse, circle, arrow,
                   line, tx, title, save, INK, BLUE, BLUE_L, GREEN, GREEN_L,
                   AMBER, AMBER_L, RED, RED_L, PURPLE, PURPLE_L, TEAL, TEAL_L,
                   GRAY, GRAY_L, PINK, PINK_L)

FDIR = "/Users/levi/IdeaProjects/操作系统/第4章_文件管理/figures/"


def f07():
    fig, ax = new_fig(15, 10.2, (0, 15), (0, 10.2))
    title(ax, "同一场景比较：读文件的第 i 块，各物理结构各需几次访盘？",
          "假设：文件已打开（FCB/索引块指针已知）；FAT 常驻内存；i 为逻辑块号", y=9.7)
    cases = [
        ("连续分配", "1 次访盘", BLUE, BLUE_L,
         "物理块号 = 起始块号 + i\n公式直接算出，一步读到数据", "无需额外表", "随机存取最快\n扩展难、外部碎片"),
        ("隐式链接", "i 次访盘", TEAL, TEAL_L,
         "第 i 块的块号藏在前一块的尾部\n必须从首块开始，逐个读链", "指针在块内\n(4B/块)", "只能顺序存取\n坏一块断链"),
        ("显式链接 FAT", "1 次访盘", GREEN, GREEN_L,
         "FAT 驻内存，查表 O(1) 得块号\n再读数据一次盘", "FAT 整表\n占用额外空间", "随机存取快\nFAT 损坏则全丢"),
        ("单级索引", "2 次访盘", AMBER, AMBER_L,
         "先读索引块(1 次)取块号\n再读数据块(1 次)", "索引块\n(每文件一个)", "随机存取\n小文件也要读索引块"),
    ]
    xs = [0.4, 4.0, 7.6, 11.2]
    for (name, cnt, cc, cl, d1, d2, d3), x0 in zip(cases, xs):
        rbox(ax, x0, 5.45, 3.4, 3.55, fc=cl, ec=cc)
        tx(ax, x0 + 1.7, 8.66, name, fs=13, bold=True, color=cc)
        rbox(ax, x0 + 0.55, 7.2, 2.3, 1.05, cnt, fc=GRAY_L, ec=GRAY, fs=15, bold=True, color=RED)
        tx(ax, x0 + 1.7, 6.55, d1, fs=9.6)
        tx(ax, x0 + 1.7, 5.75, "开销：" + d2, fs=9.4, color=INK)
    tx(ax, 7.5, 5.0, "结论：连续分配与显式链接 FAT 均能 O(1) 随机访问；隐式链接是唯一的顺序访问；单级索引多一次读索引块的开销",
       fs=11, bold=True, color=RED)
    # 结论表
    tx(ax, 7.5, 4.45, "四种物理结构全对比", fs=13, bold=True)
    col_x = [0.4, 3.0, 5.4, 7.6, 9.9, 12.2]
    col_w = [2.6, 2.4, 2.2, 2.3, 2.3, 2.4]
    head = ["结构", "随机访问", "读第 i 块访盘次数", "额外空间", "顺序存取", "主要缺点"]
    for cxx, cww, h in zip(col_x, col_w, head):
        rect(ax, cxx, 3.55, cww, 0.62, h, fc=BLUE_L, ec=BLUE, fs=10, bold=True)
    rows = [
        ("连续分配", "√ 支持", "1 次", "无", "√ 快(磁头顺序移动)", "扩展难、外部碎片"),
        ("隐式链接", "× 不支持", "i 次", "块内指针", "√ 慢(沿链前进)", "断链风险、指针占空间"),
        ("显式链接 FAT", "√ 支持", "1 次", "整张 FAT 表", "√ 快", "FAT 占用大、易损"),
        ("单级索引", "√ 支持", "2 次", "索引块", "√ 快", "小文件读取也需索引块"),
    ]
    for r, row in enumerate(rows):
        y = 2.75 - r * 0.62
        for cxx, cww, v in zip(col_x, col_w, row):
            fc = GRAY_L if r % 2 == 0 else "white"
            rect(ax, cxx, y, cww, 0.62, v, fc=fc, ec=GRAY, fs=9.4, lw=1.0)
    tx(ax, 7.5, 0.5,
       "【记忆口诀】连续一笔、隐式排队、FAT 查表、索引查库：连续和 FAT 都是 1 次访盘读到数据，隐式链接第 i 块要 i 次，单级索引 2 次。",
       fs=10.5, bold=True, color=PURPLE)
    save(fig, FDIR + "ch4-07_access_compare.png")


def f08():
    fig, ax = new_fig(15, 11.4, (0, 15), (0, 11.4))
    title(ax, "目录结构的演进：单级 → 两级 → 树形 → 无环图",
          "目录管理的要求：按名存取、检索高效、支持文件共享", y=10.9)
    # Q1 单级
    rbox(ax, 0.4, 6.65, 7.2, 3.6, fc=BLUE_L, ec=BLUE)
    tx(ax, 3.35, 9.85, "① 单级目录结构", fs=12.5, bold=True, color=BLUE)
    rbox(ax, 0.7, 8.55, 2.0, 0.75, "目录", fc=GRAY_L, ec=GRAY, fs=10.5)
    items = ["文件A", "文件B", "文件C", "文件A", "…"]
    for i, it in enumerate(items):
        rbox(ax, 3.0 + i * 0.92, 8.55, 0.84, 0.75, it, fc=BLUE_L, ec=BLUE, fs=9)
    tx(ax, 3.35, 7.7, "所有文件全在一个目录下 → 无法重名（文件 A 冲突）", fs=9.6)
    tx(ax, 3.35, 6.95, "优点：结构最简单；缺点：重名冲突、检索慢、保护难；只适用于单用户单任务系统",
       fs=9.4, color=RED)
    # Q2 两级
    rbox(ax, 7.8, 6.65, 7.2, 3.6, fc=GREEN_L, ec=GREEN)
    tx(ax, 11.4, 9.85, "② 两级目录结构", fs=12.5, bold=True, color=GREEN)
    rbox(ax, 8.1, 8.8, 2.5, 0.65, "MFD（主文件目录）", fc=GRAY_L, ec=GRAY, fs=9.5)
    rbox(ax, 8.1, 7.15, 3.1, 1.45, "", fc=GREEN_L, ec=GREEN)
    tx(ax, 9.65, 8.28, "用户1 的 UFD", fs=9.2, bold=True, color=GREEN)
    rbox(ax, 8.55, 7.35, 1.25, 0.55, "文件1", fc=GREEN_L, ec=GREEN, fs=9)
    rbox(ax, 9.95, 7.35, 1.25, 0.55, "文件2", fc=GREEN_L, ec=GREEN, fs=9)
    rbox(ax, 11.6, 7.15, 3.1, 1.45, "", fc=GREEN_L, ec=GREEN)
    tx(ax, 13.15, 8.28, "用户2 的 UFD", fs=9.2, bold=True, color=GREEN)
    rbox(ax, 12.05, 7.35, 1.25, 0.55, "F3", fc=GREEN_L, ec=GREEN, fs=9)
    rbox(ax, 13.45, 7.35, 1.25, 0.55, "F4", fc=GREEN_L, ec=GREEN, fs=9)
    arrow(ax, 9.3, 8.8, 9.6, 8.62, color=GREEN, lw=1.2, ms=9)
    arrow(ax, 10.65, 8.95, 13.0, 8.62, color=GREEN, lw=1.2, ms=9)
    tx(ax, 11.4, 6.9, "优点：解决重名（不同用户目录可同名）；缺点：用户间不能共享文件",
       fs=9.0, color=RED)
    # Q3 树形
    rbox(ax, 0.4, 1.9, 7.2, 4.3, fc=AMBER_L, ec=AMBER)
    tx(ax, 3.35, 5.75, "③ 树形目录结构（现代通用）", fs=12.5, bold=True, color=AMBER)
    rbox(ax, 1.0, 4.75, 1.5, 0.7, "根目录 /", fc=GRAY_L, ec=GRAY, fs=10)
    rbox(ax, 0.9, 3.75, 1.3, 0.7, "usr", fc=AMBER_L, ec=AMBER, fs=9.5)
    rbox(ax, 3.5, 3.75, 1.3, 0.7, "user1", fc=AMBER_L, ec=AMBER, fs=9.5)
    rbox(ax, 5.9, 3.75, 1.3, 0.7, "docs", fc=AMBER_L, ec=AMBER, fs=9.5)
    arrow(ax, 1.75, 4.75, 1.55, 4.45, color=AMBER, lw=1.2, ms=9)
    arrow(ax, 2.2, 4.45, 3.15, 4.45, color=AMBER, lw=1.2, ms=9)
    arrow(ax, 3.0, 4.45, 3.85, 4.75, color=AMBER, lw=1.2, ms=9)
    arrow(ax, 4.15, 4.45, 5.5, 4.45, color=AMBER, lw=1.2, ms=9)
    rbox(ax, 4.0, 2.7, 1.4, 0.7, "作业.txt", fc=GRAY_L, ec=GRAY, fs=9)
    arrow(ax, 4.15, 3.75, 4.6, 3.4, color=AMBER, lw=1.2, ms=9)
    tx(ax, 3.35, 2.15,
       "绝对路径：/usr/user1/作业.txt（从根出发）\n相对路径：user1/作业.txt（从当前目录出发）\n优点：层次清晰、便于管理与保护、支持多用户；\n缺点：不便实现文件共享（共享路径要绕路）",
       fs=9.4, ha="left" if False else "center")
    # Q4 无环图
    rbox(ax, 7.8, 1.9, 7.2, 4.3, fc=PURPLE_L, ec=PURPLE)
    tx(ax, 11.2, 5.75, "④ 无环图目录结构（支持共享）", fs=12.5, bold=True, color=PURPLE)
    rbox(ax, 8.4, 4.6, 1.4, 0.7, "目录A", fc=GRAY_L, ec=GRAY, fs=9.5)
    rbox(ax, 10.4, 4.6, 1.4, 0.7, "目录B", fc=GRAY_L, ec=GRAY, fs=9.5)
    rbox(ax, 9.4, 3.4, 1.5, 0.7, "文件N\n(链接计数=2)", fc=PURPLE_L, ec=PURPLE, fs=9)
    arrow(ax, 9.1, 4.6, 9.8, 4.1, color=PURPLE, lw=1.2, ms=9)
    arrow(ax, 11.1, 4.6, 10.5, 4.1, color=PURPLE, lw=1.2, ms=9)
    tx(ax, 11.2, 3.0,
       "两个目录项指向同一文件 → 共享；应禁止成环（防止\n循环查找）；删除：仅对链接计数 -1，计数为 0 才真正释放\n（文件共享的具体实现见 4.5 节硬链接/软链接）",
       fs=9.4)
    # 演进箭头
    arrow(ax, 3.35, 6.6, 3.35, 6.3, color=GRAY, lw=2)
    arrow(ax, 11.2, 6.6, 11.2, 6.3, color=GRAY, lw=2)
    arrow(ax, 7.6, 4.0, 7.8, 4.0, color=GRAY, lw=2)
    tx(ax, 7.5, 1.15, "演进主线：解决重名 → 解决多用户隔离 → 层次化管理 → 支持共享（引入链接计数）",
       fs=10.5, bold=True, color=PURPLE)
    save(fig, FDIR + "ch4-08_directory_evolution.png")


def f09():
    fig, ax = new_fig(15, 9.8, (0, 15), (0, 9.8))
    title(ax, "FCB 与索引结点 inode：目录项瘦身术",
          "把 FCB 中与检索无关的信息挪到 inode 表中，目录项只留（文件名 + inode 号）", y=9.4)
    # 左：传统
    rbox(ax, 0.4, 4.9, 6.7, 3.9, fc=BLUE_L, ec=BLUE)
    tx(ax, 3.75, 8.4, "传统目录：目录项 = 完整 FCB（约 64B）", fs=12, bold=True, color=BLUE)
    tx(ax, 3.75, 7.7, "目录项内容：文件名(8B) + 类型 + 物理位置 + 长度 + 权限 + 时间…",
       fs=9.6)
    for i, nm in enumerate(["作业1.txt", "作业2.txt", "作业3.txt", "作业4.txt"]):
        rect(ax, 0.75 + i * 1.62, 6.8, 1.5, 0.85, nm, fc=BLUE_L, ec=BLUE, fs=9.2)
    rect(ax, 0.75, 6.0, 6.0, 0.55, "", fc=GRAY_L, ec=GRAY, lw=1.0)
    tx(ax, 3.75, 6.27, "一块(1KB)只能放 1024÷64 = 16 个目录项", fs=9.8, bold=True)
    tx(ax, 3.75, 5.35, "检索（如找作业4.txt）需读到的目录块多 → I/O 开销大", fs=9.4, color=RED)
    # 右：inode
    rbox(ax, 7.4, 4.9, 7.2, 3.9, fc=GREEN_L, ec=GREEN)
    tx(ax, 11.0, 8.4, "索引结点 inode 方案：目录项瘦身（约 12B）", fs=12, bold=True, color=GREEN)
    tx(ax, 11.0, 7.7, "目录项只存：文件名(8B) + inode 号(4B)；其余信息全部放进 inode 表",
       fs=9.6)
    for i, nm in enumerate(["作业1.txt", "作业2.txt", "作业3.txt", "作业4.txt"]):
        rect(ax, 7.75 + i * 1.62, 6.95, 1.5, 0.85, nm + "\ninode#3", fc=GREEN_L, ec=GREEN, fs=8.8)
        arrow(ax, 8.5 + i * 1.62, 6.95, 8.9 + i * 1.62, 6.4, color=GREEN, lw=1.0, ms=9)
    rect(ax, 7.75, 5.9, 6.0, 0.55, "", fc=GRAY_L, ec=GRAY, lw=1.0)
    tx(ax, 10.75, 6.17, "一块(1KB)可放 1024÷12 ≈ 85 个目录项，检索目录块数大减 → I/O 更少",
       fs=9.8, bold=True)
    tx(ax, 11.0, 5.35, "（注：不同系统目录项中还可能保留文件类型/长度等少量字段，原理相同）", fs=8.6, color=GRAY)
    # 下：inode 表
    rbox(ax, 0.4, 0.75, 14.2, 3.55, fc=PURPLE_L, ec=PURPLE)
    tx(ax, 7.5, 3.95, "磁盘 inode 表（每文件一项，按 inode 号索引；文件打开后 inode 调入内存）",
       fs=12, bold=True, color=PURPLE)
    flds = ["链接计数(共享数)", "文件属主 ID", "存取权限(rwx)",
            "创建/修改/访问时间", "数据块指针(直接+间接)", "文件长度与类型"]
    for i, f in enumerate(flds):
        x = 0.75 + (i % 3) * 4.6
        y = 2.95 - (i // 3) * 1.0
        rect(ax, x, y, 4.35, 0.8, f, fc=PURPLE_L, ec=PURPLE, fs=10)
    tx(ax, 7.5, 1.1,
       "为什么文件名不进 inode？\n—— 文件名是【目录项】的内容；多个目录项可指向同一 inode（硬链接），inode 中若存文件名就冲突了。",
       fs=9.8, bold=True, color=RED)
    save(fig, FDIR + "ch4-09_inode.png")


def f10():
    fig, ax = new_fig(15, 9.4, (0, 15), (0, 9.4))
    title(ax, "文件共享：硬链接 vs 软链接（符号链接）",
          "硬链接 = 多个目录项共享同一 inode；软链接 = 独立小文件，内容是目标路径", y=8.9)
    # ---------- 左：硬链接
    rbox(ax, 0.4, 0.7, 7.1, 7.45, fc=BLUE_L, ec=BLUE)
    tx(ax, 3.95, 7.75, "硬链接 Hard Link", fs=13, bold=True, color=BLUE)
    rbox(ax, 0.75, 6.65, 2.7, 0.8, "目录项 file1\n→ inode A", fc=GRAY_L, ec=GRAY, fs=9.4)
    rbox(ax, 0.75, 5.65, 2.7, 0.8, "目录项 file2\n→ inode A", fc=GRAY_L, ec=GRAY, fs=9.4)
    rbox(ax, 4.0, 6.0, 2.9, 1.45, "inode A\n链接计数 = 2\n属主/权限/时间…", fc=AMBER_L, ec=AMBER, fs=9.4)
    arrow(ax, 2.5, 7.05, 4.0, 6.85, color=BLUE, lw=1.4)
    arrow(ax, 2.5, 6.05, 4.0, 6.25, color=BLUE, lw=1.4)
    rbox(ax, 4.0, 4.6, 2.9, 0.85, "数据块\n(文件内容)", fc=GREEN_L, ec=GREEN, fs=9.4)
    arrow(ax, 5.45, 6.0, 5.45, 5.5, color=GREEN, lw=1.4)
    tx(ax, 3.95, 4.1, "两个目录项指向同一个 inode（文件属性都在 inode 里）", fs=9.4)
    tx(ax, 3.95, 3.35,
       "删除文件 = 链接计数 -1：\nrm file1 → 计数 2→1，数据还在；\nrm file2 → 计数 1→0，才真正删除",
       fs=9.6)
    tx(ax, 3.95, 1.95,
       "× 硬链接的限制：\n① 不能跨文件系统（inode 号只在本分区有意义）\n② 不能链接目录（防止环路）",
       fs=9.6, color=RED)
    tx(ax, 3.95, 1.0, "√ 实现简单、不额外占空间、访问快（不用多读一次盘）",
       fs=9.4, color=GREEN, bold=True)
    # ---------- 右：软链接
    rbox(ax, 7.7, 0.7, 7.0, 7.45, fc=PURPLE_L, ec=PURPLE)
    tx(ax, 11.2, 7.75, "软链接 Soft Link（符号链接）", fs=13, bold=True, color=PURPLE)
    rbox(ax, 8.0, 6.65, 2.6, 0.8, "目录项 link1\n→ inode L", fc=GRAY_L, ec=GRAY, fs=9.4)
    rbox(ax, 8.0, 5.65, 2.6, 0.8, "目录项 file1\n→ inode A", fc=GRAY_L, ec=GRAY, fs=9.4)
    rbox(ax, 11.0, 6.4, 2.9, 1.05, "inode L + 数据块\n内容 = 存储路径\n/usr/u/file1", fc=PURPLE_L, ec=PURPLE, fs=9.0)
    rbox(ax, 11.0, 5.2, 2.9, 0.9, "inode A + 数据块\n(文件内容)", fc=GREEN_L, ec=GREEN, fs=9.2)
    arrow(ax, 9.6, 7.05, 11.0, 6.8, color=PURPLE, lw=1.4)
    arrow(ax, 9.6, 6.05, 11.0, 5.75, color=PURPLE, lw=1.4)
    tx(ax, 11.2, 4.55, "软链接是一个【独立的小文件】，里面存的是\n被链接文件的路径（不是 inode 号）", fs=9.2)
    tx(ax, 11.2, 3.68,
       "访问 link1 的步骤（多读一次盘）：\n① 读 link1 → 取出路径 /usr/u/file1\n② 按路径查目录 → 再读 file1 的数据块",
       fs=9.2)
    tx(ax, 11.2, 2.35,
       "删除 file1 后：inode A 释放，但 link1 仍存在——\n内容（路径）找不到目标 → 悬空链接（访问报错）",
       fs=9.2, color=RED)
    tx(ax, 11.2, 1.2,
       "√ 优点：① 可跨文件系统（存路径，与 inode 无关）\n② 可用于目录（快捷方式）\n× 缺点：访问多读一次盘、原文件删除后悬空",
       fs=9.2)
    save(fig, FDIR + "ch4-10_hard_soft_link.png")


def f11():
    fig, ax = new_fig(13.5, 9.8, (0, 13.5), (0, 9.8))
    title(ax, "文件系统的层次结构",
          "自上而下七层；【考点】功能归属判断（如'逻辑块号 → 物理块号'在哪一层？）", y=9.3)
    layers = [
        ("用户接口", "open/read/write/close 系统调用接口", BLUE, BLUE_L,
         "用户：read(fd, buf, 第3块)"),
        ("文件目录系统", "按文件名查目录、找到 FCB（按名存取）", TEAL, TEAL_L,
         "2. 目录系统：按文件名查目录，得 FCB 与逻辑块号"),
        ("存取控制模块", "权限验证：读/写/执行/属主（安全）", AMBER, AMBER_L,
         "3. 存取控制：校验权限，非法则拒绝"),
        ("逻辑文件系统与文件信息缓冲区", "逻辑块号 → 物理块号；文件信息缓冲", GREEN, GREEN_L,
         "4. 逻辑文件系统：逻辑块号 → 物理块号"),
        ("物理文件系统", "物理块号 → 物理设备地址（柱面:盘面:扇区）", PINK, PINK_L,
         "5. 物理文件系统：转成设备地址"),
        ("辅助分配模块 / 设备管理程序", "分配回收磁盘块；驱动磁盘读写（含磁盘调度）", PURPLE, PURPLE_L,
         "6. 设备管理：启动 I/O 请求，调度磁盘"),
        ("物理设备", "磁盘、磁带等外存设备", GRAY, GRAY_L,
         "7. 设备：机械动作，完成传输"),
    ]
    y0 = 8.35
    hh = 1.05
    for i, (name, func, cc, cl, note) in enumerate(layers):
        y = y0 - i * (hh + 0.12)
        rbox(ax, 0.5, y - hh / 2, 6.4, hh, "", fc=cl, ec=cc)
        tx(ax, 3.7, y + 0.2, name, fs=11, bold=True, color=cc)
        tx(ax, 3.7, y - 0.22, func, fs=8.8, color=INK)
        arrow(ax, 0.5, y - hh / 2 - 0.005, 0.5, y - hh / 2 + 0.005, color=GRAY, lw=0.01, ms=1)
        if i < 6:
            line(ax, 3.2, y - hh / 2 - 0.06, 3.2, y - hh / 2 - 0.06, color=GRAY, lw=0.01)
            arrow(ax, 3.7, y - hh / 2 - 0.06, 3.7, y - hh / 2 - 0.07, color=GRAY, lw=1.2, ms=10)
        # 右侧示例
        rbox(ax, 7.2, y - 0.5, 5.9, 0.92, "", fc="white", ec=cc, dashed=True, lw=1.0)
        tx(ax, 10.15, y, note, fs=8.8, color=INK)
    tx(ax, 6.9, 0.28,
       "【考点】'把文件的逻辑块号转换为物理块号' → 属于【逻辑文件系统与文件信息缓冲区】层；'把物理块号转换为物理设备地址' → 【物理文件系统】层。",
       fs=10, bold=True, color=RED)
    save(fig, FDIR + "ch4-11_fs_layers.png")


def f12():
    fig, ax = new_fig(15, 9.8, (0, 15), (0, 9.8))
    title(ax, "空闲空间管理之三：位示图法",
          "用一个二进制位表示一个盘块：1 = 已分配（占用），0 = 空闲；矩阵按行存储，本例 4 字 × 32 位", y=9.3)
    # 位示图矩阵
    tx(ax, 6.5, 8.62, "位示图矩阵（行 = 字，列 = 位号 0~31；列越靠右位号越大）",
       fs=10.5, bold=True)
    tx(ax, 1.6, 7.98, "字号", fs=10, bold=True, ha="left")
    bits_rows = [
        "00001111000000001111111100000000",
        "11110000000000111111000000001111",
        "00000000111100000000000011110000",
        "11111111000011110000111100000000",
    ]
    for row, bits in enumerate(bits_rows):
        y = 7.95 - row * 0.65
        tx(ax, 1.85, y + 0.3, str(row), fs=10, bold=True, ha="left")
        for b in range(32):
            v = bits[b]
            fc = BLUE_L if v == "1" else GREEN_L
            ec = BLUE if v == "1" else GREEN
            rect(ax, 2.7 + b * 0.288, y, 0.26, 0.55, "", fc=fc, ec=ec, lw=0.7)
    rbox(ax, 12.25, 5.35, 2.5, 2.75, "", fc=GRAY_L, ec=GRAY)
    tx(ax, 13.5, 7.75, "约定", fs=11, bold=True)
    tx(ax, 13.5, 7.1, "1 → 该盘块已分配\n0 → 该盘块空闲", fs=9.6)
    tx(ax, 13.5, 6.35, "（各书 0/1 约定相反，\n考题必有说明，按题写）", fs=8.4, color=GRAY)
    tx(ax, 13.5, 5.6, "分配：0 位 → 置 1\n回收：1 位 → 置 0", fs=9.0, bold=True, color=BLUE)
    # 公式
    rect(ax, 0.5, 4.35, 11.4, 1.2, "", fc=AMBER_L, ec=AMBER, lw=1.4)
    tx(ax, 6.2, 5.32, "位示图互算公式（字长 = 32；字号、位号都从 0 开始编号）", fs=11, bold=True)
    tx(ax, 6.2, 4.72,
       "盘块号 b = 字号 × 32 + 位号        ｜        字号 = b ÷ 32（整除）        ｜        位号 = b mod 32",
       fs=11.5, bold=True, color=RED)
    # 例题
    tx(ax, 7.5, 3.95, "例题（逐个演算）", fs=12, bold=True)
    ex = [
        ("① 求 b = 25 的位置", "字号 = 25 ÷ 32 = 0，位号 = 25 mod 32 = 25\n→ 该盘块对应（字号 0，位号 25），即第 0 字第 25 位"),
        ("② 求 b = 65 的位置", "字号 = 65 ÷ 32 = 2，位号 = 65 mod 32 = 1\n→ 该盘块对应（字号 2，位号 1）"),
        ("③ 求 b = 100 的位置", "字号 = 100 ÷ 32 = 3，位号 = 100 mod 32 = 4\n→ 该盘块对应（字号 3，位号 4）"),
        ("④ 反向：(字号 1，位号 30) 对应哪块", "b = 1 × 32 + 30 = 62\n→ 该位对应盘块号 62"),
    ]
    for i, (h, body) in enumerate(ex):
        x = 2.9 + (i % 2) * 5.85
        y = 2.2 - (i // 2) * 1.75
        rbox(ax, x, y, 5.6, 1.6, fc=BLUE_L, ec=BLUE)
        tx(ax, x + 2.8, y + 1.28, h, fs=10.5, bold=True, color=BLUE)
        tx(ax, x + 2.8, y + 0.55, body, fs=9.4)
    save(fig, FDIR + "ch4-12_free_bitmap.png")
