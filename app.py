import streamlit as st
import google.generativeai as genai
import re

# ڕێکخستنی لاپەڕە بۆ سەر مۆبایل
st.set_page_config(page_title="وەرگێڕی ژێرنووس کوردی", page_icon="🎬", layout="centered")

st.title("🎬 وەرگێڕی فایلی SRT بۆ کوردی")
st.write("فایلی SRT ئینگلیزی لۆد بکە و وەشانی مۆدێلەکە دیاری بکە بۆ وەرگێڕانی بێ سانسۆر بۆ زمانی کوردی سۆرانی.")

# ١. چوارچێوەی داخڵکردنی کلیلی API
API_KEY = st.text_input("کلیلی Google AI Studio (API Key):", type="password")

# ٢. دیاریکردنی ناوی مۆدێلەکە بە ئارەزووی خۆت
MODEL_VERSION = st.text_input("ناوی مۆدێلەکە دیاری بکە:", value="gemini-1.5-pro")

# ٣. شوێنی ئەپڵۆدکردنی فایلی SRT
uploaded_file = st.file_uploader("فایلی SRT ئینگلیزی هەڵبژێرە...", type=["srt"])

if uploaded_file is not None and API_KEY:
    # خوێندنەوەی ناوەڕۆکی فایلەکە
    srt_content = uploaded_file.read().decode("utf-8")
    
    if st.button("دەستپێکردنی وەرگێڕان 🚀"):
        # جێگیرکردنی کلیل بۆ سێرڤەری گووگڵ
        genai.configure(api_key=API_KEY)
        
        # دروستکردنی مۆدێل بەپێی ئەو ناوەی کە لە سەرەوە نووسیوتە
        model = genai.GenerativeModel(
            model_name=MODEL_VERSION,
            generation_config={
                "temperature": 0.2, # کەمترین ڕێژەی گۆڕانکاری بۆ ئەوەی کاتەکان (Timecodes) تێک نەچن
            }
        )
        
        # پرۆمپتی سەرەکی بۆ ڕێنمایی مۆدێلەکە بۆ زمان و نەهێشتنی سانسۆر
        system_prompt = (
            "You are an expert subtitle translator specializing in English to Kurdish Sorani translation.\n"
            "STRICT RULES:\n"
            "1. NEVER modify, delete, or translate the timecodes (e.g., 00:01:20,000 --> 00:01:23,100) or the subtitle numbers. Keep them EXACTLY as they are.\n"
            "2. Translate the text into natural, idiomatic, and culturally accurate Kurdish Sorani. Do NOT translate word-for-word. Focus on dialogue context.\n"
            "3. Do NOT censor any profanity, curse words, or mature language. Translate them accurately as they are used in the context.\n"
            "4. Output ONLY the raw valid SRT content. No explanations, no markdown formatting."
        )
        
        prompt = f"{system_prompt}\n\nHere is the SRT file to translate:\n\n{srt_content}"
        
        with st.spinner("مۆدێلەکە خەریکی کارکردنە... تکایە چاوەڕوان بە..."):
            try:
                response = model.generate_content(prompt)
                translated_text = response.text

                # پاککردنەوەی نیشانەکانی مارکداون (```srt) ئەگەر مۆدێلەکە گەڕاندبێتییەوە
                if translated_text.startswith("```"):
                    translated_text = re.sub(r"^```[a-zA-Z]*\n", "", translated_text)
                    translated_text = re.sub(r"\n```$", "", translated_text)
                
                st.success("وەرگێڕانەکە بە سەرکەوتوویی تەواو بوو! 🎉")
                
                # دروستکردنی ناوی فایلی نوێ
                output_filename = uploaded_file.name.replace(".srt", "_Kurdish.srt")
                
                # دوگمەی دابەزاندنی فایلەکە بۆ ناو Files ی ئایفۆن
                st.download_button(
                    label="📥 دابەزاندنی فایلی SRT کوردی",
                    data=translated_text,
                    file_name=output_filename,
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"هەڵەیەک ڕوویدا: {e}\n\nتێبینی: دڵنیا بەرەوە ناوی مۆدێلەکە یاخود API Key ەکەت ڕێک و دروستە.")
                
elif uploaded_file is not None and not API_KEY:
    st.warning("تکایە سەرەتا کلیلی API Key بنووسە.")

                
                

