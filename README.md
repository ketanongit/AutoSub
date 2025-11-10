# AutoSub - Automatic Subtitle Generator

🎬 Automatically generate and embed subtitles into videos using OpenAI's Whisper AI model.

## Features

- 🤖 **AI-Powered Transcription**: Uses OpenAI Whisper for accurate speech-to-text conversion
- 🎥 **Video Processing**: Extracts audio, generates subtitles, and embeds them back into video
- 📝 **SRT File Generation**: Creates industry-standard SRT subtitle files
- 🎨 **Customizable Appearance**: Beautiful, readable subtitles with customizable styling
- 🚀 **Multiple Model Sizes**: Choose from different Whisper models based on accuracy vs. speed needs
- 🧹 **Automatic Cleanup**: Removes temporary files after processing

## Requirements

- Python 3.8 or higher
- FFmpeg (for video processing)
- At least 4GB RAM (more for larger models)
- GPU recommended for faster processing (optional)

## Installation

### 1. Clone or Download the Project

```bash
git clone <your-repo-url>
cd AutoSub-b
```

### 2. Create and Activate Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

#### Windows:

1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract and add to your PATH
3. Or use chocolatey: `choco install ffmpeg`

#### macOS:

```bash
brew install ffmpeg
```

#### Linux:

```bash
sudo apt update
sudo apt install ffmpeg
```

## Usage

### Quick Start

1. Place your video file in the project directory and name it `video.mp4`
2. Run the application:

```bash
python app.py
```

### Advanced Usage

You can also use the `SubtitleGenerator` class directly for more control:

```python
from subtitle_generator import SubtitleGenerator

# Initialize with desired model size
generator = SubtitleGenerator(whisper_model="base")

# Generate subtitles
output_video, output_srt = generator.generate_subtitles(
    video_path="your_video.mp4",
    output_video_path="output_with_subs.mp4",
    output_srt_path="subtitles.srt"
)
```

## Whisper Model Options

Choose the right model for your needs:

| Model | Speed | Accuracy | VRAM Usage | Best For |
|-------|--------|----------|------------|----------|
| `tiny` | ⚡⚡⚡⚡⚡ | ⭐⭐ | ~1GB | Quick tests, low-resource systems |
| `base` | ⚡⚡⚡⚡ | ⭐⭐⭐ | ~1GB | General use, good balance |
| `small` | ⚡⚡⚡ | ⭐⭐⭐⭐ | ~2GB | Better accuracy, moderate speed |
| `medium` | ⚡⚡ | ⭐⭐⭐⭐⭐ | ~5GB | High accuracy, professional use |
| `large` | ⚡ | ⭐⭐⭐⭐⭐ | ~10GB | Best accuracy, research quality |

## Customization

### Subtitle Appearance

Edit the `create_subtitle_clip` method in `subtitle_generator.py` to customize:

```python
subtitle_clip = TextClip(
    text,
    fontsize=24,           # Font size
    font='Arial-Bold',     # Font family
    color='white',         # Text color
    stroke_color='black',  # Outline color
    stroke_width=2,        # Outline width
    method='caption',
    size=(video_size[0] * 0.8, None)  # Text box width
).set_position(('center', 'bottom'))   # Position on screen
```

### Supported Video Formats

- MP4 (recommended)
- AVI
- MOV
- MKV
- WMV
- FLV

## Output Files

The system generates:

1. **Video with embedded subtitles**: `{original_name}_with_subtitles.mp4`
2. **SRT subtitle file**: `{original_name}_subtitles.srt`

## Troubleshooting

### Common Issues

1. **"FFmpeg not found"**
    - Make sure FFmpeg is installed and in your PATH
    - Restart your terminal after installation

2. **Out of memory errors**
    - Use a smaller Whisper model (e.g., "tiny" or "base")
    - Close other applications to free up RAM

3. **Slow processing**
    - Use GPU acceleration if available
    - Try a smaller model for faster processing
    - Ensure your video file isn't too large

4. **Poor transcription quality**
    - Use a larger model ("medium" or "large")
    - Ensure audio quality is good
    - Check if the language is supported by Whisper

### Performance Tips

- **GPU Acceleration**: Install PyTorch with CUDA support for faster processing
- **SSD Storage**: Use SSD for faster file I/O operations
- **Batch Processing**: Process multiple videos by modifying the script

## Languages Supported

Whisper supports 99+ languages including:

- English, Spanish, French, German, Italian
- Chinese, Japanese, Korean
- Arabic, Russian, Portuguese
- And many more!

## License

This project is open source. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are correctly installed
3. Verify your video file is not corrupted
4. Try with a smaller test video first

---

Made with ❤️ using OpenAI Whisper and MoviePy