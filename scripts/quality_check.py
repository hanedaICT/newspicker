
import re


def check_quality(headline: str, body: str) -> list[str]:
    """台本の重大な品質問題を検出する。APIは使用しない。"""

    warnings = []

    if not headline or not headline.strip():
        warnings.append("ヘッドラインが空欄です")

    if not body or not body.strip():
        warnings.append("本文が空欄です")
        return warnings

    # 空白・改行を除いた本文文字数
    char_count = len(re.sub(r"\s", "", body))

    if char_count < 1000:
        warnings.append(
            f"本文が1000字未満です（現在：{char_count}字）"
        )

    # 句読点・空白を除いて締めの言葉を確認
    normalized = re.sub(r"[\s。、，．,.]", "", body)
    ending = "本日のワールドAIニュースは以上ですまた明日お会いしましょう"

    if not normalized.endswith(ending):
        warnings.append("指定されたエンディングがありません")

    return warnings
