# Backend API module shared by all Kivy pages
import os
import types

import requests

bm = types.SimpleNamespace()

BASE_URL = os.environ.get('MVP_EDITOR_API_BASE', 'http://127.0.0.1:5000')
API_BASE = f"{BASE_URL.rstrip('/')}/api"


def _to_error_dict(exc):
    return {'success': False, 'error': str(exc)}


def _json_or_error(response):
    try:
        data = response.json()
    except Exception:
        return {'success': False, 'error': f'Invalid server response ({response.status_code})'}

    if response.status_code >= 400:
        if 'success' not in data:
            data['success'] = False
        return data
    return data


def upload_photo(filepath):
    try:
        with open(filepath, 'rb') as file_data:
            response = requests.post(f'{API_BASE}/upload', files={'file': file_data}, timeout=30)
        return _json_or_error(response)
    except Exception as exc:
        return _to_error_dict(exc)


def upload_video(filepath):
    try:
        with open(filepath, 'rb') as file_data:
            response = requests.post(f'{API_BASE}/upload-video', files={'file': file_data}, timeout=30)
        return _json_or_error(response)
    except Exception as exc:
        return _to_error_dict(exc)


def list_photos():
    try:
        response = requests.get(f'{API_BASE}/photos', timeout=15)
        return _json_or_error(response)
    except Exception as exc:
        return _to_error_dict(exc)


def list_videos():
    try:
        response = requests.get(f'{API_BASE}/videos', timeout=15)
        return _json_or_error(response)
    except Exception as exc:
        return _to_error_dict(exc)


def list_media_files(media):
    try:
        response = requests.get(f'{API_BASE}/media/{media}/files', timeout=15)
        return _json_or_error(response)
    except Exception as exc:
        return _to_error_dict(exc)


def process_photo(filename, operation='rotate'):
    try:
        response = requests.post(
            f'{API_BASE}/process',
            json={'filename': filename, 'operation': operation},
            timeout=30,
        )
        return _json_or_error(response)
    except Exception as exc:
        return _to_error_dict(exc)


def process_video(filename, operation='trim'):
    try:
        response = requests.post(
            f'{API_BASE}/process-video',
            json={'filename': filename, 'operation': operation},
            timeout=30,
        )
        return _json_or_error(response)
    except Exception as exc:
        return _to_error_dict(exc)


def save_media(media, filename):
    try:
        response = requests.post(
            f'{API_BASE}/media/{media}/save',
            json={'filename': filename},
            timeout=30,
        )
        return _json_or_error(response)
    except Exception as exc:
        return _to_error_dict(exc)


def clear_media(media):
    try:
        response = requests.post(f'{API_BASE}/media/{media}/clear', timeout=30)
        return _json_or_error(response)
    except Exception as exc:
        return _to_error_dict(exc)


def download_media(media, filename, save_dir):
    try:
        os.makedirs(save_dir, exist_ok=True)
        target_path = os.path.join(save_dir, filename)
        with requests.get(f'{API_BASE}/download/{media}/{filename}', timeout=60, stream=True) as response:
            if response.status_code >= 400:
                return _json_or_error(response)
            with open(target_path, 'wb') as output_file:
                for chunk in response.iter_content(chunk_size=1024 * 64):
                    if chunk:
                        output_file.write(chunk)
        return {'success': True, 'path': target_path}
    except Exception as exc:
        return _to_error_dict(exc)


bm.upload_photo = upload_photo
bm.list_photos = list_photos
bm.process_photo = process_photo
bm.upload_video = upload_video
bm.list_videos = list_videos
bm.process_video = process_video
bm.list_media_files = list_media_files
bm.save_media = save_media
bm.clear_media = clear_media
bm.download_media = download_media
