# -*- coding: utf-8 -*-
"""
总结生成器模块

使用AI大模型和精心设计的提示词生成高质量的视频总结
"""

import logging
from typing import Optional

from .ai_client import AIClient


class SummaryGenerator:
    """视频总结生成器"""

    # 系统提示词
    SYSTEM_PROMPT = """你是一个专业的视频内容总结助手，擅长从视频字幕中提取关键信息并生成结构化总结。

你的总结需要：
1. 准确提取视频的核心观点和关键信息
2. 使用清晰的Markdown格式组织内容
3. 保持客观，不添加字幕中没有的内容
4. 语言简洁流畅，重点突出"""

    # 用户提示词模板
    USER_PROMPT_TEMPLATE = """请根据以下视频字幕内容，生成一份结构化的总结。

**要求：**
1. 使用Markdown格式
2. 包含以下部分：
   - 📌 **核心观点**（3-5个要点，用列表形式）
   - 💡 **关键亮点**（重要信息摘要，2-3段）
   - 📝 **详细总结**（按内容逻辑分段，可以使用小标题）

3. 格式要求：
   - 使用emoji图标标识各部分
   - 核心观点使用无序列表（-）
   - 适当使用加粗（**）强调重点
   - 详细总结部分如果内容较长，请使用二级标题（##）分段

4. 内容要求：
   - 保持客观，只提取字幕中的信息
   - 总结长度适中（500-1000字）
   - 语言流畅，便于阅读

**视频字幕内容：**
{subtitle}

请开始总结："""

    def __init__(self, ai_client: AIClient):
        """
        初始化总结生成器

        Args:
            ai_client: AI客户端实例
        """
        self.ai_client = ai_client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    async def generate_summary(self, subtitle: str) -> Optional[str]:
        """
        生成视频总结

        Args:
            subtitle: 视频字幕文本

        Returns:
            Markdown格式的总结内容，失败返回None
        """
        try:
            if not subtitle or len(subtitle.strip()) < 50:
                self.logger.error("字幕内容太短，无法生成总结")
                return None

            self.logger.info(f"开始生成总结，字幕长度: {len(subtitle)} 字符")

            # 如果字幕太长，需要截断（防止超过token限制）
            max_subtitle_length = 30000  # 约10000个token
            if len(subtitle) > max_subtitle_length:
                self.logger.warning(
                    f"字幕过长（{len(subtitle)}字符），将截断到{max_subtitle_length}字符"
                )
                subtitle = (
                    subtitle[:max_subtitle_length] + "...\n[字幕因长度限制已截断]"
                )

            # 构建提示词
            user_prompt = self.USER_PROMPT_TEMPLATE.format(subtitle=subtitle)

            # 构建消息
            messages = [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ]

            # 调用AI
            summary = await self.ai_client.chat_completion(
                messages=messages,
                temperature=0.7,  # 适中的创造性
                max_tokens=2000,  # 限制输出长度
            )

            if summary:
                self.logger.info(f"总结生成成功，长度: {len(summary)} 字符")
                return summary
            else:
                self.logger.error("AI返回的总结为空")
                return None

        except Exception as e:
            self.logger.error(f"生成总结失败: {e}", exc_info=True)
            return None

    async def generate_short_summary(self, subtitle: str) -> Optional[str]:
        """
        生成简短总结（用于快速预览）

        Args:
            subtitle: 视频字幕文本

        Returns:
            简短总结（100-200字），失败返回None
        """
        try:
            if not subtitle or len(subtitle.strip()) < 50:
                self.logger.error("字幕内容太短，无法生成总结")
                return None

            # 简短总结的提示词
            short_prompt = f"""请用一段话（100-200字）总结以下视频的核心内容：

{subtitle[:5000]}

总结："""

            messages = [
                {"role": "system", "content": "你是一个专业的内容总结助手。"},
                {"role": "user", "content": short_prompt},
            ]

            summary = await self.ai_client.chat_completion(
                messages=messages,
                temperature=0.5,
                max_tokens=300,
            )

            return summary

        except Exception as e:
            self.logger.error(f"生成简短总结失败: {e}")
            return None
