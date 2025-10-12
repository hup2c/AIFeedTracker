# -*- coding: utf-8 -*-
"""测试B站API是否正常返回数据"""

import asyncio
import json

import aiohttp

from config import BILIBILI_CONFIG, build_bilibili_cookie


async def test_bilibili_api():
    """测试获取创作者动态"""
    # 测试用户
    test_creators = [
        {"uid": 11473291, "name": "笨笨的韭菜"},
        {"uid": 550494308, "name": "卢本圆复盘"},
        {"uid": 322005137, "name": "史诗级韭菜"},
        {"uid": 32798992, "name": "下龙湾"},
    ]

    api_url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
    }

    # 添加Cookie
    cookie = build_bilibili_cookie()
    if cookie:
        headers["Cookie"] = cookie
        print(f"[OK] 已配置B站Cookie (长度: {len(cookie)})")
    else:
        print("[WARNING] 未配置B站Cookie")

    async with aiohttp.ClientSession() as session:
        for creator in test_creators:
            uid = creator["uid"]
            name = creator["name"]

            print(f"\n{'='*60}")
            print(f"测试创作者: {name} (UID: {uid})")
            print(f"{'='*60}")

            params = {
                "offset": "",
                "host_mid": str(uid),
                "timezone_offset": "-480",
                "platform": "web",
                "features": "itemOpusStyle,listOnlyfans,opusBigCover",
                "web_location": "333.1387",
            }

            headers["Referer"] = f"https://space.bilibili.com/{uid}/dynamic"

            try:
                async with session.get(
                    api_url, params=params, headers=headers, timeout=20
                ) as resp:
                    print(f"HTTP状态码: {resp.status}")

                    data = await resp.json()

                    print(f"API code: {data.get('code')}")
                    print(f"API message: {data.get('message')}")

                    items = data.get("data", {}).get("items", [])
                    print(f"动态数量: {len(items)}")

                    if items:
                        print("\n最新3条动态:")
                        for i, item in enumerate(items[:3], 1):
                            item_id = item.get("id_str") or item.get("id")
                            item_type = item.get("type", "未知")

                            # 获取发布时间
                            pub_ts = (
                                item.get("modules", {})
                                .get("module_author", {})
                                .get("pub_ts", 0)
                            )

                            # 获取动态类型
                            major = (
                                item.get("modules", {})
                                .get("module_dynamic", {})
                                .get("major", {})
                            )
                            major_type = major.get("type", "未知")

                            print(f"  {i}. ID: {item_id}")
                            print(f"     类型: {item_type} / {major_type}")
                            print(f"     时间戳: {pub_ts}")

                            # 如果是视频，显示标题
                            if major_type in ("MAJOR_TYPE_ARCHIVE", "archive"):
                                title = major.get("archive", {}).get("title", "")
                                if title:
                                    print(f"     标题: {title}")
                    else:
                        print("[WARNING] 未获取到任何动态")
                        print("\n完整响应:")
                        print(json.dumps(data, indent=2, ensure_ascii=False))

            except Exception as e:
                print(f"[ERROR] 请求失败: {e}")


if __name__ == "__main__":
    asyncio.run(test_bilibili_api())
