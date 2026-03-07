#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Legado书源调试器 - 完整测试脚本
按照Legado的调试方式测试所有页面，输出到日志文件
"""
import sys
import os
import json
import argparse
from datetime import datetime

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    # 设置控制台输出编码为UTF-8
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
os.chdir(parent_dir)


def format_log_time() -> str:
    """格式化时间 - 按照Legado格式 [mm:ss.SSS]"""
    now = datetime.now()
    return f"[{now.minute:02d}:{now.second:02d}.{now.microsecond // 1000:03d}]"


def log(log_file, step: str, msg: str):
    """按照Legado格式输出日志"""
    line = f"{format_log_time()} [{step}] {msg}"
    print(line)
    log_file.write(line + '\n')
    log_file.flush()


def run_test(source_file: str, keyword: str):
    """运行测试"""
    # 打开日志文件
    log_file = open('test_result.txt', 'w', encoding='utf-8')
    
    # 加载书源
    with open(source_file, 'r', encoding='utf-8') as f:
        source_data = json.loads(f.read())

    if isinstance(source_data, list):
        source_data = source_data[0]

    from debugger.engine import BookSource, DebugEngine

    book_source = BookSource.from_dict(source_data)
    engine = DebugEngine(book_source)

    header = f"""============================================================
 Legado Book Source Debugger
============================================================
Book Source: {book_source.bookSourceName}
URL: {book_source.bookSourceUrl}
JS Lib: {'Yes' if book_source.jsLib else 'No'}
Keyword: {keyword}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
============================================================"""
    print(header)
    log_file.write(header + '\n')
    log_file.flush()

    results = {}

    # 1. 搜索测试
    print("\n" + "="*60)
    print(" [1] Search Test")
    print("="*60)
    log_file.write("\n" + "="*60 + "\n [1] Search Test\n" + "="*60 + "\n")
    log_file.flush()

    search_result = engine.test_search(keyword)
    results['search'] = search_result

    # 输出调试日志
    if hasattr(search_result, 'steps') and search_result.steps:
        for step_info in search_result.steps:
            if isinstance(step_info, dict):
                step_name = step_info.get('step', '搜索')
                msg = step_info.get('message', '')
                if msg:
                    log(log_file, step_name, msg)

    log(log_file, "搜索", f"Success: {search_result.success}")
    log(log_file, "搜索", f"Message: {search_result.message}")

    if search_result.data:
        log(log_file, "搜索", f"Results: {len(search_result.data)}")
        for i, item in enumerate(search_result.data[:3], 1):
            log(log_file, "搜索", f"  [{i}] {item.name} - {item.author}")

    # 2. 详情测试
    print("\n" + "="*60)
    print(" [2] Book Info Test")
    print("="*60)
    log_file.write("\n" + "="*60 + "\n [2] Book Info Test\n" + "="*60 + "\n")
    log_file.flush()

    info_result = engine.test_book_info(search_keyword=keyword)
    results['info'] = info_result

    # 输出调试日志
    if hasattr(info_result, 'steps') and info_result.steps:
        for step_info in info_result.steps:
            if isinstance(step_info, dict):
                step_name = step_info.get('step', '详情')
                msg = step_info.get('message', '')
                state = step_info.get('state')
                
                # state=20表示详情页HTML内容
                if state == 20:
                    # HTML内容不直接输出到控制台，只输出到日志文件
                    if msg:
                        html_preview = msg[:500] + "..." if len(msg) > 500 else msg
                        log(log_file, step_name, f"≡HTML长度: {len(msg)}")
                        log(log_file, step_name, f"≡HTML内容预览: {html_preview}")
                elif msg:  # 其他日志正常输出
                    log(log_file, step_name, msg)

    log(log_file, "详情", f"Success: {info_result.success}")
    log(log_file, "详情", f"Message: {info_result.message}")

    if info_result.data:
        log(log_file, "详情", f"Name: {info_result.data.name}")
        log(log_file, "详情", f"Author: {info_result.data.author}")
        log(log_file, "详情", f"Toc URL: {info_result.data.tocUrl}")

    # 3. 目录测试
    print("\n" + "="*60)
    print(" [3] Toc Test")
    print("="*60)
    log_file.write("\n" + "="*60 + "\n [3] Toc Test\n" + "="*60 + "\n")
    log_file.flush()

    toc_result = engine.test_toc(search_keyword=keyword)
    results['toc'] = toc_result

    # 输出调试日志
    if hasattr(toc_result, 'steps') and toc_result.steps:
        for step_info in toc_result.steps:
            if isinstance(step_info, dict):
                step_name = step_info.get('step', '目录')
                msg = step_info.get('message', '')
                state = step_info.get('state')
                
                # state=30表示目录页HTML内容
                if state == 30:
                    # HTML内容不直接输出到控制台，只输出到日志文件
                    if msg:
                        html_preview = msg[:500] + "..." if len(msg) > 500 else msg
                        log(log_file, step_name, f"≡HTML长度: {len(msg)}")
                        log(log_file, step_name, f"≡HTML内容预览: {html_preview}")
                elif msg:  # 其他日志正常输出
                    log(log_file, step_name, msg)

    log(log_file, "目录", f"Success: {toc_result.success}")
    log(log_file, "目录", f"Message: {toc_result.message}")

    if toc_result.data:
        log(log_file, "目录", f"Chapters: {len(toc_result.data)}")
        for i, chapter in enumerate(toc_result.data[:3], 1):
            log(log_file, "目录", f"  [{i}] {chapter.title}")

    # 4. 正文测试
    print("\n" + "="*60)
    print(" [4] Content Test")
    print("="*60)
    log_file.write("\n" + "="*60 + "\n [4] Content Test\n" + "="*60 + "\n")
    log_file.flush()

    content_result = engine.test_content(search_keyword=keyword)
    results['content'] = content_result

    # 输出调试日志
    if hasattr(content_result, 'steps') and content_result.steps:
        for step_info in content_result.steps:
            if isinstance(step_info, dict):
                step_name = step_info.get('step', '正文')
                msg = step_info.get('message', '')
                state = step_info.get('state')
                
                # state=40表示HTML内容，按照Legado格式处理
                if state == 40:
                    # HTML内容不直接输出到控制台，只输出到日志文件
                    # 显示HTML长度和前500字符
                    if msg:
                        html_preview = msg[:500] + "..." if len(msg) > 500 else msg
                        log(log_file, step_name, f"≡HTML长度: {len(msg)}")
                        log(log_file, step_name, f"≡HTML内容预览: {html_preview}")
                elif msg:  # 其他日志正常输出
                    log(log_file, step_name, msg)

    log(log_file, "正文", f"Success: {content_result.success}")
    log(log_file, "正文", f"Message: {content_result.message}")

    if content_result.data:
        content_text = content_result.data.text
        log(log_file, "正文", f"Content Length: {len(content_text)}")
        
        # 打印正文内容
        content_header = """
============================================================
 解密后的正文内容
============================================================"""
        print(content_header)
        log_file.write(content_header + '\n')
        log_file.flush()
        
        print(content_text)
        log_file.write(content_text + '\n')
        log_file.flush()

    # 汇总
    print("\n" + "="*60)
    print(" Summary")
    print("="*60)
    log_file.write("\n" + "="*60 + "\n Summary\n" + "="*60 + "\n")
    log_file.flush()

    search_status = "PASS" if results['search'].success else "FAIL"
    info_status = "PASS" if results['info'].success else "FAIL"
    toc_status = "PASS" if results['toc'].success else "FAIL"
    content_status = "PASS" if results['content'].success else "FAIL"

    log(log_file, "汇总", f"Search: {search_status}")
    log(log_file, "汇总", f"Book Info: {info_status}")
    log(log_file, "汇总", f"Toc: {toc_status}")
    log(log_file, "汇总", f"Content: {content_status}")

    all_pass = all([results['search'].success, results['info'].success, results['toc'].success, results['content'].success])
    log(log_file, "汇总", f"Overall: {'ALL PASS' if all_pass else 'SOME FAILED'}")

    log_file.close()
    print("\n日志已保存到 test_result.txt")

    return all_pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Legado Book Source Debugger")
    parser.add_argument("source", help="Book source JSON file")
    parser.add_argument("-k", "--keyword", default="斗破苍穹", help="Search keyword")

    args = parser.parse_args()

    run_test(args.source, args.keyword)
