#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频合成工具测试运行脚本

该脚本用于运行MCP Server Bailian Video Synthesis的所有测试用例。
支持不同的测试模式和详细程度。

作者: MCP开发团队
版本: 1.0.0
创建时间: 2024
"""

import sys
import os
import subprocess
from pathlib import Path


def install_dependencies():
    """
    安装测试依赖
    
    Returns:
        bool: 安装是否成功
    """
    try:
        print("正在安装测试依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✓ 依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖安装失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False


def run_tests(verbose=False, coverage=False):
    """
    运行测试用例
    
    Args:
        verbose (bool): 是否显示详细输出
        coverage (bool): 是否生成覆盖率报告
    
    Returns:
        bool: 测试是否通过
    """
    # 构建pytest命令
    cmd = [sys.executable, "-m", "pytest"]
    
    # 添加测试目录
    cmd.append("test/")
    
    # 添加选项
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])
    
    # 添加其他有用的选项
    cmd.extend([
        "--tb=short",  # 简短的错误回溯
        "--strict-markers",  # 严格标记模式
        "-ra"  # 显示所有测试结果摘要
    ])
    
    try:
        print(f"正在运行测试: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=False, text=True)
        
        if result.returncode == 0:
            print("\n[OK] 所有测试通过!")
            return True
        else:
            print(f"\n[FAIL] 测试失败，退出码: {result.returncode}")
            return False
            
    except FileNotFoundError:
        print("✗ pytest未找到，请确保已安装pytest")
        return False
    except Exception as e:
        print(f"[ERROR] 运行测试时发生错误: {e}")
        return False


def main():
    """
    主函数
    """
    print("=" * 60)
    print("MCP Server Bailian Video Synthesis 测试运行器")
    print("=" * 60)
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"当前目录: {current_dir}")
    
    # 检查必要文件
    required_files = ["requirements.txt", "test"]
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"✗ 缺少必要文件: {', '.join(missing_files)}")
        print("请确保在正确的项目目录中运行此脚本")
        sys.exit(1)
    
    # 解析命令行参数
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    coverage = "--coverage" in sys.argv
    install_deps = "--install" in sys.argv
    
    # 安装依赖（如果需要）
    if install_deps:
        if not install_dependencies():
            sys.exit(1)
    
    # 运行测试
    print("\n开始运行测试...")
    success = run_tests(verbose=verbose, coverage=coverage)
    
    if success:
        print("\n[SUCCESS] 测试完成，所有用例通过!")
        if coverage:
            print("[INFO] 覆盖率报告已生成在 htmlcov/ 目录")
    else:
        print("\n[FAILED] 测试失败，请检查错误信息")
        sys.exit(1)


if __name__ == "__main__":
    main()