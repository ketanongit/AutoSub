import os
import glob
from subtitle_generator import SubtitleGenerator
import time


def batch_process_videos(input_folder=".", output_folder="output", whisper_model="base", video_extensions=None):
    """
    Process multiple video files in a folder to generate subtitles.
    
    Args:
        input_folder (str): Folder containing video files
        output_folder (str): Folder to save processed videos
        whisper_model (str): Whisper model to use
        video_extensions (list): List of video file extensions to process
    """
    if video_extensions is None:
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    print("🎬 AutoSub - Batch Subtitle Generator")
    print("=" * 60)

    # Find all video files
    video_files = []
    for ext in video_extensions:
        pattern = os.path.join(input_folder, f"*{ext}")
        video_files.extend(glob.glob(pattern, recursive=False))
        pattern = os.path.join(input_folder, f"*{ext.upper()}")
        video_files.extend(glob.glob(pattern, recursive=False))

    if not video_files:
        print(f"❌ No video files found in '{input_folder}'")
        print(f"Looking for extensions: {', '.join(video_extensions)}")
        return

    print(f"📁 Found {len(video_files)} video file(s) to process:")
    for i, video_file in enumerate(video_files, 1):
        print(f"  {i}. {os.path.basename(video_file)}")

    print(f"\n🤖 Using Whisper model: {whisper_model}")
    print(f"💾 Output folder: {output_folder}")

    # Initialize subtitle generator
    try:
        generator = SubtitleGenerator(whisper_model=whisper_model)
    except Exception as e:
        print(f"❌ Failed to initialize Whisper model: {str(e)}")
        return

    # Process each video
    successful = 0
    failed = 0
    total_start_time = time.time()

    for i, video_path in enumerate(video_files, 1):
        video_name = os.path.basename(video_path)
        base_name = os.path.splitext(video_name)[0]

        # Set output paths
        output_video_path = os.path.join(output_folder, f"{base_name}_with_subtitles.mp4")
        output_srt_path = os.path.join(output_folder, f"{base_name}_subtitles.srt")

        print(f"\n" + "=" * 60)
        print(f"🎥 Processing {i}/{len(video_files)}: {video_name}")
        print("=" * 60)

        start_time = time.time()

        try:
            # Generate subtitles
            generator.generate_subtitles(
                video_path=video_path,
                output_video_path=output_video_path,
                output_srt_path=output_srt_path
            )

            processing_time = time.time() - start_time
            print(f"✅ Completed in {processing_time:.1f} seconds")
            successful += 1

        except KeyboardInterrupt:
            print(f"\n⏹️ Process interrupted by user at video {i}/{len(video_files)}")
            break

        except Exception as e:
            print(f"❌ Failed to process {video_name}: {str(e)}")
            failed += 1
            continue

    # Summary
    total_time = time.time() - total_start_time
    print(f"\n" + "=" * 60)
    print("📊 BATCH PROCESSING SUMMARY")
    print("=" * 60)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️ Total time: {total_time:.1f} seconds ({total_time / 60:.1f} minutes)")

    if successful > 0:
        print(f"📁 Output files saved in: {output_folder}")
        print(f"⏱️ Average time per video: {total_time / successful:.1f} seconds")


def main():
    """
    Main function for batch processing configuration.
    """
    # Configuration
    INPUT_FOLDER = "."  # Folder containing video files
    OUTPUT_FOLDER = "output"  # Folder to save processed videos
    WHISPER_MODEL = "base"  # Whisper model size

    # Supported video formats
    VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']

    print("⚙️ Configuration:")
    print(f"  Input folder: {INPUT_FOLDER}")
    print(f"  Output folder: {OUTPUT_FOLDER}")
    print(f"  Whisper model: {WHISPER_MODEL}")
    print(f"  Video formats: {', '.join(VIDEO_EXTENSIONS)}")

    # Ask for confirmation
    response = input("\n▶️ Start batch processing? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Batch processing cancelled.")
        return

    # Start batch processing
    batch_process_videos(
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        whisper_model=WHISPER_MODEL,
        video_extensions=VIDEO_EXTENSIONS
    )


if __name__ == "__main__":
    main()
