BCBT 实验脚手架（以 tools/ 为准）
================================

依赖（在已激活的 conda 环境中）：
  pip install -r tools/requirements.txt

须安装：pynguin、coverage、pytest；数值库建议 conda 安装 numpy scipy sympy matplotlib。

核心文件
--------
  programs.json      36 个程序名 + chatgpt 目录映射 + pde_subset（可改）
  paths.py             路径解析
  run_pynguin.py       Pynguin 生成测试 -> results/<suite>/<程序>/
  coverage_measure.py  coverage + pytest -> 同上结果目录
  coveragerc           coverage 配置（含 omit 测试文件）
  run_all.sh / run_all.ps1  一键：Pynguin 后跑覆盖率

常用命令（在 BCBT 根目录）
--------------------------
  python tools/run_pynguin.py --list
  python tools/run_pynguin.py --program euler_diffusion
  python tools/run_pynguin.py --all
  python tools/run_pynguin.py --pde

  python tools/coverage_measure.py --suite pynguin --program euler_diffusion
  python tools/coverage_measure.py --suite pynguin --all
  python tools/coverage_measure.py --suite pynguin --pde

  bash tools/run_all.sh
  bash tools/run_all.sh --pde --time 300
  powershell -File tools\run_all.ps1
  powershell -File tools\run_all.ps1 -Pde -Time 300

输出
----
  results/<suite>/<程序>/test_example.py、pynguin.log、.coverage、coverage_report_example.txt 等
  批量时 results/coverage_summary_<suite>.csv

关于 Claude 版本
----------------
若你有一份「根目录下的 coverage_measure.py / paths.py / programs.json」：
  - 其中 programs.json 若含仓库里不存在的程序名，不能直接替换本项目的 programs.json。
  - 已合并其合理点：--all / --pde、批量 CSV、run_all 脚本；Pynguin 仍使用与本项目一致的 CLI
   （maximum-search-time、subprocess=false 等），避免你之前遇到的 EOFError。
