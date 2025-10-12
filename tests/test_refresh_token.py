# -*- coding: utf-8 -*-
"""
测试refresh_token功能

验证refresh_token是否能正常刷新B站Cookie
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import BILIBILI_CONFIG, build_bilibili_cookie
from services.bilibili_auth import BilibiliAuth


async def test_refresh_token():
    """测试refresh_token刷新功能"""
    print("=" * 70)
    print("B站refresh_token功能测试")
    print("=" * 70)

    # 检查配置
    print("\n[1/5] 检查配置...")
    print("-" * 70)

    current_cookie = build_bilibili_cookie()
    refresh_token = BILIBILI_CONFIG.get("refresh_token")

    if not current_cookie:
        print("[ERROR] 未配置B站Cookie")
        print("\n请先运行: uv run python tools/manual_set_refresh_token.py")
        return False

    if not refresh_token:
        print("[ERROR] 未配置refresh_token")
        print("\n请先运行: uv run python tools/manual_set_refresh_token.py")
        return False

    print(f"[OK] Cookie已配置 (长度: {len(current_cookie)})")
    print(f"[OK] refresh_token已配置 (长度: {len(refresh_token)})")

    # 初始化认证服务
    print("\n[2/5] 初始化认证服务...")
    print("-" * 70)
    auth = BilibiliAuth()
    print("[OK] 认证服务已初始化")

    # 检查是否需要刷新
    print("\n[3/4] 检查是否需要刷新...")
    print("-" * 70)

    need_refresh, refresh_time = await auth.check_need_refresh(current_cookie)

    if need_refresh:
        print(f"[WARNING] Cookie需要刷新 (刷新时间戳: {refresh_time})")
        print("[INFO] 系统检测到Cookie需要刷新，将自动执行刷新操作")
    else:
        print("[OK] Cookie暂时无需刷新")
        print(f"[INFO] 刷新时间戳: {refresh_time if refresh_time else '未知'}")
        print("\n[INFO] 提示：即使Cookie有效，我们也可以测试刷新功能")
        confirm = input("\n是否继续测试刷新功能？(y/N): ").strip().lower()
        if confirm != "y":
            print("\n[INFO] 测试结束")
            return True

    # 尝试刷新Cookie
    print("\n[4/4] 尝试刷新Cookie...")
    print("-" * 70)
    print("[WARNING] 注意：这将使用refresh_token刷新Cookie")
    print("[INFO] 刷新后，新的Cookie会自动保存到.env文件")

    confirm = input("\n确认开始刷新？(y/N): ").strip().lower()
    if confirm != "y":
        print("\n已取消刷新测试")
        return True

    print("\n正在刷新...")
    new_cookie_info = await auth.refresh_cookie(current_cookie, refresh_token)

    if new_cookie_info:
        print("\n" + "=" * 70)
        print("[SUCCESS] Cookie刷新成功！")
        print("=" * 70)

        print("\n[RESULT] 刷新结果:")
        print("-" * 70)
        print(f"[OK] 新Cookie已生成 (长度: {len(new_cookie_info['cookie'])})")
        print(
            f"[OK] 新refresh_token已生成 (长度: {len(new_cookie_info['refresh_token'])})"
        )
        print(f"[OK] 刷新时间: {new_cookie_info['refresh_time']}")

        print("\n" + "=" * 70)
        print("[SUCCESS] refresh_token功能测试通过！")
        print("=" * 70)
        print("\n[INFO] 说明:")
        print("- 新Cookie已自动保存到.env文件")
        print("- 新refresh_token已自动保存到.env文件")
        print("- 监控服务启动时会自动使用新配置")
        print("\n下一步:")
        print("1. 重启程序以加载新Cookie")
        print("2. 运行测试: uv run python test_api.py")
        print("3. 启动监控: uv run python main.py --mode monitor")
        return True
    else:
        print("\n" + "=" * 70)
        print("[ERROR] Cookie刷新失败")
        print("=" * 70)

        print("\n[DEBUG] 可能的原因:")
        print("-" * 70)
        print("1. refresh_token无效或过期")
        print("2. bili_jct (CSRF token) 错误")
        print("3. B站API返回错误")
        print("4. 网络连接问题")

        print("\n[INFO] 解决方案:")
        print("-" * 70)
        print("方案1：重新获取refresh_token")
        print("  uv run python tools/bilibili_qr_login.py")
        print("\n方案2：手动设置refresh_token")
        print("  uv run python tools/manual_set_refresh_token.py")
        print("\n方案3：检查网络和代理设置")

        return False


async def main():
    """主函数"""
    try:
        success = await test_refresh_token()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\n[INFO] 用户取消测试")
        return 0
    except Exception as e:
        print(f"\n[ERROR] 测试过程中发生错误: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
