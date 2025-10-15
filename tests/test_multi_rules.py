# -*- coding: utf-8 -*-
"""
测试多规则评论筛选功能

演示如何为同一个博主配置多个筛选规则
"""

import asyncio
import logging

from bilibili_api import Credential

from config import BILIBILI_CONFIG
from services.comment_fetcher import CommentFetcher


async def test_multi_rules_scenario1():
    """场景1: 获取AI总结 + 特定用户评论"""

    print("\n" + "=" * 80)
    print("场景1: 同时获取AI总结评论和特定用户评论")
    print("=" * 80)

    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)
    test_bvid = "BV1HnaHzcEag"

    # 定义多个规则
    rules = [
        {
            "name": "AI总结评论",
            "keywords": ["总结", "梗概", "AI总结"],
            "target_users": [],
            "min_likes": 10,
            "filter_mode": "keywords_only",
        },
        {
            "name": "专业评论员",
            "keywords": [],
            "target_users": ["CommentUserA", "CommentUserB"],  # 示例用户名
            "min_likes": 5,
            "filter_mode": "users_only",
        },
    ]

    print(f"\n配置了 {len(rules)} 个筛选规则：")
    for idx, rule in enumerate(rules, 1):
        print(f"  {idx}. {rule['name']} - {rule['filter_mode']}")

    # 使用多规则获取评论
    comments = await fetcher.fetch_hot_comments_with_rules(
        bvid=test_bvid,
        rules=rules,
        max_count=10,
    )

    print(f"\n✅ 总共找到 {len(comments)} 条符合条件的评论\n")

    # 显示结果
    for idx, comm in enumerate(comments, 1):
        member = comm.get("member", {})
        uname = member.get("uname", "")

        content = comm.get("content", {}).get("message", "")
        likes = comm.get("like", 0)

        # 检查匹配了哪个规则
        has_summary_keyword = any(kw in content for kw in ["总结", "梗概", "AI总结"])
        is_target_user = uname in ["CommentUserA", "CommentUserB"]

        rule_match = []
        if has_summary_keyword:
            rule_match.append("AI总结")
        if is_target_user:
            rule_match.append("专业评论员")

        match_str = " + ".join(rule_match) if rule_match else "其他"

        print(f"{idx}. [{match_str}] {uname} ({likes}赞)")
        print(f"   {content[:100]}...\n")


async def test_multi_rules_scenario2():
    """场景2: 三重筛选 - AI总结 + 专家评论 + 高赞评论"""

    print("\n" + "=" * 80)
    print("场景2: 三重筛选（演示多规则的强大之处）")
    print("=" * 80)

    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)
    test_bvid = "BV1HnaHzcEag"

    # 定义三个规则
    rules = [
        {
            "name": "AI总结类评论",
            "keywords": ["总结", "梗概"],
            "target_users": [],
            "min_likes": 10,
            "filter_mode": "keywords_only",
        },
        {
            "name": "专业分析评论",
            "keywords": ["分析", "复盘"],
            "target_users": [],
            "min_likes": 15,
            "filter_mode": "keywords_only",
        },
        {
            "name": "超高赞评论",
            "keywords": [],
            "target_users": [],
            "min_likes": 100,
            "filter_mode": "any",
        },
    ]

    print(f"\n配置了 {len(rules)} 个筛选规则：")
    for idx, rule in enumerate(rules, 1):
        print(f"  {idx}. {rule['name']}")
        print(f"     - 关键词: {rule['keywords'] or '无'}")
        print(f"     - 最低点赞: {rule['min_likes'] or '无限制'}")
        print(f"     - 模式: {rule['filter_mode']}")

    # 使用多规则获取评论
    comments = await fetcher.fetch_hot_comments_with_rules(
        bvid=test_bvid,
        rules=rules,
        max_count=15,
    )

    print(f"\n✅ 三个规则共找到 {len(comments)} 条评论\n")

    # 按规则分类显示
    for idx, comm in enumerate(comments, 1):
        content = comm.get("content", {}).get("message", "")
        likes = comm.get("like", 0)
        uname = comm.get("member", {}).get("uname", "")

        print(f"{idx}. {uname} ({likes}赞)")
        print(f"   {content[:80]}...\n")


async def test_single_vs_multi():
    """对比单规则和多规则的区别"""

    print("\n" + "=" * 80)
    print("对比：单规则 vs 多规则")
    print("=" * 80)

    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)
    test_bvid = "BV1HnaHzcEag"

    # 单规则模式
    print("\n【单规则模式】只能选一种筛选逻辑")
    print("─" * 40)

    single_comments = await fetcher.fetch_hot_comments(
        bvid=test_bvid,
        keywords=["总结"],
        min_likes=10,
        filter_mode="keywords_only",
        max_count=10,
    )

    print(f"获取到 {len(single_comments)} 条评论")

    # 多规则模式
    print("\n【多规则模式】可以同时应用多种筛选逻辑")
    print("─" * 40)

    multi_rules = [
        {
            "name": "AI总结",
            "keywords": ["总结"],
            "target_users": [],
            "min_likes": 10,
            "filter_mode": "keywords_only",
        },
        {
            "name": "高赞评论",
            "keywords": [],
            "target_users": [],
            "min_likes": 50,
            "filter_mode": "any",
        },
    ]

    multi_comments = await fetcher.fetch_hot_comments_with_rules(
        bvid=test_bvid,
        rules=multi_rules,
        max_count=10,
    )

    print(f"获取到 {len(multi_comments)} 条评论")

    print("\n" + "─" * 40)
    print(f"💡 多规则获取到更多评论：{len(multi_comments)} vs {len(single_comments)}")
    print("=" * 80)


async def main():
    """运行所有测试"""

    print("\n🚀 多规则评论筛选测试")

    # 检查配置
    if not BILIBILI_CONFIG.get("SESSDATA"):
        print("\n❌ 错误: 未配置SESSDATA")
        print("请在.env文件中配置B站Cookie")
        return

    try:
        # 场景1
        await test_multi_rules_scenario1()
        await asyncio.sleep(2)

        # 场景2
        await test_multi_rules_scenario2()
        await asyncio.sleep(2)

        # 对比测试
        await test_single_vs_multi()

        print("\n✅ 所有测试完成！")

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    asyncio.run(main())
