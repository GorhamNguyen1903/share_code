import requests
import json
import sys
import os

def send_content(server_url, content):
    """
    Gửi nội dung lên server
    
    Args:
        server_url (str): URL của API endpoint (ví dụ: http://192.168.1.100:5000/api/update)
        content (str): Nội dung cần gửi
    
    Returns:
        bool: True nếu gửi thành công, False nếu có lỗi
    """
    try:
        headers = {'Content-Type': 'application/json'}
        data = {'content': content}
        
        response = requests.post(server_url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("Đã gửi nội dung thành công!")
                return True
            else:
                print(f"Lỗi: {result.get('error', 'Không xác định')}")
                return False
        else:
            print(f"Lỗi HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
        return False

def read_file(file_path):
    """Đọc nội dung từ file với encoding UTF-8"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return None

if __name__ == "__main__":
    # Mặc định URL của server
    server_url = "http://localhost:5000/api/update"
    
    if len(sys.argv) < 2:
        print("Sử dụng: python client.py <đường_dẫn_file> [url_server]")
        print("Ví dụ: python client.py my_code.py http://192.168.1.100:5000/api/update")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # Nếu có tham số thứ 2, sử dụng làm server URL
    if len(sys.argv) >= 3:
        server_url = sys.argv[2]
    
    # Kiểm tra file tồn tại
    if not os.path.exists(file_path):
        print(f"File không tồn tại: {file_path}")
        sys.exit(1)
    
    # Đọc nội dung file
    content = read_file(file_path)
    if content is None:
        sys.exit(1)
    
    # Gửi nội dung lên server
    if send_content(server_url, content):
        print(f"Nội dung từ file '{file_path}' đã được gửi thành công lên {server_url}")
    else:
        print("Không thể gửi nội dung lên server.")