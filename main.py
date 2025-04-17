import os
import qrcode
from PIL import Image

def ensure_dirs():
    os.makedirs('traffic_signs', exist_ok=True)
    os.makedirs('qr_codes', exist_ok=True)

# توليد رمز QR لكل صورة في مجلد traffic_signs
# رمز QR يحتوي على اسم الصورة فقط (محلي)
def generate_qr_for_signs():
    signs_dir = 'traffic_signs'
    qr_dir = 'qr_codes'
    for filename in os.listdir(signs_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # محتوى الـQR هو اسم الصورة فقط
            qr_content = filename
            qr_img = qrcode.make(qr_content)
            qr_img.save(os.path.join(qr_dir, f'{os.path.splitext(filename)[0]}_qr.png'))
            print(f'Generated QR for {filename}')

if __name__ == '__main__':
    ensure_dirs()
    print('تم إنشاء مجلد traffic_signs لوضع الصور بداخله.')
    print('ضع صور اللوحات المرورية في هذا المجلد ثم شغل السكريبت مرة أخرى لتوليد رموز QR.')
    generate_qr_for_signs()
    print('تم توليد رموز QR في مجلد qr_codes.')

