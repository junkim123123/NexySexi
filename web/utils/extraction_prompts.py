"""
Extraction Prompts for NexSupply
LLM-based extraction of structured data from unstructured user input.
"""
from enum import Enum
from typing import Optional, Dict, Any
import re
import logging


EXTRACTION_USER_PROMPT_TEMPLATE = """
You are an AI parser that converts messy, natural-language sourcing requests
(multi-language: Korean, English, Chinese, Japanese, Spanish, Arabic, Hindi, etc.) 
into a clean JSON object for our NexSupply app.

Your job:
- Read the user's free-text message about what product they want to source.
- The user may write in ANY language (Korean, English, Chinese, Japanese, Spanish, Arabic, Hindi, etc.)
- Infer and normalize the following fields:
  - volume
  - channel
  - target_market
  - price_range (optional)
  - delivery_timeline (optional)
  - moq (optional)

Output:
- Return ONLY a valid JSON object with these keys:
  - "volume": integer or null
  - "volume_raw": original user text for volume, or null
  - "channel": one of [
      "Convenience Store",
      "Amazon FBA",
      "eCommerce D2C",
      "Wholesale Distributor",
      "Offline Retail",
      "Other"
    ]
  - "channel_raw": original user text for channel, or null
  - "target_market": one of [
      "USA",
      "EU",
      "Korea",
      "Japan",
      "Global",
      "Other"
    ]
  - "target_market_raw": original user text for target market, or null
  - "price_range": {{"min": number or null, "max": number or null, "currency": "USD" | "KRW" | null}} or null
  - "price_range_raw": original user text for price, or null
  - "delivery_timeline": one of [
      "Urgent (under 1 week)",
      "Short-term (1-4 weeks)",
      "Medium-term (1-3 months)",
      "Long-term (over 3 months)",
      "Other"
    ] or null
  - "delivery_timeline_raw": original user text for delivery timeline, or null
  - "moq": integer or null
  - "moq_raw": original user text for MOQ, or null

Normalization rules:

1) Volume (Multi-language number → integer)
- Convert number expressions from ANY language to a plain integer.

**Korean units:**
  - "천" (1,000), "만" (10,000), "억" (100,000,000)

**Chinese units (中文):**
  - "千" (1,000), "万" (10,000), "亿" (100,000,000)
  - Examples: "200万个" → 2000000, "5千个" → 5000, "1~2万个" → 20000

**Japanese units (日本語):**
  - "千" (1,000), "万" (10,000), "億" (100,000,000)
  - Examples: "200万個" → 2000000, "5千個" → 5000, "1〜2万個" → 20000

**Spanish units (Español):**
  - "mil" (1,000), "millón" (1,000,000)
  - Examples: "200 mil unidades" → 200000, "5 millones" → 5000000

**Arabic units (العربية):**
  - "ألف" (1,000), "مليون" (1,000,000)
  - Examples: "200 ألف" → 200000, "5 مليون" → 5000000

**Hindi units (हिंदी):**
  - "हज़ार" (1,000), "लाख" (100,000), "करोड़" (10,000,000)
  - Examples: "200 हज़ार" → 200000, "5 लाख" → 500000

**English units:**
  - "k" (1,000), "m" (1,000,000), "thousand", "million"

**Exact quantity examples:**
  - "200개", "200ea", "200피스" → 200
  - "1천개", "천 개", "1k", "1k개", "1k units" → 1000
  - "2만", "2만장", "20k" → 20000
  - "10만개", "십만 개" → 100000
  - "200만개", "200만 장", "200만개 정도" → 2000000
  - "500만", "5m" → 5000000
  - "1억개 정도" → 100000000
  - "300만 세트" → 3000000
  - "한 5천개 정도", "대략 2만개" → 5000, 20000 (approximate)

**Range examples (use UPPER bound):**
  - "1~2천개", "1000-2000" → 2000
  - "5천~1만개 사이" → 10000
  - "1만~2만개" → 20000
  - "2만에서 5만개" → 50000
  - "100~500개 정도" → 500
  - "최소 3만~ 최대 10만개" → 100000
  - "5만개 이상", "10만개 이상" → 50000, 100000 (use that number)

**Minimum quantity examples:**
  - "최소 500개는 해야 됨", "최소 1만개" → 500, 10000 (use that number as initial order volume)

**Packaging unit examples:**
  - "1박스 (약 200개)", "테스트로 1박스 (약 200개)" → 200 (use piece count if given)
  - "1팔레트 (5000개 포장)" → 5000 (use piece count if given)
  - "박스당 50개, 10박스" → 500 (calculate if both given)
  - "50 box", "50 boxes", "50박스" → null (no piece count per box, keep in volume_raw)
  - "50 box (100 pieces each)" → 5000 (calculate if piece count given)
  - "1박스", "한 박스만", "1팔레트", "1카톤", "20FT 컨테이너 1개", "40HQ 한 동" → null (no piece count, keep in volume_raw)

**Vague/ambiguous examples (set to null):**
  - "몇천개", "몇만개", "수백만 개" → null (do NOT guess)
  - "소량", "테스트로 조금만", "아주 조금만" → null
  - "많이", "대량", "왕창", "몇십만 개까지 갈 수 있음" → null
  - "첫 오더는 작게, 그다음에 키우고 싶음" → null
  - "최소 MOQ", "MOQ 수준", "샘플만", "샘플 몇 개" → null

**Recurring orders:**
  - "매월 10만개" → 100000 (use the quantity)
  - "초기 1천개 후 대량" → 1000 (use initial amount)

**Rule summary:**
  - If ambiguous like "몇천개", "몇만개", "수백만 개": Set "volume": null, keep "volume_raw"
  - If range like "1~2만개": Use UPPER bound (20000), keep original in "volume_raw"
  - If packaging unit with piece count: Use piece count
  - If packaging unit without piece count: Set "volume": null, keep in "volume_raw"
  - If vague words with no number: Set "volume": null, keep "volume_raw"

2) Channel (Multi-language → normalized English label)
- Map channel expressions from ANY language to standardized labels.

**Convenience Store:**
  - Korean: "편의점", "편의점 시장", "CVS", "CU", "GS25", "세븐일레븐", "이마트24"
  - Chinese: "便利店", "CVS", "7-11", "全家", "罗森"
  - Japanese: "コンビニ", "コンビニエンスストア", "セブンイレブン", "ファミマ", "ローソン"
  - Spanish: "tienda de conveniencia", "CVS", "7-Eleven"
  - Arabic: "متجر صغير", "CVS"
  - English: "convenience store", "CVS", "7-Eleven"

**Amazon FBA:**
  - Korean: "아마존", "Amazon", "FBA", "아마존 FBA", "아마존 셀러"
  - Chinese: "亚马逊", "Amazon", "FBA", "亚马逊FBA"
  - Japanese: "アマゾン", "Amazon", "FBA", "アマゾンFBA"
  - Spanish: "Amazon", "FBA", "Amazon FBA"
  - Arabic: "أمازون", "Amazon", "FBA"
  - Hindi: "अमेज़न", "Amazon", "FBA"
  - English: "Amazon", "FBA", "Amazon FBA"

**eCommerce D2C:**
  - Korean: "자사몰", "D2C", "스마트스토어", "쿠팡", "Shopify", "온라인 판매"
  - Chinese: "自营店", "D2C", "电商", "天猫", "京东", "Shopify", "独立站"
  - Japanese: "自社EC", "D2C", "ECサイト", "Shopify", "オンライン販売"
  - Spanish: "tienda propia", "D2C", "eCommerce", "Shopify", "venta online"
  - Arabic: "متجر خاص", "D2C", "تجارة إلكترونية", "Shopify"
  - Hindi: "अपना स्टोर", "D2C", "ई-कॉमर्स", "Shopify"
  - English: "own website", "D2C", "eCommerce", "Shopify", "online store"

**Wholesale Distributor:**
  - Korean: "도매", "홀세일", "B2B", "유통업체", "총판"
  - Chinese: "批发", "B2B", "分销商", "经销商"
  - Japanese: "卸売", "B2B", "ディストリビューター", "問屋"
  - Spanish: "mayoreo", "B2B", "distribuidor", "mayorista"
  - Arabic: "الجملة", "B2B", "موزع", "تاجر جملة"
  - Hindi: "थोक", "B2B", "वितरक", "थोक व्यापारी"
  - English: "wholesale", "B2B", "distributor", "bulk"

**Offline Retail:**
  - Korean: "오프라인", "매장", "백화점", "대형마트", "올리브영"
  - Chinese: "线下", "实体店", "百货商店", "超市", "屈臣氏"
  - Japanese: "オフライン", "実店舗", "デパート", "スーパー", "ドラッグストア"
  - Spanish: "tienda física", "retail", "supermercado", "farmacia"
  - Arabic: "متجر فعلي", "بيع بالتجزئة", "سوبر ماركت"
  - Hindi: "ऑफलाइन", "दुकान", "सुपरमार्केट"
  - English: "offline", "retail store", "supermarket", "pharmacy"

**Other:**
  - Any specific channel not listed above
  - If unclear or not mentioned: Set "channel": "Other", keep "channel_raw": original text

3) Target Market (Multi-language country/region → code)
- Map country/region names from ANY language to region codes.

**USA:**
  - Korean: "미국", "미주", "북미", "US", "USA", "미국 시장"
  - Chinese: "美国", "北美", "US", "USA", "美国市场"
  - Japanese: "アメリカ", "米国", "US", "USA", "アメリカ市場"
  - Spanish: "Estados Unidos", "EE.UU.", "US", "USA", "Norteamérica"
  - Arabic: "الولايات المتحدة", "أمريكا", "US", "USA"
  - Hindi: "अमेरिका", "US", "USA", "उत्तरी अमेरिका"
  - English: "United States", "US", "USA", "North America"

**EU:**
  - Korean: "유럽", "EU", "유럽 시장", "독일", "프랑스", "영국"
  - Chinese: "欧洲", "EU", "欧盟", "德国", "法国", "英国"
  - Japanese: "ヨーロッパ", "EU", "欧州", "ドイツ", "フランス", "イギリス"
  - Spanish: "Europa", "UE", "Unión Europea", "Alemania", "Francia", "Reino Unido"
  - Arabic: "أوروبا", "EU", "الاتحاد الأوروبي", "ألمانيا", "فرنسا"
  - Hindi: "यूरोप", "EU", "यूरोपीय संघ", "जर्मनी", "फ्रांस"
  - English: "Europe", "EU", "European Union", "Germany", "France", "UK"

**Korea:**
  - Korean: "한국", "대한민국", "코리아", "국내", "내수"
  - Chinese: "韩国", "大韩民国"
  - Japanese: "韓国", "コリア"
  - Spanish: "Corea", "Corea del Sur"
  - Arabic: "كوريا", "كوريا الجنوبية"
  - Hindi: "कोरिया", "दक्षिण कोरिया"
  - English: "Korea", "South Korea"

**Japan:**
  - Korean: "일본", "Japan", "JP", "일본 시장"
  - Chinese: "日本", "Japan", "JP"
  - Japanese: "日本", "Japan", "JP", "日本市場"
  - Spanish: "Japón", "Japan", "JP"
  - Arabic: "اليابان", "Japan", "JP"
  - Hindi: "जापान", "Japan", "JP"
  - English: "Japan", "JP"

**Global:**
  - Korean: "전세계", "글로벌", "해외 전반"
  - Chinese: "全球", "全世界", "国际市场"
  - Japanese: "全世界", "グローバル", "国際市場"
  - Spanish: "global", "mundial", "internacional"
  - Arabic: "عالمي", "دولي", "السوق العالمي"
  - Hindi: "वैश्विक", "अंतर्राष्ट्रीय"
  - English: "global", "worldwide", "international"

**Other (set to "Other" and keep raw text):**
  - Southeast Asia: "동남아", "SEA", "东南亚", "東南アジア", "ASEAN", "ASEAN"
  - Middle East: "중동", "MENA", "GCC", "中东", "中東", "الشرق الأوسط"
  - China: "중국", "대만", "홍콩", "中国", "台湾", "香港", "中国", "台湾", "香港"
  - Latin America: "남미", "LATAM", "拉美", "ラテンアメリカ", "América Latina"
  - Oceania: "오세아니아", "ANZ", "大洋洲", "オセアニア"
  - Canada: "캐나다", "加拿大", "カナダ", "Canadá"
  - UK: "영국", "英国", "イギリス", "Reino Unido" (post-Brexit)
  
**Rule:**
  - If user mentions regions like "동남아/SEA", "중동/MENA", "중국/China", "남미/LATAM" in ANY language:
    - Set "target_market": "Other"
    - Set "target_market_raw": the original phrase
  - If unclear or not mentioned: Set "target_market": "Other", keep "target_market_raw": original text (if provided)

4) Price Range (Multi-language price → structured object)
- Extract target price or price range from user input in ANY language.
- Convert number units from any language (see Volume section for unit conversions).
- Currency detection:
  - "원", "KRW", "W" → "KRW"
  - "달러", "USD", "$", "US$", "dollar" → "USD"
  - "元", "人民币", "CNY", "RMB" → "CNY"
  - "円", "JPY", "¥" → "JPY"
  - "欧元", "EUR", "€" → "EUR"
  - "比索", "peso", "MXN" → "MXN"
  - "ريال", "SAR", "AED" → detect from context
  - "रुपया", "INR", "₹" → "INR"
- Examples:
  - "개당 1천원 이하" → {"min": null, "max": 1000, "currency": "KRW"}
  - "5~10달러" → {"min": 5, "max": 10, "currency": "USD"}
  - "개당 5000원 정도" → {"min": 4500, "max": 5500, "currency": "KRW"} (approximate)
  - "저가로" → null (too vague, keep "price_range_raw": "저가로")
  - "프리미엄 제품" → null (too vague)
  - "1만원대" → {"min": 10000, "max": 19999, "currency": "KRW"}
- If not mentioned or too vague, set:
  - "price_range": null
  - "price_range_raw": original text (if provided)

5) Delivery Timeline (Multi-language time expression → category)
- Extract delivery urgency or timeline from user input in ANY language.

**Urgent (under 1 week):**
  - Korean: "1주일 이내", "일주일 안에", "급하게", "빨리", "즉시", "가능한 빨리"
  - Chinese: "一周内", "紧急", "尽快", "立即"
  - Japanese: "1週間以内", "急ぎ", "すぐに", "至急"
  - Spanish: "en una semana", "urgente", "rápido", "inmediato"
  - Arabic: "في أسبوع", "عاجل", "سريع", "فوراً"
  - Hindi: "एक सप्ताह में", "जरूरी", "जल्दी", "तुरंत"
  - English: "within 1 week", "urgent", "asap", "immediate"

**Short-term (1-4 weeks):**
  - Korean: "2주일", "2~3주", "한 달 안에"
  - Chinese: "2周", "2-3周", "一个月内"
  - Japanese: "2週間", "2〜3週間", "1ヶ月以内"
  - Spanish: "2 semanas", "2-3 semanas", "en un mes"
  - Arabic: "أسبوعين", "2-3 أسابيع", "في شهر"
  - Hindi: "2 सप्ताह", "2-3 सप्ताह", "एक महीने में"
  - English: "2 weeks", "2-3 weeks", "within a month"

**Medium-term (1-3 months):**
  - Korean: "2~3개월", "분기 내", "3개월 이내"
  - Chinese: "2-3个月", "季度内", "3个月内"
  - Japanese: "2〜3ヶ月", "四半期内", "3ヶ月以内"
  - Spanish: "2-3 meses", "en el trimestre", "en 3 meses"
  - Arabic: "2-3 أشهر", "في الربع", "في 3 أشهر"
  - Hindi: "2-3 महीने", "तिमाही में", "3 महीने में"
  - English: "2-3 months", "within quarter", "in 3 months"

**Long-term (over 3 months):**
  - Korean: "6개월", "장기적으로", "여유있게"
  - Chinese: "6个月", "长期", "不着急"
  - Japanese: "6ヶ月", "長期的に", "余裕を持って"
  - Spanish: "6 meses", "a largo plazo", "sin prisa"
  - Arabic: "6 أشهر", "على المدى الطويل", "بلا عجلة"
  - Hindi: "6 महीने", "दीर्घकालिक", "जल्दी नहीं"
  - English: "6 months", "long-term", "no rush"
- If not mentioned, set:
  - "delivery_timeline": null
  - "delivery_timeline_raw": null

6) MOQ (Minimum Order Quantity)
- Extract minimum order quantity requirement mentioned by user in ANY language.
- Similar to volume extraction, but specifically for MOQ mentions.

**Examples (multi-language):**
  - Korean: "MOQ 1만개", "최소 500개", "최소 주문량 1000개" → 10000, 500, 1000
  - Chinese: "MOQ 1万个", "最少500个", "最低订购量1000个" → 10000, 500, 1000
  - Japanese: "MOQ 1万個", "最低500個", "最小注文数量1000個" → 10000, 500, 1000
  - Spanish: "MOQ 10 mil", "mínimo 500", "cantidad mínima 1000" → 10000, 500, 1000
  - Arabic: "الحد الأدنى 10 آلاف", "الحد الأدنى 500" → 10000, 500
  - Hindi: "MOQ 10 हज़ार", "न्यूनतम 500", "न्यूनतम आदेश 1000" → 10000, 500, 1000
  - English: "MOQ 10k", "minimum 500", "min order 1000" → 10000, 500, 1000
  - "MOQ 없이", "no MOQ", "无MOQ要求" → null
- If not mentioned, set:
  - "moq": null
  - "moq_raw": null

General:
- The user may write in ANY language (Korean, English, Chinese, Japanese, Spanish, Arabic, Hindi, etc.) or mix languages.
- Be tolerant of typos, slang, and language mixing.
- Never invent information that the user did not imply.
- If a field is not mentioned at all, set its value to null and keep *_raw as null.
- For numbers, convert units from the source language (Korean 万=10k, Chinese 万=10k, Japanese 万=10k, etc.)

Now read the following user message and extract the fields.

User message:
\"\"\"{user_message}\"\"\"

Return ONLY the JSON. Do not add explanations.
"""


def build_extraction_prompt(user_input_text: str) -> str:
    """
    Build the extraction prompt for LLM.
    
    Args:
        user_input_text: Raw user input (may contain product description, volume, channel, market)
        
    Returns:
        Complete prompt string for extraction
    """
    return EXTRACTION_USER_PROMPT_TEMPLATE.format(user_message=user_input_text)


def create_user_prompt(user_input: str) -> str:
    """
    Create a user prompt for the sourcing parser API call.
    Alias for build_extraction_prompt for compatibility.
    
    Args:
        user_input: User's sourcing request text
        
    Returns:
        Formatted user prompt string
    """
    return f"""Parse the following sourcing request and extract volume, channel, and target_market.

User Input:
{user_input}

Return ONLY the JSON object. Do not add any explanation."""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

class VolumeCategory(str, Enum):
    """Volume size categories based on quantity"""
    VERY_SMALL = "very_small"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    UNKNOWN = "unknown"


def normalize_korean_number(text: str) -> Optional[int]:
    """
    Convert number expressions from multiple languages to integers.
    
    Supports: Korean, Chinese, Japanese, Spanish, Arabic, Hindi, English
    
    Examples:
        "200만개" → 2000000 (Korean)
        "200万个" → 2000000 (Chinese)
        "200万個" → 2000000 (Japanese)
        "5천개" → 5000 (Korean)
        "5千个" → 5000 (Chinese)
        "5千個" → 5000 (Japanese)
        "1~2만개" → 20000 (range, use upper bound)
    """
    if not text:
        return None
    
    # Handle ranges (use upper bound)
    if "~" in text or "-" in text or "〜" in text or "～" in text:
        numbers = re.findall(r'\d+(?:\.\d+)?', text)
        if numbers:
            upper = int(float(numbers[-1]))
            # Check for units after the last number
            text_after_last_num = text.split(numbers[-1])[-1] if numbers else ""
            # Korean/Chinese/Japanese: 亿/억 (100M), 万/만 (10K), 千/천 (1K)
            if "억" in text_after_last_num or "亿" in text_after_last_num or "億" in text_after_last_num:
                return upper * 100000000
            elif "만" in text_after_last_num or "万" in text_after_last_num:
                return upper * 10000
            elif "천" in text_after_last_num or "千" in text_after_last_num:
                return upper * 1000
            # Spanish: millón (1M), mil (1K)
            elif "millón" in text_after_last_num.lower() or "million" in text_after_last_num.lower():
                return upper * 1000000
            elif "mil" in text_after_last_num.lower() and "millón" not in text_after_last_num.lower():
                return upper * 1000
            # Arabic: مليون (1M), ألف (1K)
            elif "مليون" in text_after_last_num:
                return upper * 1000000
            elif "ألف" in text_after_last_num:
                return upper * 1000
            # Hindi: करोड़ (10M), लाख (100K), हज़ार (1K)
            elif "करोड़" in text_after_last_num:
                return upper * 10000000
            elif "लाख" in text_after_last_num:
                return upper * 100000
            elif "हज़ार" in text_after_last_num:
                return upper * 1000
            return upper
        return None
    
    text_normalized = text.lower().strip()
    match = re.search(r'(\d+(?:\.\d+)?)', text_normalized)
    if not match:
        return None
    
    base_num = int(float(match.group(1)))
    
    # Korean/Chinese/Japanese units
    if "억" in text or "亿" in text or "億" in text:
        return base_num * 100000000
    elif "만" in text or "万" in text:
        return base_num * 10000
    elif "천" in text or "千" in text:
        return base_num * 1000
    
    # Spanish units
    if "millón" in text_normalized or "million" in text_normalized:
        return base_num * 1000000
    if "mil" in text_normalized and "millón" not in text_normalized:
        return base_num * 1000
    
    # Arabic units
    if "مليون" in text:
        return base_num * 1000000
    if "ألف" in text:
        return base_num * 1000
    
    # Hindi units
    if "करोड़" in text:
        return base_num * 10000000
    if "लाख" in text:
        return base_num * 100000
    if "हज़ार" in text:
        return base_num * 1000
    
    # English units
    if "m" in text_normalized and "million" in text_normalized or text_normalized.endswith("m"):
        return base_num * 1000000
    if "k" in text_normalized or "thousand" in text_normalized:
        return base_num * 1000
    
    return base_num


def infer_volume_category(volume: Optional[int], volume_raw: Optional[str]) -> Optional[str]:
    """
    Infer volume category from quantity or raw text (multi-language support).
    
    Args:
        volume: Normalized volume integer
        volume_raw: Original volume text (any language)
        
    Returns:
        Volume category string or None
    """
    if volume is None:
        if volume_raw:
            # Multi-language vague terms
            vague_terms = [
                # Korean
                "소량", "조금", "테스트", "박스", "최소", "moq", "mq",
                # Chinese
                "少量", "测试", "样品", "最小", "MOQ",
                # Japanese
                "少量", "テスト", "サンプル", "最小", "MOQ",
                # Spanish
                "poco", "prueba", "muestra", "mínimo", "MOQ",
                # Arabic
                "قليل", "اختبار", "عينة", "الحد الأدنى", "MOQ",
                # Hindi
                "कम", "परीक्षण", "नमूना", "न्यूनतम", "MOQ",
                # English
                "small", "test", "sample", "minimum", "moq"
            ]
            if any(term in volume_raw.lower() for term in vague_terms):
                return VolumeCategory.VERY_SMALL.value
        return VolumeCategory.UNKNOWN.value
    
    if volume < 5000:
        return VolumeCategory.SMALL.value
    elif volume < 100000:
        return VolumeCategory.MEDIUM.value
    elif volume < 1000000:
        return VolumeCategory.LARGE.value
    else:
        return VolumeCategory.LARGE.value


def normalize_extracted_values(extracted: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize extracted values to match internal system format.
    
    Args:
        extracted: Raw extraction result from LLM
        
    Returns:
        Normalized dictionary with standard keys
    """
    from utils.config import AppSettings
    
    # Normalize channel
    channel = extracted.get("channel", "Other")
    channel_mapping = {
        "Convenience Store": "Convenience Store",
        "Amazon FBA": "Amazon FBA",
        "eCommerce D2C": "Online",
        "Wholesale Distributor": "Wholesale",
        "Offline Retail": "Retail",
        "Other": AppSettings.DEFAULT_CHANNEL
    }
    normalized_channel = channel_mapping.get(channel, AppSettings.DEFAULT_CHANNEL)
    
    # Normalize target market
    target_market = extracted.get("target_market", "Other")
    market_mapping = {
        "USA": "USA",
        "EU": "EU",
        "Korea": "Korea",
        "Japan": "Japan",
        "Global": "Global",
        "Other": AppSettings.DEFAULT_TARGET_MARKET
    }
    normalized_market = market_mapping.get(target_market, AppSettings.DEFAULT_TARGET_MARKET)
    
    # Infer route from target market
    route_mapping = {
        "USA": "cn_to_us_west_coast",
        "EU": "cn_to_eu",
        "Korea": "cn_to_korea",
        "Japan": "cn_to_japan",
        "Global": "cn_to_us_west_coast",  # Default
        "Other": AppSettings.DEFAULT_ROUTE
    }
    route = route_mapping.get(normalized_market, AppSettings.DEFAULT_ROUTE)
    
    return {
        "volume_units": extracted.get("volume"),
        "volume_raw": extracted.get("volume_raw"),
        "channel": normalized_channel,
        "channel_raw": extracted.get("channel_raw"),
        "target_market": normalized_market,
        "target_market_raw": extracted.get("target_market_raw"),
        "route": route
    }


def validate_and_normalize_extraction(llm_response_str: str) -> tuple[Dict[str, Any], Optional[str]]:
    """
    Validate LLM response using Pydantic and normalize to internal format.
    
    Args:
        llm_response_str: JSON string from LLM (may include markdown)
        
    Returns:
        Tuple of (normalized_dict, error_message)
        If validation fails, returns (None, error_message)
    """
    import json
    import re
    
    # Clean and parse JSON first
    try:
        cleaned = llm_response_str.strip()
        # Remove markdown code blocks
        if "```json" in cleaned:
            cleaned = re.sub(r'```json\s*\n?(.*?)\n?```', r'\1', cleaned, flags=re.DOTALL)
        elif "```" in cleaned:
            cleaned = re.sub(r'```\s*\n?(.*?)\n?```', r'\1', cleaned, flags=re.DOTALL)
        
        # Extract JSON object
        first_brace = cleaned.find('{')
        last_brace = cleaned.rfind('}')
        if first_brace != -1 and last_brace != -1:
            cleaned = cleaned[first_brace:last_brace + 1]
        
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {str(e)}"
    except Exception as e:
        return None, f"Error cleaning response: {str(e)}"
    
    # Try to validate with Pydantic if available
    try:
        from utils.models import SourcingIntents
        from pydantic import ValidationError
        
        # Validate with Pydantic
        validated = SourcingIntents.model_validate(data)
        # Convert to dict for normalization
        data_dict = validated.model_dump()
        
        # Normalize and return
        normalized = normalize_extracted_values(data_dict)
        
        # Add volume_category if not present
        if "volume_category" not in normalized:
            normalized["volume_category"] = infer_volume_category(
                normalized.get("volume_units"),
                normalized.get("volume_raw")
            )
        
        return normalized, None
        
    except ImportError:
        # Pydantic not available, use direct normalization
        return normalize_extracted_values(data), None
    except ValidationError as e:
        # Pydantic validation failed, try direct normalization anyway
        try:
            return normalize_extracted_values(data), None
        except Exception as norm_err:
            return None, f"Pydantic validation failed: {str(e)}, normalization also failed: {str(norm_err)}"
    except Exception as e:
        # Other error, try direct normalization
        try:
            return normalize_extracted_values(data), None
        except Exception as norm_err:
            return None, f"Error: {str(e)}, normalization also failed: {str(norm_err)}"
    
    try:
        # Clean response text
        cleaned = llm_response_str.strip()
        
        # Remove markdown code blocks
        if "```json" in cleaned:
            cleaned = re.sub(r'```json\s*\n?(.*?)\n?```', r'\1', cleaned, flags=re.DOTALL)
        elif "```" in cleaned:
            cleaned = re.sub(r'```\s*\n?(.*?)\n?```', r'\1', cleaned, flags=re.DOTALL)
        
        # Extract JSON object
        first_brace = cleaned.find('{')
        last_brace = cleaned.rfind('}')
        if first_brace != -1 and last_brace != -1:
            cleaned = cleaned[first_brace:last_brace + 1]
        
        # Validate with Pydantic
        parsed = SourcingIntents.model_validate_json(cleaned)
        
        # Convert to dict and normalize
        extracted_dict = parsed.model_dump()
        normalized = normalize_extracted_values(extracted_dict)
        
        # Add volume_category if not present
        if "volume_category" not in normalized:
            normalized["volume_category"] = infer_volume_category(
                normalized.get("volume_units"),
                normalized.get("volume_raw")
            )
        
        return normalized, None
        
    except ValidationError as e:
        # Pydantic validation failed - try to extract what we can
        try:
            data = json.loads(cleaned)
            # Use normalize_extracted_values even if validation failed
            normalized = normalize_extracted_values(data)
            return normalized, f"Validation warning: {str(e)}"
        except:
            return None, f"Pydantic validation failed: {str(e)}"
    except json.JSONDecodeError as e:
        return None, f"JSON parse error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

