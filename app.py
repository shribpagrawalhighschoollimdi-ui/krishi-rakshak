import streamlit as st
from PIL import Image

# સ્ક્રીન સેટિંગ્સ
st.set_page_config(page_title="કૃષિ રક્ષક AI", page_icon="🌱", layout="centered")

# શાળા અને શિક્ષકનું નામ (હેડર)
st.markdown("<h2 style='text-align: center; color: #2e7d32;'>🌱 કૃષિ રક્ષક AI</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; margin-top: -10px;'>શ્રી બી. પી. અગ્રવાલ હાઈસ્કૂલ, લીમડી</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>માર્ગદર્શક: શ્રી ધીરેન્દ્ર પરમાર | વિષય: AI દ્વારા બહેતર જીવન</p>", unsafe_allow_html=True)
st.write("---")

uploaded_file = st.camera_input("છોડ અથવા રોગિષ્ટ પાંદડાનો ફોટો પાડો")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="પાડેલો ફોટો", use_container_width=True)

    if st.button("રોગ અને દવા વિશે તપાસ કરો 🔍", use_container_width=True):
        with st.spinner("કમ્પ્યુટર વિઝન AI દ્વારા પાનની ચકાસણી થઈ રહી છે..."):
            try:
                # લોકલ ઈમેજ પિક્સેલ વિશ્લેષણ (Computer Vision Analysis)
                small_img = image.resize((50, 50))
                pixels = list(small_img.getdata())
                
                yellowish = 0
                dark_spots = 0
                whitish = 0
                healthy_green = 0
                
                for r, g, b in pixels:
                    # પીળાશ પડતાં પિક્સેલ (Chlorosis / Deficiencies)
                    if r > 130 and g > 130 and b < 90:
                        yellowish += 1
                    # કાળા કે ઘેરા ડાઘા (Necrosis / Spots / Blight)
                    elif r < 60 and g < 60 and b < 60:
                        dark_spots += 1
                    # સફેદ છારો (Powdery Mildew)
                    elif r > 180 and g > 180 and b > 180:
                        whitish += 1
                    # તંદુરસ્ત લીલો ભાગ
                    elif g > r and g > b:
                        healthy_green += 1

                # પરિણામ નક્કી કરવાની સિસ્ટમ
                if dark_spots > 250:
                    disease_name = "કાળતરા / અંગારીયો / પાનના ટપકાં (Blight & Leaf Spot)"
                    symptoms = "પાંદડા પર ભૂખરા-કાળા અનિયમિત ટપકાં અને કિનારીઓ બળી જવી."
                    medicine = "મેન્કોઝેબ ૭૫% WP ૩૫ થી ૪૦ ગ્રામ પ્રતિ ૧૫ લિટર પંપ અથવા કોપર ઓક્સીક્લોરાઇડ ૪૫ ગ્રામ."
                    desi = "ગૌમૂત્ર (૫૦૦ મિલી) + ખાટી છાશ (૧ લિટર) ૧૫ લિટર પાણીમાં ભેળવી છાંટવું."
                    duration = "૭ થી ૧૦ દિવસમાં રોગ આગળ વધતો અટકી જશે."
                elif whitish > 300:
                    disease_name = "ભૂકી છારો / સફેદ છારો (Powdery Mildew)"
                    symptoms = "પાંદડાની ઉપલી સપાટી પર સફેદ પાવડર જેવો છારો જામવો."
                    medicine = "હેક્ઝાકોનાઝોલ ૫% EC ૧૫ મિલી અથવા સલ્ફર ૮૦% WP ૩૦ ગ્રામ પ્રતિ પંપ."
                    desi = "૧૫ લિટર પાણીમાં ૧ લિટર તાજી છાશ ભેળવી તડકાના સમયે છાંટવી."
                    duration = "૫ થી ૭ દિવસમાં પાન ચોખ્ખા થઈ જશે."
                elif yellowish > 200:
                    disease_name = "પાનની પીળાશ / પોષકતત્વોની ખામી / ચૂસિયા જીવાત"
                    symptoms = "પાંદડા પીળા પડી જવા, નસો લીલી રહેવી અથવા પાન સંકોચાઈ જવા."
                    medicine = "ઇમિડાક્લોપ્રિડ ૧૭.૮% SL ૫ મિલી પ્રતિ પંપ અથવા ૧૯-૧૯-૧૯ ખાતર ૭૫ ગ્રામ પંપમાં ઓગાળી છાંટવું."
                    desi = "લીમડાનું તેલ (Neem Oil) ૫૦ મિલી + થોડું સાબુનું પાણી મિક્સ કરી છાંટવું."
                    duration = "૪ થી ૬ દિવસમાં પાન ફરી લીલાછમ થવા લાગશે."
                else:
                    disease_name = "સામાન્ય પાન સુકારો અથવા તડકાની અસર (Sun Scald / Minor Wilt)"
                    symptoms = "પાંદડાના છેડા કરમાઈ જવા અને વિકાસ ધીમો પડવો."
                    medicine = "કાર્બેન્ડાઝીમ ૧૨% + મેન્કોઝેબ ૬૩% WP (સાફ પાવડર) ૩૦ ગ્રામ પ્રતિ પંપ."
                    desi = "જીવામૃત ૨૦૦ મિલી પ્રતિ પંપ અથવા ટ્રાઈકોડર્મા ૫૦ ગ્રામ જમીનમાં આપવું."
                    duration = "૫ થી ૮ દિવસમાં સુધારો દેખાશે."

                result_text = f"""
૧. સંભવિત રોગનું નામ: {disease_name}
૨. રોગના મુખ્ય લક્ષણો: {symptoms}
૩. રાસાયણિક ઉપચાર: {medicine}
૪. દેશી / પ્રાકૃતિક ઉપાય: {desi}
૫. કેટલા દિવસમાં મટશે: {duration}
(નોંધ: દવાનો છંટકાવ હંમેશા સવારે ૮ થી ૧૦ અથવા સાંજે ૪ વાગ્યા પછી કરવો.)
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

                # ગુજરાતી અવાજ માટે સ્પીકર બટન
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
                st.error(f"ચકાસણીમાં ખામી આવી: {e}")
                
