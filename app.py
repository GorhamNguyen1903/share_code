from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Đường dẫn đến file lưu nội dung
CONTENT_FILE = 'content.txt'

# Đảm bảo file tồn tại
if not os.path.exists(CONTENT_FILE):
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        f.write('')

def read_content():
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return ""

def write_content(content):
    try:
        with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Lỗi khi ghi file: {e}")
        return False

@app.route('/')
def index():
    content = read_content()
    return render_template('index.html', content=content)

@app.route('/update', methods=['POST'])
def update():
    content = request.form.get('content', '')
    success = write_content(content)
    
    if success:
        # Phát sóng nội dung mới đến tất cả các kết nối
        socketio.emit('content_update', {'content': content})
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Không thể cập nhật nội dung'}), 500

@app.route('/api/update', methods=['POST'])
def api_update():
    """API endpoint cho máy A gửi nội dung lên"""
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'success': False, 'error': 'Dữ liệu không hợp lệ'}), 400
    
    content = data['content']
    success = write_content(content)
    
    if success:
        # Phát sóng nội dung mới đến tất cả các kết nối
        socketio.emit('content_update', {'content': content})
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Không thể cập nhật nội dung'}), 500

@socketio.on('connect')
def handle_connect():
    # Khi có kết nối mới, gửi nội dung hiện tại
    content = read_content()
    socketio.emit('content_update', {'content': content}, room=request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True)