from __future__ import annotations

from pathlib import Path
import math
import textwrap

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper_figures"
OUT.mkdir(exist_ok=True)


def choose_font() -> str:
    preferred = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in preferred:
        if name in installed:
            return name
    return "DejaVu Sans"


FONT = choose_font()

mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": [FONT, "Arial", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.linewidth": 0.8,
        "legend.frameon": False,
        "font.size": 7,
        "axes.unicode_minus": False,
    }
)


PALETTE = {
    "ours": "#0F4D92",
    "ours_light": "#DDEAF7",
    "coverup": "#6AA6B8",
    "codamosa": "#B89458",
    "direct": "#7C7C7C",
    "pynguin": "#BDBDBD",
    "text": "#222222",
    "muted": "#666666",
    "line": "#D7DCE2",
    "bg": "#F7F9FB",
    "green": "#2E9E44",
    "red": "#C95555",
    "gold": "#D8A028",
}


def save_all(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=600, bbox_inches="tight")


def wrap(text: str, width: int = 16) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def add_box(
    ax,
    xy,
    wh,
    title: str,
    body: str,
    *,
    face="#FFFFFF",
    edge="#D7DCE2",
    title_color="#222222",
    body_color="#555555",
    lw=1.1,
):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        linewidth=lw,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(
        x + w * 0.06,
        y + h * 0.68,
        title,
        ha="left",
        va="center",
        fontsize=7.8,
        fontweight="bold",
        color=title_color,
    )
    ax.text(
        x + w * 0.06,
        y + h * 0.34,
        body,
        ha="left",
        va="center",
        fontsize=6.3,
        color=body_color,
        linespacing=1.25,
    )
    return patch


def arrow(ax, start, end, *, color="#8B96A4", lw=1.2, rad=0.0, style="-|>"):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=style,
            mutation_scale=10,
            linewidth=lw,
            color=color,
            connectionstyle=f"arc3,rad={rad}",
        )
    )


def draw_method_overview() -> None:
    fig = plt.figure(figsize=(7.2, 3.45))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.02, 0.955, "方法总流程", fontsize=8.8, fontweight="bold", color=PALETTE["text"], va="top")
    ax.text(
        0.15,
        0.955,
        "从 Pynguin 未覆盖分支出发，将开放式 LLM 生成约束为面向目标分支的测试构造。",
        fontsize=6.8,
        color=PALETTE["muted"],
        va="top",
    )

    # Input strip
    add_box(
        ax,
        (0.035, 0.695),
        (0.18, 0.145),
        "科学计算程序",
        "228 个程序\n程序文件 + 依赖文件",
        face="#FFFFFF",
        edge=PALETTE["line"],
    )
    add_box(
        ax,
        (0.035, 0.485),
        (0.18, 0.145),
        "Pynguin 基线",
        "搜索式生成测试\n分支覆盖报告",
        face="#FFFFFF",
        edge=PALETTE["line"],
    )
    arrow(ax, (0.125, 0.695), (0.125, 0.63), color=PALETTE["line"], style="-")

    # Main pipeline
    boxes = [
        ((0.265, 0.59), (0.16, 0.18), "目标分支提取", "未覆盖分支\n目标方向\n源码上下文"),
        ((0.465, 0.59), (0.17, 0.18), "分支特征分析", "复杂数据\n跨函数状态\n循环/迭代状态"),
        ((0.675, 0.59), (0.17, 0.18), "分类提示词", "目标分支列表\n生成约束\n基线测试摘要"),
    ]
    for xy, wh, title, body in boxes:
        add_box(ax, xy, wh, title, body, face="#FFFFFF", edge=PALETTE["line"])

    add_box(
        ax,
        (0.675, 0.31),
        (0.17, 0.18),
        "LLM 生成",
        "面向目标分支的\n补充 pytest 测试",
        face=PALETTE["ours_light"],
        edge=PALETTE["ours"],
        title_color=PALETTE["ours"],
    )
    add_box(
        ax,
        (0.465, 0.31),
        (0.17, 0.18),
        "执行与测量",
        "pytest 执行\n统一分支覆盖率\n失败日志",
        face="#FFFFFF",
        edge=PALETTE["line"],
    )
    add_box(
        ax,
        (0.265, 0.31),
        (0.16, 0.18),
        "过滤与保留",
        "仅保留可执行且\n提升覆盖率的测试",
        face="#FFFFFF",
        edge=PALETTE["line"],
    )
    add_box(
        ax,
        (0.035, 0.31),
        (0.18, 0.18),
        "最终测试套件",
        "Pynguin 测试\n+ 有效 LLM 测试",
        face="#FFFFFF",
        edge=PALETTE["line"],
    )

    # Arrows
    arrow(ax, (0.215, 0.56), (0.265, 0.68))
    arrow(ax, (0.425, 0.68), (0.465, 0.68))
    arrow(ax, (0.635, 0.68), (0.675, 0.68))
    arrow(ax, (0.76, 0.59), (0.76, 0.49))
    arrow(ax, (0.675, 0.40), (0.635, 0.40))
    arrow(ax, (0.465, 0.40), (0.425, 0.40))
    arrow(ax, (0.265, 0.40), (0.215, 0.40))
    arrow(ax, (0.55, 0.31), (0.68, 0.26), rad=-0.18, color=PALETTE["ours"])
    ax.text(
        0.61,
        0.235,
        "覆盖增益 / 错误反馈",
        color=PALETTE["ours"],
        fontsize=6.9,
        ha="center",
    )

    # Branch-type tiles
    tile_y = 0.08
    tile_xs = [0.28, 0.45, 0.62]
    tile_titles = ["复杂数据", "跨函数依赖", "循环/迭代"]
    tile_body = ["数组、矩阵\nshape、对象状态", "辅助函数\n中间返回状态", "残差、容忍度\n收敛过程"]
    tile_colors = ["#E8F2FB", "#EEF6F4", "#FFF4DD"]
    for i, (x, title, body, color) in enumerate(zip(tile_xs, tile_titles, tile_body, tile_colors)):
        add_box(
            ax,
            (x, tile_y),
            (0.145, 0.13),
            title,
            body,
            face=color,
            edge="#D5DCE3",
            lw=0.9,
        )
    ax.text(
        0.035,
        tile_y + 0.065,
        "分支类型标签\n将覆盖缺口转化为\n输入构造策略。",
        fontsize=6.6,
        color=PALETTE["muted"],
        va="center",
        linespacing=1.22,
    )
    arrow(ax, (0.55, 0.59), (0.55, 0.215), color="#B8C1CC", style="->", lw=0.8)

    # Numeric callout
    callout = FancyBboxPatch(
        (0.86, 0.31),
        0.11,
        0.46,
        boxstyle="round,pad=0.014,rounding_size=0.02",
        facecolor="#FFFFFF",
        edgecolor=PALETTE["line"],
        linewidth=1,
    )
    ax.add_patch(callout)
    callouts = [("104", "有效\n程序"), ("334", "目标\n分支"), ("3", "分支\n类型")]
    for j, (num, lab) in enumerate(callouts):
        cy = 0.69 - j * 0.14
        ax.text(0.915, cy, num, color=PALETTE["ours"], fontsize=15, fontweight="bold", ha="center")
        ax.text(0.915, cy - 0.055, lab, color=PALETTE["muted"], fontsize=6.2, ha="center", linespacing=1.05)

    save_all(fig, "figure1_method_overview")
    plt.close(fig)


def add_panel_label(ax, label: str):
    ax.text(
        -0.12,
        1.04,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        va="top",
        ha="left",
        color=PALETTE["text"],
    )


def draw_results_summary() -> None:
    fig = plt.figure(figsize=(7.25, 3.95))
    gs = fig.add_gridspec(
        2,
        2,
        width_ratios=[1.15, 1.0],
        height_ratios=[1.0, 0.76],
        left=0.08,
        right=0.98,
        bottom=0.14,
        top=0.94,
        wspace=0.34,
        hspace=0.48,
    )
    ax1 = fig.add_subplot(gs[:, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 1])

    # Panel a: method comparison
    methods = ["Pynguin", "CodaMOSA", "CoverUp", "Direct\nLLM-only", "Ours"]
    values = np.array([65.25, 69.18, 89.47, 89.74, 93.85])
    colors = [PALETTE["pynguin"], PALETTE["codamosa"], PALETTE["coverup"], PALETTE["direct"], PALETTE["ours"]]
    y = np.arange(len(methods))
    ax1.barh(y, values, color=colors, height=0.62, edgecolor="white", linewidth=0.8)
    ax1.set_yticks(y)
    ax1.set_yticklabels(methods)
    ax1.invert_yaxis()
    ax1.set_xlim(60, 100)
    ax1.set_xlabel("104 个有效程序上的平均分支覆盖率 (%)")
    ax1.set_title("程序级覆盖率对比", loc="left", fontsize=8.0, fontweight="bold")
    add_panel_label(ax1, "a")
    ax1.grid(axis="x", color="#EAECEF", linewidth=0.6)
    ax1.set_axisbelow(True)
    for yy, val in zip(y, values):
        ax1.text(val + 0.7, yy, f"{val:.2f}", va="center", ha="left", fontsize=7.2, color=PALETTE["text"])
    ax1.annotate(
        "+28.60 个百分点",
        xy=(93.85, 4),
        xytext=(73, 3.15),
        arrowprops=dict(arrowstyle="->", color=PALETTE["ours"], lw=1.1),
        fontsize=7.3,
        color=PALETTE["ours"],
    )

    # Panel b: hard-branch categories
    cats = ["复杂\n数据", "跨函数\n依赖", "循环/\n迭代"]
    direct = np.array([71.56, 72.66, 71.15])
    ours = np.array([84.44, 83.74, 82.69])
    x = np.arange(len(cats))
    width = 0.33
    ax2.bar(x - width / 2, direct, width, color="#C7CCD2", label="Direct LLM-only")
    ax2.bar(x + width / 2, ours, width, color=PALETTE["ours"], label="Ours")
    ax2.set_ylim(60, 90)
    ax2.set_xticks(x)
    ax2.set_xticklabels(cats)
    ax2.set_ylabel("目标分支覆盖率 (%)")
    ax2.set_title("三类难覆盖分支", loc="left", fontsize=8.0, fontweight="bold")
    add_panel_label(ax2, "b")
    ax2.grid(axis="y", color="#EAECEF", linewidth=0.6)
    ax2.set_axisbelow(True)
    ax2.legend(loc="upper left", fontsize=6.6, handlelength=1.0, borderaxespad=0.2)
    for xi, d, o in zip(x, direct, ours):
        ax2.text(xi + width / 2, o + 0.8, f"+{o-d:.1f}", ha="center", va="bottom", fontsize=6.6, color=PALETTE["ours"])

    # Panel c: cost-effectiveness. CodaMOSA is shown as a lower-bound marker
    # because the experiment logs did not contain complete token accounting.
    names = ["Ours", "CoverUp", "CodaMOSA\n(lower bound)"]
    costs = np.array([0.020, 0.049, 0.018])
    covs = np.array([93.85, 89.47, 69.18])
    ax3.scatter(
        costs[:2],
        covs[:2],
        s=[120, 110],
        color=[PALETTE["ours"], PALETTE["coverup"]],
        edgecolor="white",
        linewidth=0.8,
        zorder=3,
    )
    ax3.scatter(
        costs[2],
        covs[2],
        s=120,
        marker="^",
        facecolor="white",
        edgecolor=PALETTE["codamosa"],
        linewidth=1.4,
        zorder=4,
    )
    for name, xx, yy in zip(names, costs, covs):
        dy = 0.35 if yy > 75 else 1.2
        ax3.text(xx + 0.002, yy + dy, name, fontsize=7.0, color=PALETTE["text"])
    ax3.set_xlim(0.0, 0.06)
    ax3.set_ylim(66, 96)
    ax3.set_xlabel("每个有效程序估算成本 (USD)")
    ax3.set_ylabel("覆盖率 (%)")
    ax3.set_title("成本-效果关系", loc="left", fontsize=8.0, fontweight="bold")
    add_panel_label(ax3, "c")
    ax3.grid(color="#EAECEF", linewidth=0.6)
    ax3.set_axisbelow(True)
    ax3.annotate(
        "更高覆盖率\n更低成本",
        xy=(0.02, 93.85),
        xytext=(0.033, 94.8),
        arrowprops=dict(arrowstyle="->", color=PALETTE["ours"], lw=1.0),
        fontsize=6.6,
        color=PALETTE["ours"],
        ha="left",
    )

    save_all(fig, "figure2_results_summary")
    plt.close(fig)


def draw_model_ablation_summary() -> None:
    """Additional comparison figure for RQ3 and RQ4."""
    fig = plt.figure(figsize=(7.25, 3.65))
    gs = fig.add_gridspec(
        1,
        2,
        width_ratios=[1.05, 1.15],
        left=0.08,
        right=0.98,
        bottom=0.17,
        top=0.91,
        wspace=0.34,
    )
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    # Panel a: model sensitivity.
    models = ["GPT-4o", "GPT-4o-mini", "Qwen2.5-7B"]
    direct = np.array([89.74, 87.44, 79.20])
    v1 = np.array([93.85, 84.80, 77.86])
    v2 = np.array([87.83, 85.38, 80.46])
    x = np.arange(len(models))
    w = 0.24
    ax1.bar(x - w, direct, w, label="Direct LLM-only", color="#C7CCD2")
    ax1.bar(x, v1, w, label="Ours v1", color=PALETTE["ours"])
    ax1.bar(x + w, v2, w, label="Ours v2", color="#8FAFD3")
    ax1.set_ylim(74, 96)
    ax1.set_xticks(x)
    ax1.set_xticklabels(["GPT-4o", "GPT-4o-\nmini", "Qwen2.5-\n7B"])
    ax1.set_ylabel("平均分支覆盖率 (%)")
    ax1.set_title("模型能力敏感性", loc="left", fontsize=8.0, fontweight="bold")
    add_panel_label(ax1, "a")
    ax1.grid(axis="y", color="#EAECEF", linewidth=0.6)
    ax1.set_axisbelow(True)
    ax1.legend(fontsize=6.4, loc="upper right", handlelength=1.0)
    for xi, d, o in zip(x, direct, v1):
        delta = o - d
        color = PALETTE["ours"] if delta >= 0 else PALETTE["red"]
        ax1.text(xi, max(o, d) + 0.7, f"{delta:+.1f}", ha="center", fontsize=6.5, color=color)

    # Panel b: ablation drops.
    labels = [
        "Full\nOurs",
        "No category\nprompt",
        "One\nround",
        "No error\nfeedback",
        "No test\nfilter",
        "No branch\ntargets",
    ]
    values = np.array([93.85, 87.61, 85.51, 88.01, 74.97, 86.83])
    drops = 93.85 - values
    colors = [PALETTE["ours"]] + ["#9BB9D7", "#AFC7DE", "#BDD2E5", PALETTE["red"], "#C9D9EA"]
    y = np.arange(len(labels))
    ax2.barh(y, values, color=colors, height=0.64, edgecolor="white", linewidth=0.8)
    ax2.set_yticks(y)
    ax2.set_yticklabels(labels)
    ax2.invert_yaxis()
    ax2.set_xlim(70, 96)
    ax2.set_xlabel("平均分支覆盖率 (%)")
    ax2.set_title("组件消融", loc="left", fontsize=8.0, fontweight="bold")
    add_panel_label(ax2, "b")
    ax2.grid(axis="x", color="#EAECEF", linewidth=0.6)
    ax2.set_axisbelow(True)
    for yy, val, drop in zip(y, values, drops):
        suffix = "" if drop == 0 else f"  −{drop:.2f}"
        ax2.text(val + 0.35, yy, f"{val:.2f}{suffix}", va="center", fontsize=6.5, color=PALETTE["text"])
    ax2.annotate(
        "过滤失败测试\n贡献最大",
        xy=(74.97, 4),
        xytext=(79.2, 4.75),
        arrowprops=dict(arrowstyle="->", color=PALETTE["red"], lw=1.0),
        fontsize=6.8,
        color=PALETTE["red"],
    )

    save_all(fig, "figure3_model_ablation")
    plt.close(fig)


def draw_cost_reliability_summary() -> None:
    """Dedicated cost and result-availability comparison for RQ5."""
    fig = plt.figure(figsize=(7.25, 3.2))
    gs = fig.add_gridspec(
        1,
        2,
        width_ratios=[1.12, 1.0],
        left=0.08,
        right=0.98,
        bottom=0.19,
        top=0.88,
        wspace=0.38,
    )
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    # Panel a: cost-effectiveness with CodaMOSA shown as a lower bound.
    names = ["Ours", "CoverUp", "CodaMOSA\n(成本下界)"]
    costs = np.array([0.020, 0.049, 0.018])
    coverage = np.array([93.85, 89.47, 69.18])
    colors = [PALETTE["ours"], PALETTE["coverup"], PALETTE["codamosa"]]
    markers = ["o", "o", "^"]
    for i, (name, cost, cov, color, marker) in enumerate(zip(names, costs, coverage, colors, markers)):
        face = color if i < 2 else "white"
        ax1.scatter(cost, cov, s=135, marker=marker, facecolor=face, edgecolor=color, linewidth=1.4, zorder=3)
        ax1.text(cost + 0.002, cov + (0.6 if i < 2 else 1.2), name, fontsize=7.0, color=PALETTE["text"])
    ax1.set_xlim(0, 0.06)
    ax1.set_ylim(66, 96)
    ax1.set_xlabel("每个有效程序估算成本 (USD)")
    ax1.set_ylabel("平均分支覆盖率 (%)")
    ax1.set_title("成本-效果关系", loc="left", fontsize=8.0, fontweight="bold")
    ax1.grid(color="#EAECEF", linewidth=0.6)
    ax1.set_axisbelow(True)
    add_panel_label(ax1, "a")
    ax1.annotate(
        "更高覆盖率\n更低成本",
        xy=(0.020, 93.85),
        xytext=(0.034, 94.2),
        arrowprops=dict(arrowstyle="->", color=PALETTE["ours"], lw=1.0),
        fontsize=6.7,
        color=PALETTE["ours"],
        ha="left",
    )

    # Panel b: how many programs produce a comparable coverage record.
    tools = ["Ours", "CoverUp", "CodaMOSA"]
    valid = np.array([228, 213, 215])
    invalid = 228 - valid
    y = np.arange(len(tools))
    ax2.barh(y, valid, color=[PALETTE["ours"], PALETTE["coverup"], PALETTE["codamosa"]], height=0.62)
    ax2.barh(y, invalid, left=valid, color="#ECEFF3", height=0.62)
    ax2.set_yticks(y)
    ax2.set_yticklabels(tools)
    ax2.invert_yaxis()
    ax2.set_xlim(0, 228)
    ax2.set_xlabel("可比较覆盖率记录的程序数")
    ax2.set_title("结果可统计性", loc="left", fontsize=8.0, fontweight="bold")
    ax2.grid(axis="x", color="#EAECEF", linewidth=0.6)
    ax2.set_axisbelow(True)
    add_panel_label(ax2, "b")
    for yy, ok, bad in zip(y, valid, invalid):
        ax2.text(ok - 4, yy, f"{ok}", va="center", ha="right", fontsize=6.8, color="white")
        if bad:
            ax2.text(ok + bad + 1, yy, f"缺失 {bad}", va="center", fontsize=6.6, color=PALETTE["muted"])

    save_all(fig, "figure4_cost_reliability")
    plt.close(fig)


if __name__ == "__main__":
    draw_method_overview()
    draw_results_summary()
    draw_model_ablation_summary()
    draw_cost_reliability_summary()
    print(f"Saved figures to {OUT}")
