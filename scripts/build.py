# scripts/build.py
import sys
import subprocess
from pathlib import Path

def main() -> None:
    # 构建 Nuitka 打包命令
    command = [
        # 使用当前 Python 解释器的路径
        sys.executable,
        
        # 表示运行模块
        "-m",
        
        # 指定要运行的模块
        "nuitka",
        
        # 指定入口文件
        "./main.py",
        
        # 启用独立模式进行输出
        "--standalone",
        
        # 启用单文件模式
        "--onefile",
        
        # 禁用控制台
        # "--disable-console",
        
        # 指定输出文件名
        "--output-filename=Ouroboros",
        
        # 输出目录
        "--output-dir=output",
        
        # 删除构建文件夹
        "--remove-output",
        
        # 使用指定编译器
        # "--mingw64",
        # "--clang",
        
        # 并行编译任务数
        "--jobs=6",
        
        # 显示执行的命令
        "--show-scons",
        
        # 包含包
        # "--include-package=",
        
        # 包含模块
        # "--include-module=",
        
        # 模块参数
        # "--module-parameter= =",
        
        # 启用插件
        "--enable-plugin=pyside6",
        
        # 包含数据文件
        # "--include-data-files= =",
        
        # 包含数据目录
        # "--include-data-dir= =",
        
        # 假设允许下载
        "--assume-yes-for-downloads",
    ]

    # 打印将要执行的完整命令
    print("构建命令:", " ".join(command))
    
    # 运行打包命令
    try:
        subprocess.run(
            # 要执行的命令列表
            command,
            # 设置工作目录为当前目录
            cwd=Path(__file__).parent.parent,
        )
    except subprocess.CalledProcessError as e:
        print(f"构建错误! 出错原因: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("未找到 nuitka! 请安装: pip install nuitka")
        sys.exit(1)

if __name__ == "__main__":
    main()
