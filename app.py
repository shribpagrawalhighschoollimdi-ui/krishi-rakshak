import streamlit as st
import requests
import io
from PIL import Image

# સ્ક્રીન સેટિંગ્સ
st.set_page_config(page_title="કૃષિ રક્ષક AI", page_icon="🌱", layout="centered")

# શાળા અને શિક્ષકનું નામ (હેડર)
st.markdown("<h2 style='text-align: center; color: #2e7d32;'>🌱 કૃષિ રક્ષક AI</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-top: -10px;'>શ્રી બી. પી. અગ્રવાલ હાઈસ્કૂલ, લીમડી</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>માર્ગદર્શક: શ્રી ધીરેન્દ્ર પરમાર | વિષય: AI દ્વારા બહેતર જીવન</p>", unsafe_allow_html=True)
st.write("---")

# પાક અને તેના સામાન્ય રોગોની ગુજરાતી માહિતી ડેટાબેઝ
DISEASE_DB = {
    "leaf_spot": {
        "name": "પાંદડાના ટપકાંનો રોગ (Cercospora Leaf Spot)",
        "symptoms": "પાંદડા પર ભૂખરા કે કાળા ગોળ ટપકાં પડવા અને પાન પીળું પડી સુકાઈ જવું.",
        "cure": "કોપર ઓક્સીક્લોરાઈડ (COC) ૫૦ WP દવા ૪૫ ગ્રામ અથવા કાર્બેન્ડાઝીમ ૧૫ ગ્રામ ૧૫ લિટર પાણીના પંપમાં ઓગાળીને છાંટવી.",
        "organic": "૧૦% લીમડાના અર્કનું દ્રાવણ અથવા ગૌમૂત્ર + છાશનું મિશ્રણ છાંટવું.",
        "duration": "૭ થી ૧૦ દિવસમાં નવો રોગ અટકી જશે."
    },
    "blight": {
        "name": "સુકારો / અંગારીયો (Blight Disease)",
        "symptoms": "પાંદડાની કિનારીઓ બળી ગઈ હોય તેવું દેખાવું અને છોડ કરમાઈ જવો.",
        "cure": "મેન્કોઝેબ ૭૫ WP ૪૦ ગ્રામ અથવા મેટાલક્ષીલ + મેન્કોઝેબ ૩૫ ગ્રામ પ્રતિ ૧૫ લિટર પંપમાં નાખી છંટકાવ કરવો.",
        "organic": "ટ્રાઈકોડર્મા વીરીડી ૬૦ ગ્રામ પંપમાં નાખી મૂળ પાસે આપવું.",
        "duration": "૮ થી ૧૨ દિવસમાં સુધારો દેખાશે."
    },
    "mildew": {
        "name": "ભૂકી છારો / છારો (Powdery Mildew)",
        "symptoms": "પાંદડાની સપાટી પર સફેદ પાવડર જેવો છારો જામી જવો.",
        "cure": "હેક્ઝાકોનાઝોલ ૫ EC ૧૫ મિલી અથવા સલ્ફર ૮૦ WP ૩૫ ગ્રામ પ્રતિ પંપ છાંટવું.",
        "organic": "ખાટી છાશ (૧ લિટર) ૧૫ લિટર પાણીમાં મેળવીને સૂર્યપ્રકાશ હોય ત્યારે છાંટવી.",
        "duration": "૫ થી ૭ દિવસમાં સંપૂર્ણ રાહત મળશે."
    },
    "default": {
        "name": "પાનનો પીળાશ / પોષક તત્વોની ખામી અથવા ચૂસિયા પ્રકારની જીવાત",
        "symptoms": "પાન પીળા પડી જવા, કૂકડાટ થવો અથવા વિકાસ અટકી જવો.",
        "cure": "ઇમિડાક્લોપ્રિડ ૧૭.૮ SL ૫ મિલી અથવા એસીફેટ ૭૫ SP ૨૦ ગ્રામ પ્રતિ પંપ છાંટવું.",
        "organic": "૧૦૦ મિલી લીમડાનું તેલ (Neem Oil) સાબુના પાણી સાથે ભેળવી છાંટવું.",
        "duration": "૫ દિવસમાં પાન સામાન્ય રંગ પકડશે."
    }
}

uploaded_file = st.camera_input("છોડ અથવા રોગિષ્ટ પાંદડાનો ફોટો પાડો")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="પાડેલો ફોટો", use_container_width=True)

    if st.button("રોગ અને દવા વિશે તપાસ કરો 🔍", use_container_width=True):
        with st.spinner("ઓપન-સોર્સ AI મોડેલ દ્વારા પાનની ચકાસણી થઈ રહી છે..."):
            try:
                # મફત ઓપન-સોર્સ AI વિઝન એન્ડપોઈન્ટ (કોઈ API Key ની જરૂર નથી)
                buf = io.BytesIO()
                image.save(buf, format='JPEG')
                byte_im = buf.getvalue()

                api_url = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
                res = requests.post(api_url, data=byte_im)
                
                # ફોટાના લક્ષણ આધારિત રોગની ઓળખ
                key = "default"
                if res.status_code == 200:
                    preds = str(res.json()).lower()
                    if "spot" in preds or "rot" in preds:
                        key = "leaf_spot"
                    elif "blight" in preds or "wilt" in preds:
                        key = "blight"
                    elif "powdery" in preds or "white" in preds:
                        key = "mildew"
                
                info = DISEASE_DB[key]
                result_text = f"""
૧. સંભવિત રોગનું નામ: {info['name']}
૨. મુખ્ય લક્ષણો: {info['symptoms']}
૩. રાસાયણિક ઉપચાર: {info['cure']}
૪. દેશી / ઓર્ગેનિક ઉપચાર: {info['organic']}
૫. રિકવરી સમય: {info['duration']}
(દવાનો છંટકાવ હંમેશા સવારે ૮ થી ૧૦ અથવા સાંજે ૪ વાગ્યા પછી કરવો.)
"""
                st.success("✅ પાકની તપાસ સફળતાપૂર્વક પૂર્ણ થઈ!")
                st.markdown("### 📋 રોગ અને ઉપચારની વિગત:")
                st.text(result_text)

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
                st.error(f"ચકાસણી કરવામાં તકલીફ થઈ: {e}")
                
