from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper_figures"
OUT.mkdir(exist_ok=True)


mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "font.size": 7.5,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.linewidth": 0.65,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "axes.labelcolor": "#222222",
        "text.color": "#222222",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "legend.frameon": False,
    }
)


COLORS = {
    "pynguin": "#9DA3A6",
    "direct": "#7D9CB8",
    "codamosa": "#C9A24C",
    "coverup": "#4CA7A1",
    "ours": "#D95F59",
    "ours_dark": "#B74742",
    "v2": "#E39973",
    "neutral": "#5B6670",
    "light": "#EEF2F4",
    "line": "#D8DEE2",
    "red_light": "#F6D2CF",
    "amber_light": "#F3E1B7",
    "teal_light": "#D7ECEA",
    "blue_light": "#DAE5EF",
}


def save_figure(fig: plt.Figure, name: str) -> None:
    base = OUT / name
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(base.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def panel_label(ax: plt.Axes, label: str, x: float = -0.08, y: float = 1.05) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=9.2,
        fontweight="bold",
        va="bottom",
        ha="left",
    )


def despine(ax: plt.Axes) -> None:
    ax.spines["left"].set_color("#444444")
    ax.spines["bottom"].set_color("#444444")
    ax.grid(axis="y", color="#E7EBEE", lw=0.6, zorder=0)
    ax.set_axisbelow(True)


def add_value_labels(ax: plt.Axes, bars, suffix: str = "%", dy: float = 1.0) -> None:
    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + dy,
            f"{h:.1f}{suffix}",
            ha="center",
            va="bottom",
            fontsize=6.7,
            color="#333333",
        )


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_source_csv(name: str, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    path = OUT / f"{name}_source.csv"
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def draw_box(
    ax: plt.Axes,
    xy: tuple[float, float],
    wh: tuple[float, float],
    title: str,
    body: str,
    fc: str,
    ec: str = "#FFFFFF",
    title_color: str = "#222222",
    title_size: float = 8.2,
    body_size: float = 6.7,
    title_offset: float = 0.07,
    body_offset: float = 0.15,
    linespacing: float = 1.3,
) -> FancyBboxPatch:
    x, y = xy
    w, h = wh
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.025",
        linewidth=0.7,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(box)
    ax.text(
        x + 0.025,
        y + h - title_offset,
        title,
        fontsize=title_size,
        fontweight="bold",
        color=title_color,
    )
    ax.text(
        x + 0.025,
        y + h - body_offset,
        body,
        fontsize=body_size,
        color="#3A3A3A",
        va="top",
        linespacing=linespacing,
    )
    return box


def arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], color: str = "#6B7280") -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=8,
            linewidth=0.8,
            color=color,
            shrinkA=2,
            shrinkB=2,
        )
    )


def text_card(
    ax: plt.Axes,
    xy: tuple[float, float],
    wh: tuple[float, float],
    title: str,
    lines: list[str],
    fc: str,
    title_size: float = 7.4,
    body_size: float = 5.7,
    mono: bool = False,
    accent: str | None = None,
) -> FancyBboxPatch:
    x, y = xy
    w, h = wh
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.016,rounding_size=0.022",
        linewidth=0.7,
        edgecolor="#FFFFFF",
        facecolor=fc,
    )
    ax.add_patch(box)
    if accent:
        ax.plot(
            [x + 0.016, x + 0.016],
            [y + 0.04, y + h - 0.04],
            color=accent,
            lw=2.0,
            solid_capstyle="round",
        )
    ax.text(x + 0.032, y + h - 0.055, title, fontsize=title_size, fontweight="bold", va="top")
    ax.text(
        x + 0.032,
        y + h - 0.135,
        "\n".join(lines),
        fontsize=body_size,
        color="#3A3A3A",
        va="top",
        linespacing=1.22,
        family="monospace" if mono else None,
    )
    return box


def figure3_1_method_flow() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 4.05))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.04,
        0.94,
        "The method turns Pynguin-residual branches into targeted repair prompts.",
        fontsize=8.8,
        fontweight="bold",
        ha="left",
        va="top",
    )

    text_card(
        ax,
        (0.04, 0.58),
        (0.27, 0.25),
        "1. Baseline evidence",
        ["Pynguin tests run first", "coverage exposes gaps", "ordinary paths are removed"],
        COLORS["light"],
    )
    text_card(
        ax,
        (0.365, 0.58),
        (0.27, 0.25),
        "2. Residual branch",
        ["if residual < tol:", "    break", "missing: True branch"],
        COLORS["blue_light"],
        mono=True,
        accent=COLORS["direct"],
    )
    text_card(
        ax,
        (0.69, 0.58),
        (0.27, 0.25),
        "3. Trigger diagnosis",
        ["Loop state", "residual variable", "tolerance threshold"],
        COLORS["amber_light"],
        accent=COLORS["codamosa"],
    )
    text_card(
        ax,
        (0.69, 0.18),
        (0.27, 0.25),
        "4. Targeted prompt",
        ["state the missing branch", "turn label into input rule", "ask for pytest only"],
        COLORS["teal_light"],
        accent=COLORS["coverup"],
    )
    text_card(
        ax,
        (0.365, 0.18),
        (0.27, 0.25),
        "5. Candidate tests",
        ["construct inputs", "call target function", "assert branch outcome"],
        "#F5DED9",
    )
    text_card(
        ax,
        (0.04, 0.18),
        (0.27, 0.25),
        "6. Execute and filter",
        ["run pytest", "measure branch coverage", "keep only useful tests"],
        COLORS["red_light"],
        accent=COLORS["ours"],
    )

    arrow(ax, (0.31, 0.705), (0.365, 0.705))
    arrow(ax, (0.635, 0.705), (0.69, 0.705))
    arrow(ax, (0.825, 0.58), (0.825, 0.43))
    arrow(ax, (0.69, 0.305), (0.635, 0.305))
    arrow(ax, (0.365, 0.305), (0.31, 0.305))
    feedback = FancyBboxPatch(
        (0.36, 0.035),
        0.28,
        0.075,
        boxstyle="round,pad=0.014,rounding_size=0.02",
        linewidth=0.7,
        edgecolor="#FFFFFF",
        facecolor="#FAE7E5",
    )
    ax.add_patch(feedback)
    ax.text(
        0.50,
        0.073,
        "Feedback: failure reason + remaining target",
        fontsize=5.8,
        color=COLORS["ours_dark"],
        ha="center",
        va="center",
        fontweight="bold",
    )
    arrow(ax, (0.17, 0.18), (0.38, 0.085), color=COLORS["ours_dark"])
    arrow(ax, (0.62, 0.085), (0.80, 0.18), color=COLORS["ours_dark"])
    save_figure(fig, "figure3_1_method_flow")


def figure3_2_prompt_structure() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.15))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.94,
        "Prompt construction turns branch evidence into concrete input constraints.",
        ha="center",
        va="top",
        fontsize=8.4,
        fontweight="bold",
    )

    evidence = [
        ("Output contract", ["pytest only", "include assertions"], COLORS["light"], 0.045, False),
        ("Target branch", ["jacobi:34", "residual < tol"], COLORS["blue_light"], 0.285, False),
        ("Branch type", ["Loop state", "control tolerance"], COLORS["amber_light"], 0.525, False),
        ("Context", ["source excerpt", "prior Pynguin test"], COLORS["teal_light"], 0.765, False),
    ]
    for title, lines, color, x, mono in evidence:
        text_card(
            ax,
            (x, 0.58),
            (0.19, 0.22),
            title,
            lines,
            color,
            title_size=6.7,
            body_size=5.0,
            mono=mono,
        )

    text_card(
        ax,
        (0.18, 0.17),
        (0.64, 0.24),
        "Prompt sent to the LLM",
        [
            "Generate one pytest test for jacobi.",
            "Choose inputs that make residual < tol true.",
            "Reuse only relevant context and include an assertion.",
        ],
        "#F7F2E8",
        title_size=7.2,
        body_size=5.3,
        accent=COLORS["ours"],
    )
    for x in [0.14, 0.38, 0.62, 0.86]:
        arrow(ax, (x, 0.58), (0.50, 0.41), color="#6B7280")
    save_figure(fig, "figure3_2_prompt_structure")


def figure3_3_feedback_prompt() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.05))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(
        0.5,
        0.94,
        "The next prompt keeps only the failure signal and the remaining branch.",
        ha="center",
        va="top",
        fontsize=8.4,
        fontweight="bold",
    )
    text_card(
        ax,
        (0.05, 0.56),
        (0.27, 0.24),
        "Execution outcome",
        ["test runs", "coverage unchanged"],
        COLORS["blue_light"],
        title_size=7.0,
        body_size=5.3,
    )
    text_card(
        ax,
        (0.365, 0.56),
        (0.27, 0.24),
        "Remaining branch",
        ["jacobi:34", "residual < tol not covered"],
        COLORS["amber_light"],
        title_size=7.0,
        body_size=5.3,
    )
    text_card(
        ax,
        (0.68, 0.56),
        (0.27, 0.24),
        "Repair constraint",
        ["change initial values", "stay deterministic"],
        "#F5DED9",
        title_size=7.0,
        body_size=5.3,
    )
    arrow(ax, (0.32, 0.68), (0.365, 0.68))
    arrow(ax, (0.635, 0.68), (0.68, 0.68))
    text_card(
        ax,
        (0.20, 0.16),
        (0.60, 0.24),
        "Next-round prompt",
        [
            "Use the remaining branch and repair constraint.",
            "Do not repeat a test that ran but added no coverage.",
        ],
        COLORS["teal_light"],
        title_size=7.1,
        body_size=5.3,
        accent=COLORS["ours"],
    )
    arrow(ax, (0.50, 0.56), (0.50, 0.40), color=COLORS["ours_dark"])
    save_figure(fig, "figure3_3_feedback_prompt")


def figure4_1_results_overview() -> None:
    rows = [
        {"method": "Pynguin", "coverage": 65.25},
        {"method": "CodaMOSA", "coverage": 69.18},
        {"method": "CoverUp", "coverage": 89.47},
        {"method": "Ours", "coverage": 93.85},
    ]
    category_rows = [
        {
            "category": "Complex\ndata",
            "Direct": 71.56,
            "CodaMOSA": 23.56,
            "CoverUp": 75.56,
            "Ours": 84.44,
        },
        {
            "category": "Cross-\nfunction",
            "Direct": 72.66,
            "CodaMOSA": 21.80,
            "CoverUp": 78.55,
            "Ours": 83.74,
        },
        {
            "category": "Loop\nstate",
            "Direct": 71.15,
            "CodaMOSA": 18.85,
            "CoverUp": 73.08,
            "Ours": 82.69,
        },
    ]
    cost_rows = [
        {"method": "Ours", "cost": 2.07, "coverage": 93.85},
        {"method": "CoverUp", "cost": 5.11, "coverage": 89.47},
        {"method": "CodaMOSA", "cost": 5.95, "coverage": 69.18},
    ]
    write_source_csv("figure4_1_results_overview", rows)

    fig = plt.figure(figsize=(7.2, 4.25), constrained_layout=False)
    gs = fig.add_gridspec(2, 3, height_ratios=[1.0, 1.0], width_ratios=[1.0, 1.55, 1.15], wspace=0.46, hspace=0.62)
    ax1 = fig.add_subplot(gs[:, 0])
    ax2 = fig.add_subplot(gs[:, 1])
    ax3 = fig.add_subplot(gs[:, 2])

    methods = [r["method"] for r in rows]
    vals = [r["coverage"] for r in rows]
    colors = [COLORS["pynguin"], COLORS["codamosa"], COLORS["coverup"], COLORS["ours"]]
    x = np.arange(len(vals))
    bars = ax1.bar(x, vals, color=colors, width=0.68, zorder=2)
    add_value_labels(ax1, bars, dy=1.1)
    ax1.set_ylim(0, 105)
    ax1.set_ylabel("Average branch coverage (%)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(methods, rotation=35, ha="right")
    despine(ax1)
    panel_label(ax1, "a")
    ax1.set_title("Average branch coverage", fontsize=8.5, pad=8)

    cats = [r["category"] for r in category_rows]
    method_order = ["Direct", "CodaMOSA", "CoverUp", "Ours"]
    method_colors = [COLORS["direct"], COLORS["codamosa"], COLORS["coverup"], COLORS["ours"]]
    width = 0.18
    x = np.arange(len(cats))
    for i, method in enumerate(method_order):
        vals = [r[method] for r in category_rows]
        ax2.bar(x + (i - 1.5) * width, vals, width=width, label=method, color=method_colors[i], zorder=2)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Target branch coverage (%)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(cats)
    ax2.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.18), fontsize=6.8, handlelength=1.1, columnspacing=0.9)
    despine(ax2)
    panel_label(ax2, "b")
    ax2.set_title("Coverage on Pynguin-residual branches", fontsize=8.5, pad=8)

    for row, color, marker in [
        (cost_rows[0], COLORS["ours"], "o"),
        (cost_rows[1], COLORS["coverup"], "o"),
        (cost_rows[2], COLORS["codamosa"], "^"),
    ]:
        ax3.scatter(row["cost"], row["coverage"], s=54, color=color, edgecolor="white", linewidth=0.8, zorder=3, marker=marker)
        if row["method"] == "CodaMOSA":
            label = "CodaMOSA\nest. $5.95"
            ax3.text(row["cost"] - 0.18, row["coverage"] + 1.0, label, fontsize=6.8, color="#333333", ha="right")
        else:
            label = f"{row['method']}\n${row['cost']:.2f}"
            ax3.text(row["cost"] + 0.18, row["coverage"] + 0.8, label, fontsize=7.0, color="#333333")
    ax3.set_xlim(0, 6.8)
    ax3.set_ylim(60, 100)
    ax3.set_xlabel("Estimated LLM cost (USD)")
    ax3.set_ylabel("Average branch coverage (%)")
    despine(ax3)
    panel_label(ax3, "c")
    ax3.set_title("Cost-effectiveness", fontsize=8.5, pad=8)
    save_figure(fig, "figure4_1_results_overview")


def figure4_2_model_ablation() -> None:
    model_rows = read_csv_dicts(ROOT / "model_direct_v1_v2_program_comparison.csv")
    models = ["GPT-4o", "GPT-4o-mini", "Qwen2.5-7B"]
    variants = ["Direct LLM-only", "Ours v1", "Ours v2"]
    values = {
        (r["model"], r["variant"]): float(r["avg_branch"])
        for r in model_rows
    }

    ablations = [
        ("w/o filtering", 93.85 - 74.97),
        ("w/o coverage\nfeedback", 93.85 - 83.23),
        ("one-shot\nonly", 93.85 - 85.51),
        ("w/o branch\nguidance", 93.85 - 86.83),
        ("w/o category\nprompt", 93.85 - 87.61),
        ("w/o error\nfeedback", 93.85 - 88.01),
    ]
    write_source_csv(
        "figure4_2_model_ablation",
        [{"model": m, "variant": v, "coverage": values[(m, v)]} for m in models for v in variants],
    )

    fig = plt.figure(figsize=(7.2, 3.35), constrained_layout=False)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.22, 1.0], wspace=0.36)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    x = np.arange(len(models))
    width = 0.23
    variant_colors = [COLORS["direct"], COLORS["ours"], COLORS["v2"]]
    for i, variant in enumerate(variants):
        vals = [values[(m, variant)] for m in models]
        ax1.bar(x + (i - 1) * width, vals, width=width, label=variant, color=variant_colors[i], zorder=2)
    ax1.set_ylim(60, 100)
    ax1.set_ylabel("Average branch coverage (%)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(["GPT-4o", "GPT-4o-\nmini", "Qwen2.5-\n7B"])
    ax1.legend(loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=3, fontsize=6.7, handlelength=1.0, columnspacing=0.8)
    despine(ax1)
    panel_label(ax1, "a", x=-0.1, y=1.12)
    ax1.set_title("Model capacity changes the value of context", fontsize=8.5, pad=8)

    labels = [x[0] for x in ablations][::-1]
    drops = [x[1] for x in ablations][::-1]
    y = np.arange(len(labels))
    cmap = [COLORS["amber_light"], COLORS["amber_light"], "#F0C28F", "#ECA37D", "#E47F72", COLORS["ours"]]
    ax2.barh(y, drops, color=cmap, height=0.62, zorder=2)
    for yi, drop in zip(y, drops):
        ax2.text(drop + 0.35, yi, f"-{drop:.2f} pp", va="center", fontsize=6.8, color="#333333")
    ax2.set_yticks(y)
    ax2.set_yticklabels(labels)
    ax2.set_xlim(0, 21)
    ax2.set_xlabel("Coverage drop from full method (percentage points)")
    ax2.grid(axis="x", color="#E7EBEE", lw=0.6, zorder=0)
    ax2.spines["left"].set_visible(False)
    ax2.spines["bottom"].set_color("#444444")
    ax2.tick_params(axis="y", length=0)
    panel_label(ax2, "b", x=-0.12, y=1.14)
    ax2.set_title("Filtering is the largest quality-control component", fontsize=8.5, pad=8)
    save_figure(fig, "figure4_2_model_ablation")


def figure4_3_cost_reliability() -> None:
    fig = plt.figure(figsize=(7.2, 3.1), constrained_layout=False)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.36)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

    methods = ["Ours", "CoverUp", "CodaMOSA"]
    total_cost = [2.07, 5.11, 5.95]
    colors = [COLORS["ours"], COLORS["coverup"], COLORS["codamosa"]]
    x = np.arange(len(methods))
    bars = ax1.bar(x, total_cost, color=colors, width=0.55, zorder=2)
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.16, f"${h:.2f}", ha="center", va="bottom", fontsize=7)
    ax1.text(x[2], total_cost[2] + 0.55, "estimated", ha="center", fontsize=6.5, color="#666666")
    ax1.set_ylim(0, 7.0)
    ax1.set_ylabel("Estimated LLM cost (USD)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(methods)
    despine(ax1)
    panel_label(ax1, "a")
    ax1.set_title("Estimated total LLM cost", fontsize=8.5, pad=8)

    methods2 = ["Pynguin", "Ours", "CoverUp", "CodaMOSA"]
    records = [228, 228, 227, 215]
    colors2 = [COLORS["pynguin"], COLORS["ours"], COLORS["coverup"], COLORS["codamosa"]]
    x2 = np.arange(len(methods2))
    bars = ax2.bar(x2, records, color=colors2, width=0.62, zorder=2)
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, h + 3, f"{int(h)}", ha="center", va="bottom", fontsize=7)
    ax2.set_ylim(0, 250)
    ax2.set_ylabel("Programs with comparable coverage records")
    ax2.set_xticks(x2)
    ax2.set_xticklabels(methods2, rotation=25, ha="right")
    despine(ax2)
    panel_label(ax2, "b")
    ax2.set_title("Recorded outcomes across the full benchmark", fontsize=8.5, pad=8)
    save_figure(fig, "figure4_3_cost_reliability")


def main() -> None:
    figure3_1_method_flow()
    figure3_2_prompt_structure()
    figure3_3_feedback_prompt()
    figure4_1_results_overview()
    figure4_2_model_ablation()
    figure4_3_cost_reliability()
    print(f"Figures written to {OUT}")


if __name__ == "__main__":
    main()
