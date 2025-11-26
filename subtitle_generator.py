import os
import whisper
import torch
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import re
from datetime import timedelta


class SubtitleGenerator:
    def __init__(self, whisper_model="base"):
        """
        Initialize the subtitle generator with a Whisper model.
        
        Args:
            whisper_model (str): Whisper model size ("tiny", "base", "small", "medium", "large")
        """
        print(f"Loading Whisper model: {whisper_model}")
        self.model = whisper.load_model(whisper_model)
        print("Model loaded successfully!")

    def extract_audio(self, video_path, audio_path="temp_audio.wav"):
        """
        Extract audio from video file.
        
        Args:
            video_path (str): Path to the input video
            audio_path (str): Path to save the extracted audio
            
        Returns:
            str: Path to the extracted audio file
        """
        print("Extracting audio from video...")
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path, verbose=False, logger=None)
        audio.close()
        video.close()
        print(f"Audio extracted to: {audio_path}")
        return audio_path

    def transcribe_audio(self, audio_path):
        """
        Transcribe audio using Whisper.
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            dict: Whisper transcription result with segments
        """
        print("Transcribing audio with Whisper...")
        result = self.model.transcribe(audio_path, word_timestamps=True)
        print("Transcription completed!")
        return result

    def format_time(self, seconds):
        """
        Format time in seconds to SRT time format (HH:MM:SS,mmm).
        
        Args:
            seconds (float): Time in seconds
            
        Returns:
            str: Formatted time string
        """
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(td.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"

    def create_srt_file(self, transcription_result, srt_path="subtitles.srt"):
        """
        Create SRT subtitle file from Whisper transcription.
        
        Args:
            transcription_result (dict): Whisper transcription result
            srt_path (str): Path to save the SRT file
            
        Returns:
            str: Path to the created SRT file
        """
        print("Creating SRT subtitle file...")

        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(transcription_result['segments'], 1):
                start_time = self.format_time(segment['start'])
                end_time = self.format_time(segment['end'])
                text = segment['text'].strip()

                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")

        print(f"SRT file created: {srt_path}")
        return srt_path

    def create_subtitle_clip(self, text, start, end, video_size):
        """
        Create a subtitle text clip using a method that doesn't require ImageMagick.
        
        Args:
            text (str): Subtitle text
            start (float): Start time in seconds
            end (float): End time in seconds
            video_size (tuple): Video dimensions (width, height)
            
        Returns:
            TextClip: Subtitle text clip
        """
        try:
            # Try using caption method without ImageMagick
            subtitle_clip = TextClip(
                text,
                fontsize=min(video_size[1] // 20, 48),  # Dynamic font size based on video height
                color='white',
                method='label'  # Use label method instead of caption to avoid ImageMagick
            ).set_start(start).set_end(end).set_position(('center', video_size[1] - 100))

            return subtitle_clip

        except Exception as e:
            print(f"Warning: Could not create text clip with method 'label': {str(e)}")
            # Fallback: create a simple text clip
            try:
                subtitle_clip = TextClip(
                    text,
                    fontsize=24,
                    color='white'
                ).set_start(start).set_end(end).set_position(('center', 'bottom'))

                return subtitle_clip
            except Exception as e2:
                print(f"Warning: Fallback text clip creation also failed: {str(e2)}")
                return None

    def add_subtitles_to_video_with_srt(self, video_path, srt_path, output_path="video_with_subtitles.mp4", style_config=None):
        """
        Add subtitles to video using external SRT file with FFmpeg.
        This method burns the subtitles directly into the video using FFmpeg.
        
        Args:
            video_path (str): Path to the input video
            srt_path (str): Path to the SRT subtitle file
            output_path (str): Path to save the output video
            style_config (dict): Optional configuration for subtitle styling
            
        Returns:
            str: Path to the output video with subtitles
        """
        print("Adding subtitles to video using FFmpeg...")

        import subprocess

        # Default style
        style_str = "FontSize=24,PrimaryColour=&Hffffff&,OutlineColour=&H000000&,Outline=2"
        
        # Override with custom style if provided
        if style_config:
            # Map frontend style keys to FFmpeg style keys
            # Front: fontSize, fontColor, outlineColor, outlineWidth, marginV
            font_size = style_config.get('fontSize', 24)
            
            # Convert hex colors (#RRGGBB) to FFmpeg format (&HBBGGRR&)
            def hex_to_ffmpeg(hex_color):
                if not hex_color or not hex_color.startswith('#'):
                    return "&Hffffff&"
                hex_color = hex_color.lstrip('#')
                r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
                return f"&H{b}{g}{r}&"

            primary_color = hex_to_ffmpeg(style_config.get('fontColor', '#ffffff'))
            outline_color = hex_to_ffmpeg(style_config.get('outlineColor', '#000000'))
            outline_width = style_config.get('outlineWidth', 2)
            margin_v = style_config.get('marginV', 10)
            
            style_str = f"FontSize={font_size},PrimaryColour={primary_color},OutlineColour={outline_color},Outline={outline_width},MarginV={margin_v}"

        # Use FFmpeg to burn subtitles into video
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf',
            f"subtitles='{srt_path}':force_style='{style_str}'",
            '-c:a', 'copy',  # Copy audio without re-encoding
            '-y',  # Overwrite output file if it exists
            output_path
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"Video with subtitles saved to: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr}")
            raise Exception(f"Failed to add subtitles with FFmpeg: {e.stderr}")
        except FileNotFoundError:
            print("FFmpeg not found. Falling back to MoviePy method...")
            return self.add_subtitles_to_video_moviepy(video_path, srt_path, output_path)

    def add_subtitles_to_video_moviepy(self, video_path, srt_path, output_path="video_with_subtitles.mp4"):
        """
        Add subtitles to video using MoviePy (fallback method).
        
        Args:
            video_path (str): Path to the input video
            srt_path (str): Path to the SRT subtitle file
            output_path (str): Path to save the output video
            
        Returns:
            str: Path to the output video with subtitles
        """
        print("Adding subtitles to video using MoviePy...")

        # Parse SRT file
        subtitles = self.parse_srt_file(srt_path)

        # Load the original video
        video = VideoFileClip(video_path)
        video_size = video.size

        # Create subtitle clips
        subtitle_clips = []
        for subtitle in subtitles:
            start_time = subtitle['start']
            end_time = subtitle['end']
            text = subtitle['text']

            if text:  # Only create clip if text is not empty
                subtitle_clip = self.create_subtitle_clip(text, start_time, end_time, video_size)
                if subtitle_clip:
                    subtitle_clips.append(subtitle_clip)

        # Composite video with subtitles
        if subtitle_clips:
            final_video = CompositeVideoClip([video] + subtitle_clips)
        else:
            final_video = video

        # Write the final video
        print("Rendering final video with subtitles...")
        final_video.write_videofile(
            output_path,
            fps=video.fps,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )

        # Clean up
        video.close()
        final_video.close()
        for clip in subtitle_clips:
            if clip:
                clip.close()

        print(f"Video with subtitles saved to: {output_path}")
        return output_path

    def parse_srt_file(self, srt_path):
        """
        Parse SRT file to extract subtitle information.
        
        Args:
            srt_path (str): Path to the SRT file
            
        Returns:
            list: List of subtitle dictionaries with start, end, and text
        """
        subtitles = []

        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into subtitle blocks
        blocks = content.strip().split('\n\n')

        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                # Parse time
                time_line = lines[1]
                if ' --> ' in time_line:
                    start_str, end_str = time_line.split(' --> ')
                    start_time = self.parse_time_string(start_str)
                    end_time = self.parse_time_string(end_str)

                    # Get text (everything after the time line)
                    text = '\n'.join(lines[2:])

                    subtitles.append({
                        'start': start_time,
                        'end': end_time,
                        'text': text
                    })

        return subtitles

    def parse_time_string(self, time_str):
        """
        Parse SRT time string to seconds.
        
        Args:
            time_str (str): Time string in format HH:MM:SS,mmm
            
        Returns:
            float: Time in seconds
        """
        time_str = time_str.replace(',', '.')
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])

        return hours * 3600 + minutes * 60 + seconds

    def add_subtitles_to_video(self, video_path, transcription_result, output_path="video_with_subtitles.mp4"):
        """
        Add subtitles to video. First creates SRT file, then uses the best available method.
        
        Args:
            video_path (str): Path to the input video
            transcription_result (dict): Whisper transcription result
            output_path (str): Path to save the output video
            
        Returns:
            str: Path to the output video with subtitles
        """
        # Create temporary SRT file
        temp_srt_path = "temp_subtitles.srt"
        self.create_srt_file(transcription_result, temp_srt_path)

        try:
            # Try FFmpeg method first (better quality and performance)
            result = self.add_subtitles_to_video_with_srt(video_path, temp_srt_path, output_path)
            return result
        except Exception as e:
            print(f"FFmpeg method failed: {str(e)}")
            print("Falling back to MoviePy method...")

            # Fallback to MoviePy method
            result = self.add_subtitles_to_video_moviepy(video_path, temp_srt_path, output_path)
            return result
        finally:
            # Clean up temporary SRT file
            if os.path.exists(temp_srt_path):
                os.remove(temp_srt_path)

    def generate_subtitles(self, video_path, output_video_path=None, output_srt_path=None, cleanup_temp=True):
        """
        Complete pipeline to generate subtitles for a video.
        
        Args:
            video_path (str): Path to the input video
            output_video_path (str): Path for output video with subtitles
            output_srt_path (str): Path for output SRT file
            cleanup_temp (bool): Whether to clean up temporary files
            
        Returns:
            tuple: (output_video_path, output_srt_path)
        """
        # Set default output paths
        if output_video_path is None:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_video_path = f"{base_name}_with_subtitles.mp4"

        if output_srt_path is None:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_srt_path = f"{base_name}_subtitles.srt"

        temp_audio_path = "temp_audio.wav"

        try:
            # Step 1: Extract audio
            self.extract_audio(video_path, temp_audio_path)

            # Step 2: Transcribe audio
            transcription_result = self.transcribe_audio(temp_audio_path)

            # Step 3: Create SRT file
            self.create_srt_file(transcription_result, output_srt_path)

            # Step 4: Add subtitles to video
            self.add_subtitles_to_video(video_path, transcription_result, output_video_path)

            print(f"\n✅ Subtitle generation completed!")
            print(f"📹 Video with subtitles: {output_video_path}")
            print(f"📝 SRT file: {output_srt_path}")

            return output_video_path, output_srt_path

        finally:
            # Clean up temporary files
            if cleanup_temp and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
                print("🧹 Temporary audio file cleaned up")


def main():
    """
    Main function to demonstrate subtitle generation.
    """
    # Configuration
    VIDEO_PATH = "video.mp4"  # Your input video
    WHISPER_MODEL = "base"  # Options: tiny, base, small, medium, large

    # Check if video file exists
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ Error: Video file '{VIDEO_PATH}' not found!")
        print("Please make sure the video file exists in the current directory.")
        return

    print("🎬 AutoSub - Automatic Subtitle Generator")
    print("=" * 50)

    # Initialize subtitle generator
    generator = SubtitleGenerator(whisper_model=WHISPER_MODEL)

    # Generate subtitles
    try:
        output_video, output_srt = generator.generate_subtitles(VIDEO_PATH)
        print("\n🎉 Success! Your video now has subtitles!")

    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print("Please check the error message and try again.")


if __name__ == "__main__":
    main()
