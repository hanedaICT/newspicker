
import unittest
from datetime import UTC, datetime

from agents.scout import Article, _score


class ScoutScoringTests(unittest.TestCase):
    def test_more_informative_summary_gets_higher_score(self):
        config = {"keywords": ["AI"]}

        short_article = Article(
            title="AI news",
            url="https://example.com/short",
            summary="AI",
            published_at=datetime.now(UTC),
            source="Test",
        )

        detailed_article = Article(
            title="AI news",
            url="https://example.com/detailed",
            summary=(
                "AI企業が新しい技術を発表しました。"
                "発表内容には技術の特徴や利用方法が説明されています。"
                "今後の活用についても具体的な情報が含まれています。"
            ),
            published_at=datetime.now(UTC),
            source="Test",
        )

        self.assertGreater(
            _score(detailed_article, config),
            _score(short_article, config),
        )


if __name__ == "__main__":
    unittest.main()
