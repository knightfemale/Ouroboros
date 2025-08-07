# utils/nuitka_util.py
scripts = """# nuitka_build.py
import sys
import subprocess
from pathlib import Path
def main() -> None:
    command = [sys.executable] + {command}
    print("打包命令:", " ".join(command))
    try:
        subprocess.run(command, cwd=Path(__file__).parent)
    except subprocess.CalledProcessError as e:
        print(f"构建错误! 出错原因: {{e}}")
        sys.exit(1)
    except FileNotFoundError:
        print("未找到 nuitka! 请安装: pip install nuitka")
        sys.exit(1)
if __name__ == "__main__":
    main()
"""
