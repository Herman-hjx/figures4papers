import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as path_effects


PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "blue_light": "#DDEAF8",
    "teal": "#42949E",
    "teal_light": "#DFF1F0",
    "green": "#5FB27A",
    "green_light": "#E6F6EA",
    "purple": "#7D5BA6",
    "purple_light": "#F0E7FB",
    "orange": "#E78B3C",
    "orange_light": "#FDE7D5",
    "red": "#B64342",
    "red_light": "#F8D7D6",
    "gray": "#CFCECE",
    "gray_deep": "#4D4D4D",
    "warm_white": "#F7F7F5",
    "ink": "#2A2D2F",
    "soft_shadow": "#E0E0DE",
}


def apply_style():
    plt.rcParams.update({
        "figure.facecolor": PALETTE["warm_white"],
        "axes.facecolor": PALETTE["warm_white"],
        "font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
        "font.size": 18,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.spines.left": False,
        "axes.spines.bottom": False,
        "axes.linewidth": 2.2,
        "svg.fonttype": "none",
        "axes.unicode_minus": False,
    })


def add_card(ax, x, y, w, h, title, subtitle, facecolor, edgecolor, title_color=None, subtitle_color=None):
    card = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.12",
        linewidth=2.2,
        edgecolor=edgecolor,
        facecolor=facecolor,
        zorder=2,
    )
    card.set_path_effects([
        path_effects.withSimplePatchShadow(offset=(2, -2), alpha=0.18, shadow_rgbFace=(0, 0, 0)),
        path_effects.Normal(),
    ])
    ax.add_patch(card)

    if title_color is None:
        title_color = PALETTE["ink"]
    if subtitle_color is None:
        subtitle_color = PALETTE["gray_deep"]

    ax.text(
        x + w / 2,
        y + h * 0.62,
        title,
        ha="center",
        va="center",
        fontsize=20,
        color=title_color,
        fontweight="bold",
        zorder=3,
    )

    if subtitle:
        ax.text(
            x + w / 2,
            y + h * 0.28,
            subtitle,
            ha="center",
            va="center",
            fontsize=12,
            color=subtitle_color,
            fontweight="normal",
            zorder=3,
        )

    return card


def add_arrow(ax, x1, y1, x2, y2, color=PALETTE["gray_deep"], lw=2.6, dashed=False):
    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=lw,
        linestyle=(0, (6, 4)) if dashed else "solid",
        color=color,
        zorder=1,
    )
    ax.add_patch(arrow)


def add_chip(ax, x, y, r, text, color, text_color="white"):
    dot = Circle((x, y), r, facecolor=color, edgecolor=color, linewidth=1.5, zorder=3)
    ax.add_patch(dot)
    ax.text(x, y, text, ha="center", va="center", fontsize=14, fontweight="bold", color=text_color, zorder=4)


def main():
    apply_style()
    fig = plt.figure(figsize=(16, 9), dpi=300, facecolor=PALETTE["warm_white"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()

    ax.text(
        0.5,
        0.92,
        "前端委任型：生成任务集中分配的分工共创",
        ha="center",
        va="center",
        fontsize=26,
        fontweight="bold",
        color=PALETTE["ink"],
        zorder=5,
    )

    # central actors
    left = add_card(
        ax,
        0.085,
        0.58,
        0.22,
        0.18,
        "人类作者",
        "任务设定与方向控制",
        facecolor=PALETTE["blue_light"],
        edgecolor=PALETTE["blue_main"],
        title_color=PALETTE["blue_main"],
    )
    center = add_card(
        ax,
        0.39,
        0.58,
        0.22,
        0.18,
        "AI",
        "文本生成与候选构建",
        facecolor=PALETTE["purple_light"],
        edgecolor=PALETTE["purple"],
        title_color=PALETTE["purple"],
    )
    right = add_card(
        ax,
        0.68,
        0.58,
        0.22,
        0.18,
        "人类作者",
        "结果接受与价值判断",
        facecolor=PALETTE["teal_light"],
        edgecolor=PALETTE["teal"],
        title_color=PALETTE["teal"],
    )

    add_arrow(ax, 0.305, 0.67, 0.39, 0.67, color=PALETTE["blue_main"], lw=2.8)
    add_arrow(ax, 0.61, 0.67, 0.68, 0.67, color=PALETTE["purple"], lw=2.8)

    # R/T/E panel
    panel_x, panel_y, panel_w, panel_h = 0.83, 0.50, 0.12, 0.28
    panel = FancyBboxPatch(
        (panel_x, panel_y), panel_w, panel_h,
        boxstyle="round,pad=0.012,rounding_size=0.1",
        linewidth=2.2,
        facecolor=PALETTE["gray"],
        edgecolor=PALETTE["gray_deep"],
        alpha=0.22,
        zorder=1,
    )
    ax.add_patch(panel)
    ax.text(panel_x + panel_w / 2, panel_y + panel_h * 0.90, "R / T / E", ha="center", va="center", fontsize=18, fontweight="bold", color=PALETTE["gray_deep"])

    add_chip(ax, panel_x + panel_w * 0.22, panel_y + panel_h * 0.68, 0.05, "R", PALETTE["blue_main"])
    add_chip(ax, panel_x + panel_w * 0.22, panel_y + panel_h * 0.45, 0.05, "T", PALETTE["purple"])
    add_chip(ax, panel_x + panel_w * 0.22, panel_y + panel_h * 0.22, 0.05, "E", PALETTE["green"])

    ax.text(panel_x + panel_w * 0.52, panel_y + panel_h * 0.68, "约束定义权", ha="left", va="center", fontsize=11, color=PALETTE["blue_main"], fontweight="bold")
    ax.text(panel_x + panel_w * 0.52, panel_y + panel_h * 0.45, "创意生成遍历权", ha="left", va="center", fontsize=11, color=PALETTE["purple"], fontweight="bold")
    ax.text(panel_x + panel_w * 0.52, panel_y + panel_h * 0.22, "价值评判权", ha="left", va="center", fontsize=11, color=PALETTE["green"], fontweight="bold")

    ax.text(
        panel_x + panel_w / 2,
        panel_y - 0.04,
        "人类作者：主要保留 R，定义创作约束\nAI：主要承担 T，生成文本候选\n人类作者：在结果端行使 E，决定是否接受\n仅为功能结构说明，非认知过程测量",
        ha="center",
        va="top",
        fontsize=9.5,
        color=PALETTE["gray_deep"],
        linespacing=1.4,
    )

    # process flow boxes
    process_boxes = [
        (0.07, 0.28, 0.18, 0.12, "输入", "任务设定\n提示 / 约束", PALETTE["blue_light"], PALETTE["blue_main"]),
        (0.30, 0.28, 0.19, 0.12, "AI文本生成", "创意遍历与候选产出", PALETTE["orange_light"], PALETTE["orange"]),
        (0.55, 0.28, 0.18, 0.12, "人类筛选", "接受或拒绝", PALETTE["green_light"], PALETTE["green"]),
        (0.79, 0.28, 0.15, 0.12, "输出", "进入最终文本\n或被回退", PALETTE["red_light"], PALETTE["red"]),
    ]

    for i, (x, y, w, h, label, subtitle, facecolor, edgecolor) in enumerate(process_boxes):
        add_card(ax, x, y, w, h, label, subtitle, facecolor, edgecolor, title_color=edgecolor, subtitle_color=edgecolor)
        if i < len(process_boxes) - 1:
            add_arrow(ax, x + w, y + h / 2, process_boxes[i + 1][0], process_boxes[i + 1][1] + process_boxes[i + 1][3] / 2, color=edgecolor, lw=2.2)

    # branching accept/reject arrow from screening
    add_arrow(ax, 0.55 + 0.18, 0.28 + 0.06, 0.79, 0.31, color=PALETTE["green"], lw=2.2)
    add_arrow(ax, 0.55 + 0.09, 0.28, 0.55 + 0.09, 0.17, color=PALETTE["red"], lw=2.2, dashed=True)
    ax.text(0.63, 0.16, "被回退", ha="center", va="center", fontsize=12, color=PALETTE["red"], fontweight="bold")
    ax.text(0.87, 0.36, "进入最终文本", ha="center", va="center", fontsize=11, color=PALETTE["red"], fontweight="bold")

    # lower comparison panel
    compare_x0, compare_y0, compare_w = 0.10, 0.08, 0.32
    compare1 = FancyBboxPatch(
        (compare_x0, compare_y0), compare_w, 0.16,
        boxstyle="round,pad=0.012,rounding_size=0.1",
        facecolor=PALETTE["blue_light"],
        edgecolor=PALETTE["blue_main"],
        linewidth=2.8,
        zorder=2,
    )
    compare1.set_path_effects([
        path_effects.withSimplePatchShadow(offset=(2, -2), alpha=0.20, shadow_rgbFace=(0, 0, 0)),
        path_effects.Normal(),
    ])
    ax.add_patch(compare1)
    ax.text(compare_x0 + compare_w / 2, compare_y0 + 0.08, "生成—验收", ha="center", va="center", fontsize=23, fontweight="bold", color=PALETTE["blue_main"])

    compare2_x = 0.52
    compare2 = FancyBboxPatch(
        (compare2_x, compare_y0), 0.30, 0.16,
        boxstyle="round,pad=0.012,rounding_size=0.1",
        facecolor=PALETTE["warm_white"],
        edgecolor=PALETTE["gray"],
        linewidth=2.0,
        linestyle=(0, (4, 4)),
        zorder=2,
    )
    ax.add_patch(compare2)
    ax.text(compare2_x + 0.15, compare_y0 + 0.08, "提议—回应", ha="center", va="center", fontsize=21, color=PALETTE["gray_deep"], fontweight="bold")

    ax.text(0.27, 0.04, "主导机制", ha="center", va="center", fontsize=12, color=PALETTE["blue_main"], fontweight="bold")
    ax.text(0.69, 0.04, "非必然建立", ha="center", va="center", fontsize=12, color=PALETTE["gray_deep"], fontweight="bold")

    # summary annotation
    summary = (
        "生成能力的委任，不等同于创作控制权的整体转移\n"
        "AI可以承担较大比例的文本生产，而人类通过前端设置与后端筛选保持控制\n"
        "如果后续修改和反馈不足，则其授权主要发挥验收作用，而非形成新的共创轮次"
    )
    ax.text(
        0.5,
        0.01,
        summary,
        ha="center",
        va="bottom",
        fontsize=11.5,
        color=PALETTE["ink"],
        fontweight="bold",
        linespacing=1.6,
    )

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "front_end_assignment_concept")
    fig.savefig(output_path + ".png", dpi=300, facecolor=fig.get_facecolor())
    fig.savefig(output_path + ".pdf", dpi=300, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    main()
