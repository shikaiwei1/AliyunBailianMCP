#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云百炼MCP工具发布准备检查脚本

此脚本用于检查两个MCP工具是否准备好发布到PyPI，包括：
1. 文件完整性检查
2. 配置文件验证
3. 测试运行状态
4. 文档完整性
5. 版本一致性

Usage:
    python check_release_readiness.py
"""

import os
import sys
import subprocess
from pathlib import Path
import re


class ReleaseChecker:
    """
    发布准备检查器
    """
    
    def __init__(self):
        self.tools = [
            'mcp_server_bailian_video_synthesis',
            'mcp_server_bailian_image'
        ]
        self.errors = []
        self.warnings = []
        self.success_count = 0
        self.total_checks = 0
    
    def log_error(self, message):
        """记录错误信息"""
        self.errors.append(f"❌ {message}")
        print(f"❌ {message}")
    
    def log_warning(self, message):
        """记录警告信息"""
        self.warnings.append(f"⚠️  {message}")
        print(f"⚠️  {message}")
    
    def log_success(self, message):
        """记录成功信息"""
        self.success_count += 1
        print(f"✅ {message}")
    
    def check_file_exists(self, file_path, description):
        """检查文件是否存在"""
        self.total_checks += 1
        if os.path.exists(file_path):
            self.log_success(f"{description}: {file_path}")
            return True
        else:
            self.log_error(f"{description}不存在: {file_path}")
            return False
    
    def check_directory_structure(self, tool_name):
        """检查目录结构"""
        print(f"\n📁 检查 {tool_name} 目录结构...")
        
        base_path = Path(tool_name)
        
        # 必需文件列表
        required_files = [
            'pyproject.toml',
            'requirements.txt',
            'README.md',
            'PUBLISH.md',
            'CHANGELOG.md',
            'publish.py',
            'run_tests.py',
            f'src/{tool_name}/__init__.py',
            f'src/{tool_name}/server.py',
            'test/__init__.py'
        ]
        
        for file_path in required_files:
            full_path = base_path / file_path
            self.check_file_exists(full_path, f"必需文件")
    
    def check_pyproject_toml(self, tool_name):
        """检查pyproject.toml配置"""
        print(f"\n⚙️  检查 {tool_name} pyproject.toml配置...")
        
        pyproject_path = Path(tool_name) / 'pyproject.toml'
        
        if not os.path.exists(pyproject_path):
            self.log_error(f"pyproject.toml不存在: {pyproject_path}")
            return
        
        try:
            with open(pyproject_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查必需字段
            required_fields = [
                'name =',
                'version =',
                'description =',
                'authors =',
                'dependencies ='
            ]
            
            for field in required_fields:
                self.total_checks += 1
                if field in content:
                    self.log_success(f"pyproject.toml包含{field.strip(' =')}字段")
                else:
                    self.log_error(f"pyproject.toml缺少{field.strip(' =')}字段")
            
            # 检查版本号格式
            version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
            if version_match:
                version = version_match.group(1)
                if re.match(r'^\d+\.\d+\.\d+$', version):
                    self.log_success(f"版本号格式正确: {version}")
                else:
                    self.log_warning(f"版本号格式可能不规范: {version}")
            
        except Exception as e:
            self.log_error(f"读取pyproject.toml失败: {e}")
    
    def check_requirements_txt(self, tool_name):
        """检查requirements.txt"""
        print(f"\n📦 检查 {tool_name} requirements.txt...")
        
        req_path = Path(tool_name) / 'requirements.txt'
        
        if not os.path.exists(req_path):
            self.log_error(f"requirements.txt不存在: {req_path}")
            return
        
        try:
            with open(req_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查基本依赖
            if 'mcp' in content:
                self.log_success("requirements.txt包含mcp依赖")
            else:
                self.log_error("requirements.txt缺少mcp依赖")
            
            # 检查工具特定依赖
            if tool_name == 'mcp_server_bailian_video_synthesis':
                if 'httpx' in content:
                    self.log_success("requirements.txt包含httpx依赖")
                else:
                    self.log_warning("requirements.txt可能缺少httpx依赖")
            
            elif tool_name == 'mcp_server_bailian_image':
                if 'dashscope' in content:
                    self.log_success("requirements.txt包含dashscope依赖")
                else:
                    self.log_error("requirements.txt缺少dashscope依赖")
            
        except Exception as e:
            self.log_error(f"读取requirements.txt失败: {e}")
    
    def check_documentation(self, tool_name):
        """检查文档完整性"""
        print(f"\n📚 检查 {tool_name} 文档完整性...")
        
        base_path = Path(tool_name)
        
        # 检查README.md
        readme_path = base_path / 'README.md'
        if os.path.exists(readme_path):
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查README内容
                required_sections = ['安装', '使用', '示例']
                for section in required_sections:
                    self.total_checks += 1
                    if section in content:
                        self.log_success(f"README.md包含{section}部分")
                    else:
                        self.log_warning(f"README.md可能缺少{section}部分")
                
            except Exception as e:
                self.log_error(f"读取README.md失败: {e}")
    
    def run_tests(self, tool_name):
        """运行测试"""
        print(f"\n🧪 运行 {tool_name} 测试...")
        
        test_script = Path(tool_name) / 'run_tests.py'
        
        if not os.path.exists(test_script):
            self.log_error(f"测试脚本不存在: {test_script}")
            return
        
        try:
            # 切换到工具目录
            original_cwd = os.getcwd()
            os.chdir(tool_name)
            
            # 运行测试
            result = subprocess.run(
                [sys.executable, 'run_tests.py'],
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='ignore'
            )
            
            os.chdir(original_cwd)
            
            self.total_checks += 1
            if result.returncode == 0:
                self.log_success(f"测试通过")
            else:
                self.log_error(f"测试失败: {result.stderr.strip()}")
                
        except subprocess.TimeoutExpired:
            self.log_error("测试超时")
            os.chdir(original_cwd)
        except Exception as e:
            self.log_error(f"运行测试失败: {str(e)}")
            os.chdir(original_cwd)
    
    def check_tool(self, tool_name):
        """检查单个工具"""
        print(f"\n{'='*60}")
        print(f"[CHECK] 检查工具: {tool_name}")
        print(f"{'='*60}")
        
        if not os.path.exists(tool_name):
            self.log_error(f"工具目录不存在: {tool_name}")
            return
        
        # 执行各项检查
        self.check_directory_structure(tool_name)
        self.check_pyproject_toml(tool_name)
        self.check_requirements_txt(tool_name)
        self.check_documentation(tool_name)
        self.run_tests(tool_name)
    
    def generate_report(self):
        """生成检查报告"""
        print(f"\n{'='*60}")
        print("[REPORT] 发布准备检查报告")
        print(f"{'='*60}")
        
        print(f"\n[SUCCESS] 成功检查: {self.success_count}/{self.total_checks}")
        print(f"[WARNING] 警告数量: {len(self.warnings)}")
        print(f"[ERROR] 错误数量: {len(self.errors)}")
        
        if self.warnings:
            print("\n[WARNING] 警告列表:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if self.errors:
            print("\n[ERROR] 错误列表:")
            for error in self.errors:
                print(f"  {error}")
        
        # 总体评估
        print(f"\n{'='*60}")
        if not self.errors:
            if not self.warnings:
                print("[SUCCESS] 所有检查通过！工具已准备好发布。")
            else:
                print("[OK] 基本检查通过，但有一些警告需要注意。")
        else:
            print("[FAILED] 发现错误，需要修复后才能发布。")
        
        print(f"{'='*60}")
        
        return len(self.errors) == 0
    
    def run(self):
        """运行完整检查"""
        print("[START] 开始发布准备检查...")
        
        # 检查每个工具
        for tool_name in self.tools:
            self.check_tool(tool_name)
        
        # 生成报告
        success = self.generate_report()
        
        return success


def main():
    """
    主函数
    """
    checker = ReleaseChecker()
    success = checker.run()
    
    # 返回适当的退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()