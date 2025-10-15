# -*- coding: utf-8 -*-
"""
测试各种评论筛选模式

演示6种筛选模式的实际效果
"""

import asyncio
import logging

from bilibili_api import Credential

from config import BILIBILI_CONFIG
from services.comment_fetcher import CommentFetcher


async def test_all_filter_modes():
    """测试所有筛选模式"""

    # 创建凭证
    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)
    test_bvid = "BV1HnaHzcEag"  # 测试视频

    # 测试参数
    test_keywords = ["总结", "梗概"]
    test_usernames = []  # 留空，因为我们不知道具体的用户名
    test_min_likes = 10

    print("\n" + "=" * 80)
    print("🧪 评论筛选模式测试")
    print("=" * 80)
    print(f"\n测试视频: {test_bvid}")
    print(f"测试关键字: {test_keywords}")
    print(f"最低点赞数: {test_min_likes}")
    print("\n" + "=" * 80)

    # 测试所有模式
    modes = [
        ("keywords_or_users", "关键字或用户（推荐）"),
        ("keywords_and_users", "关键字且用户"),
        ("keywords_only", "只看关键字"),
        ("users_only", "只看用户"),
        ("all", "所有条件（严格）"),
        ("any", "任一条件（宽松）"),
    ]

    for mode, description in modes:
        print(f"\n{'─' * 80}")
        print(f"📋 模式: {mode} - {description}")
        print(f"{'─' * 80}")

        try:
            comments = await fetcher.fetch_hot_comments(
                bvid=test_bvid,
                max_count=3,
                keywords=test_keywords,
                target_usernames=test_usernames,
                min_likes=test_min_likes,
                filter_mode=mode,
            )

            print(f"\n✅ 找到 {len(comments)} 条评论")

            for idx, comm in enumerate(comments, 1):
                member = comm.get("member", {})
                uname = member.get("uname", "")
                mid = member.get("mid", 0)

                content = comm.get("content", {}).get("message", "")
                likes = comm.get("like", 0)

                # 检查是否匹配关键字
                has_keyword = any(kw in content for kw in test_keywords)
                keyword_mark = "🔑" if has_keyword else "  "

                print(f"\n  {idx}. {keyword_mark} {uname} (UID:{mid}) | {likes}赞")
                print(f"     {content[:80]}...")

            await asyncio.sleep(1)  # 避免请求过快

        except Exception as e:
            print(f"\n❌ 测试失败: {e}")

    print("\n" + "=" * 80)
    print("✅ 所有模式测试完成！")
    print("=" * 80)


async def demo_real_world_scenarios():
    """演示实际使用场景"""

    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)
    test_bvid = "BV1HnaHzcEag"

    print("\n" + "=" * 80)
    print("🌟 实际使用场景演示")
    print("=" * 80)

    # 场景1: 获取AI总结评论
    print("\n场景1: 获取评论区的AI总结（最常用）")
    print("─" * 40)
    comments = await fetcher.fetch_hot_comments(
        bvid=test_bvid,
        keywords=["总结", "梗概", "AI总结", "TL;DR"],
        comment_min_likes=10,
        filter_mode="keywords_only",
    )
    print(f"找到 {len(comments)} 条AI总结评论")

    await asyncio.sleep(1)

    # 场景2: 获取所有高赞评论（不限内容）
    print("\n场景2: 获取所有高赞评论")
    print("─" * 40)
    comments = await fetcher.fetch_hot_comments(
        bvid=test_bvid,
        min_likes=100,
        filter_mode="any",
    )
    print(f"找到 {len(comments)} 条高赞评论（>=100赞）")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    print("\n🚀 开始测试评论筛选模式...")

    try:
        asyncio.run(test_all_filter_modes())
        print("\n")
        asyncio.run(demo_real_world_scenarios())
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
    except Exception as e:
        print(f"\n\n❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()
