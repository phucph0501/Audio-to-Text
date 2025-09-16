# 🎙️ Automatic Speaker-Diarized Transcription Tool

Một công cụ nhận diện lời nói từ video/audio kết hợp phân tích người nói, sử dụng OpenAI Whisper và pyannote-audio.

**🚀 Tính năng**
- Tự động chuyển đổi định dạng file sang WAV chuẩn đầu vào.
- Nhận diện lời nói bằng Whisper với hỗ trợ dấu thời gian từng từ.
- Phân tích người nói bằng pyannote (speaker diarization).
- Xuất ra .txt và .srt (phụ đề) có chú thích người nói.

**🛠️ Yêu cầu hệ thống**
- Python 3.9+
- GPU CUDA(12.8) để tăng tốc (tùy chọn)

**📦 Cài đặt thư viện:**
1. pip install git+https://github.com/openai/whisper.git
2. pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
3. pip install srt
4. pip install pyannote-audio
5. pip install hf_xet

⚠️ Lưu ý: Cần cài đặt ffmpeg và cấu hình đường dẫn ./ffmpeg/bin để chạy được.
- Tải file https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
- Giải nén ffmpeg-release-essentials.zip và đổi tên thành ffmpeg sau đó lưu trong thư mục code

🔑 Chuẩn bị Hugging Face Token
Truy cập https://huggingface.co/settings/tokens để lấy access token. Gán vào biến HF_TOKEN trong script:
HF_TOKEN = "hf_abc123..." 


**📁 Cấu trúc thư mục**
- media/: chứa các file video/audio đầu vào (.mp3, .wav, .mp4,...)
- transcripts/: nơi lưu kết quả .txt và .srt
- models/: nơi chứa model được tự động tải xuống
- ffmpeg/: nơi chứa ứng dụng tách file âm thanh

Script sẽ:
- Duyệt qua tất cả các file trong media/
- Chuyển đổi sang WAV chuẩn
- Nhận diện lời nói và người nói
- Xuất kết quả sang transcripts/

**📄 Kết quả**

- filename.txt: toàn bộ nội dung chuyển thành text
- filename.srt: phụ đề chuẩn, kèm chú thích tên người nói

**💬 Ví dụ output .srt**

1

00:00:00,000 --> 00:00:03,260
Speaker_00: Xin chào bà con, khoảng 5 phút nữa là bão sẽ hết.

2

00:00:03,300 --> 00:00:05,120
Speaker_01: Ai ạ? Ôi trời...




