# -*- coding: utf-8 -*-
"""
测试评论获取功能

测试视频：
- BV1HnaHzcEag
- BV1hcaJzKExE
- BV11M4m1z7Js
"""

import asyncio
import logging

from bilibili_api import Credential

from config import BILIBILI_CONFIG
from services.comment_fetcher import CommentFetcher


async def test_basic_comment_fetch():
    """测试基础评论获取"""
    print("\n" + "=" * 60)
    print("测试1: 基础评论获取（无筛选条件）")
    print("=" * 60)

    # 创建凭证
    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)

    # 测试视频
    test_bvid = "BV1HnaHzcEag"

    comments = await fetcher.fetch_hot_comments(
        bvid=test_bvid,
        max_count=5,
    )

    print(f"\n✅ 获取到 {len(comments)} 条评论")

    for idx, comm in enumerate(comments, 1):
        formatted = fetcher.format_comment_for_display(comm)
        print(f"\n--- 评论 {idx} ---")
        print(formatted)


async def test_keyword_filter():
    """测试关键字筛选"""
    print("\n" + "=" * 60)
    print("测试2: 关键字筛选")
    print("=" * 60)

    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)

    # 测试关键字筛选
    test_keywords = ["总结", "梗概", "要点", "TL;DR", "概括"]

    comments = await fetcher.fetch_hot_comments(
        bvid="BV1HnaHzcEag",
        max_count=10,
        keywords=test_keywords,
    )

    print(f"\n✅ 使用关键字 {test_keywords}")
    print(f"✅ 筛选后获取到 {len(comments)} 条评论")

    for idx, comm in enumerate(comments, 1):
        content = comm.get("content", {}).get("message", "")
        likes = comm.get("like", 0)
        uname = comm.get("member", {}).get("uname", "")
        print(f"\n{idx}. {uname} ({likes}赞): {content[:100]}...")


async def test_likes_filter():
    """测试点赞数筛选"""
    print("\n" + "=" * 60)
    print("测试3: 点赞数筛选")
    print("=" * 60)

    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)

    # 测试点赞数筛选
    min_likes = 50

    comments = await fetcher.fetch_hot_comments(
        bvid="BV1HnaHzcEag",
        max_count=10,
        min_likes=min_likes,
    )

    print(f"\n✅ 筛选点赞数 >= {min_likes}")
    print(f"✅ 获取到 {len(comments)} 条评论")

    for idx, comm in enumerate(comments, 1):
        likes = comm.get("like", 0)
        uname = comm.get("member", {}).get("uname", "")
        content = comm.get("content", {}).get("message", "")
        print(f"\n{idx}. {uname} ({likes}赞): {content[:80]}...")


async def test_user_filter():
    """测试特定用户筛选"""
    print("\n" + "=" * 60)
    print("测试4: 特定用户筛选")
    print("=" * 60)

    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)

    # 首先获取所有评论，找出一些用户ID
    all_comments = await fetcher.fetch_hot_comments(
        bvid="BV1HnaHzcEag",
        max_count=20,
    )

    if not all_comments:
        print("❌ 没有获取到评论")
        return

    # 提取前几个用户ID进行测试
    test_user_ids = [comm.get("member", {}).get("mid", 0) for comm in all_comments[:3]]
    test_user_ids = [uid for uid in test_user_ids if uid != 0]

    print(f"\n测试用户ID: {test_user_ids}")

    # 使用用户ID筛选
    filtered_comments = await fetcher.fetch_hot_comments(
        bvid="BV1HnaHzcEag",
        max_count=10,
        target_user_ids=test_user_ids,
    )

    print(f"\n✅ 筛选特定用户的评论")
    print(f"✅ 获取到 {len(filtered_comments)} 条评论")

    for idx, comm in enumerate(filtered_comments, 1):
        uname = comm.get("member", {}).get("uname", "")
        mid = comm.get("member", {}).get("mid", 0)
        content = comm.get("content", {}).get("message", "")
        print(f"\n{idx}. {uname} (UID:{mid}): {content[:80]}...")


async def test_combined_filters():
    """测试组合筛选条件"""
    print("\n" + "=" * 60)
    print("测试5: 组合筛选（关键字 + 点赞数）")
    print("=" * 60)

    credential = Credential(
        sessdata=BILIBILI_CONFIG.get("SESSDATA"),
        bili_jct=BILIBILI_CONFIG.get("bili_jct"),
        buvid3=BILIBILI_CONFIG.get("buvid3"),
    )

    fetcher = CommentFetcher(credential=credential)

    # 组合筛选
    comments = await fetcher.fetch_hot_comments(
        bvid="BV1HnaHzcEag",
        max_count=10,
        keywords=["总结", "梗概", "要点"],
        min_likes=10,
    )

    print(f"\n✅ 组合筛选：包含关键字 且 点赞数>=10")
    print(f"✅ 获取到 {len(comments)} 条评论")

    if comments:
        # 使用完整格式化
        formatted = fetcher.format_comments_for_feishu(
            comments, "测试视频", "BV1HnaHzcEag"
        )
        print("\n" + "=" * 60)
        print("飞书消息格式预览:")
        print("=" * 60)
        print(formatted)


async def main():
    """运行所有测试"""
    print("\n🚀 开始测试评论获取功能")
    print("=" * 60)

    # 检查配置
    if not BILIBILI_CONFIG.get("SESSDATA"):
        print("\n❌ 错误: 未配置SESSDATA")
        print("请在.env文件中配置B站Cookie")
        return

    print(f"\n✅ SESSDATA已配置: {BILIBILI_CONFIG.get('SESSDATA')[:20]}...")
    print(f"✅ bili_jct已配置: {BILIBILI_CONFIG.get('bili_jct')[:10]}...")
    print(f"✅ buvid3已配置: {BILIBILI_CONFIG.get('buvid3')[:20]}...")

    try:
        # 运行所有测试
        await test_basic_comment_fetch()
        await asyncio.sleep(2)  # 避免请求过快

        await test_keyword_filter()
        await asyncio.sleep(2)

        await test_likes_filter()
        await asyncio.sleep(2)

        await test_user_filter()
        await asyncio.sleep(2)

        await test_combined_filters()

        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # 设置日志
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 运行测试
    asyncio.run(main())
