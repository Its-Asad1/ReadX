streamlit as st
import google.generativeai as genai
from PIL import Image as Im

st.set_page_config(page_title="ReadX AI", page_icon="📖", layout="centered")

# Camera UI ko bada aur clean banane ke liye CSS
st.markdown("""
    <style>
    /* Camera container ko tall/vertical banana */
    [data-testid="stCameraInput"] > div:first-child {
        aspect-ratio: 9 / 16 !important;
        height: 60vh !important; /* Screen ki height ke mutabiq adjust hoga */
        max-height: 520px !important;
        max-width: 100% !important;
        overflow: hidden !important;
        border-radius: 16px;
        border: 2px solid #333;
        margin: 0 auto;
    }
    
    /* Video Stream fitting */
    [data-testid="stCameraInput"] video {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
    }
    
    /* "Take Photo" Button Styling */
    [data-testid="stCameraInput"] button {
        width: 100% !important;
        margin: 12px auto 0 auto !important;
        padding: 16px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        background-color: #FF4B4B !important;
        color: white !important;
        border: none !important;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Session state initialize karo
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None
if "result" not in st.session_state:
    st.session_state.result = None

st.title("📖 ReadX AI")
st.caption("Let AI help you read & learn faster")

def resize_image(image, max_size=1024):
    """Image ko chota karo taake upload aur processing fast ho"""
    image.thumbnail((max_size, max_size))
    return image

def analyze_page(image):
    prompt = """Analyze this book page and give:
    1. **Core Idea**: 3-4 simple sentences on what's happening/being said.
    2. **Main Lesson**: 1-2 lines - the key takeaway.
    3. **Action Points**: Practical tips if any exist, else say "No direct action points."
    Use simple, plain English."""

    model = genai.GenerativeModel("gemini-3.5-flash-lite")
    response = model.generate_content([prompt, image])
    return response.text

# Agar result nahi hai, camera dikhao
if st.session_state.result is None:
    photo = st.camera_input("📷 Book page ki photo lo", label_visibility="collapsed")

    if photo is not None:
        image = Im.open(photo)
        image = resize_image(image)
        st.session_state.captured_image = image

        with st.spinner("Padh raha hoon... ⏳"):
            st.session_state.result = analyze_page(image)
        st.rerun()

# Agar result hai, wo dikhao + Next button
else:
    st.image(st.session_state.captured_image, use_container_width=True)
    st.markdown("### 📝 Summary")
    st.write(st.session_state.result)

    if st.button("➡️ Next Page", use_container_width=True, type="primary"):
        st.session_state.captured_image = None
        st.session_state.result = None
        st.rerun()
