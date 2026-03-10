---
name: translate
description: "Translate text between languages using free APIs. Supports 100+ languages."
metadata: {"nanobot":{"emoji":"🌐","requires":{"bins":["curl"]}}}
---

# Translation Skill

Translate text between languages using free translation APIs.

## Quick Translation

### Using MyMemory API (Free, No Key)
```bash
curl -s "https://api.mymemory.translated.net/get?q=Hello+World&langpair=en|zh" | jq '.responseData.translatedText'
# Output: "你好世界"
```

### Using LibreTranslate (Self-hosted or Public)
```bash
curl -s -X POST "https://libretranslate.com/translate" \
  -H "Content-Type: application/json" \
  -d '{"q":"Hello World","source":"en","target":"zh","format":"text"}' | jq '.translatedText'
```

## Common Language Codes

| Code | Language | Code | Language |
|------|----------|------|----------|
| en | English | zh | Chinese (Simplified) |
| zh-TW | Chinese (Traditional) | es | Spanish |
| fr | French | de | German |
| ja | Japanese | ko | Korean |
| ru | Russian | pt | Portuguese |
| it | Italian | ar | Arabic |
| hi | Hindi | th | Thai |
| vi | Vietnamese | id | Indonesian |

## Usage Examples

### Translate Single Text
```bash
# English to Chinese
curl -s "https://api.mymemory.translated.net/get?q=Good+morning&langpair=en|zh" | jq -r '.responseData.translatedText'

# Chinese to English
curl -s "https://api.mymemory.translated.net/get?q=早上好&langpair=zh|en" | jq -r '.responseData.translatedText'

# Japanese to English
curl -s "https://api.mymemory.translated.net/get?q=こんにちは&langpair=ja|en" | jq -r '.responseData.translatedText'
```

### Batch Translation
```bash
# Translate multiple texts
texts=("Hello" "Goodbye" "Thank you")
for text in "${texts[@]}"; do
  result=$(curl -s "https://api.mymemory.translated.net/get?q=$text&langpair=en|zh" | jq -r '.responseData.translatedText')
  echo "$text -> $result"
done
```

### Translate File Content
```bash
# Translate content of a file
content=$(cat input.txt)
encoded=$(echo "$content" | sed 's/ /+/g')
curl -s "https://api.mymemory.translated.net/get?q=$encoded&langpair=en|zh" | jq -r '.responseData.translatedText' > translated.txt
```

## Advanced Usage

### Detect Language
```bash
curl -s "https://api.mymemory.translated.net/get?q=こんにちは&langpair=|en" | jq '.responseData'
# Check detectedLanguage field
```

### Translation with Context
```bash
# Provide context for better accuracy
curl -s "https://api.mymemory.translated.net/get?q=Bank&langpair=en|zh&de=金融" | jq -r '.responseData.translatedText'
# More likely to translate as "银行" (financial) not "河岸"
```

### HTML Content (Preserve Tags)
```bash
curl -s -X POST "https://libretranslate.com/translate" \
  -H "Content-Type: application/json" \
  -d '{"q":"<p>Hello <strong>World</strong></p>","source":"en","target":"zh","format":"html"}' | jq '.translatedText'
```

## Alternative Services

### Google Translate (Unofficial)
```bash
# Using translate.google.com (rate limited)
text="Hello World"
curl -s "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh&dt=t&q=$text" | jq '.[0][0][0]'
```

### Bing Translator (Requires API Key)
```bash
curl -s -X POST "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=zh" \
  -H "Ocp-Apim-Subscription-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"Text":"Hello World"}]' | jq '.[0].translations[0].text'
```

### DeepL (Requires API Key)
```bash
curl -s -X POST "https://api-free.deepl.com/v2/translate" \
  -H "Authorization: DeepL-Auth-Key YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":["Hello World"],"target_lang":"ZH"}' | jq '.translations[0].text'
```

## Tips

- URL encode spaces as `+` or `%20`
- MyMemory API: 50 translations/day free, then requires email
- For production, use official APIs (Google, DeepL, Azure)
- Cache frequent translations
- Handle special characters properly
