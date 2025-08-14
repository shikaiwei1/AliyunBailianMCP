#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云百炼MCP工具集一键发布脚本

此脚本用于自动发布两个MCP工具到PyPI：
1. mcp-server-bailian-video-synthesis (视频合成工具)
2. mcp-server-bailian-image (图像生成工具)

使用方法:
    python publish_all.py [--test-pypi] [--skip-tests]
    
参数:
    --test-pypi: 上传到测试PyPI而不是正式PyPI
    --skip-tests: 跳过测试步骤
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """
    运行命令并返回结果
    
    Args:
        cmd: 要运行的命令
        cwd: 工作目录
        check: 是否检查返回码
        
    Returns:
        subprocess.CompletedProcess: 命令执行结果
    """
    print(f"[CMD] {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    if cwd:
        print(f"[CWD] {cwd}")
    
    result = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True if isinstance(cmd, str) else False,
        check=False,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    if result.stdout:
        print(f"[OUT] {result.stdout.strip()}")
    if result.stderr:
        print(f"[ERR] {result.stderr.strip()}")
    
    if check and result.returncode != 0:
        print(f"[FAIL] 命令执行失败，退出码: {result.returncode}")
        sys.exit(1)
    
    return result


def publish_tool(tool_path, tool_name, test_pypi=False, skip_tests=False):
    """
    发布单个工具
    
    Args:
        tool_path: 工具路径
        tool_name: 工具名称
        test_pypi: 是否上传到测试PyPI
        skip_tests: 是否跳过测试
        
    Returns:
        bool: 是否成功
    """
    print(f"\n{'='*60}")
    print(f"[PUBLISH] 开始发布工具: {tool_name}")
    print(f"{'='*60}")
    
    if not os.path.exists(tool_path):
        print(f"[ERROR] 工具目录不存在: {tool_path}")
        return False
    
    try:
        # 1. 运行测试（如果不跳过）
        if not skip_tests:
            print(f"\n[STEP 1] 运行测试...")
            result = run_command([sys.executable, "run_tests.py"], cwd=tool_path, check=False)
            if result.returncode != 0:
                print(f"[ERROR] {tool_name} 测试失败")
                return False
            print(f"[SUCCESS] {tool_name} 测试通过")
        else:
            print(f"\n[SKIP] 跳过测试步骤")
        
        # 2. 清理旧的构建文件
        print(f"\n[STEP 2] 清理旧的构建文件...")
        dist_path = os.path.join(tool_path, "dist")
        build_path = os.path.join(tool_path, "build")
        
        if os.path.exists(dist_path):
            run_command(["rmdir", "/s", "/q", "dist"], cwd=tool_path, check=False)
        if os.path.exists(build_path):
            run_command(["rmdir", "/s", "/q", "build"], cwd=tool_path, check=False)
        
        # 3. 构建包
        print(f"\n[STEP 3] 构建包...")
        run_command([sys.executable, "-m", "build"], cwd=tool_path)
        print(f"[SUCCESS] {tool_name} 包构建完成")
        
        # 4. 检查包
        print(f"\n[STEP 4] 检查包完整性...")
        run_command(["twine", "check", "dist/*"], cwd=tool_path)
        print(f"[SUCCESS] {tool_name} 包检查通过")
        
        # 5. 上传包
        print(f"\n[STEP 5] 上传包到PyPI...")
        if test_pypi:
            upload_cmd = ["twine", "upload", "--repository", "testpypi", "dist/*"]
            print(f"[INFO] 上传到测试PyPI")
        else:
            upload_cmd = ["twine", "upload", "dist/*"]
            print(f"[INFO] 上传到正式PyPI")
        
        result = run_command(upload_cmd, cwd=tool_path, check=False)
        if result.returncode != 0:
            print(f"[ERROR] {tool_name} 上传失败")
            return False
        
        print(f"[SUCCESS] {tool_name} 发布成功！")
        return True
        
    except Exception as e:
        print(f"[ERROR] 发布 {tool_name} 时发生错误: {e}")
        return False


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="阿里云百炼MCP工具集一键发布脚本")
    parser.add_argument("--test-pypi", action="store_true", help="上传到测试PyPI")
    parser.add_argument("--skip-tests", action="store_true", help="跳过测试步骤")
    
    args = parser.parse_args()
    
    print("🚀 阿里云百炼MCP工具集发布脚本")
    print(f"测试PyPI: {'是' if args.test_pypi else '否'}")
    print(f"跳过测试: {'是' if args.skip_tests else '否'}")
    
    # 获取项目根目录
    project_root = Path(__file__).parent
    
    # 定义工具列表
    tools = [
        {
            "name": "mcp-server-bailian-video-synthesis",
            "path": project_root / "mcp_server_bailian_video_synthesis",
            "description": "视频合成工具"
        },
        {
            "name": "mcp-server-bailian-image",
            "path": project_root / "mcp_server_bailian_image",
            "description": "图像生成工具"
        }
    ]
    
    # 发布前检查
    print(f"\n[CHECK] 运行发布前检查...")
    check_result = run_command([sys.executable, "check_release_readiness.py"], cwd=project_root, check=False)
    if check_result.returncode != 0:
        print(f"[WARNING] 发布前检查发现问题，但继续发布...")
    
    # 发布每个工具
    success_count = 0
    failed_tools = []
    
    for tool in tools:
        print(f"\n[INFO] 准备发布: {tool['description']} ({tool['name']})")
        
        if publish_tool(
            tool_path=str(tool['path']),
            tool_name=tool['name'],
            test_pypi=args.test_pypi,
            skip_tests=args.skip_tests
        ):
            success_count += 1
        else:
            failed_tools.append(tool['name'])
    
    # 发布总结
    print(f"\n{'='*60}")
    print(f"[SUMMARY] 发布总结")
    print(f"{'='*60}")
    print(f"成功发布: {success_count}/{len(tools)} 个工具")
    
    if failed_tools:
        print(f"失败工具: {', '.join(failed_tools)}")
        print(f"[FAILED] 部分工具发布失败")
        sys.exit(1)
    else:
        print(f"[SUCCESS] 所有工具发布成功！")
        
        # 显示安装命令
        print(f"\n[INFO] 安装命令:")
        for tool in tools:
            if args.test_pypi:
                print(f"  pip install -i https://test.pypi.org/simple/ {tool['name']}")
            else:
                print(f"  pip install {tool['name']}")


if __name__ == "__main__":
    main()