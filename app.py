import os
import subprocess
import streamlit as st
import imageio_ffmpeg

# Setup ffmpeg path
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
ffmpeg_dir = os.path.dirname(ffmpeg_exe)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

st.title("🎬 Fast Video Audio Replacer")
st.write("Ekhane apnar video ebong audio file upload korun, ebong instant output download korun.")

video_file = st.file_uploader("Upload Video File", type=[".mp4", ".mov", ".mkv", ".avi"])
audio_file = st.file_uploader("Upload Audio File", type=[".mp3", ".wav", ".m4a", ".aac"])

if st.button("🚀 Process Video"):
    if video_file is not None and audio_file is not None:
        with st.spinner("Processing hocche... oboshshoi ektu opekkha korun..."):
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
                st.success("✨ DONE! Successfully processed!")
                
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Processed Video",
                        data=file,
                        file_name="PRO_output_video.mp4",
                        mime="video/mp4"
                    )
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Error during processing: {e}")
    else:
        st.warning("⚠️ Doyakore oboshshoi ekti video ebong ekti audio file upload korun.")