# -*- coding: utf-8 -*-
"""
系统通知功能测试脚本

测试飞书机器人的系统状态通知功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from services import FeishuBot


async def test_system_notifications():
    """测试系统通知功能"""
    print("初始化飞书机器人...")
    bot = FeishuBot()
    
    print("\n测试1: INFO级别通知")
    success1 = await bot.send_system_notification(
        bot.LEVEL_INFO,
        "系统通知测试 - INFO",
        "这是一条信息级别的测试通知\n\n**功能:** 系统通知\n**状态:** 正常运行"
    )
    print(f"INFO通知发送结果: {'成功' if success1 else '失败'}")
    
    await asyncio.sleep(2)
    
    print("\n测试2: WARNING级别通知")
    success2 = await bot.send_system_notification(
        bot.LEVEL_WARNING,
        "系统通知测试 - WARNING",
        "这是一条警告级别的测试通知\n\n**问题:** 账号额度不足\n**建议:** 需要注册新账号"
    )
    print(f"WARNING通知发送结果: {'成功' if success2 else '失败'}")
    
    await asyncio.sleep(2)
    
    print("\n测试3: ERROR级别通知")
    success3 = await bot.send_system_notification(
        bot.LEVEL_ERROR,
        "系统通知测试 - ERROR",
        "这是一条错误级别的测试通知\n\n**错误信息:**\n```\nTest error: Connection timeout\n```\n\n**影响范围:** 视频总结服务暂时不可用"
    )
    print(f"ERROR通知发送结果: {'成功' if success3 else '失败'}")
    
    print("\n所有测试完成！")
    print(f"总计: 3个测试, 成功: {sum([success1, success2, success3])}, 失败: {3 - sum([success1, success2, success3])}")


if __name__ == "__main__":
    print("="*50)
    print("系统通知功能测试")
    print("="*50)
    asyncio.run(test_system_notifications())

