from subtitle_generator import SubtitleGenerator
import os


def main():
    """
    Main application to generate subtitles for a video file.
    """
    # Configuration
    VIDEO_PATH = "video.mp4"
    WHISPER_MODEL = "base"  # You can change this to "tiny", "small", "medium", or "large"

    print("🎬 AutoSub - Automatic Subtitle Generator")
    print("=" * 50)

    # Check if video exists
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Video file '{VIDEO_PATH}' not found!")
        print("Available video files in current directory:")
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']
        video_files = [f for f in os.listdir('.') if any(f.lower().endswith(ext) for ext in video_extensions)]

        if video_files:
            for video_file in video_files:
                print(f"  - {video_file}")
            print(f"\nPlease rename your video to '{VIDEO_PATH}' or modify VIDEO_PATH in this script.")
        else:
            print("  No video files found!")
        return

    # Initialize and run subtitle generation
    try:
        print(f"📹 Processing video: {VIDEO_PATH}")
        print(f"🤖 Using Whisper model: {WHISPER_MODEL}")
        print("\nThis may take a few minutes depending on video length and model size...")

        generator = SubtitleGenerator(whisper_model=WHISPER_MODEL)
        output_video, output_srt = generator.generate_subtitles(VIDEO_PATH)

        print("\n" + "=" * 50)
        print("🎉 Subtitle generation completed successfully!")
        print(f"📹 Video with subtitles: {output_video}")
        print(f"📝 SRT subtitle file: {output_srt}")
        print("\nYou can now play your video with embedded subtitles!")

    except KeyboardInterrupt:
        print("\n\n⏹️ Process interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Ensure your video file is not corrupted")
        print("3. Try using a smaller Whisper model (e.g., 'tiny' instead of 'base')")
        print("4. Make sure you have enough disk space for processing")


if __name__ == "__main__":
    main()
