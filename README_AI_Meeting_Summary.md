
# 🧠 AI Meeting Summary Pipeline

Chuyển đổi file cuộc họp (audio, video, text) thành **tóm tắt**, **danh sách công việc**, và **thông tin thời gian** bằng mô hình LLM.

---

## 🧩 Kiến trúc Pipeline

```
+------------------+        +------------------------+        +------------------------+
|   User Uploads   | -----> |   Text Conversion      | -----> |    LLM Processing      |
| (Video/Audio/Txt)|        |  (ASR or File Parsing) |        | (Summarize/Extract)    |
+------------------+        +------------------------+        +------------------------+
                                                              | - Summary              |
                                                              | - Action Items         |
                                                              | - Dates / Times        |
                                                              +------------------------+
                                                                          |
                                                                          v
                                                              +------------------------+
                                                              |      JSON Output       |
                                                              |  (Save or Send Next)   |
                                                              +------------------------+
```

---

## 📥 1. User Uploads

Người dùng có thể gửi các định dạng file sau:

- 🎥 `.mp4` – video cuộc họp
- 🔊 `.mp3`, `.wav` – file audio
- 📄 `.txt`, `.srt` – transcript văn bản có sẵn

---

## 🔄 2. Text Conversion

### Đối với video/audio:
- **Công cụ sử dụng:** `ffmpeg` để trích audio, sau đó dùng `Whisper` (OpenAI) để chuyển sang text.
- **ASR:** (Automatic Speech Recognition)

### Đối với file `.txt` hoặc `.srt`:
- Đọc nội dung, chuẩn hóa dấu câu, loại bỏ thừa từ, làm sạch văn bản đầu vào.

---

## 🤖 3. LLM Processing

Sử dụng Large Language Model (LLM) để thực hiện:

- ✅ **Tóm tắt nội dung chính** cuộc họp
- 📝 **Trích xuất danh sách nhiệm vụ** (gồm người phụ trách & deadline)
- 📆 **Xác định thời gian** quan trọng được nhắc đến

**Prompt sử dụng** (gợi ý mẫu):
```
Tóm tắt nội dung sau:
- Viết 3-5 ý chính
- Trích nhiệm vụ (task), người thực hiện, thời hạn
- Trích xuất các ngày giờ được nhắc đến
```

---

## 📦 4. JSON Output (Cấu trúc kết quả)

Kết quả đầu ra được lưu dưới dạng JSON có cấu trúc rõ ràng như sau:

```json
{
  "summary": [
    "Project X is delayed by 2 weeks.",
    "Team agreed to shift testing to August.",
    "A new hire will start on Sept 1."
  ],
  "action_items": [
    {
      "task": "Create updated project plan",
      "assigned_to": "Minh",
      "due_date": "2025-08-01"
    },
    {
      "task": "Prepare client presentation",
      "assigned_to": "Linh",
      "due_date": "2025-08-03"
    }
  ],
  "dates_mentioned": [
    "2025-08-01",
    "2025-08-03",
    "2025-09-01"
  ]
}
```

---

## 🛠️ Công nghệ sử dụng

| Thành phần          | Công cụ                         |
|---------------------|----------------------------------|
| Audio extraction    | `ffmpeg`                        |
| Speech-to-text      | `OpenAI Whisper`                |
| Văn bản đầu vào     | `.txt`, `.srt` parser           |
| LLM                 | `GPT-4`|
| Format đầu ra       | `JSON`, lưu vào file hoặc database|

---

## 📁 Kết quả đầu ra có thể sử dụng tiếp cho:
- Tạo Jira Task
- Gửi Email thông báo
- Đặt lịch Google Calendar
- Gợi ý truy vấn qua chatbot

---

## 🧪 Gợi ý test
- Dùng file `demo.mp4` (~3 phút)

---

## 📌 Ghi chú
- Prompt được version hóa để đánh giá chất lượng qua từng lần cải tiến
- Có thể mở rộng để dùng vector database, RAG nếu cần tìm kiếm theo ngữ nghĩa trong nhiều cuộc họp

---
