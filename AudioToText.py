import os
import whisper
import torch
import subprocess
import srt
import datetime
from pyannote.audio import Pipeline

# ====== Cấu hình =======
INPUT_FOLDER = "media"  # Thư mục chứa file video/audio
OUTPUT_FOLDER = "transcripts"  # Nơi lưu file text và .srt
MODEL_NAME = "medium"  # Model Whisper small/medium/large/large-v3
MODEL_DIR = "./models"  # Thư mục chứa model .pt nếu muốn dùng local
HF_TOKEN = "" Huggingface token
# ========================

ffmpeg_dir = os.path.abspath("./ffmpeg/bin")
os.environ["PATH"] += os.pathsep + ffmpeg_dir


def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def get_speaker_segments(audio_path, hf_token):
    """Chạy pyannote để lấy đoạn phân người nói"""
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1", use_auth_token=hf_token)
    diarization = pipeline(audio_path)
    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })
    return segments


def is_audio_or_video(file):
    audio_exts = [".mp3", ".wav", ".m4a", ".aac", ".flac"]
    video_exts = [".mp4", ".mkv", ".avi", ".mov"]
    return os.path.splitext(file)[1].lower() in audio_exts + video_exts


def convert_to_wav(input_path, output_path):
    """Dùng ffmpeg để chuyển sang WAV (mono, 16kHz)"""
    subprocess.run([
        "ffmpeg", "-y", "-i", input_path,
        "-ar", "16000", "-ac", "1", "-loglevel", "error", output_path
    ])


def seconds_to_timedelta(seconds):
    return datetime.timedelta(seconds=seconds)


def write_srt_with_speakers(result, diar_segments, srt_path):
    subs = []
    i = 1
    for segment in result["segments"]:
        # Tìm speaker phù hợp với đoạn này
        start = segment["start"]
        end = segment["end"]
        speaker = "Unknown"

        # for diar in diar_segments:
        #     if diar["start"] <= start <= diar["end"]:
        #         speaker = diar["speaker"]
        #         break

        def is_overlap(start1, end1, start2, end2):
            return max(start1, start2) < min(end1, end2)

        best_overlap = 0.0
        best_speaker = "Unknown"

        for diar in diar_segments:
            if is_overlap(start, end, diar["start"], diar["end"]):
                overlap = min(end, diar["end"]) - max(start, diar["start"])
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_speaker = diar["speaker"]

        speaker = best_speaker

        text = f"{speaker}: {segment['text'].strip()}"
        subs.append(srt.Subtitle(
            index=i,
            start=seconds_to_timedelta(start),
            end=seconds_to_timedelta(end),
            content=text
        ))
        i += 1

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt.compose(subs))


def transcribe_file(model, input_file, output_txt, hf_token):
    temp_wav = "audio.wav"
    convert_to_wav(input_file, temp_wav)

    # Nhận diện lời nói
    result = model.transcribe(temp_wav, verbose=True, word_timestamps=True, fp16=False)

    # Nhận diện người nói
    diar_segments = get_speaker_segments(temp_wav, hf_token)

    # Ghi file .txt
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # Ghi file .srt có speaker
    base_name = os.path.splitext(os.path.basename(output_txt))[0]
    srt_path = os.path.join(OUTPUT_FOLDER, base_name + ".srt")
    write_srt_with_speakers(result, diar_segments, srt_path)

    os.remove(temp_wav)


def load_model(model_name, device, download_root=None):
    model =  whisper.load_model(model_name, device=device, download_root=download_root)
    return model

def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    device = get_device()
    print(f"🔍 Đang dùng thiết bị: {device.upper()}")

    print("📦 Đang tải model...")
    model = load_model(MODEL_NAME, device=device, download_root=MODEL_DIR)

    for filename in os.listdir(INPUT_FOLDER):
        if not is_audio_or_video(filename):
            continue

        input_path = os.path.join(INPUT_FOLDER, filename)
        base_name = os.path.splitext(filename)[0]
        output_txt = os.path.join(OUTPUT_FOLDER, base_name + ".txt")

        print(f"🎧 Xử lý: {filename}...")
        try:
            transcribe_file(model, input_path, output_txt, HF_TOKEN)
            print(f"✅ Xong: {output_txt}")
        except Exception as e:
            print(f"❌ Lỗi với {filename}: {e}")


if __name__ == "__main__":
    main()