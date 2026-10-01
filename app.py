import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page setting
st.set_page_config(page_title="કૃષિ રક્ષક AI", page_icon="🌱", layout="centered")

# Tamari sachi API Key
API_KEY = "AIzaSyDb5aHiqCWv5tFlg1HGl0lPdw1Y69sAavU"
genai.configure(api_key=API_KEY)

# School and Guide Name
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
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = """
                તમે એક અનુભવી કૃષિ વૈજ્ઞાનિક (Plant Doctor) છો.
                આ ફોટાનું નિરીક્ષણ કરી ખેડૂત મિત્ર માટે એકદમ સરળ અને શુદ્ધ ગુજરાતીમાં નીચે મુજબ જ મુદ્દાસર માહિતી આપો:
                1. પાકનું નામ અને થયેલ રોગ કે જીવાતનું નામ.
                2. રોગના મુખ્ય લક્ષણો.
                3. રાસાયણિક તથા દેશી/ઓર્ગેનિક ઉપચાર (દવાનું ચોક્કસ નામ અને 15 લિટર પંપમાં નાખવાની ચોક્કસ માત્રા - મિલી કે ગ્રામમાં).
                4. દવા છાંટવાની પદ્ધતિ અને યોગ્ય સમય (સવારે કે સાંજે).
                5. કેટલા દિવસમાં રોગ સંપૂર્ણ મટી જશે.
                ખેડૂત સહેલાઈથી સમજી શકે તેવી વ્યવહારુ ભાષા રાખવી.
                """
                response = model.generate_content([prompt, image])
                result_text = response.text

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

            except Exception as e:
                st.error(f"Error aavi: {e}")
                
