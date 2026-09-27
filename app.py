import os
import subprocess
import streamlit as st
import imageio_ffmpeg

# Setup page configuration
st.set_page_config(
    page_title="Pro Video Audio Replacer",
    page_icon="🎬",
    layout="centered"
)

# Custom CSS for Clean, High-Contrast Professional UI
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #ffffff;
    }
    h1 {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 800;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    .main-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 35px;
    }
    div[data-testid="stFileUploader"] {
        background-color: #1e293b;
        border: 2px dashed #475569;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stFileUploader"] label {
        color: #f8fafc !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 14px;
        font-size: 17px;
        font-weight: 700;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Setup ffmpeg path
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_exe)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# Header Section
st.markdown("<h1>🎬 Pro Video Audio Replacer</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Seamlessly replace background audio in your videos with live preview support.</div>", unsafe_allow_html=True)

# Layout Columns for File Uploaders
col1, col2 = st.columns(2, gap="large")

with col1:
    video_file = st.file_uploader("🎥 Upload Video File", type=[".mp4", ".mov", ".mkv", ".avi"], key="video")
    if video_file is not None:
        st.markdown("##### 👁️ Video Preview")
        st.video(video_file)

with col2:
    audio_file = st.file_uploader("🎵 Upload Audio File", type=[".mp3", ".wav", ".m4a", ".aac"], key="audio")
    if audio_file is not None:
        st.markdown("##### 🔊 Audio Preview")
        st.audio(audio_file)

st.markdown("<br>", unsafe_allow_html=True)

# Process Button & Action Logic
if st.button("🚀 Process & Replace Audio Now"):
    if video_file is not None and audio_file is not None:
        with st.spinner("⚡ Processing video files with FFmpeg... Please wait..."):
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
                
                st.markdown("### 📥 Final Output Preview")
                st.video(output_path)
                
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
