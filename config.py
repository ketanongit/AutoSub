"""
AutoSub Configuration File
Customize your subtitle generation settings here.
"""

# Whisper Model Settings
# Options: "tiny", "base", "small", "medium", "large"
# Tiny: Fastest, lowest accuracy (~1GB VRAM)
# Base: Good balance of speed and accuracy (~1GB VRAM) 
# Small: Better accuracy, moderate speed (~2GB VRAM)
# Medium: High accuracy, slower (~5GB VRAM)
# Large: Best accuracy, slowest (~10GB VRAM)
WHISPER_MODEL = "base"

# Video Input Settings
DEFAULT_VIDEO_PATH = "video.mp4"
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv']

# Output Settings
OUTPUT_VIDEO_SUFFIX = "_with_subtitles"
OUTPUT_SRT_SUFFIX = "_subtitles"
OUTPUT_FOLDER = "output"  # For batch processing

# Subtitle Appearance (for FFmpeg method)
SUBTITLE_STYLE = {
    'FontSize': 24,
    'PrimaryColour': '&Hffffff&',  # White
    'OutlineColour': '&H000000&',  # Black outline
    'Outline': 2,
    'BorderStyle': 1,
    'Alignment': 2,  # Bottom center
    'MarginV': 50  # Distance from bottom
}

# Processing Settings
CLEANUP_TEMP_FILES = True
TEMP_AUDIO_FORMAT = "wav"
ENABLE_WORD_TIMESTAMPS = True

# Performance Settings
USE_GPU_IF_AVAILABLE = True
BATCH_SIZE = 1  # For future batch processing optimizations

# Language Settings (optional - Whisper auto-detects by default)
# Set to None for auto-detection, or specify language code like "en", "es", "fr", etc.
LANGUAGE = None

# Advanced Settings
VERBOSE_OUTPUT = False
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR


def get_subtitle_style_string():
    """
    Convert subtitle style dictionary to FFmpeg format string.
    
    Returns:
        str: FFmpeg subtitle style string
    """
    style_parts = []
    for key, value in SUBTITLE_STYLE.items():
        style_parts.append(f"{key}={value}")

    return ','.join(style_parts)


def validate_config():
    """
    Validate configuration settings.
    
    Returns:
        bool: True if config is valid, False otherwise
    """
    valid_models = ["tiny", "base", "small", "medium", "large"]
    if WHISPER_MODEL not in valid_models:
        print(f"❌ Invalid WHISPER_MODEL: {WHISPER_MODEL}")
        print(f"Valid options: {', '.join(valid_models)}")
        return False

    if not isinstance(SUBTITLE_STYLE, dict):
        print("❌ SUBTITLE_STYLE must be a dictionary")
        return False

    return True


if __name__ == "__main__":
    print("🔧 AutoSub Configuration")
    print("=" * 50)
    print(f"Whisper Model: {WHISPER_MODEL}")
    print(f"Default Video: {DEFAULT_VIDEO_PATH}")
    print(f"Output Folder: {OUTPUT_FOLDER}")
    print(f"Subtitle Style: {get_subtitle_style_string()}")
    print(f"Language: {LANGUAGE if LANGUAGE else 'Auto-detect'}")
    print(f"GPU Enabled: {USE_GPU_IF_AVAILABLE}")

    if validate_config():
        print("\n✅ Configuration is valid!")
    else:
        print("\n❌ Configuration has errors!")
