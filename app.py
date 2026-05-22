from flask import Flask, render_template, request, jsonify, send_file
from crypto_core import *
import io
import traceback
from werkzeug.utils import secure_filename

app = Flask(__name__)
# 首页
@app.route('/')
def index():
    return render_template('index.html')
# 初始化密钥
@app.route('/init_keys', methods=['GET'])
def init_keys():
    try:
        priv_key, pub_key = generate_sm2_keys()
        key_file = save_sm2_private_key(priv_key)
        sm4_key = generate_sm4_key()
        enc_sm4_key = sm2_encrypt(sm4_key, pub_key)
        return jsonify({
            "key_id": key_file,
            "sm2_public_key": pub_key,
            "encrypted_sm4_key": enc_sm4_key})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
# 文本加密
@app.route('/text_encrypt', methods=['POST'])
def text_encrypt():
    try:
        data = request.json
        key_id = data['key_id']
        encrypted_sm4_key = data['encrypted_sm4_key']
        plaintext = data['text']
        private_key = load_sm2_private_key(key_id)
        sm4_key = sm2_decrypt(encrypted_sm4_key,private_key)
        encrypted_text = sm4_encrypt(plaintext.encode(),sm4_key)
        return jsonify({"encrypted_text": encrypted_text})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"文本加密失败: {str(e)}"}), 500
# 文本解密
@app.route('/text_decrypt', methods=['POST'])
def text_decrypt():
    try:
        data = request.json
        key_id = data['key_id']
        encrypted_sm4_key = data['encrypted_sm4_key']
        encrypted_text = data['encrypted_text']
        private_key = load_sm2_private_key(key_id)
        sm4_key = sm2_decrypt(encrypted_sm4_key,private_key)
        decrypted = sm4_decrypt(encrypted_text,sm4_key)
        return jsonify({"decrypted_text": decrypted.decode()})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"文本解密失败: {str(e)}"}), 500
# 文件加密
@app.route('/file_encrypt', methods=['POST'])
def file_encrypt():
    try:
        uploaded_file = request.files['file']
        key_id = request.form['key_id']
        encrypted_sm4_key = request.form['encrypted_sm4_key']
        private_key = load_sm2_private_key(key_id)
        sm4_key = sm2_decrypt(encrypted_sm4_key,private_key)
        file_data = uploaded_file.read()
        encrypted_data = sm4_encrypt(file_data,sm4_key)
        return jsonify({"encrypted_data": encrypted_data})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"文件加密失败: {str(e)}"}), 500
# 文件解密
@app.route('/file_decrypt', methods=['POST'])
def file_decrypt():
    try:
        uploaded_file = request.files['file']
        key_id = request.form['key_id']
        encrypted_sm4_key = request.form['encrypted_sm4_key']
        encrypted_content = uploaded_file.read().decode()
        private_key = load_sm2_private_key(key_id)
        sm4_key = sm2_decrypt(encrypted_sm4_key,private_key)
        decrypted_data = sm4_decrypt(encrypted_content,sm4_key)
        filename = uploaded_file.filename
        if filename.endswith(".enc"):
            filename = filename[:-4]
        else:
            filename = "decrypted_" + filename
        return send_file(io.BytesIO(decrypted_data),as_attachment=True,download_name=filename)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"文件解密失败: {str(e)}"}), 500
@app.route('/pgp_encrypt', methods=['POST'])
def pgp_encrypt():
    try:
        uploaded_file = request.files['file']
        pgp_public_key = request.form['pgp_public_key']
        filename = secure_filename(uploaded_file.filename)
        file_data = uploaded_file.read()
        encrypted_data = pgp_encrypt_file(file_data,filename,pgp_public_key)
        output_name = filename + ".gpg"
        return send_file(io.BytesIO(encrypted_data),as_attachment=True,
            download_name=output_name,mimetype='application/octet-stream')
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"PGP加密失败: {str(e)}"}), 500
# 启动
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=False)