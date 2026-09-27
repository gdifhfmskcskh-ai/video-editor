import os
import subprocess
import streamlit as st
import imageio_ffmpeg

# Setup page configuration for professional look
st.set_page_config(
    page_title="Pro Video Audio Replacer",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Modern Sleek UI
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    h1 {
        font-family: 'Segoe UI', sans-serif;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    .stFileUploader {
        background: rgba(30, 41, 59, 0.7);
        border: 2px dashed #334155;
        border-radius: 12px;
        padding: 15px;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 12px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.6);
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# Setup ffmpeg path
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_exe)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# Header Section
st.markdown("<h1>🎬 Pro Video Audio Replacer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Seamlessly replace background audio in your videos with lightning-fast processing.</p>", unsafe_allow_html=True)

# Layout Columns for File Uploaders
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("### 🎥 Video File")
    video_file = st.file_uploader("Upload Video", type=[".mp4", ".mov", ".mkv", ".avi"], key="video")

with col2:
    st.markdown("### 🎵 Audio File")
    audio_file = st.file_uploader("Upload Audio", type=[".mp3", ".wav", ".m4a", ".aac"], key="audio")

st.markdown("<br>", unsafe_allow_html=True)

# Process Button & Action Logic
if st.button("🚀 Process & Replace Audio Now"):
    if video_file is not None and audio_file is not None:
        with st.spinner("⚡ Processing video files with FFmpeg... Please wait..."):
            # Save uploaded files temporarily
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
                st.success("✨ Success! Your video has been processed successfully.")
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Final Output Video",
                        data=file,
                        file_name="Processed_Video.mp4",
                        mime="video/mp4"
                    )
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Error during processing: {e}")
    else:
        st.warning("⚠️ Please upload both a video file and an audio file to proceed.")
