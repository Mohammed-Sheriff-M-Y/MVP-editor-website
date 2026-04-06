# MVP Editor API Documentation

## Base URL
```
http://127.0.0.1:5000/api
```

## Authentication
Currently, the API does not require authentication. Authentication can be added for production deployment.

---

## 🏥 Health & Status

### Health Check
Check if the API is running and healthy.

**Request:**
```
GET /api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "message": "MVP Editor API is running",
  "timestamp": "2024-01-09T12:30:45.123456"
}
```

---

### API Information
Get general API information and available endpoints.

**Request:**
```
GET /api
GET /api/
```

**Response (200 OK):**
```json
{
  "app": "MVP Editor",
  "version": "1.0.0",
  "endpoints": {
    "health": "/api/health",
    "photo": {
      "upload": "POST /api/photos/upload",
      "list": "GET /api/photos/list",
      "process": "POST /api/photos/process",
      "download": "GET /api/photos/download/<filename>"
    },
    "video": {
      "upload": "POST /api/videos/upload",
      "list": "GET /api/videos/list",
      "process": "POST /api/videos/process",
      "download": "GET /api/videos/download/<filename>"
    }
  }
}
```

---

## 📷 Photo Endpoints

### Upload Photo
Upload a new photo file.

**Request:**
```
POST /api/photos/upload
Content-Type: multipart/form-data

file: <binary image data>
```

**Supported Formats:** JPG, JPEG, PNG, GIF

**Max File Size:** 500 MB

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Photo uploaded successfully",
  "filename": "20240109_123045_photo.jpg",
  "size": 2048576,
  "timestamp": "2024-01-09T12:30:45.123456"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "No file provided"
}
```

**Error Response (413 Payload Too Large):**
```json
{
  "error": "File is too large. Maximum size is 500MB"
}
```

---

### List Photos
Get a list of all uploaded photos.

**Request:**
```
GET /api/photos/list
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 3,
  "photos": [
    {
      "filename": "20240109_123045_photo1.jpg",
      "size": 2048576,
      "created": "2024-01-09T12:30:45.123456"
    },
    {
      "filename": "20240109_120000_photo2.png",
      "size": 3145728,
      "created": "2024-01-09T12:00:00.000000"
    }
  ]
}
```

---

### Process Photo
Apply editing operations to a photo.

**Request:**
```
POST /api/photos/process
Content-Type: application/json

{
  "filename": "20240109_123045_photo.jpg",
  "operation": "rotate",
  "angle": 90
}
```

**Available Operations:**

#### Rotate
```json
{
  "filename": "photo.jpg",
  "operation": "rotate",
  "angle": 90
}
```

#### Crop
```json
{
  "filename": "photo.jpg",
  "operation": "crop",
  "box": [100, 100, 300, 300]
}
```

#### Resize
```json
{
  "filename": "photo.jpg",
  "operation": "resize",
  "width": 800,
  "height": 600
}
```

#### Brightness
```json
{
  "filename": "photo.jpg",
  "operation": "brightness",
  "factor": 1.5
}
```

#### Filter
```json
{
  "filename": "photo.jpg",
  "operation": "filter",
  "filter_type": "blur"
}
```

**Filter Types:** blur, sharpen, grayscale

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Photo processed with rotate",
  "original_filename": "photo.jpg",
  "processed_filename": "processed_20240109_123100_photo.jpg",
  "operation": "rotate"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "File not found"
}
```

---

### Download Photo
Download an uploaded or processed photo.

**Request:**
```
GET /api/photos/download/20240109_123045_photo.jpg
```

**Response:** Binary image file

**Error Response (404 Not Found):**
```json
{
  "error": "File not found"
}
```

---

## 🎥 Video Endpoints

### Upload Video
Upload a new video file.

**Request:**
```
POST /api/videos/upload
Content-Type: multipart/form-data

file: <binary video data>
```

**Supported Formats:** MP4, AVI, MOV, MKV

**Max File Size:** 500 MB

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Video uploaded successfully",
  "filename": "20240109_123045_video.mp4",
  "size": 104857600,
  "timestamp": "2024-01-09T12:30:45.123456"
}
```

---

### List Videos
Get a list of all uploaded videos.

**Request:**
```
GET /api/videos/list
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "videos": [
    {
      "filename": "20240109_123045_video1.mp4",
      "size": 104857600,
      "created": "2024-01-09T12:30:45.123456"
    }
  ]
}
```

---

### Process Video
Apply editing operations to a video.

**Request:**
```
POST /api/videos/process
Content-Type: application/json

{
  "filename": "20240109_123045_video.mp4",
  "operation": "trim"
}
```

**Available Operations:** trim, cut, split, audio, effects, transitions, music

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Video processing started with trim",
  "original_filename": "video.mp4",
  "processed_filename": "processed_trim_20240109_123100_video.mp4",
  "operation": "trim",
  "note": "Full video processing requires ffmpeg installation"
}
```

---

### Download Video
Download an uploaded or processed video.

**Request:**
```
GET /api/videos/download/20240109_123045_video.mp4
```

**Response:** Binary video file

---

## 🔄 CORS Headers

All responses include CORS headers to allow cross-origin requests:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS, HEAD
Access-Control-Allow-Headers: Content-Type
```

---

## Error Handling

### Common Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 200 | OK | Successful request |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 413 | Payload Too Large | File exceeds 500MB limit |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "error": "Description of the error"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. Rate limiting can be added for production deployment.

---

## File Management

### Upload Directory Structure
```
uploads/
├── photos/
│   └── 20240109_123045_photo.jpg
└── videos/
    └── 20240109_123045_video.mp4
```

### Processed Directory Structure
```
processed/
├── photos/
│   └── processed_20240109_123100_photo.jpg
└── videos/
    └── processed_trim_20240109_123100_video.mp4
```

---

## cURL Examples

### Upload Photo
```bash
curl -X POST -F "file=@/path/to/photo.jpg" \
  http://127.0.0.1:5000/api/photos/upload
```

### List Photos
```bash
curl http://127.0.0.1:5000/api/photos/list
```

### Process Photo (Rotate)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"filename":"photo.jpg","operation":"rotate","angle":90}' \
  http://127.0.0.1:5000/api/photos/process
```

### Download Photo
```bash
curl -O http://127.0.0.1:5000/api/photos/download/photo.jpg
```

---

## JavaScript/Fetch Examples

### Upload Photo
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://127.0.0.1:5000/api/photos/upload', {
  method: 'POST',
  body: formData
});

const data = await response.json();
console.log(data);
```

### Process Photo
```javascript
const response = await fetch('http://127.0.0.1:5000/api/photos/process', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    filename: 'photo.jpg',
    operation: 'rotate',
    angle: 90
  })
});

const data = await response.json();
console.log(data);
```

---

## Python/Requests Examples

### Upload Photo
```python
import requests

files = {'file': open('photo.jpg', 'rb')}
response = requests.post('http://127.0.0.1:5000/api/photos/upload', files=files)
print(response.json())
```

### Process Photo
```python
import requests

data = {
    'filename': 'photo.jpg',
    'operation': 'rotate',
    'angle': 90
}

response = requests.post('http://127.0.0.1:5000/api/photos/process', json=data)
print(response.json())
```

---

## Version History

### v1.0.0 (Current)
- Initial release
- Photo upload and basic processing
- Video upload and processing (metadata)
- CORS support

### Planned Features
- Authentication and user accounts
- Advanced video processing with ffmpeg
- Batch processing
- Cloud storage integration
- Real-time processing updates

---

**Last Updated:** January 9, 2024
