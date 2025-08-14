#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云百炼图像生成MCP工具发布脚本

此脚本用于自动化发布流程，包括：
1. 运行测试
2. 构建包
3. 检查包完整性
4. 上传到PyPI

Usage:
    python publish.py [--test-pypi] [--skip-tests]
    
Options:
    --test-pypi: 上传到测试PyPI而不是正式PyPI
    --skip-tests: 跳过测试步骤
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, check=True):
    """
    执行命令并返回结果
    
    Args:
        cmd (str): 要执行的命令
        check (bool): 是否检查返回码
        
    Returns:
        subprocess.CompletedProcess: 命令执行结果
    """
    print(f"执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if check and result.returncode != 0:
        print(f"命令执行失败: {cmd}")
        print(f"错误输出: {result.stderr}")
        sys.exit(1)
    
    if result.stdout:
        print(result.stdout)
    
    return result


def check_prerequisites():
    """
    检查发布前置条件
    """
    print("检查发布前置条件...")
    
    # 检查必要的工具
    required_tools = ['python', 'pip']
    for tool in required_tools:
        result = run_command(f"which {tool}", check=False)
        if result.returncode != 0:
            print(f"错误: 未找到必要工具 {tool}")
            sys.exit(1)
    
    # 检查必要的包
    required_packages = ['build', 'twine']
    for package in required_packages:
        result = run_command(f"pip show {package}", check=False)
        if result.returncode != 0:
            print(f"安装缺失的包: {package}")
            run_command(f"pip install {package}")
    
    print("前置条件检查完成")


def run_tests():
    """
    运行测试套件
    """
    print("运行测试套件...")
    
    if os.path.exists("run_tests.py"):
        run_command("python run_tests.py")
    else:
        run_command("pytest test/ -v")
    
    print("测试通过")


def clean_build():
    """
    清理构建文件
    """
    print("清理构建文件...")
    
    dirs_to_clean = ['dist', 'build', '*.egg-info']
    for dir_pattern in dirs_to_clean:
        if os.name == 'nt':  # Windows
            run_command(f"if exist {dir_pattern} rmdir /s /q {dir_pattern}", check=False)
        else:  # Unix-like
            run_command(f"rm -rf {dir_pattern}", check=False)
    
    print("构建文件清理完成")


def build_package():
    """
    构建包
    """
    print("构建包...")
    run_command("python -m build")
    print("包构建完成")


def check_package():
    """
    检查包完整性
    """
    print("检查包完整性...")
    run_command("twine check dist/*")
    print("包检查通过")


def upload_package(test_pypi=False):
    """
    上传包到PyPI
    
    Args:
        test_pypi (bool): 是否上传到测试PyPI
    """
    if test_pypi:
        print("上传到测试PyPI...")
        run_command("twine upload --repository testpypi dist/*")
        print("上传到测试PyPI完成")
    else:
        print("上传到正式PyPI...")
        
        # 确认上传
        confirm = input("确认上传到正式PyPI? (y/N): ")
        if confirm.lower() != 'y':
            print("取消上传")
            return
        
        run_command("twine upload dist/*")
        print("上传到正式PyPI完成")


def get_version():
    """
    从pyproject.toml获取版本号
    
    Returns:
        str: 版本号
    """
    try:
        with open('pyproject.toml', 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.split('\n'):
                if line.strip().startswith('version ='):
                    version = line.split('=')[1].strip().strip('"')
                    return version
    except Exception as e:
        print(f"无法获取版本号: {e}")
    return "unknown"


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='发布MCP工具到PyPI')
    parser.add_argument('--test-pypi', action='store_true', 
                       help='上传到测试PyPI而不是正式PyPI')
    parser.add_argument('--skip-tests', action='store_true', 
                       help='跳过测试步骤')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("MCP Server Bailian Image 发布脚本")
    print(f"版本: {get_version()}")
    print("=" * 50)
    
    try:
        # 检查前置条件
        check_prerequisites()
        
        # 运行测试
        if not args.skip_tests:
            run_tests()
        else:
            print("跳过测试步骤")
        
        # 清理构建文件
        clean_build()
        
        # 构建包
        build_package()
        
        # 检查包
        check_package()
        
        # 上传包
        upload_package(test_pypi=args.test_pypi)
        
        print("\n" + "=" * 50)
        print("发布完成!")
        
        if args.test_pypi:
            print("测试安装命令:")
            print("pip install --index-url https://test.pypi.org/simple/ mcp-server-bailian-image")
        else:
            print("安装命令:")
            print("pip install mcp-server-bailian-image")
        
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n发布被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n发布失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()