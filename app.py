import streamlit as st
import google-generativeai as genai
import re

# ڕێکخستنی لاپەڕە بۆ سەر مۆبایل
st.set_page_config(page_title="وەرگێڕی ژێرنووس", page_icon="🎬", layout="centered")

# ستایلی زمانی کوردی
st.markdown("""
    <style>
    body, div, h1, p, label, button {
        direction: RTL !important;
        text-align: right !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        width: 100%;
        background-color: #238636;
        color: white;
        padding: 12px;
        font-size: 18px;
    }
    </style>
    """, unsafe_with_html=True)

st.title("🎬 وەرگێڕی فایلی SRT بۆ کوردی")
st.write("فایلی SRT ئینگلیزی لۆد بکە بۆ وەرگێڕانی بێ سانسۆر.")

# وەرگرتنی کلیلی API
API_KEY = st.text_input("کلیلی Google AI Studio (API Key):", type="password")

uploaded_file = st.file_uploader("فایلی SRT هەڵبژێرە...", type=["srt"])

if uploaded_file is not None and API_KEY:
    srt_content = uploaded_file.read().decode("utf-8")
    
    if st.button("دەستپێکردنی وەرگێڕان 🚀"):
        genai.configure(api_key=API_KEY)
        
        # بەکارهێنانی وەشانی جێگیر بۆ ئەوەی تووشی کێشە نەبیت
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={"temperature": 0.2}
        )
        
        system_prompt = (
            "You are an expert subtitle translator. Your task is to translate this SRT file from English to Kurdish Sorani.\n"
            "STRICT RULES:\n"
            "1. NEVER modify or translate the timecodes or the subtitle numbers. Keep them EXACTLY as they are.\n"
            "2. Translate the text into natural Kurdish Sorani. Do NOT translate word-for-word.\n"
            "3. Do NOT censor any profanity, curse words, or mature language.\n"
            "4. Output ONLY the raw valid SRT content. No explanations, no markdown formatting."
        )
        
        prompt = f"{system_prompt}\n\nHere is the SRT file:\n\n{srt_content}"
        
        with st.spinner("خەریکی وەرگێڕانە... چاوەڕوان بە..."):
            try:
                response = model.generate_content(prompt)
                translated_text = response.text

                if translated_text.startswith("```"):
                    translated_text = re.sub(r"^
```[a-zA-Z]*\n", "", translated_text)
                    translated_text = re.sub(r"\n```$", "", translated_text)
                
                st.success("تەواو بوو! 🎉")
                
                output_filename = uploaded_file.name.replace(".srt", "_Kurdish.srt")
                
                st.download_button(
                    label="📥 دابەزاندنی فایلی کوردی",
                    data=translated_text,
                    file_name=output_filename,
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"هەڵەیەک ڕوویدا: {e}")

