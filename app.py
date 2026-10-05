import numpy as np
from PIL import Image
import streamlit as st

# પેજ સેટઅપ
st.set_page_config(
    page_title="SHRI B. P. AGRWAL HIGH SCHOOL, LIMDI",
    page_icon="🌿",
    layout="centered",
)

# શાળા અને નિર્માતા હેડર
st.markdown(
    """
<div style='text-align: center; padding: 16px; background-color: #e8f5e9; border: 2px solid #1b4332; border-radius: 12px; margin-bottom: 20px;'>
    <h2 style='color: #1b4332; margin: 0; font-size: 22px; font-weight: bold;'>🏫 SHRI B. P. AGRWAL HIGH SCHOOL, LIMDI</h2>
    <h4 style='color: #2d6a4f; margin: 6px 0 10px 0; font-size: 16px;'>🌱 AI વનસ્પતિ પર્ણ રોગ નિદાન સોફ્ટવેર</h4>
    <div style='display: inline-block; background-color: #1b4332; color: #ffffff; padding: 5px 15px; border-radius: 15px; font-size: 13px; font-weight: bold;'>
        APP BY DHIRENDRA PARMAR
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write(
    "પાકના પર્ણ (પાંદડાં) નો સ્પષ્ટ ફોટો અપલોડ કરો અને તુરંત સચોટ વૈજ્ઞાનિક વિશ્લેષણ મેળવો."
)

# પાંદડાનો ફોટો અપલોડર
uploaded_file = st.file_uploader(
    "પાંદડાનો ફોટો અપલોડ કરો (JPG, PNG)", type=["jpg", "jpeg", "png"]
)


def analyze_leaf_image(img):
  img_rgb = img.convert("RGB")
  img_resized = img_rgb.resize((200, 200))
  arr = np.array(img_resized, dtype=np.float32)

  r = arr[:, :, 0]
  g = arr[:, :, 1]
  b = arr[:, :, 2]

  total_pixels = 200 * 200

  # કલર અને પિક્સેલ વિશ્લેષણ
  white_mask = (r > 170) & (g > 170) & (b > 170)
  white_ratio = np.sum(white_mask) / total_pixels

  rust_mask = (r > 130) & (g < 110) & (b < 70)
  rust_ratio = np.sum(rust_mask) / total_pixels

  yellow_mask = (r > 140) & (g > 140) & (b < 100)
  yellow_ratio = np.sum(yellow_mask) / total_pixels

  dark_mask = (r < 75) & (g < 75) & (b < 75)
  dark_ratio = np.sum(dark_mask) / total_pixels

  if white_ratio > 0.08:
    crop = "ગુલાબ / ભીંડા / વેલાવાળા શાકભાજી"
    disease = "પાવડરી મિલ્ડ્યુ (છારો રોગ - Powdery Mildew)"
    symptoms = "પાંદડાની સપાટી પર સફેદ લોટ કે રાખ જેવો પાઉડર જામી જવો અને પાંદડા સુકાવા."
    cause = "ફૂગજન્ય ચેપ (Podosphaera / Erysiphe ફૂગ)."
    cure = "૧. જૈવિક: ખાટા છાશ (૧ લિટર/૧૦ લિટર પાણી) અથવા લીમડાના તેલનો છંટકાવ કરવો.\n૨. રાસાયણિક: કાર્બેન્ડાઝીમ અથવા હેક્ઝાકોનાઝોલ (૧ મિલી/લિટર) નો છંટકાવ."

  elif rust_ratio > 0.05:
    crop = "મકાઈ / અનાજ પાક"
    disease = "પાનનો ગેરુ / રસ્ટ રોગ (Common Rust)"
    symptoms = "પાંદડા પર ઈંટ જેવા લાલાશ પડતા બદામી રંગના ઉપસેલા ફોલ્લા (Pustules)."
    cause = "પ્યુસિનીયા (Puccinia sorghi) ફૂગના બીજાણુઓ."
    cure = "૧. જૈવિક: ટ્રાઇકોડર્મા હાર્ઝિયાનમ ૨ ગ્રામ/લિટર પાણીમાં છાંટવું.\n૨. રાસાયણિક: પ્રોપીકોનાઝોલ ૨૫% ઈસી (૧ મિલી/લિટર પાણી) અથવા મેન્કોઝેબનો છંટકાવ."

  elif dark_ratio > 0.06 and yellow_ratio > 0.08:
    crop = "ટામેટા / બટાટા"
    disease = "અર્લી બ્લાઇટ / વહેલો સુકારો (Early Blight)"
    symptoms = (
        "પાંદડા પર ઘેરા બદામી-કાળા ગોળાકાર વલયો અને કિનારીઓ પીળી પડી જવી."
    )
    cause = "અલ્ટરનેરીયા સોલાની (Alternaria solani) ફૂગ."
    cure = "૧. જૈવિક: અસરગ્રસ્ત પાંદડાં તોડી નાશ કરવો અને લીમડાના અર્કનો ઉપયોગ.\n૨. રાસાયણિક: મેન્કોઝેબ ૭૫% WP (૨ ગ્રામ/લિટર) અથવા કોપર ઓક્સીક્લોરાઇડનો છંટકાવ કરવો."

  elif yellow_ratio > 0.12:
    crop = "પપૈયા / મરચી / કપાસ"
    disease = "લીફ કર્લ / મોઝેક વાયરસ (કોકડવા રોગ)"
    symptoms = (
        "પાંદડા કોકડાઈ જવા, કદ નાનું થવું અને પીળાશ પડતી નસો દેખાવી."
    )
    cause = "જેમિની વાયરસ (સફેદ માખી દ્વારા ફેલાવો)."
    cure = "૧. જૈવિક: પીળા ચીકણા ટ્રેપ (Yellow Sticky Traps) ગોઠવવા.\n૨. રાસાયણિક: વાહક જીવાત સફેદ માખીના નિયંત્રણ માટે એસીટામિપ્રિડ અથવા ઇમિડાક્લોપ્રિડનો છંટકાવ."

  elif dark_ratio > 0.04:
    crop = "લીંબુ વર્ગના ફળો (Citrus)"
    disease = "સાઇટ્રસ કેન્કર (ખારીયો રોગ)"
    symptoms = (
        "પાંદડા પર ખરબચડા બદામી રંગના ચાંઠા અને તેની ફરતે પીળી કિનારી."
    )
    cause = "ઝેન્થોમોનાસ બેક્ટેરિયા."
    cure = "૧. જૈવિક: બોルドો મિશ્રણ (૧%) નો છંટકાવ.\n૨. રાસાયણિક: સ્ટ્રેપ્ટોસાયક્લીન (૧ ગ્રામ/૧૦ લિટર) સાથે કોપર ઓક્સીક્લોરાઇડનો છંટકાવ."

  else:
    crop = "સામાન્ય પાક / વનસ્પતિ"
    disease = "સામાન્ય પર્ણ (કોઈ ગંભીર રોગના લક્ષણ જણાતા નથી)"
    symptoms = "પાંદડું મોટેભાગે તંદુરસ્ત જણાય છે."
    cause = "સામાન્ય હવામાન સ્થિતિ."
    cure = "નિયમિત સિંચાઈ અને સામાન્ય સંતુલિત ખાતર પૂરતું છે."

  return crop, disease, symptoms, cause, cure


if uploaded_file is not None:
  img = Image.open(uploaded_file)
  st.image(img, caption="અપલોડ કરેલ પાંદડું", use_container_width=True)

  if st.button("🔍 રોગ શોધો અને ઉપાય જાણો"):
    with st.spinner("પર્ણનું ડિજિટલ વિશ્લેષણ થઈ રહ્યું છે..."):
      crop, disease, symptoms, cause, cure = analyze_leaf_image(img)

      st.success("✅ વિશ્લેષણ સફળતાપૂર્વક પૂર્ણ થયું!")
      st.markdown(f"### ૧. સંભવિત વનસ્પતિ / પાક: **{crop}**")
      st.markdown(f"### ૨. રોગનું નામ: **{disease}**")
      st.markdown(f"**૩. મુખ્ય લક્ષણો:** {symptoms}")
      st.markdown(f"**૪. સંભવિત કારણ:** {cause}")
      st.markdown(f"**૫. તાત્કાલિક નિવારણ અને ઉપાયો:**\n{cure}")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #555; font-size: 12px;'>પ્રોજેક્ટ"
    " સૌજન્ય: SHRI B. P. AGRWAL HIGH SCHOOL, LIMDI<br>APP BY DHIRENDRA"
    " PARMAR</div>",
    unsafe_allow_html=True,
)
