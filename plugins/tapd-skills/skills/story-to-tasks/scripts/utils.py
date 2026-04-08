import sys
import json
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("Error: requests module not found. Install with: pip install requests")
    sys.exit(1)

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from prompts import VISION_PROMPT
from typings import EnvConfig


def load_env() -> EnvConfig:
    """
    从 skill 目录的 .env 文件加载环境配置

    Returns:
        包含 TAPD_WORKSPACE_ID、TAPD_ACCESS_TOKEN、GLM_API_KEY 的配置字典
    """
    skill_dir = Path(__file__).parent.parent
    env_file = skill_dir / ".env"

    if not env_file.exists():
        print(f"Error: .env file not found at {env_file}")
        print("Please copy .env.example to .env and configure your settings.")
        sys.exit(1)

    config = {}

    with open(env_file) as lines:
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


def make_request(
    method: str,
    endpoint: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
) -> Dict:
    """
    向 TAPD API 发送 HTTP 请求

    Args:
        method: HTTP 方法（GET、POST、PUT、DELETE 等）
        endpoint: API 端点路径（如 /stories）
        params: URL 查询参数
        data: 请求体数据（JSON 格式）

    Returns:
        API 响应的 JSON 数据

    Raises:
        requests.HTTPError: 请求失败时抛出异常
    """
    config = load_env()

    headers = {
        "Authorization": f"Bearer {config['TAPD_ACCESS_TOKEN']}",
        "Content-Type": "application/json",
    }

    url = urljoin("https://api.tapd.cn/", endpoint)

    response = requests.request(
        method=method, url=url, headers=headers, params=params, json=data, timeout=30
    )

    response.raise_for_status()

    return response.json()


def format_json(data) -> str:
    """格式化 JSON 为字符串"""
    return json.dumps(data, ensure_ascii=False, indent=2)


def print_json(data):
    """美化打印 JSON"""
    print(format_json(data))


def to_long_id(story_id: str, workspace_id: str, is_cloud: bool = True) -> str:
    """
    将短 story_id 转换为长 ID

    Args:
        story_id: 原始 story_id
        workspace_id: 工作区 ID
        is_cloud: 是否为云环境，默认 True

    Returns:
        转换后的 story_id（如果不是短 ID，原样返回）
    """
    story_id = str(story_id).strip()

    # 如果是纯数字且 ≤ 9 位，视为短 ID
    if story_id.isdigit() and len(story_id) <= 9:
        pre_id = "11" if is_cloud else "10"
        padded_id = story_id.zfill(9)
        return f"{pre_id}{workspace_id}{padded_id}"

    return story_id


def analyze_image_with_vision(url: str, context: str = "") -> str:
    """
    使用智谱 GLM-4.6V FlashX 视觉模型解析图片内容

    Args:
        url: 图片 URL
        context: 图片周围的文字上下文（可选）

    Returns:
        图片内容描述文本，失败或无 API Key 时返回空字符串
    """
    config = load_env()
    api_key = config.get("GLM_API_KEY", "")

    if not api_key:
        return ""

    # 构建带上下文的 user prompt（按句子截断）
    context_text = ""
    if context:
        context_trimmed = context[:500]
        # 找最后一个句号/换行截断，避免截在句子中间
        cut = max(context_trimmed.rfind("。"), context_trimmed.rfind("\n"))
        if cut > 100:  # 截断点太靠前就不管了
            context_trimmed = context_trimmed[: cut + 1]
        context_text = f"\n\n图片所在段落的文字上下文：\n{context_trimmed}"

    user_text = f"这张图片来自产品需求文档。{context_text}\n\n请分析图片内容。"

    # 配置重试策略
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,  # 1s, 2s, 4s
        status_forcelist=[429, 500, 502, 503],
        allowed_methods=["POST"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))

    try:
        response = session.post(
            "https://open.bigmodel.cn/api/coding/paas/v4/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "glm-4.6v-flashx",
                "messages": [
                    {
                        "role": "system",
                        "content": VISION_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_text},
                            {"type": "image_url", "image_url": {"url": url}},
                        ],
                    },
                ],
                "thinking": {"type": "disabled"},
                "stream": False,
            },
            timeout=(5, 25),  # (connect_timeout, read_timeout)
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return ""
    finally:
        session.close()
