from flask import Flask, jsonify, request, send_from_directory, render_template_string, redirect, url_for, session
import os
import time

try:
    from backend.models.activity_store import init_db, log_event, today_activities
    from backend.models.member_store import add_member, delete_member, init_member_db, list_members
    from backend.services.paths import FRONTEND_DIR, PROCESSED_DIR, UPLOAD_DIR, ensure_directories
    from backend.services.photo_options import PHOTO_OPERATIONS, process_photo
    from backend.services.storage_service import (
        all_files,
        clear_media,
        list_files,
        media_folder,
        resolve_file_for_download,
        save_media_copy,
        timestamp_name,
    )
    from backend.services.video_options import VIDEO_OPERATIONS, process_video
except ImportError:
    from models.activity_store import init_db, log_event, today_activities
    from models.member_store import add_member, delete_member, init_member_db, list_members
    from services.paths import FRONTEND_DIR, PROCESSED_DIR, UPLOAD_DIR, ensure_directories
    from services.photo_options import PHOTO_OPERATIONS, process_photo
    from services.storage_service import (
        all_files,
        clear_media,
        list_files,
        media_folder,
        resolve_file_for_download,
        save_media_copy,
        timestamp_name,
    )
    from services.video_options import VIDEO_OPERATIONS, process_video

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)


LINKEDIN_URL = 'https://www.linkedin.com/in/your-profile'
GITHUB_URL = 'https://github.com/your-username'

ensure_directories()

app = Flask(__name__)
app.secret_key = os.environ.get('MVP_EDITOR_SECRET_KEY', 'mvp-editor-dev-secret')

COMMON_STYLE = """
<style>
    * { box-sizing: border-box; }
    body { margin: 0; font-family: Arial, sans-serif; background: #d9d9d9; color: #111; }
    .wrap { max-width: 1200px; margin: 24px auto; padding: 0 16px; }
    .panel { background: #111; color: #fff; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
    .title { margin: 0; font-size: 34px; font-weight: 800; }
    .welcome-inline { margin: 0; font-size: 26px; font-weight: 700; }
    .sub { margin-top: 8px; opacity: 0.9; }
    .topbar { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 18px; }
    .title-row { display: flex; align-items: center; gap: 20px; }
    .home-topbar { position: relative; }
    .home-welcome-center {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        margin: 0;
    }
    .menu { display: flex; gap: 10px; flex-wrap: wrap; }
    .btn, button, select, input[type='text'], input[type='file'] {
        border: 1px solid #222; border-radius: 8px; padding: 10px 12px; font-size: 14px;
    }
    .btn, button { background: #000; color: #fff; text-decoration: none; display: inline-block; cursor: pointer; }
    .btn.active { background: #fff; color: #000; }
    .btn-light { background: #fff; color: #000; border: 1px solid #555; }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .card { background: #fff; border-radius: 12px; border: 1px solid #bbb; padding: 16px; }
    .card h2, .card h3 { margin-top: 0; }
    .option-grid { display: grid; grid-template-columns: repeat(4, minmax(120px, 1fr)); gap: 10px; margin-top: 12px; }
    .list { margin: 0; padding-left: 18px; }
    .msg { padding: 10px 12px; border-radius: 8px; background: #eef3ff; border: 1px solid #c7d3ff; margin-bottom: 14px; }
    .hero { display: grid; grid-template-columns: 260px 1fr; gap: 20px; align-items: center; }
    .logo-box { background: #fff; border-radius: 12px; height: 220px; display: flex; align-items: center; justify-content: center; border: 1px solid #bbb; }
    .logo-box img { max-width: 180px; max-height: 180px; }
    .action-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; align-items: center; }
    .action-row form { margin: 0; }
    .action-row select { min-width: 220px; }
    .search-row { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 10px 0 14px; }
    .file-grid { display: grid; grid-template-columns: repeat(2, minmax(220px, 1fr)); gap: 10px; }
    .file-card { border: 1px solid #bbb; border-radius: 8px; padding: 10px; background: #fff; }
    .social-row { display: flex; gap: 12px; margin-top: 12px; }
    .icon-link {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        font-weight: 800;
        font-size: 15px;
        border: 1px solid #222;
        color: #fff;
        background: #000;
    }
    .icon-link.linkedin { background: #0a66c2; border-color: #0a66c2; }
    .icon-link.github { background: #24292f; border-color: #24292f; }
    .auth-wrap { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
    .auth-card { width: 100%; max-width: 420px; }
    .auth-logo { text-align: center; margin-bottom: 10px; }
    .auth-logo img { width: 96px; height: 96px; object-fit: contain; }
    .auth-card h1 { margin-top: 0; margin-bottom: 10px; }
    .auth-card .sub { margin-bottom: 14px; }
    .auth-card form { display: grid; gap: 10px; }
    .auth-card input[type='password'] { border: 1px solid #222; border-radius: 8px; padding: 10px 12px; font-size: 14px; }
    .password-wrap { display: grid; grid-template-columns: 1fr auto; gap: 8px; align-items: center; }
    .password-wrap input { width: 100%; border: 1px solid #222; border-radius: 8px; padding: 10px 12px; font-size: 14px; }
    .eye-btn { min-width: 48px; padding: 10px; }
    .forgot-link { text-align: right; font-size: 14px; margin-top: -4px; }
    .forgot-link a { color: #111; }
    @media (max-width: 900px) {
        .row { grid-template-columns: 1fr; }
        .option-grid { grid-template-columns: repeat(2, minmax(120px, 1fr)); }
        .hero { grid-template-columns: 1fr; }
        .file-grid { grid-template-columns: 1fr; }
    }
</style>
"""

FORGOT_PASSWORD_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MVP Editor - Forgot Password</title>
    <link rel="icon" type="image/png" href="{{ url_for('favicon') }}" />
    {{ style|safe }}
</head>
<body>
<div class="auth-wrap">
    <div class="card auth-card">
        <div class="auth-logo">
            <img src="{{ url_for('logo_asset') }}" alt="MVP Editor Logo" />
        </div>
        <h1>FORGOT PASSWORD</h1>
        <div class="msg">Please contact admin to reset your password.</div>
        <a class="btn" href="{{ url_for('signup_page') }}">Back to Sign Up</a>
    </div>
</div>
</body>
</html>
"""

LOGIN_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MVP Editor - Sign Up</title>
    <link rel="icon" type="image/png" href="{{ url_for('favicon') }}" />
    {{ style|safe }}
</head>
<body>
<div class="auth-wrap">
    <div class="card auth-card">
        <div class="auth-logo">
            <img src="{{ url_for('logo_asset') }}" alt="MVP Editor Logo" />
        </div>
        <h1>MVP EDITOR SIGN UP</h1>

        {% if message %}
        <div class="msg">{{ message }}</div>
        {% endif %}

        <form action="{{ url_for('signup_page') }}" method="post">
            <input type="email" name="email" placeholder="Enter your email" required />
            <div class="password-wrap">
                <input id="password-field" type="password" name="password" placeholder="Create password" required />
                <button class="eye-btn" id="toggle-password" type="button" aria-label="Show password" title="Show password">👁</button>
            </div>
            <div class="forgot-link">
                <a href="{{ url_for('forgot_password') }}">Forgot password?</a>
            </div>
            <button type="submit">Sign Up</button>
        </form>
    </div>
</div>
<script>
    (function () {
        var passwordField = document.getElementById('password-field');
        var toggleButton = document.getElementById('toggle-password');
        if (!passwordField || !toggleButton) return;

        toggleButton.addEventListener('click', function () {
            var isHidden = passwordField.type === 'password';
            passwordField.type = isHidden ? 'text' : 'password';
            toggleButton.textContent = isHidden ? '🙈' : '👁';
            toggleButton.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
            toggleButton.setAttribute('title', isHidden ? 'Hide password' : 'Show password');
        });
    })();
</script>
</body>
</html>
"""

HOME_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MVP Editor - Home</title>
    <link rel="icon" type="image/png" href="{{ url_for('favicon') }}" />
    {{ style|safe }}
</head>
<body>
<div class="wrap">
    <div class="panel">
        <div class="topbar home-topbar">
            <div class="title-row">
                <h1 class="title">MVP EDITOR</h1>
            </div>
            <h2 class="welcome-inline home-welcome-center">Welcome</h2>
            <div class="menu">
                <form action="{{ url_for('logout') }}" method="post" style="display:inline; margin:0;">
                    <button type="submit">LOGOUT</button>
                </form>
                <a class="btn" href="{{ url_for('activity_page') }}">ACTIVITY</a>
                <a class="btn" href="{{ url_for('help_page') }}">HELP</a>
            </div>
        </div>
    </div>

    <div class="hero">
        <div class="logo-box">
            <img src="{{ url_for('logo_asset') }}" alt="logo" />
        </div>
        <div class="card">
            <p>
                <a class="btn" href="{{ url_for('photo_page') }}">PHOTO EDITING</a>
                <a class="btn" href="{{ url_for('video_page') }}">VIDEO EDITING</a>
                <a class="btn" href="{{ url_for('team_page') }}">TEAM</a>
            </p>
            <div class="social-row">
                <a class="icon-link linkedin" href="{{ linkedin_url }}" target="_blank" rel="noopener noreferrer" title="LinkedIn">in</a>
                <a class="icon-link github" href="{{ github_url }}" target="_blank" rel="noopener noreferrer" title="GitHub">GH</a>
            </div>

            <h3 style="margin-top: 16px;">Social Connect</h3>
            <form action="{{ url_for('social_connect') }}" method="post" class="action-row">
                <select name="provider" required>
                    <option value="">Select provider</option>
                    <option value="github">GitHub</option>
                    <option value="linkedin">LinkedIn</option>
                </select>
                <input type="text" name="username" placeholder="Enter profile username" required />
                <button type="submit">Connect</button>
            </form>

            {% if social_profiles %}
            <div style="margin-top: 10px;">
                <strong>Connected Profiles:</strong>
                <ul class="list">
                    {% for provider, username in social_profiles.items() %}
                    <li>
                        {{ provider }}: {{ username }}
                        <form action="{{ url_for('social_disconnect') }}" method="post" style="display:inline; margin-left:8px;">
                            <input type="hidden" name="provider" value="{{ provider }}" />
                            <button type="submit">Disconnect</button>
                        </form>
                    </li>
                    {% endfor %}
                </ul>
            </div>
            {% else %}
            <p style="margin-top:10px;">No social profile connected yet.</p>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
"""

PHOTO_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MVP Editor - Photo</title>
    <link rel="icon" type="image/png" href="{{ url_for('favicon') }}" />
    {{ style|safe }}
</head>
<body>
<div class="wrap">
    <div class="panel">
        <div class="topbar">
            <h1 class="title">PHOTO EDITING</h1>
            <div class="menu">
                <a class="btn" href="{{ url_for('index') }}">HOME</a>
                <a class="btn" href="{{ url_for('video_page') }}">VIDEO PAGE</a>
                <a class="btn active" href="{{ url_for('photo_page') }}">PHOTO PAGE</a>
                <a class="btn" href="{{ url_for('activity_page') }}">ACTIVITY</a>
                <a class="btn" href="{{ url_for('help_page') }}">HELP</a>
            </div>
        </div>
        <p class="sub">Select an option and process your photo.</p>
    </div>

    {% if message %}
    <div class="msg">{{ message }}</div>
    {% endif %}

    <div class="row">
        <div class="card">
            <h2>Upload Photo</h2>
            <form action="{{ url_for('web_upload_photo') }}" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required />
                <button type="submit">Add Photo</button>
            </form>

            <h3 style="margin-top: 20px;">Process Options</h3>
            <form action="{{ url_for('web_process_photo') }}" method="post">
                <select name="filename" required>
                    <option value="">Select a photo</option>
                    {% for item in uploaded %}
                    <option value="{{ item }}">{{ item }}</option>
                    {% endfor %}
                </select>
                <div class="option-grid">
                    <button class="btn-light" type="submit" name="operation" value="crop">✂ Crop</button>
                    <button class="btn-light" type="submit" name="operation" value="rotate">🔄 Rotate</button>
                    <button class="btn-light" type="submit" name="operation" value="filters">🎨 Filters</button>
                    <button class="btn-light" type="submit" name="operation" value="brightness">✨ Brightness</button>
                    <button class="btn-light" type="submit" name="operation" value="resize">🔍 Resize</button>
                    <button class="btn-light" type="submit" name="operation" value="export">💾 Export</button>
                    <button class="btn-light" type="submit" name="operation" value="undo">← Undo</button>
                    <button class="btn-light" type="submit" name="operation" value="redo">→ Redo</button>
                </div>
            </form>

            <div class="action-row">
                <form action="{{ url_for('web_photo_download_selected') }}" method="post">
                    <select name="filename" required>
                        <option value="">Select file for download</option>
                        {% for item in all_files %}
                        <option value="{{ item }}">{{ item }}</option>
                        {% endfor %}
                    </select>
                    <button type="submit">Download</button>
                </form>

                <form action="{{ url_for('web_photo_save') }}" method="post">
                    <select name="filename" required>
                        <option value="">Select file for save</option>
                        {% for item in all_files %}
                        <option value="{{ item }}">{{ item }}</option>
                        {% endfor %}
                    </select>
                    <button type="submit">Save</button>
                </form>

                <form action="{{ url_for('web_photo_clear') }}" method="post">
                    <button type="submit">Clear</button>
                </form>

                <a class="btn" href="{{ url_for('index') }}">Back to Menu</a>
            </div>
        </div>

        <div class="card">
            <h2>Uploaded Photos</h2>
            <form method="get" action="{{ url_for('photo_page') }}" class="search-row">
                <input type="text" name="q" value="{{ q }}" placeholder="Search photo file" />
                <select name="view">
                    <option value="list" {% if view == 'list' %}selected{% endif %}>List View</option>
                    <option value="grid" {% if view == 'grid' %}selected{% endif %}>Grid View</option>
                </select>
                <button type="submit">Apply</button>
            </form>

            {% if uploaded %}
            {% if view == 'grid' %}
            <div class="file-grid">
                {% for item in uploaded %}
                <div class="file-card">
                    <strong>{{ item }}</strong><br />
                    <a href="{{ url_for('web_download', media='photo', filename=item) }}">download</a>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <ul class="list">
                {% for item in uploaded %}
                <li>{{ item }} - <a href="{{ url_for('web_download', media='photo', filename=item) }}">download</a></li>
                {% endfor %}
            </ul>
            {% endif %}
            {% else %}
            <p>No uploaded photos.</p>
            {% endif %}

            <h2 style="margin-top: 20px;">Processed Photos</h2>
            {% if processed %}
            {% if view == 'grid' %}
            <div class="file-grid">
                {% for item in processed %}
                <div class="file-card">
                    <strong>{{ item }}</strong><br />
                    <a href="{{ url_for('web_download', media='photo', filename=item) }}">download</a>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <ul class="list">
                {% for item in processed %}
                <li>{{ item }} - <a href="{{ url_for('web_download', media='photo', filename=item) }}">download</a></li>
                {% endfor %}
            </ul>
            {% endif %}
            {% else %}
            <p>No processed photos.</p>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
"""

VIDEO_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MVP Editor - Video</title>
    <link rel="icon" type="image/png" href="{{ url_for('favicon') }}" />
    {{ style|safe }}
</head>
<body>
<div class="wrap">
    <div class="panel">
        <div class="topbar">
            <h1 class="title">VIDEO EDITING</h1>
            <div class="menu">
                <a class="btn" href="{{ url_for('index') }}">HOME</a>
                <a class="btn active" href="{{ url_for('video_page') }}">VIDEO PAGE</a>
                <a class="btn" href="{{ url_for('photo_page') }}">PHOTO PAGE</a>
                <a class="btn" href="{{ url_for('activity_page') }}">ACTIVITY</a>
                <a class="btn" href="{{ url_for('help_page') }}">HELP</a>
            </div>
        </div>
        <p class="sub">Choose video options similar to your old output.</p>
    </div>

    {% if message %}
    <div class="msg">{{ message }}</div>
    {% endif %}

    <div class="row">
        <div class="card">
            <h2>Upload Video</h2>
            <form action="{{ url_for('web_upload_video') }}" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required />
                <button type="submit">Add Video</button>
            </form>

            <h3 style="margin-top: 20px;">Process Options</h3>
            <form action="{{ url_for('web_process_video') }}" method="post">
                <select name="filename" required>
                    <option value="">Select a video</option>
                    {% for item in uploaded %}
                    <option value="{{ item }}">{{ item }}</option>
                    {% endfor %}
                </select>
                <div class="option-grid">
                    <button class="btn-light" type="submit" name="operation" value="trim">✂ Trim</button>
                    <button class="btn-light" type="submit" name="operation" value="cut">🎬 Cut</button>
                    <button class="btn-light" type="submit" name="operation" value="split">🎞 Split</button>
                    <button class="btn-light" type="submit" name="operation" value="audio">🔊 Audio</button>
                    <button class="btn-light" type="submit" name="operation" value="effects">🎨 Effects</button>
                    <button class="btn-light" type="submit" name="operation" value="transitions">⚡ Transitions</button>
                    <button class="btn-light" type="submit" name="operation" value="music">🎵 Music</button>
                    <button class="btn-light" type="submit" name="operation" value="export">💾 Export</button>
                    <button class="btn-light" type="submit" name="operation" value="undo">← Undo</button>
                    <button class="btn-light" type="submit" name="operation" value="redo">→ Redo</button>
                    <button class="btn-light" type="submit" name="operation" value="settings">⚙ Settings</button>
                    <button class="btn-light" type="submit" name="operation" value="preview">📊 Preview</button>
                </div>
            </form>

            <div class="action-row">
                <form action="{{ url_for('web_video_download_selected') }}" method="post">
                    <select name="filename" required>
                        <option value="">Select file for download</option>
                        {% for item in all_files %}
                        <option value="{{ item }}">{{ item }}</option>
                        {% endfor %}
                    </select>
                    <button type="submit">Download</button>
                </form>

                <form action="{{ url_for('web_video_save') }}" method="post">
                    <select name="filename" required>
                        <option value="">Select file for save</option>
                        {% for item in all_files %}
                        <option value="{{ item }}">{{ item }}</option>
                        {% endfor %}
                    </select>
                    <button type="submit">Save</button>
                </form>

                <form action="{{ url_for('web_video_clear') }}" method="post">
                    <button type="submit">Clear</button>
                </form>

                <a class="btn" href="{{ url_for('index') }}">Back to Menu</a>
            </div>
        </div>

        <div class="card">
            <h2>Uploaded Videos</h2>
            <form method="get" action="{{ url_for('video_page') }}" class="search-row">
                <input type="text" name="q" value="{{ q }}" placeholder="Search video file" />
                <select name="view">
                    <option value="list" {% if view == 'list' %}selected{% endif %}>List View</option>
                    <option value="grid" {% if view == 'grid' %}selected{% endif %}>Grid View</option>
                </select>
                <button type="submit">Apply</button>
            </form>

            {% if uploaded %}
            {% if view == 'grid' %}
            <div class="file-grid">
                {% for item in uploaded %}
                <div class="file-card">
                    <strong>{{ item }}</strong><br />
                    <a href="{{ url_for('web_download', media='video', filename=item) }}">download</a>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <ul class="list">
                {% for item in uploaded %}
                <li>{{ item }} - <a href="{{ url_for('web_download', media='video', filename=item) }}">download</a></li>
                {% endfor %}
            </ul>
            {% endif %}
            {% else %}
            <p>No uploaded videos.</p>
            {% endif %}

            <h2 style="margin-top: 20px;">Processed Videos</h2>
            {% if processed %}
            {% if view == 'grid' %}
            <div class="file-grid">
                {% for item in processed %}
                <div class="file-card">
                    <strong>{{ item }}</strong><br />
                    <a href="{{ url_for('web_download', media='video', filename=item) }}">download</a>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <ul class="list">
                {% for item in processed %}
                <li>{{ item }} - <a href="{{ url_for('web_download', media='video', filename=item) }}">download</a></li>
                {% endfor %}
            </ul>
            {% endif %}
            {% else %}
            <p>No processed videos.</p>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
"""

HELP_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MVP Editor - Help</title>
    <link rel="icon" type="image/png" href="{{ url_for('favicon') }}" />
    {{ style|safe }}
</head>
<body>
<div class="wrap">
    <div class="panel">
        <div class="topbar">
            <h1 class="title">HELP</h1>
            <div class="menu">
                <a class="btn" href="{{ url_for('index') }}">HOME</a>
                <a class="btn" href="{{ url_for('photo_page') }}">PHOTO</a>
                <a class="btn" href="{{ url_for('video_page') }}">VIDEO</a>
                <a class="btn" href="{{ url_for('activity_page') }}">ACTIVITY</a>
            </div>
        </div>
        <p class="sub">User guide</p>
    </div>

    <div class="card">
        <h2>Quick Steps</h2>
        <ol>
            <li>Open Photo Editing or Video Editing from Home.</li>
            <li>Upload file with Add Photo / Add Video.</li>
            <li>Select file, then click one option button.</li>
            <li>Download result from processed list.</li>
        </ol>

        <h2 style="margin-top:18px;">Event Attachment Demo</h2>
        <p>Attach multiple events to elements in this page.</p>
        <div class="action-row">
            <button id="q9-click-btn" type="button">Click Event</button>
            <button id="q9-dblclick-btn" type="button">Double Click Event</button>
            <input id="q9-input" type="text" placeholder="Type to trigger keyup" />
            <select id="q9-select">
                <option value="">Select event option</option>
                <option value="photo">Photo</option>
                <option value="video">Video</option>
            </select>
            <div id="q9-hover-box" class="file-card" style="min-width:220px;">Hover over this box</div>
        </div>
        <div id="q9-output" class="msg" style="margin-top:10px;">Waiting for event...</div>

        <script>
            (function () {
                var output = document.getElementById('q9-output');
                var clickBtn = document.getElementById('q9-click-btn');
                var dblClickBtn = document.getElementById('q9-dblclick-btn');
                var input = document.getElementById('q9-input');
                var select = document.getElementById('q9-select');
                var hoverBox = document.getElementById('q9-hover-box');

                if (!output) return;

                clickBtn.addEventListener('click', function () {
                    output.textContent = 'Click event triggered on Click Event button';
                });
                dblClickBtn.addEventListener('dblclick', function () {
                    output.textContent = 'Double click event triggered on Double Click Event button';
                });
                input.addEventListener('keyup', function () {
                    output.textContent = 'Keyup event triggered, typed value = ' + input.value;
                });
                select.addEventListener('change', function () {
                    output.textContent = 'Change event triggered, selected = ' + select.value;
                });
                hoverBox.addEventListener('mouseenter', function () {
                    output.textContent = 'Mouse enter event triggered on hover box';
                });
                hoverBox.addEventListener('mouseleave', function () {
                    output.textContent = 'Mouse leave event triggered on hover box';
                });
            })();
        </script>

        <h3 style="margin-top:14px;">Social</h3>
        <p>
            <a class="btn" href="https://github.com" target="_blank">GitHub</a>
            <a class="btn" href="https://www.linkedin.com" target="_blank">LinkedIn</a>
        </p>

        <h2 style="margin-top:18px;">Effects Demo</h2>
        <p>Run fade, slide, and animation effects on the demo box.</p>
        <div class="action-row">
            <button id="q10-fadeout" type="button">Fade Out</button>
            <button id="q10-fadein" type="button">Fade In</button>
            <button id="q10-slidetoggle" type="button">Slide Toggle</button>
            <button id="q10-animate" type="button">Animate</button>
        </div>
        <div id="q10-box" class="file-card" style="width: 220px; margin-top: 10px; position: relative;">Effects box</div>

        <script>
            (function () {
                var box = document.getElementById('q10-box');
                var fadeOutBtn = document.getElementById('q10-fadeout');
                var fadeInBtn = document.getElementById('q10-fadein');
                var slideToggleBtn = document.getElementById('q10-slidetoggle');
                var animateBtn = document.getElementById('q10-animate');
                var shown = true;

                if (!box) return;

                box.style.transition = 'opacity 0.3s ease, transform 0.25s ease';

                fadeOutBtn.addEventListener('click', function () {
                    box.style.opacity = '0';
                    box.style.pointerEvents = 'none';
                });

                fadeInBtn.addEventListener('click', function () {
                    box.style.opacity = '1';
                    box.style.pointerEvents = 'auto';
                });

                slideToggleBtn.addEventListener('click', function () {
                    shown = !shown;
                    box.style.transform = shown ? 'translateY(0px)' : 'translateY(-12px)';
                    box.style.opacity = shown ? '1' : '0';
                });

                animateBtn.addEventListener('click', function () {
                    box.style.transform = 'translateX(30px)';
                    box.style.opacity = '0.6';
                    setTimeout(function () {
                        box.style.transform = 'translateX(0px)';
                        box.style.opacity = '1';
                    }, 180);
                });
            })();
        </script>
    </div>
</div>
</body>
</html>
"""

TEAM_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MVP Editor - Team</title>
    <link rel="icon" type="image/png" href="{{ url_for('favicon') }}" />
    {{ style|safe }}
</head>
<body>
<div class="wrap">
    <div class="panel">
        <div class="topbar">
            <h1 class="title">TEAM ENLIST</h1>
            <div class="menu">
                <a class="btn" href="{{ url_for('index') }}">HOME</a>
                <a class="btn" href="{{ url_for('photo_page') }}">PHOTO</a>
                <a class="btn" href="{{ url_for('video_page') }}">VIDEO</a>
                <a class="btn active" href="{{ url_for('team_page') }}">TEAM</a>
                <a class="btn" href="{{ url_for('help_page') }}">HELP</a>
            </div>
        </div>
        <p class="sub">Full-stack module to enlist editor team members.</p>
    </div>

    {% if message %}
    <div class="msg">{{ message }}</div>
    {% endif %}

    <div class="row">
        <div class="card">
            <h2>Add Member</h2>
            <form action="{{ url_for('team_page') }}" method="post" style="display:grid; gap:10px;">
                <input type="text" name="name" placeholder="Member name" required />
                <input type="text" name="role" placeholder="Role (Editor, Designer, QA...)" required />
                <button type="submit">Add Member</button>
            </form>
        </div>

        <div class="card">
            <h2>Team List</h2>
            {% if members %}
            <ul class="list">
                {% for item in members %}
                <li>
                    #{{ item.id }} - {{ item.name }} ({{ item.role }}) - {{ item.created_at }}
                    <form action="{{ url_for('team_delete', member_id=item.id) }}" method="post" style="display:inline; margin-left:8px;">
                        <button type="submit">Delete</button>
                    </form>
                </li>
                {% endfor %}
            </ul>
            {% else %}
            <p>No members yet.</p>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
"""

ACTIVITY_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>MVP Editor - Activity</title>
    <link rel="icon" type="image/png" href="{{ url_for('favicon') }}" />
    {{ style|safe }}
</head>
<body>
<div class="wrap">
    <div class="panel">
        <div class="topbar">
            <h1 class="title">PAST ACTIVITY TODAY</h1>
            <div class="menu">
                <a class="btn" href="{{ url_for('index') }}">HOME</a>
                <a class="btn" href="{{ url_for('photo_page') }}">PHOTO</a>
                <a class="btn" href="{{ url_for('video_page') }}">VIDEO</a>
                <a class="btn active" href="{{ url_for('activity_page') }}">ACTIVITY</a>
                <a class="btn" href="{{ url_for('help_page') }}">HELP</a>
            </div>
        </div>
        <p class="sub">Activity log for {{ today_label }}</p>
    </div>

    <div class="card">
        <h2>Today Events</h2>
        <form method="get" action="{{ url_for('activity_page') }}" class="search-row">
            <input type="text" name="q" value="{{ q }}" placeholder="Search event, filename, operation" />
            <select name="view">
                <option value="list" {% if view == 'list' %}selected{% endif %}>List View</option>
                <option value="grid" {% if view == 'grid' %}selected{% endif %}>Grid View</option>
            </select>
            <button type="submit">Apply</button>
        </form>

        {% if activities %}
        {% if view == 'grid' %}
        <div class="file-grid">
            {% for item in activities %}
            <div class="file-card">
                <strong>{{ item.event_type }}</strong><br />
                file: {{ item.filename }}<br />
                op: {{ item.operation }}<br />
                time: {{ item.created_at }}
            </div>
            {% endfor %}
        </div>
        {% else %}
        <ul class="list">
            {% for item in activities %}
            <li>{{ item.created_at }} - {{ item.event_type }} - file: {{ item.filename }} - op: {{ item.operation }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        {% else %}
        <p>No activity found for today.</p>
        {% endif %}
    </div>
</div>
</body>
</html>
"""

def _log_event(event_type, filename=None, operation=None):
    log_event(event_type, filename=filename, operation=operation)


def _today_activities(query=''):
    return today_activities(query)


def _timestamp_name(filename):
    return timestamp_name(filename)


def _list_files(media, processed=False):
    return list_files(media, processed=processed)


def _all_files(media):
    return all_files(media)


def _resolve_file_for_download(media, filename):
    return resolve_file_for_download(media, filename)


def _clear_media(media):
    return clear_media(media)


def _save_media_copy(media, filename):
    return save_media_copy(media, filename)


init_db()
init_member_db()


def _is_logged_in():
    return bool(session.get('logged_in'))


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        password = (request.form.get('password') or '').strip()
        if not email or '@' not in email or '.' not in email or not password:
            return render_template_string(LOGIN_TEMPLATE, style=COMMON_STYLE, message='Please enter a valid email and password.')
        session['logged_in'] = True
        return redirect(url_for('index'))

    if _is_logged_in():
        return redirect(url_for('index'))

    return render_template_string(LOGIN_TEMPLATE, style=COMMON_STYLE, message='')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('signup_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page_redirect():
    if request.method == 'POST':
        return redirect(url_for('signup_page'), code=307)
    return redirect(url_for('signup_page'))


@app.route('/forgot-password', methods=['GET'])
def forgot_password():
    return render_template_string(FORGOT_PASSWORD_TEMPLATE, style=COMMON_STYLE)


@app.route('/assets/logo')
def logo_asset():
    logo_path = os.path.join(FRONTEND_DIR, 'logo.png')
    if os.path.exists(logo_path):
        return send_from_directory(FRONTEND_DIR, 'logo.png')
    return jsonify({'success': False, 'error': 'logo not found'}), 404


@app.route('/favicon.ico')
def favicon():
    logo_path = os.path.join(FRONTEND_DIR, 'logo.png')
    if os.path.exists(logo_path):
        return send_from_directory(FRONTEND_DIR, 'logo.png', mimetype='image/png')
    return '', 204


@app.route('/')
def index():
    if not _is_logged_in():
        return redirect(url_for('signup_page'))
    return render_template_string(
        HOME_TEMPLATE,
        style=COMMON_STYLE,
        linkedin_url=LINKEDIN_URL,
        github_url=GITHUB_URL,
        social_profiles=session.get('social_profiles', {}),
    )


@app.route('/social/connect', methods=['POST'])
def social_connect():
    if not _is_logged_in():
        return redirect(url_for('signup_page'))

    provider = (request.form.get('provider') or '').strip().lower()
    username = (request.form.get('username') or '').strip()
    if provider not in ('github', 'linkedin') or not username:
        return redirect(url_for('index'))

    social_profiles = session.get('social_profiles', {})
    social_profiles[provider] = username
    session['social_profiles'] = social_profiles
    _log_event('social_connect', filename=username, operation=provider)
    return redirect(url_for('index'))


@app.route('/social/disconnect', methods=['POST'])
def social_disconnect():
    if not _is_logged_in():
        return redirect(url_for('signup_page'))

    provider = (request.form.get('provider') or '').strip().lower()
    social_profiles = session.get('social_profiles', {})
    if provider in social_profiles:
        removed = social_profiles.pop(provider)
        session['social_profiles'] = social_profiles
        _log_event('social_disconnect', filename=removed, operation=provider)
    return redirect(url_for('index'))


@app.route('/photo')
def photo_page():
    if not _is_logged_in():
        return redirect(url_for('signup_page'))
    q = (request.args.get('q') or '').strip()
    view = (request.args.get('view') or 'list').strip().lower()
    if view not in ('list', 'grid'):
        view = 'list'

    uploaded = _list_files('photo', processed=False)
    processed = _list_files('photo', processed=True)
    if q:
        uploaded = [item for item in uploaded if q.lower() in item.lower()]
        processed = [item for item in processed if q.lower() in item.lower()]

    return render_template_string(
        PHOTO_TEMPLATE,
        style=COMMON_STYLE,
        uploaded=uploaded,
        processed=processed,
        all_files=_all_files('photo'),
        q=q,
        view=view,
        message=request.args.get('message', ''),
    )


@app.route('/video')
def video_page():
    if not _is_logged_in():
        return redirect(url_for('signup_page'))
    q = (request.args.get('q') or '').strip()
    view = (request.args.get('view') or 'list').strip().lower()
    if view not in ('list', 'grid'):
        view = 'list'

    uploaded = _list_files('video', processed=False)
    processed = _list_files('video', processed=True)
    if q:
        uploaded = [item for item in uploaded if q.lower() in item.lower()]
        processed = [item for item in processed if q.lower() in item.lower()]

    return render_template_string(
        VIDEO_TEMPLATE,
        style=COMMON_STYLE,
        uploaded=uploaded,
        processed=processed,
        all_files=_all_files('video'),
        q=q,
        view=view,
        message=request.args.get('message', ''),
    )


@app.route('/help')
def help_page():
    if not _is_logged_in():
        return redirect(url_for('signup_page'))
    return render_template_string(HELP_TEMPLATE, style=COMMON_STYLE)


@app.route('/activity')
def activity_page():
    if not _is_logged_in():
        return redirect(url_for('signup_page'))

    q = (request.args.get('q') or '').strip()
    view = (request.args.get('view') or 'list').strip().lower()
    if view not in ('list', 'grid'):
        view = 'list'

    return render_template_string(
        ACTIVITY_TEMPLATE,
        style=COMMON_STYLE,
        activities=_today_activities(q),
        q=q,
        view=view,
        today_label=time.strftime('%Y-%m-%d'),
    )


@app.route('/team', methods=['GET', 'POST'])
def team_page():
    if not _is_logged_in():
        return redirect(url_for('signup_page'))

    message = (request.args.get('message') or '').strip()
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        role = (request.form.get('role') or '').strip()
        if name and role:
            add_member(name, role)
            _log_event('team_add_member', filename=name, operation=role)
            message = f'Added member: {name}'
        else:
            message = 'Please provide member name and role.'

    return render_template_string(
        TEAM_TEMPLATE,
        style=COMMON_STYLE,
        members=list_members(),
        message=message,
    )


@app.route('/team/delete/<int:member_id>', methods=['POST'])
def team_delete(member_id):
    if not _is_logged_in():
        return redirect(url_for('signup_page'))

    if delete_member(member_id):
        _log_event('team_delete_member', filename=f'id={member_id}', operation='delete')
        return redirect(url_for('team_page', message='Member deleted'))
    return redirect(url_for('team_page', message='Member not found'))


@app.route('/web/download/<media>/<path:filename>', methods=['GET'])
def web_download(media, filename):
    if media not in ('photo', 'video'):
        return jsonify({'success': False, 'error': 'invalid media type'}), 400
    root = _resolve_file_for_download(media, filename)
    if root:
        return send_from_directory(root, filename, as_attachment=True)
    return jsonify({'success': False, 'error': 'file not found'}), 404


@app.route('/web/photo/upload', methods=['POST'])
def web_upload_photo():
    if 'file' not in request.files:
        return redirect(url_for('photo_page', message='Upload failed: no file part.'))
    file_data = request.files['file']
    if file_data.filename == '':
        return redirect(url_for('photo_page', message='Upload failed: no selected file.'))
    name = _timestamp_name(file_data.filename)
    dest = os.path.join(UPLOAD_DIR, 'photos', name)
    file_data.save(dest)
    _log_event('upload_photo', filename=name)
    return redirect(url_for('photo_page', message=f'Uploaded: {name}'))


@app.route('/web/photo/process', methods=['POST'])
def web_process_photo():
    filename = (request.form.get('filename') or '').strip()
    operation = (request.form.get('operation') or 'rotate').strip()
    if not filename:
        return redirect(url_for('photo_page', message='Process failed: no filename provided.'))
    response = process_photo(filename, operation)
    if response.get('success'):
        processed_name = response['processed_filename']
        _log_event('process_photo', filename=processed_name, operation=operation)
        return redirect(url_for('photo_page', message=f'Processed with {operation}: {processed_name}'))
    return redirect(url_for('photo_page', message=f"Process failed: {response.get('error', 'unknown error')}"))


@app.route('/web/photo/download', methods=['POST'])
def web_photo_download_selected():
    filename = (request.form.get('filename') or '').strip()
    if not filename:
        return redirect(url_for('photo_page', message='Download failed: choose a file.'))
    return redirect(url_for('web_download', media='photo', filename=filename))


@app.route('/web/photo/save', methods=['POST'])
def web_photo_save():
    filename = (request.form.get('filename') or '').strip()
    if not filename:
        return redirect(url_for('photo_page', message='Save failed: choose a file.'))
    try:
        saved_name = _save_media_copy('photo', filename)
        if not saved_name:
            return redirect(url_for('photo_page', message='Save failed: file not found.'))
        _log_event('save_photo', filename=saved_name)
        return redirect(url_for('photo_page', message=f'Saved: {saved_name}'))
    except Exception as exc:
        return redirect(url_for('photo_page', message=f'Save failed: {str(exc)}'))


@app.route('/web/photo/clear', methods=['POST'])
def web_photo_clear():
    removed = _clear_media('photo')
    _log_event('clear_photo', operation='clear_all')
    return redirect(url_for('photo_page', message=f'Cleared photos: {removed} file(s) removed.'))


@app.route('/web/video/upload', methods=['POST'])
def web_upload_video():
    if 'file' not in request.files:
        return redirect(url_for('video_page', message='Upload failed: no file part.'))
    file_data = request.files['file']
    if file_data.filename == '':
        return redirect(url_for('video_page', message='Upload failed: no selected file.'))
    name = _timestamp_name(file_data.filename)
    dest = os.path.join(UPLOAD_DIR, 'videos', name)
    file_data.save(dest)
    _log_event('upload_video', filename=name)
    return redirect(url_for('video_page', message=f'Uploaded: {name}'))


@app.route('/web/video/process', methods=['POST'])
def web_process_video():
    filename = (request.form.get('filename') or '').strip()
    operation = (request.form.get('operation') or 'trim').strip()
    if not filename:
        return redirect(url_for('video_page', message='Process failed: no filename provided.'))
    response = process_video(filename, operation)
    if response.get('success'):
        processed_name = response['processed_filename']
        _log_event('process_video', filename=processed_name, operation=operation)
        return redirect(url_for('video_page', message=f'Processed with {operation}: {processed_name}'))
    return redirect(url_for('video_page', message=f"Process failed: {response.get('error', 'unknown error')}"))


@app.route('/web/video/download', methods=['POST'])
def web_video_download_selected():
    filename = (request.form.get('filename') or '').strip()
    if not filename:
        return redirect(url_for('video_page', message='Download failed: choose a file.'))
    return redirect(url_for('web_download', media='video', filename=filename))


@app.route('/web/video/save', methods=['POST'])
def web_video_save():
    filename = (request.form.get('filename') or '').strip()
    if not filename:
        return redirect(url_for('video_page', message='Save failed: choose a file.'))
    try:
        saved_name = _save_media_copy('video', filename)
        if not saved_name:
            return redirect(url_for('video_page', message='Save failed: file not found.'))
        _log_event('save_video', filename=saved_name)
        return redirect(url_for('video_page', message=f'Saved: {saved_name}'))
    except Exception as exc:
        return redirect(url_for('video_page', message=f'Save failed: {str(exc)}'))


@app.route('/web/video/clear', methods=['POST'])
def web_video_clear():
    removed = _clear_media('video')
    _log_event('clear_video', operation='clear_all')
    return redirect(url_for('video_page', message=f'Cleared videos: {removed} file(s) removed.'))


@app.route('/api/photos', methods=['GET'])
def list_photos():
    items = []
    for filename in _list_files('photo', processed=False):
        path = os.path.join(UPLOAD_DIR, 'photos', filename)
        items.append({'filename': filename, 'size': os.path.getsize(path)})
    return jsonify({'success': True, 'photos': items})


@app.route('/api/videos', methods=['GET'])
def list_videos():
    items = []
    for filename in _list_files('video', processed=False):
        path = os.path.join(UPLOAD_DIR, 'videos', filename)
        items.append({'filename': filename, 'size': os.path.getsize(path)})
    return jsonify({'success': True, 'videos': items})


@app.route('/api/upload', methods=['POST'])
def upload_photo_api():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'no file part'}), 400
    file_data = request.files['file']
    if file_data.filename == '':
        return jsonify({'success': False, 'error': 'no selected file'}), 400
    name = _timestamp_name(file_data.filename)
    dest = os.path.join(UPLOAD_DIR, 'photos', name)
    file_data.save(dest)
    _log_event('upload_photo', filename=name)
    return jsonify({'success': True, 'filename': name})


@app.route('/api/upload-video', methods=['POST'])
def upload_video_api():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'no file part'}), 400
    file_data = request.files['file']
    if file_data.filename == '':
        return jsonify({'success': False, 'error': 'no selected file'}), 400
    name = _timestamp_name(file_data.filename)
    dest = os.path.join(UPLOAD_DIR, 'videos', name)
    file_data.save(dest)
    _log_event('upload_video', filename=name)
    return jsonify({'success': True, 'filename': name})


@app.route('/api/process', methods=['POST'])
def process_photo_api():
    data = request.get_json() or {}
    filename = data.get('filename')
    operation = data.get('operation', 'none')
    if not filename:
        return jsonify({'success': False, 'error': 'no filename provided'}), 400
    response = process_photo(filename, operation)
    if response.get('success'):
        _log_event('process_photo', filename=response['processed_filename'], operation=operation)
        return jsonify(response)
    error = response.get('error', 'unknown error')
    status_code = 404 if error == 'file not found' else 400
    return jsonify({'success': False, 'error': error}), status_code


@app.route('/api/process-video', methods=['POST'])
def process_video_api():
    data = request.get_json() or {}
    filename = data.get('filename')
    operation = data.get('operation', 'trim')
    if not filename:
        return jsonify({'success': False, 'error': 'no filename provided'}), 400
    response = process_video(filename, operation)
    if response.get('success'):
        _log_event('process_video', filename=response['processed_filename'], operation=operation)
        return jsonify(response)
    error = response.get('error', 'unknown error')
    status_code = 404 if error == 'file not found' else 400
    return jsonify({'success': False, 'error': error}), status_code


@app.route('/api/options', methods=['GET'])
def options_api():
    return jsonify(
        {
            'success': True,
            'photo': sorted(PHOTO_OPERATIONS),
            'video': sorted(VIDEO_OPERATIONS),
        }
    )


@app.route('/api/media/<media>/files', methods=['GET'])
def media_files_api(media):
    media = (media or '').strip().lower()
    if media not in ('photo', 'video'):
        return jsonify({'success': False, 'error': 'invalid media type'}), 400

    uploaded = _list_files(media, processed=False)
    processed = _list_files(media, processed=True)
    return jsonify({'success': True, 'uploaded': uploaded, 'processed': processed, 'all_files': _all_files(media)})


@app.route('/api/media/<media>/clear', methods=['POST'])
def media_clear_api(media):
    media = (media or '').strip().lower()
    if media not in ('photo', 'video'):
        return jsonify({'success': False, 'error': 'invalid media type'}), 400

    removed = _clear_media(media)
    _log_event(f'clear_{media}', operation='clear_all')
    return jsonify({'success': True, 'removed': removed})


@app.route('/api/media/<media>/save', methods=['POST'])
def media_save_api(media):
    media = (media or '').strip().lower()
    if media not in ('photo', 'video'):
        return jsonify({'success': False, 'error': 'invalid media type'}), 400

    data = request.get_json() or {}
    filename = (data.get('filename') or '').strip()
    if not filename:
        return jsonify({'success': False, 'error': 'no filename provided'}), 400

    saved_name = _save_media_copy(media, filename)
    if not saved_name:
        return jsonify({'success': False, 'error': 'file not found'}), 404

    _log_event(f'save_{media}', filename=saved_name)
    return jsonify({'success': True, 'saved_filename': saved_name})


@app.route('/api/download/<media>/<path:filename>', methods=['GET'])
def download_by_media_api(media, filename):
    media = (media or '').strip().lower()
    if media not in ('photo', 'video'):
        return jsonify({'success': False, 'error': 'invalid media type'}), 400

    root = _resolve_file_for_download(media, filename)
    if root:
        return send_from_directory(root, filename, as_attachment=True)
    return jsonify({'success': False, 'error': 'file not found'}), 404


@app.route('/api/download/<path:filename>', methods=['GET'])
def download(filename):
    for media in ('photo', 'video'):
        root = _resolve_file_for_download(media, filename)
        if root:
            return send_from_directory(root, filename, as_attachment=True)
    return jsonify({'success': False, 'error': 'file not found'}), 404


@app.route('/api/team', methods=['GET', 'POST'])
def api_team():
    if request.method == 'GET':
        return jsonify({'success': True, 'members': list_members()})

    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    role = (data.get('role') or '').strip()
    if not name or not role:
        return jsonify({'success': False, 'error': 'name and role are required'}), 400

    member_id = add_member(name, role)
    _log_event('team_add_member', filename=name, operation=role)
    return jsonify({'success': True, 'id': member_id, 'name': name, 'role': role})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
