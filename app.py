import os
import subprocess
import streamlit as st
import imageio_ffmpeg

# Setup page configuration
st.set_page_config(
    page_title="Cinematic Video Audio Replacer",
    page_icon="✨",
    layout="centered"
)

# Custom CSS with High-Visibility Download Button & Glassmorphism UI
st.markdown("""
    <style>
    /* Global Styling with Visible Cinematic Background Image */
    .stApp {
        background: linear-gradient(rgba(3, 7, 18, 0.65), rgba(3, 7, 18, 0.75)), 
                    url('https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #f9fafb;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Hero Banner Styling */
    .hero-container {
        text-align: center;
        padding: 2.5rem 1rem;
        background: rgba(11, 15, 25, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6);
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(to right, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        color: #d1d5db;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* Transparent Glassmorphism Cards */
    .card {
        background: rgba(11, 15, 25, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .card:hover {
        border-color: #818cf8;
    }
    .card-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Custom Gradient Buttons (Process & Download both) */
    .stButton>button, div.stDownloadButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100% !important);
        color: #ffffff !important;
        border: none !important;
        padding: 16px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4) !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover, div.stDownloadButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(168, 85, 247, 0.6) !important;
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important;
        color: #ffffff !important;
    }
    
    /* File Uploader Clean-up */
    div[data-testid="stFileUploader"] {
        background-color: rgba(3, 7, 18, 0.4);
        border: 2px dashed #6b7280;
        border-radius: 12px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Setup ffmpeg path
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_exe)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# Header / Hero Section
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">✨ Pro Video Audio Replacer</div>
        <div class="hero-subtitle">Transform your videos instantly with lightning-fast rendering & live preview.</div>
    </div>
""", unsafe_allow_html=True)

# Layout Columns with Card Design
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎥 Upload Video File</div>', unsafe_allow_html=True)
    video_file = st.file_uploader("Video", type=[".mp4", ".mov", ".mkv", ".avi"], key="video", label_visibility="collapsed")
    if video_file is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        st.video(video_file)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🎵 Upload Audio File</div>', unsafe_allow_html=True)
    audio_file = st.file_uploader("Audio", type=[".mp3", ".wav", ".m4a", ".aac"], key="audio", label_visibility="collapsed")
    if audio_file is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        st.audio(audio_file)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Process Button & Action Logic
if st.button("🚀 Process & Generate Video Now"):
    if video_file is not None and audio_file is not None:
        with st.spinner("⚡ Rendering your cinematic video with FFmpeg... Please hold on..."):
            video_path = "temp_video.mp4"
            audio_path = "temp_audio.mp3"
            
            with open(video_path, "wb") as f:
                f.write(video_file.read())
            with open(audio_path, "wb") as f:
                f.write(audio_file.read())
                
            output_path = "PRO_output_video.mp4"

            cmd = [
                ffmpeg_exe, "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-shortest",
                output_path
            ]

            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                st.success("🎉 Success! Your video has been processed successfully.")
                
                st.markdown('<div class="card" style="margin-top: 20px;">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">📺 Final Output Preview</div>', unsafe_allow_html=True)
                st.video(output_path)
                
                st.markdown("<br>", unsafe_allow_html=True)
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download High-Quality Output Video",
                        data=file,
                        file_name="Cinematic_Output.mp4",
                        mime="video/mp4"
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Error during processing: {e}")
    else:
        st.warning("⚠️ Doyakore prothom ekti video ebong ekti audio file upload korun!")
