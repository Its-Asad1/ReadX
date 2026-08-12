import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Setup
# genai.configure(api_key="PASTE_YOUR_COPIED_API_KEY_HERE")

st.set_page_config(page_title="ReadX Mobile Companion", page_icon="📱", layout="centered")

st.title("📱 ReadX AI Companion")

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0  # To programmatically open the uploader again

current_page = len(st.session_state.history) + 1

# Mobile Sidebar Memory
with st.sidebar:
    st.header("📚 Book Memory")
    st.write(f"Pages Analyzed: {len(st.session_state.history)}")
    if st.button("🗑️ Reset Memory"):
        st.session_state.history = []
        st.session_state.uploader_key += 1
        st.rerun()

# --- Main App Logic ---

# We only show uploader if we don't have a new summary on screen
has_just_scanned = False
if len(st.session_state.history) > 0 and st.session_state.get('last_summary_seen', False) is False:
     has_just_scanned = True

# 2. File Uploader configured to capture from Camera on Mobile
if not has_just_scanned:
    st.subheader(f"📸 Step 1: Scan Page #{current_page}")
    st.caption("Click below to open your phone's native camera.")
    
    # The 'accept' attribute helps suggest opening the camera
    photo_buffer = st.file_uploader(
        "Capture Page Photo",
        type=["jpg", "jpeg", "png"],
        key=f"uploader_{st.session_state.uploader_key}",
        accept_multiple_files=False,
    )

    if photo_buffer:
        image = Image.open(photo_buffer)
        
        # Immediate Analyze (Auto-Action upon upload)
        with st.spinner("🚀 AI analyzing the page..."):
             # Previous Context Build
            context_prompt = ""
            if len(st.session_state.history) > 0:
                context_prompt = "PREVIOUS PAGES CONTEXT:\n"
                for idx, prev in enumerate(st.session_state.history, 1):
                    context_prompt += f"--- Page {idx} ---\n{prev}\n\n"

            prompt = f"""
            You are a book reading assistant.
            {context_prompt}
            Analyze this image for CURRENT Page #{current_page}:
            "Analyze this book page and give:
    1. **Core Idea**: 3-4 simple sentences on what's happening/being said.
    2. **Main Lesson**: 1-2 lines - the key takeaway.
    3. **Action Points**: Practical tips if any exist, else say "No direct action points."
    Use simple, plain English.
            """
            
            # API Call (Uncomment when you have key)
            # model = genai.GenerativeModel("gemini-1.5-flash")
            # response = model.generate_content([prompt, image])
            # summary_text = response.text
            
            # Placeholder summary (Comment when API key is set)
            summary_text = f"Sample summary for Page {current_page}. Gemini analyzed the photo taken from your phone camera perfectly."

            # Save to Memory
            st.session_state.history.append(summary_text)
            st.session_state.last_summary_seen = False # Mark as just scanned
            st.rerun()

# 3. Display the New Summary AND the 'Next Page' Button
else:
    latest_page_idx = len(st.session_state.history)
    latest_page_num = latest_page_idx
    
    st.success(f"Page #{latest_page_num} Breakdown (New)")
    
    # Custom styling for summary card
    st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; margin-bottom:20px;">
            {st.session_state.history[latest_page_idx - 1]}
        </div>
    """, unsafe_allow_html=True)
    
    # THE CRUCIAL PART: The "NEXT PAGE" Button
    st.subheader(f"🔜 Step 2: Next Page Cycle")
    
    if st.button("➡️ Scan Page #{}" .format(latest_page_num + 1), type="primary", use_container_width=True):
        st.session_state.uploader_key += 1 # Reset the uploader
        st.session_state.last_summary_seen = True # Mark summary as acknowledged
        st.rerun() # Forces rerendering and reopens uploader

# --- Display History Accordion ---
if len(st.session_state.history) > 1:
    st.markdown("---")
    st.header("📄 Reading Trail")
    
    # Show history but hide the latest one as it's shown above
    for idx, page_summary in enumerate(st.session_state.history[:-1], 1):
        with st.expander(f"Page {idx} Breakdown"):
            st.markdown(page_summary)
