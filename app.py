import streamlit as st
import requests
import base64

# Hugging Face API Model URL
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

# Function to generate image
def generate_image(prompt, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": prompt}
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.content  # Image bytes
    else:
        return None

# Streamlit UI
st.set_page_config(page_title="Text to Image Generator", layout="centered", initial_sidebar_state="expanded")

# Step 1: Ask for API Key
st.sidebar.title("🔑 Enter API Key")
api_key = st.sidebar.text_input("Create and Enter your Hugging Face API Key:", type="password")

st.sidebar.markdown(
    "[🔗 Get your API key here](https://huggingface.co/settings/tokens)",
    unsafe_allow_html=True
)

if api_key:
    # Step 2: Show the image generation interface only after API key is entered
    st.title("🖼️ Text to Image Converter")
    st.write("Enter a text prompt, and AI will generate an image for you!")

    # Step 3: Get user input and generate image
    prompt = st.text_area("Enter text prompt:", placeholder="e.g., A futuristic robot in a city")

    if st.button("Generate Image"):
        if not prompt:
            st.warning("⚠️ Please enter a text prompt!")
        else:
            st.write("⏳ Generating image... Please wait.")
            image_bytes = generate_image(prompt, api_key)

            if image_bytes:
                st.image(image_bytes, caption="Generated Image", use_column_width=True)

                # Convert image to a download link
                b64 = base64.b64encode(image_bytes).decode()
                href = f'<a href="data:image/png;base64,{b64}" download="generated-image.png">📥 Download Image</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.error("❌ Error generating image. Please check your API key and try again.")

else:
    st.warning("⚠️ Please enter your Hugging Face API Key in the sidebar to continue.")
