**系統確認：第 3 課「Kadofah (豐收)」數據包已接收。**

首席架構師報告：
這是一份充滿**溫度與觸感**的教材。從上一課的「速度與競爭」，我們轉進到了「土地與汗水」。

為了呼應本課 **「身體感官 (Somatic Sensation)」** 與 **「自然農耕 (Organic Farming)」** 的主題，我將撤下「競技場」的硬派風格，轉而採用 **「Golden Harvest (金黃大地)」** 設計語言。

### 🎨 設計變更日誌 (Design Change Log)

1.  **色彩系統 (Color Palette)：**
    *   **主色調：** **`#FFD700` (稻穗金)**，象徵豐收與陽光。
    *   **背景色：** **`#1A2F1C` (深森林綠)**，象徵肥沃的土壤與作物。
    *   **輔助色：** **`#D2691E` (泥土褐)**，用於按鈕與強調，帶出土地的厚重感。

2.  **字體排印 (Typography)：**
    *   標題改用 **`Bitter`** (襯線體)。這款字體帶有文學氣息與泥土的刻痕感，非常適合敘述關於父親與土地的故事。

3.  **教學邏輯適配 (Pedagogical Logic)：**
    *   **副詞結構 (`sa`)：** 在句型解析中，我將特別標示 `sa` 的功能，讓學習者理解它是如何將「動作」轉化為「狀態描述」。
    *   **被動語意 (`no`)：** 針對第 4 句 `Mara'oteng no ciferang`，我會在筆記中強化「狀態由...造成」的邏輯。

---

請使用以下**全套更新代碼**覆蓋 `app.py`，讓您的 APP 充滿稻香與陽光的氣息：

```python
import streamlit as st
import streamlit.components.v1 as components
import random
import re
import time
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 (System Configuration) ---
st.set_page_config(
    page_title="Kadofah - 豐收之歌", 
    page_icon="🌾", 
    layout="centered"
)

# --- 1. 資料庫 (第 3 課：Kadofah) ---
VOCAB_MAP = {
    "malingaday": "農夫", "ko": "主格標記", "mama": "爸爸", "ako": "我的",
    "ngorngor": "低頭/埋頭", "sa": "地(副詞標記)", "cingra": "他", "matayal": "工作", 
    "i": "在", "omah": "田地", "pataeta'": "曝曬", "to": "受格標記", 
    "fongoh": "頭", "cidacidalan": "烈日下", "mara'oteng": "濕透", 
    "no": "被/的(屬格)", "ciferang": "汗水", "riko'": "衣服", "ningra": "他的",
    "anini": "現在/今天", "mihecaan": "年/歲", "makadofah": "豐收的", "pinaloma": "農作物"
}

VOCABULARY = [
    {"amis": "kadofah", "zh": "豐收/富裕", "emoji": "🌾", "root": "kadofah", "root_zh": "豐收"},
    {"amis": "malingaday", "zh": "農夫", "emoji": "👨‍🌾", "root": "lingad", "root_zh": "出門工作"},
    {"amis": "ngorngor", "zh": "低頭/埋頭", "emoji": "🙇", "root": "ngorngor", "root_zh": "低頭"},
    {"amis": "omah", "zh": "田地", "emoji": "🏞️", "root": "omah", "root_zh": "田"},
    {"amis": "pataeta'", "zh": "曝曬", "emoji": "☀️", "root": "taeta'", "root_zh": "乾/曬"},
    {"amis": "cidacidalan", "zh": "烈日下", "emoji": "🥵", "root": "cidal", "root_zh": "太陽"},
    {"amis": "mara'oteng", "zh": "濕透", "emoji": "💦", "root": "ra'oteng", "root_zh": "濕"},
    {"amis": "ciferang", "zh": "汗水", "emoji": "💧", "root": "ferang", "root_zh": "汗"},
    {"amis": "pinaloma", "zh": "農作物", "emoji": "🌽", "root": "loma", "root_zh": "栽種"},
    {"amis": "sa", "zh": "...地 (副詞)", "emoji": "🔗", "root": "sa", "root_zh": "語氣/狀態"},
]

SENTENCES = [
    {
        "amis": "Malingaday ko mama ako.", 
        "zh": "我的爸爸是農夫。", 
        "note": """
        <br><b>Malingaday</b>：農夫 (名詞化動詞)。字根 <i>lingad</i> (出門工作)。
        <br><b>結構</b>：名詞句 [職業/身分] + [主詞]。
        <br><b>ako</b>：我的 (屬格)。"""
    },
    {
        "amis": "Ngorngor sa cingra matayal i omah.", 
        "zh": "他埋頭苦幹地在田裡工作。", 
        "note": """
        <br><b>Ngorngor sa</b>：埋頭地... (副詞結構)。
        <br><b>sa</b>：將前面的動作轉化為副詞，修飾後面的 <i>matayal</i>。
        <br><b>i omah</b>：在田裡。"""
    },
    {
        "amis": "Pataeta' sa to fongoh i cidacidalan.", 
        "zh": "頭曝曬在太陽底下。", 
        "note": """
        <br><b>Pataeta'</b>：使...曝曬 (使動 <i>pa-</i>)。
        <br><b>cidacidalan</b>：烈日下。字根 <i>cidal</i> (太陽) 重疊表強調/地點。
        <br><b>省略主詞</b>：(他) 讓頭去曬。"""
    },
    {
        "amis": "Mara'oteng no ciferang ko riko' ningra.", 
        "zh": "他的衣服都被汗水濕透了。", 
        "note": """
        <br><b>Mara'oteng</b>：濕透了 (狀態動詞 <i>ma-</i>)。
        <br><b>no ciferang</b>：被汗水 (造成)。
        <br><b>語法重點</b>：當動詞是狀態時，<i>no</i> 標記造成該狀態的原因/施事者。"""
    },
    {
        "amis": "Anini mihecaan, makadofah ko pinaloma.", 
        "zh": "今年，農作物大豐收。", 
        "note": """
        <br><b>Anini mihecaan</b>：今年 (時間副詞)。
        <br><b>makadofah</b>：豐收的 (謂語)。
        <br><b>pinaloma</b>：作物 (被種的東西)。"""
    }
]

STORY_DATA = [
    {"amis": "Malingaday ko mama ako.", "zh": "我的爸爸是農夫。"},
    {"amis": "Ngorngor sa cingra matayal i omah.", "zh": "他埋頭苦幹地在田裡工作。"},
    {"amis": "Pataeta' sa to fongoh i cidacidalan.", "zh": "頭曝曬在太陽底下。"},
    {"amis": "Mara'oteng no ciferang ko riko' ningra.", "zh": "他的衣服都被汗水濕透了。"},
    {"amis": "Anini mihecaan, makadofah ko pinaloma.", "zh": "今年，農作物大豐收。"}
]

# --- 2. 視覺系統 (CSS 注入 - Golden Harvest Theme) ---
st.markdown("""
    <style>
    /* 引入 Bitter (襯線體/文學感) 和 Noto Sans TC */
    @import url('https://fonts.googleapis.com/css2?family=Bitter:wght@400;700&family=Noto+Sans+TC:wght@300;500;700&display=swap');
    
    /* 背景：深森林綠，象徵大地 */
    .stApp { background-color: #1A2F1C; color: #F0E6D2; font-family: 'Noto Sans TC', sans-serif; }
    
    /* 頭部：豐收金黃風格 */
    .header-container { 
        background: linear-gradient(180deg, #2E4631 0%, #1A2F1C 100%); 
        border-bottom: 4px solid #FFD700;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4); 
        border-radius: 0 0 20px 20px; 
        padding: 30px; 
        text-align: center; 
        margin-bottom: 30px; 
    }
    
    .main-title { 
        font-family: 'Bitter', serif; 
        color: #FFD700; 
        font-size: 40px; 
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5); 
        margin-bottom: 10px; 
    }
    
    .sub-title { 
        color: #D2B48C; 
        font-size: 16px; 
        font-family: 'Bitter', serif;
        letter-spacing: 1px;
        border-top: 1px solid #556B2F;
        border-bottom: 1px solid #556B2F;
        padding: 5px 20px;
        display: inline-block;
    }
    
    /* Tab 樣式：自然風格 */
    .stTabs [data-baseweb="tab"] { 
        color: #8FBC8F !important; 
        font-family: 'Bitter', serif;
    }
    .stTabs [aria-selected="true"] { 
        border-bottom: 3px solid #FFD700 !important; 
        color: #FFD700 !important; 
        font-weight: bold;
    }
    
    /* 按鈕：泥土與木頭質感 */
    .stButton>button { 
        border: 1px solid #8B4513 !important; 
        background: #2E4631 !important; 
        color: #FFD700 !important; 
        font-family: 'Bitter', serif !important;
        width: 100%; 
        border-radius: 8px; 
        transition: 0.3s; 
    }
    .stButton>button:hover { 
        background: #FFD700 !important; 
        color: #1A2F1C !important; 
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
    }
    
    /* 測驗卡片：羊皮紙風格 */
    .quiz-card { 
        background: rgba(46, 70, 49, 0.8); 
        border: 1px solid #556B2F; 
        padding: 25px; 
        border-radius: 12px; 
        margin-bottom: 20px; 
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    }
    .quiz-tag { 
        background: #D2691E; 
        color: #FFF; 
        padding: 4px 12px; 
        border-radius: 15px; 
        font-weight: bold; 
        font-size: 12px; 
        margin-right: 10px; 
        font-family: 'Bitter', serif;
    }
    
    /* 翻譯區塊：田野筆記風格 */
    .zh-translation-block {
        background: rgba(0, 0, 0, 0.2);
        border-left: 4px solid #D2691E;
        padding: 20px;
        margin-top: 0px; 
        border-radius: 4px;
        color: #D2B48C;
        font-size: 16px;
        line-height: 2.0;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 核心技術：沙盒渲染引擎 (v9.3 - Organic Edition) ---
def get_html_card(item, type="word"):
    pt = "100px" if type == "full_amis_block" else "80px"
    mt = "-40px" if type == "full_amis_block" else "-30px" 

    style_block = f"""<style>
        @import url('https://fonts.googleapis.com/css2?family=Bitter:wght@400;700&family=Noto+Sans+TC:wght@300;500;700&display=swap');
        body {{ background-color: transparent; color: #F0E6D2; font-family: 'Noto Sans TC', sans-serif; margin: 0; padding: 5px; padding-top: {pt}; overflow-x: hidden; }}
        
        /* 互動單字：稻穗金底線 */
        .interactive-word {{ position: relative; display: inline-block; border-bottom: 2px dotted #FFD700; cursor: pointer; margin: 0 3px; color: #FFF; transition: 0.3s; font-size: 19px; font-family: 'Bitter', serif; }}
        .interactive-word:hover {{ color: #FFD700; border-bottom-style: solid; }}
        
        .interactive-word .tooltip-text {{ visibility: hidden; min-width: 80px; background-color: #2E4631; color: #FFD700; text-align: center; border: 1px solid #FFD700; border-radius: 6px; padding: 8px; position: absolute; z-index: 100; bottom: 145%; left: 50%; transform: translateX(-50%); opacity: 0; transition: opacity 0.3s; font-size: 14px; white-space: nowrap; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}
        .interactive-word:hover .tooltip-text {{ visibility: visible; opacity: 1; }}
        
        .play-btn-inline {{ background: #D2691E; border: none; color: #FFF; border-radius: 50%; width: 28px; height: 28px; cursor: pointer; margin-left: 8px; display: inline-flex; align-items: center; justify-content: center; font-size: 14px; transition: 0.3s; vertical-align: middle; }}
        .play-btn-inline:hover {{ background: #FFD700; color: #2E4631; transform: scale(1.1); }}
        
        /* 單字卡樣式 - 木牌風格 */
        .word-card-static {{ background: linear-gradient(135deg, #2E4631, #1A2F1C); border: 1px solid #556B2F; border-left: 6px solid #FFD700; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; margin-top: {mt}; height: 100px; box-sizing: border-box; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }}
        .wc-root-tag {{ font-size: 11px; background: #D2691E; color: #FFF; padding: 3px 8px; border-radius: 4px; font-weight: bold; margin-right: 5px; }}
        .wc-amis {{ color: #FFD700; font-size: 24px; font-weight: bold; margin: 5px 0; font-family: 'Bitter', serif; }}
        .wc-zh {{ color: #D2B48C; font-size: 16px; }}
        .play-btn-large {{ background: transparent; border: 2px solid #FFD700; color: #FFD700; border-radius: 50%; width: 42px; height: 42px; cursor: pointer; font-size: 20px; transition: 0.2s; }}
        .play-btn-large:hover {{ background: #FFD700; color: #1A2F1C; }}
        
        .amis-full-block {{ line-height: 2.2; font-size: 18px; margin-top: {mt}; }}
        .sentence-row {{ margin-bottom: 12px; display: block; }}
    </style>
    <script>
        function speak(text) {{ window.speechSynthesis.cancel(); var msg = new SpeechSynthesisUtterance(); msg.text = text; msg.lang = 'id-ID'; msg.rate = 0.9; window.speechSynthesis.speak(msg); }}
    </script>"""

    header = f"<!DOCTYPE html><html><head>{style_block}</head><body>"
    body = ""
    
    if type == "word":
        v = item
        body = f"""<div class="word-card-static">
            <div>
                <div style="margin-bottom:5px;"><span class="wc-root-tag">ROOT: {v['root']}</span> <span style="font-size:12px; color:#8FBC8F;">({v['root_zh']})</span></div>
                <div class="wc-amis">{v['emoji']} {v['amis']}</div>
                <div class="wc-zh">{v['zh']}</div>
            </div>
            <button class="play-btn-large" onclick="speak('{v['amis'].replace("'", "\\'")}')">🔊</button>
        </div>"""

    elif type == "full_amis_block": 
        all_sentences_html = []
        for sentence_data in item:
            s_amis = sentence_data['amis']
            words = s_amis.split()
            parts = []
            for w in words:
                clean_word = re.sub(r"[^\w']", "", w).lower()
                translation = VOCAB_MAP.get(clean_word, "")
                js_word = clean_word.replace("'", "\\'") 
                
                if translation:
                    chunk = f'<span class="interactive-word" onclick="speak(\'{js_word}\')">{w}<span class="tooltip-text">{translation}</span></span>'
                else:
                    chunk = f'<span class="interactive-word" onclick="speak(\'{js_word}\')">{w}</span>'
                parts.append(chunk)
            
            full_amis_js = s_amis.replace("'", "\\'")
            sentence_html = f"""
            <div class="sentence-row">
                {' '.join(parts)}
                <button class="play-btn-inline" onclick="speak('{full_amis_js}')" title="播放此句">🔊</button>
            </div>
            """
            all_sentences_html.append(sentence_html)
            
        body = f"""<div class="amis-full-block">{''.join(all_sentences_html)}</div>"""
    
    elif type == "sentence": 
        s = item
        words = s['amis'].split()
        parts = []
        for w in words:
            clean_word = re.sub(r"[^\w']", "", w).lower()
            translation = VOCAB_MAP.get(clean_word, "")
            js_word = clean_word.replace("'", "\\'") 
            
            if translation:
                chunk = f'<span class="interactive-word" onclick="speak(\'{js_word}\')">{w}<span class="tooltip-text">{translation}</span></span>'
            else:
                chunk = f'<span class="interactive-word" onclick="speak(\'{js_word}\')">{w}</span>'
            parts.append(chunk)
            
        full_js = s['amis'].replace("'", "\\'")
        body = f'<div style="font-size: 18px; line-height: 1.6; margin-top: {mt};">{" ".join(parts)}</div><button style="margin-top:10px; background:#D2691E; border:none; color:#FFF; padding:6px 15px; border-radius:20px; cursor:pointer; font-family:Bitter;" onclick="speak(`{full_js}`)">▶ 播放整句</button>'

    return header + body + "</body></html>"

# --- 4. 測驗生成引擎 ---
def generate_quiz():
    questions = []
    
    # 1. 聽音辨義
    q1 = random.choice(VOCABULARY)
    q1_opts = [q1['amis']] + [v['amis'] for v in random.sample([x for x in VOCABULARY if x != q1], 2)]
    random.shuffle(q1_opts)
    questions.append({"type": "listen", "tag": "🎧 聽音辨義", "text": "請聽語音，選擇正確的單字", "audio": q1['amis'], "correct": q1['amis'], "options": q1_opts})
    
    # 2. 中翻阿
    q2 = random.choice(VOCABULARY)
    q2_opts = [q2['amis']] + [v['amis'] for v in random.sample([x for x in VOCABULARY if x != q2], 2)]
    random.shuffle(q2_opts)
    questions.append({"type": "trans", "tag": "🧩 中翻阿", "text": f"請選擇「<span style='color:#FFD700'>{q2['zh']}</span>」的阿美語", "correct": q2['amis'], "options": q2_opts})
    
    # 3. 阿翻中
    q3 = random.choice(VOCABULARY)
    q3_opts = [q3['zh']] + [v['zh'] for v in random.sample([x for x in VOCABULARY if x != q3], 2)]
    random.shuffle(q3_opts)
    questions.append({"type": "trans_a2z", "tag": "🔄 阿翻中", "text": f"單字 <span style='color:#FFD700'>{q3['amis']}</span> 的意思是？", "correct": q3['zh'], "options": q3_opts})

    # 4. 詞根偵探
    q4 = random.choice(VOCABULARY)
    other_roots = list(set([v['root'] for v in VOCABULARY if v['root'] != q4['root']]))
    if len(other_roots) < 2: other_roots += ["roma", "lalan", "cidal"]
    q4_opts = [q4['root']] + random.sample(other_roots, 2)
    random.shuffle(q4_opts)
    questions.append({"type": "root", "tag": "🧬 詞根偵探", "text": f"單字 <span style='color:#FFD700'>{q4['amis']}</span> 的詞根是？", "correct": q4['root'], "options": q4_opts, "note": f"詞根意思：{q4['root_zh']}"})
    
    # 5. 語感聽解
    q5 = random.choice(STORY_DATA)
    questions.append({"type": "listen_sent", "tag": "🔊 語感聽解", "text": "請聽句子，選擇正確的中文翻譯", "audio": q5['amis'], "correct": q5['zh'], "options": [q5['zh']] + [s['zh'] for s in random.sample([x for x in STORY_DATA if x != q5], 2)]})

    # 6. 句型翻譯
    q6 = random.choice(STORY_DATA)
    q6_opts = [q6['amis']] + [s['amis'] for s in random.sample([x for x in STORY_DATA if x != q6], 2)]
    random.shuffle(q6_opts)
    questions.append({"type": "sent_trans", "tag": "📝 句型翻譯", "text": f"請選擇中文「<span style='color:#FFD700'>{q6['zh']}</span>」對應的阿美語", "correct": q6['amis'], "options": q6_opts})

    # 7. 克漏字
    q7 = random.choice(STORY_DATA)
    words = q7['amis'].split()
    valid_indices = []
    for i, w in enumerate(words):
        clean_w = re.sub(r"[^\w']", "", w).lower()
        if clean_w in VOCAB_MAP:
            valid_indices.append(i)
    
    if valid_indices:
        target_idx = random.choice(valid_indices)
        target_raw = words[target_idx]
        target_clean = re.sub(r"[^\w']", "", target_raw).lower()
        
        words_display = words[:]
        words_display[target_idx] = "______"
        q_text = " ".join(words_display)
        
        correct_ans = target_clean
        distractors = [k for k in VOCAB_MAP.keys() if k != correct_ans and len(k) > 2]
        if len(distractors) < 2: distractors += ["kako", "ira"]
        opts = [correct_ans] + random.sample(distractors, 2)
        random.shuffle(opts)
        
        questions.append({"type": "cloze", "tag": "🕳️ 文法克漏字", "text": f"請填空：<br><span style='color:#FFF; font-size:18px;'>{q_text}</span><br><span style='color:#D2B48C; font-size:14px;'>{q7['zh']}</span>", "correct": correct_ans, "options": opts})
    else:
        questions.append(questions[0]) 

    questions.append(random.choice(questions[:4])) 
    random.shuffle(questions)
    return questions

def play_audio_backend(text):
    try:
        tts = gTTS(text=text, lang='id'); fp = BytesIO(); tts.write_to_fp(fp); st.audio(fp, format='audio/mp3')
    except: pass

# --- 5. UI 呈現層 ---
st.markdown("""
<div class="header-container">
    <h1 class="main-title">Kadofah</h1>
    <div class="sub-title">第 3 課：豐收之歌</div>
    <div style="font-size: 12px; margin-top:10px; color:#8FBC8F;">Code-CRF v6.4 | Theme: Golden Harvest</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🌾 互動課文", 
    "👨‍🌾 核心單字", 
    "🧬 句型解析", 
    "⚔️ 實戰測驗"
])

with tab1:
    st.markdown("### // 文章閱讀")
    st.caption("👆 點擊單字可聽發音並查看翻譯")
    
    st.markdown("""<div style="background:#2E4631; padding:10px; border-left:4px solid #FFD700; border-radius:5px 5px 0 0;">""", unsafe_allow_html=True)
    components.html(get_html_card(STORY_DATA, type="full_amis_block"), height=400, scrolling=True)
    st.markdown("</div>", unsafe_allow_html=True)

    zh_content = "<br>".join([item['zh'] for item in STORY_DATA])
    st.markdown(f"""
    <div class="zh-translation-block">
        {zh_content}
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### // 單字與詞根")
    for v in VOCABULARY:
        components.html(get_html_card(v, type="word"), height=150)

with tab3:
    st.markdown("### // 語法結構分析")
    for s in SENTENCES:
        st.markdown("""<div style="background:#2E4631; padding:15px; border:1px dashed #556B2F; border-radius: 5px; margin-bottom:15px;">""", unsafe_allow_html=True)
        components.html(get_html_card(s, type="sentence"), height=160)
        st.markdown(f"""
        <div style="color:#FFF; font-size:16px; margin-bottom:10px; border-top:1px solid #556B2F; padding-top:10px;">{s['zh']}</div>
        <div style="color:#D2B48C; font-size:14px; line-height:1.8; border-top:1px dashed #556B2F; padding-top:5px;"><span style="color:#FFD700; font-family:Bitter; font-weight:bold;">ANALYSIS:</span> {s.get('note', '')}</div>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = generate_quiz()
        st.session_state.quiz_step = 0; st.session_state.quiz_score = 0
    
    if st.session_state.quiz_step < len(st.session_state.quiz_questions):
        q = st.session_state.quiz_questions[st.session_state.quiz_step]
        st.markdown(f"""<div class="quiz-card"><div style="margin-bottom:10px;"><span class="quiz-tag">{q['tag']}</span> <span style="color:#D2B48C;">Q{st.session_state.quiz_step + 1}</span></div><div style="font-size:18px; color:#FFF; margin-bottom:10px;">{q['text']}</div></div>""", unsafe_allow_html=True)
        if 'audio' in q: play_audio_backend(q['audio'])
        opts = q['options']; cols = st.columns(min(len(opts), 3))
        for i, opt in enumerate(opts):
            with cols[i % 3]:
                if st.button(opt, key=f"q_{st.session_state.quiz_step}_{i}"):
                    if opt.lower() == q['correct'].lower():
                        st.success("✅ 正確 (Correct)"); st.session_state.quiz_score += 1
                    else:
                        st.error(f"❌ 錯誤 - 正解: {q['correct']}"); 
                        if 'note' in q: st.info(q['note'])
                    time.sleep(1.5); st.session_state.quiz_step += 1; st.rerun()
    else:
        st.markdown(f"""<div style="text-align:center; padding:30px; border:4px solid #FFD700; border-radius:10px; background:#2E4631;"><h2 style="color:#FFD700; font-family:Bitter;">MISSION COMPLETE</h2><p style="font-size:20px;">得分: {st.session_state.quiz_score} / {len(st.session_state.quiz_questions)}</p></div>""", unsafe_allow_html=True)
        if st.button("🔄 重新挑戰 (Reboot)"): del st.session_state.quiz_questions; st.rerun()

st.markdown("---")
st.caption("Powered by Code-CRF v6.4 | Architecture: Chief Architect")
```
