"""
AutoSub - Example Usage Script
This script demonstrates different ways to use the subtitle generation system.
"""

from subtitle_generator import SubtitleGenerator
import os


def example_basic_usage():
    """
    Example 1: Basic usage with default settings
    """
    print("=" * 60)
    print("📚 EXAMPLE 1: Basic Usage")
    print("=" * 60)

    video_path = "video.mp4"

    if not os.path.exists(video_path):
        print(f"❌ Video file '{video_path}' not found!")
        return

    # Initialize with default 'base' model
    generator = SubtitleGenerator()

    # Generate subtitles with default output names
    output_video, output_srt = generator.generate_subtitles(video_path)

    print(f"✅ Generated: {output_video} and {output_srt}")


def example_custom_settings():
    """
    Example 2: Custom model and output paths
    """
    print("\n" + "=" * 60)
    print("📚 EXAMPLE 2: Custom Settings")
    print("=" * 60)

    video_path = "video.mp4"

    if not os.path.exists(video_path):
        print(f"❌ Video file '{video_path}' not found!")
        return

    # Initialize with a faster model for quick processing
    generator = SubtitleGenerator(whisper_model="tiny")

    # Custom output paths
    custom_video_output = "my_subtitled_video.mp4"
    custom_srt_output = "my_subtitles.srt"

    output_video, output_srt = generator.generate_subtitles(
        video_path=video_path,
        output_video_path=custom_video_output,
        output_srt_path=custom_srt_output
    )

    print(f"✅ Generated: {output_video} and {output_srt}")


def example_high_quality():
    """
    Example 3: High quality transcription (slower but more accurate)
    """
    print("\n" + "=" * 60)
    print("📚 EXAMPLE 3: High Quality Transcription")
    print("=" * 60)

    video_path = "video.mp4"

    if not os.path.exists(video_path):
        print(f"❌ Video file '{video_path}' not found!")
        return

    print("⚠️ Note: This will be slower but more accurate")

    # Use large model for best quality
    generator = SubtitleGenerator(whisper_model="medium")  # or "large" for even better quality

    output_video, output_srt = generator.generate_subtitles(
        video_path=video_path,
        output_video_path="hq_video_with_subtitles.mp4",
        output_srt_path="hq_subtitles.srt"
    )

    print(f"✅ High quality subtitles generated: {output_video} and {output_srt}")


def example_batch_processing():
    """
    Example 4: Process multiple videos
    """
    print("\n" + "=" * 60)
    print("📚 EXAMPLE 4: Batch Processing")
    print("=" * 60)

    # List of video files to process
    video_files = ["video.mp4"]  # Add more video files here

    # Initialize generator once
    generator = SubtitleGenerator(whisper_model="base")

    for video_path in video_files:
        if os.path.exists(video_path):
            print(f"\n🎥 Processing: {video_path}")
            try:
                output_video, output_srt = generator.generate_subtitles(video_path)
                print(f"✅ Completed: {output_video}")
            except Exception as e:
                print(f"❌ Failed to process {video_path}: {str(e)}")
        else:
            print(f"❌ File not found: {video_path}")


def example_srt_only():
    """
    Example 5: Generate SRT file only (no video processing)
    """
    print("\n" + "=" * 60)
    print("📚 EXAMPLE 5: SRT File Only")
    print("=" * 60)

    video_path = "video.mp4"

    if not os.path.exists(video_path):
        print(f"❌ Video file '{video_path}' not found!")
        return

    generator = SubtitleGenerator(whisper_model="base")

    # Extract audio
    audio_path = generator.extract_audio(video_path, "temp_audio.wav")

    # Transcribe
    transcription = generator.transcribe_audio(audio_path)

    # Create SRT only
    srt_path = generator.create_srt_file(transcription, "subtitles_only.srt")

    # Clean up
    if os.path.exists(audio_path):
        os.remove(audio_path)

    print(f"✅ SRT file created: {srt_path}")


def main():
    """
    Run all examples
    """
    print("🎬 AutoSub - Usage Examples")
    print("Choose an example to run:")
    print("1. Basic usage")
    print("2. Custom settings")
    print("3. High quality (slower)")
    print("4. Batch processing")
    print("5. SRT file only")
    print("6. Run all examples")

    choice = input("\nEnter your choice (1-6): ").strip()

    if choice == "1":
        example_basic_usage()
    elif choice == "2":
        example_custom_settings()
    elif choice == "3":
        example_high_quality()
    elif choice == "4":
        example_batch_processing()
    elif choice == "5":
        example_srt_only()
    elif choice == "6":
        example_basic_usage()
        example_custom_settings()
        example_high_quality()
        example_batch_processing()
        example_srt_only()
    else:
        print("❌ Invalid choice!")


if __name__ == "__main__":
    main()
