import streamlit as st
import google.generativeai as genai
from PIL import Image

# સ્ક્રીન સેટિંગ્સ
st.set_page_config(page_title="કૃષિ રક્ષક AI", page_icon="🌱", layout="centered")

# શાળા અને તમારું નામ
st.markdown("<h2 style='text-align: center; color: #2e7d32;'>🌱 કૃષિ રક્ષક AI</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>શ્રી બી. પી. અગ્રવાલ હાઈસ્કૂલ, લીમડી</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>માર્ગદર્શક: શ્રી ધીરેન્દ્ર પરમાર | AI દ્વારા બહેતર જીવન</p>", unsafe_allow_html=True)
st.write("---")

# API Key માટેનું બોક્સ
api_key = st.text_input("Gemini API Key અહીં નાખો:", type="password")

# કેમેરા બટન
uploaded_file = st.camera_input("છોડ અથવા રોગિષ્ટ પાંદડાનો ફોટો પાડો")

if uploaded_file and api_key:
    genai.configure(api_key=api_key)
    image = Image.open(uploaded_file)
    st.image(image, caption="તમે લીધેલો ફોટો", use_column_width=True)

    if st.button("રોગ અને દવા વિશે તપાસ કરો 🔍"):
        with st.spinner("AI દ્વારા પાકની તપાસ થઈ રહી છે..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = """
                તમે એક ખેતીવાડી નિષ્ણાત (Agri Expert) છો.
                આ ફોટાનું નિરીક્ષણ કરી ખેડૂત માટે સરળ ગુજરાતીમાં નીચે મુજબ જ માહિતી આપો:
                1. પાકનું નામ અને થયેલ રોગ કે જીવાતનું નામ.
                2. રોગના મુખ્ય લક્ષણો.
                3. રાસાયણિક તથા દેશી ઉપચાર (દવાનું ચોક્કસ નામ અને 15 લિટર પંપમાં નાખવાની માત્રા/પ્રમાણ).
                4. દવા છાંટવાની રીત અને સમય.
                5. કેટલા દિવસમાં રોગ મટી જશે.
                ખેડૂત સમજી શકે તેવી તળપદી/સરળ ભાષા રાખવી.
                """
                response = model.generate_content([prompt, image])
                result_text = response.text

                st.success("તપાસ પૂર્ણ થઈ ગઈ છે!")
                st.markdown("### 📋 રોગ અને ઉપચારની વિગત:")
                st.write(result_text)

                # અવાજ સંભળાવવા માટેનું સ્પીકર બટન
                clean_text = result_text.replace('\n', ' ').replace('*', '').replace('#', '').replace('"', '')
                audio_html = f"""
                <button onclick="speakText()" style="background-color: #2e7d32; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; width: 100%;">
                    🔊 ગુજરાતીમાં સાંભળો (Speak)
                </button>
                <script>
                function speakText() {{
                    var msg = new SpeechSynthesisUtterance("{clean_text}");
                    msg.lang = 'gu-IN';
                    window.speechSynthesis.speak(msg);
                }}
                </script>
                """
                st.components.v1.html(audio_html, height=80)

            except Exception:
                st.error("માહિતી મેળવવામાં ભૂલ થઈ. કૃપા કરીને API Key સાચી છે કે નહીં તે ચકાસો.")
              
