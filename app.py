import streamlit as st
import requests
import base64
from PIL import Image
import io

# Page settings
st.set_page_config(page_title="કૃષિ રક્ષક AI", page_icon="🌱", layout="centered")

# School and Guide Details
st.markdown("<h2 style='text-align: center; color: #2e7d32;'>🌱 કૃષિ રક્ષક AI</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-top: -10px;'>શ્રી બી. પી. અગ્રવાલ હાઈસ્કૂલ, લીમડી</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>માર્ગદર્શક: શ્રી ધીરેન્દ્ર પરમાર | વિષય: AI દ્વારા બહેતર જીવન</p>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.camera_input("છોડ અથવા રોગિષ્ટ પાંદડાનો ફોટો પાડો")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="પાડેલો ફોટો", use_container_width=True)

    if st.button("રોગ અને દવા વિશે તપાસ કરો 🔍", use_container_width=True):
        with st.spinner("AI દ્વારા પાકની તપાસ થઈ રહી છે, કૃપા કરીને થોડી સેકન્ડ રાહ જુઓ..."):
            try:
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

                api_key = "AQ.Ab8RN6KyIJBA8YdaAbZ6GqZYVLYB29AqXab0OjicMmoGLiuJmw"
                
                # gemini-2.0-flash endpoint
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

                prompt_text = (
                    "તમે એક કૃષિ વૈજ્ઞાનિક છો. આ ફોટાનું વિશ્લેષણ કરી ખેડૂત માટે સરળ ગુજરાતીમાં મુદ્દાસર જણાવો: "
                    "૧. પાકનું નામ અને થયેલ રોગ. "
                    "૨. રોગના મુખ્ય લક્ષણો. "
                    "૩. ઉપચાર (દવાનું નામ, ૧૫ લિટર પંપમાં નાખવાનું ચોક્કસ માપ). "
                    "૪. દવા છાંટવાની પદ્ધતિ. "
                    "૫. કેટલા દિવસમાં રોગ મટશે."
                )

                payload = {
                    "contents": [{
                        "parts": [
                            {"text": prompt_text},
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": img_b64
                                }
                            }
                        ]
                    }]
                }

                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, headers=headers, json=payload)
                data = response.json()

                if "candidates" in data:
                    result_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("✅ તપાસ પૂર્ણ થઈ ગઈ છે!")
                    st.markdown("### 📋 રોગ અને ઉપચારની વિગત:")
                    st.write(result_text)

                    clean_text = (
                        result_text.replace('\n', ' ')
                        .replace('*', '')
                        .replace('#', '')
                        .replace('"', '')
                        .replace("'", "")
                    )

                    audio_html = f"""
                    <div style="margin-top: 20px;">
                        <button onclick="speakText()" style="background-color: #2e7d32; color: white; padding: 14px 20px; border: none; border-radius: 8px; font-size: 17px; cursor: pointer; width: 100%; font-weight: bold;">
                            🔊 ગુજરાતીમાં સાંભળો (Speak)
                        </button>
                    </div>
                    <script>
                    function speakText() {{
                        window.speechSynthesis.cancel();
                        var msg = new SpeechSynthesisUtterance("{clean_text}");
                        msg.lang = 'gu-IN';
                        msg.rate = 0.9;
                        window.speechSynthesis.speak(msg);
                    }}
                    </script>
                    """
                    st.components.v1.html(audio_html, height=90)
                else:
                    err_msg = data.get("error", {}).get("message", "API response error")
                    st.error(f"ભૂલ આવી: {err_msg}")

            except Exception as e:
                st.error(f"વિશ્લેષણ કરવામાં ભૂલ આવી: {e}")
                    
