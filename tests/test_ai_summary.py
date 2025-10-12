# -*- coding: utf-8 -*-
"""
AI总结服务测试脚本

测试字幕获取和AI总结功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core import configure_logging
from services.ai_summary import AISummaryService
from services.ai_summary.subtitle_fetcher import SubtitleFetcher


async def test_subtitle_fetch():
    """测试字幕获取"""
    print("\n" + "=" * 60)
    print("测试1: 字幕获取")
    print("=" * 60)

    # 测试视频URL
    test_urls = [
        "https://www.bilibili.com/video/BV11M4m1z7Js",
        "https://www.bilibili.com/video/BV1HnaHzcEag",
    ]

    fetcher = SubtitleFetcher()

    for i, url in enumerate(test_urls, 1):
        print(f"\n测试视频 {i}: {url}")
        try:
            subtitle = await fetcher.fetch_subtitle(url)
            if subtitle:
                print(f"✅ 字幕获取成功")
                print(f"   长度: {len(subtitle)} 字符")
                print(f"   预览: {subtitle[:200]}...")
            else:
                print(f"❌ 字幕获取失败")
        except Exception as e:
            print(f"❌ 异常: {e}")


async def test_ai_summary_single():
    """测试单个视频AI总结"""
    print("\n" + "=" * 60)
    print("测试2: 单个视频AI总结")
    print("=" * 60)

    # 使用有字幕的视频进行测试
    test_url = "https://www.bilibili.com/video/BV1HnaHzcEag"

    try:
        service = AISummaryService()
        print(f"\n总结视频: {test_url}")

        success, message, links, contents = await service.summarize_videos([test_url])

        if success:
            print(f"✅ 总结成功: {message}")
            if contents:
                print(f"\n总结内容:")
                print("-" * 60)
                print(contents[0])
                print("-" * 60)
        else:
            print(f"❌ 总结失败: {message}")

    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback

        traceback.print_exc()


async def test_ai_summary_multiple():
    """测试多个视频批量总结"""
    print("\n" + "=" * 60)
    print("测试3: 多个视频批量总结")
    print("=" * 60)

    test_urls = [
        "https://www.bilibili.com/video/BV11M4m1z7Js",
        "https://www.bilibili.com/video/BV1HnaHzcEag",
    ]

    try:
        service = AISummaryService()
        print(f"\n批量总结 {len(test_urls)} 个视频")

        success, message, links, contents = await service.summarize_videos(test_urls)

        print(f"\n结果: {message}")
        if success:
            print(f"✅ 批量总结完成")
            for i, content in enumerate(contents, 1):
                print(f"\n--- 视频 {i} 总结 ---")
                print(content[:300] + "..." if len(content) > 300 else content)
        else:
            print(f"❌ 批量总结失败")

    except Exception as e:
        print(f"❌ 测试异常: {e}")
        import traceback

        traceback.print_exc()


async def test_service_statistics():
    """测试服务统计信息"""
    print("\n" + "=" * 60)
    print("测试4: 服务统计信息")
    print("=" * 60)

    try:
        service = AISummaryService()
        stats = await service.get_service_statistics()

        print("\n服务统计:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        print("\n✅ 统计信息获取成功")

    except Exception as e:
        print(f"❌ 测试异常: {e}")


async def main():
    """运行所有测试"""
    import sys

    # 配置日志
    configure_logging()

    print("=" * 60)
    print("AI总结服务测试套件")
    print("=" * 60)

    # 运行测试
    await test_subtitle_fetch()
    await test_service_statistics()

    # 检查是否有 --run-ai-test 参数
    run_ai_test = "--run-ai-test" in sys.argv or "-a" in sys.argv

    if run_ai_test:
        print("\n检测到 --run-ai-test 参数，将运行AI总结测试")
        await test_ai_summary_single()
        # await test_ai_summary_multiple()  # 可选：批量测试
    else:
        print("\n" + "=" * 60)
        print("提示：添加 --run-ai-test 或 -a 参数可运行AI总结测试（将消耗API额度）")
        print("示例：uv run python tests/test_ai_summary.py --run-ai-test")
        print("=" * 60)

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
