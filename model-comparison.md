# Model Comparison

| Model Name | Documentation | Price | Note |
|------------|---------------|--------|------|
| gpt-4o-mini | [OpenAI Vision Guide](https://platform.openai.com/docs/guides/vision) | Input: $0.15/1M<br>Output: $0.60/1M | openai还有其他模型，但是其他的价格有些贵 |
| Gemini | [Gemini API Docs](https://ai.google.dev/gemini-api/docs/text-generation?lang=python) | Input: $0.10/1M<br>Output: $0.40/1M | 有免费套餐 [pricing details](https://ai.google.dev/gemini-api/docs/pricing) |
| Claude 3.5 Haiku | [Claude Vision Guide](https://docs.anthropic.com/en/docs/build-with-claude/vision) | Input: $0.80/1M<br>Output: $4/1M | anthropic还有其他模型，问题是别的都贵得离谱 |

注：
1. 均支持图片上传，分析图片内容
2. tokens = (width px * height px)/750
