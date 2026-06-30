"""工程根路径、程序目录（只读输入）与就地结果目录布局。

本项目的历史布局曾出现过“结果写在 `pynguin/` 下，但 suite 又叫 coverup-failed/codamosa”
的情况。为避免你已有产物丢失，本文件提供：
1) 面向新布局的默认映射
2) 对旧布局的自动回退（只在新目录不存在时生效）
"""

from __future__ import annotations

import json
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
ROOT = _TOOLS.parent
SCI_ROOT = ROOT / "scientific_calculation"
PROGRAMS_JSON = _TOOLS / "programs.json"
NEW_PROGRAM_PREFIXES = (
    "PDEBench_",
    "FiPy_",
    "SfePy_",
    "CodaCover_",
    "NumPy_",
    "SciPy_",
    "PDEExtra_",
    "FiPyExtra_",
    "SfePyExtra_",
    "TBCExtra_",
    "CodaExtra_",
    "AlgoExtra_",
    "NumericalExtra_",
    "ODEPDEExtra_",
)


def default_results_root() -> Path:
    """
    兼容旧参数保留。
    新布局已不再使用统一 results 根目录，结果默认写入各程序目录下 result_4o/。
    """
    return ROOT.resolve()


def load_program_names() -> list[str]:
    data = json.loads(PROGRAMS_JSON.read_text(encoding="utf-8-sig"))
    return list(data["programs"])


def load_new_program_names() -> list[str]:
    """Programs added after the original 36-program dataset."""
    return [name for name in load_program_names() if name.startswith(NEW_PROGRAM_PREFIXES)]


def load_pde_program_names() -> list[str]:
    """与 scientific_programs_catalog 中偏微分/差分类一致；可在 programs.json 里改。"""
    data = json.loads(PROGRAMS_JSON.read_text(encoding="utf-8-sig"))
    return list(data.get("pde_subset", []))


def summary_csv_path(results_root: Path, suite: str) -> Path:
    # 汇总文件默认放到对应 suite 根目录，避免生成顶层 results 目录
    s = suite.lower().strip()
    return (SCI_ROOT / f"coverage_summary_{s}.csv").resolve()


def chatgpt_overrides() -> dict[str, str]:
    data = json.loads(PROGRAMS_JSON.read_text(encoding="utf-8-sig"))
    return dict(data.get("chatgpt_subdir_overrides", {}))


def program_root(canonical_name: str) -> Path:
    """被测科学计算程序根目录：`scientific_calculation/<program>/`。"""
    return SCI_ROOT / canonical_name


def program_dir(suite: str, canonical_name: str) -> Path:
    """只读：被测程序所在目录（应至少包含 example.py）。

    suite->目录映射：
    - pynguin : `scientific_calculation/<program>/pynguin`
    - chatgpt : `scientific_calculation/<program>/chatgpt`
    - coverup : `scientific_calculation/<program>/coverup`
    - codamosa: `scientific_calculation/<program>/codamosa`
    """
    suite = suite.lower().strip()
    if suite not in {"pynguin", "coverup", "coverup-failed", "codamosa", "chatgpt"}:
        raise ValueError("suite must be pynguin / coverup / codamosa / chatgpt")
    return program_root(canonical_name) / suite


def example_path(suite: str, canonical_name: str) -> Path:
    """示例/被测源代码：只放在程序根目录。"""
    del suite  # 兼容旧签名
    return program_root(canonical_name) / "example.py"


def program_results_dir(results_root: Path, suite: str, canonical_name: str) -> Path:
    """某一程序专属结果目录（会用于 pytest / coverage 输出）。

    新布局：
    - pynguin : scientific_calculation/<program>/pynguin/result_4o
    - chatgpt : scientific_calculation/<program>/chatgpt/result_4o
    - coverup : scientific_calculation/<program>/coverup/result_4o
    - codamosa: scientific_calculation/<program>/codamosa/result_4o

    兼容旧布局回退：
    - coverup-failed 历史上可能写在 scientific_calculation/<program>/pynguin/result_coverup
    - codamosa 历史上可能写在 scientific_calculation/<program>/pynguin/result_codamosa
    """
    del results_root  # 兼容旧签名
    s = suite.lower().strip()

    preferred = {
        "pynguin": SCI_ROOT / canonical_name / "pynguin" / "result_4o",
        "chatgpt": SCI_ROOT / canonical_name / "chatgpt" / "result_4o",
        "coverup": SCI_ROOT / canonical_name / "coverup" / "result_4o",
        "coverup-failed": SCI_ROOT / canonical_name / "coverup" / "result_4o",
        "codamosa": SCI_ROOT / canonical_name / "codamosa" / "result_4o",
    }.get(s)

    if preferred is None:
        raise ValueError("suite must be pynguin / coverup / codamosa / chatgpt")

    # 如果新目录存在，优先使用新目录
    if preferred.exists():
        return preferred.resolve()

    # 兼容旧布局
    if s in {"coverup", "coverup-failed"}:
        legacy0 = SCI_ROOT / canonical_name / "coverup-failed" / "result_4o"
        if legacy0.exists():
            return legacy0.resolve()
        legacy = SCI_ROOT / canonical_name / "pynguin" / "result_coverup"
        if legacy.exists():
            return legacy.resolve()
        # 再兜底：曾有过 scientific_calculation/<program>/result_coverup
        legacy2 = SCI_ROOT / canonical_name / "result_coverup"
        if legacy2.exists():
            return legacy2.resolve()
    if s == "codamosa":
        legacy = SCI_ROOT / canonical_name / "pynguin" / "result_codamosa"
        if legacy.exists():
            return legacy.resolve()
        legacy2 = SCI_ROOT / canonical_name / "result_codamosa"
        if legacy2.exists():
            return legacy2.resolve()
    if s == "pynguin":
        legacy = SCI_ROOT / canonical_name / "result_4o"
        if legacy.exists():
            return legacy.resolve()

    # 新目录不存在时，返回 preferred（调用方会 mkdir）
    return preferred.resolve()
