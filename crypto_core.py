import os
import base64
from gmssl import sm2, sm4
from Crypto.Random import get_random_bytes
import uuid
import gnupg
import tempfile
import shutil

# 目录初始化
KEY_DIR = "keys"
GPG_HOME = "temp_gpg"
if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)
if not os.path.exists(GPG_HOME):
    os.makedirs(GPG_HOME)
# 生成 SM2 密钥对
def generate_sm2_keys():
    private_key = os.urandom(32).hex()
    sm2_crypt = sm2.CryptSM2(public_key='',private_key=private_key)
    public_key = sm2_crypt._kg(int(private_key, 16),sm2.default_ecc_table['g'])
    return private_key, public_key
# 保存私钥
def save_sm2_private_key(priv_key):
    key_id = str(uuid.uuid4())
    filename = os.path.join(
        KEY_DIR,
        f"{key_id}.pem")
    with open(filename, "w") as f:
        f.write(priv_key)
    return filename
# 加载私钥
def load_sm2_private_key(filepath):
    with open(filepath, "r") as f:
        return f.read()
# SM2 加密
def sm2_encrypt(data: bytes, public_key: str):
    sm2_crypt = sm2.CryptSM2(public_key=public_key,private_key='')
    encrypted = sm2_crypt.encrypt(data)
    return base64.b64encode(encrypted).decode()
# SM2 解密
def sm2_decrypt(enc_b64: str, private_key: str):
    sm2_crypt = sm2.CryptSM2(public_key='',private_key=private_key)
    encrypted_data = base64.b64decode(enc_b64)
    return sm2_crypt.decrypt(encrypted_data)
# 生成 SM4 Key
def generate_sm4_key():
    return get_random_bytes(16)
# SM4 ECB 加密
def sm4_encrypt(data: bytes, key: bytes):
    crypt_sm4 = sm4.CryptSM4()
    crypt_sm4.set_key(key, sm4.SM4_ENCRYPT)
    encrypted = crypt_sm4.crypt_ecb(data)
    return base64.b64encode(encrypted).decode()
# SM4 ECB 解密
def sm4_decrypt(enc_b64: str, key: bytes):
    crypt_sm4 = sm4.CryptSM4()
    crypt_sm4.set_key(key, sm4.SM4_DECRYPT)
    encrypted_data = base64.b64decode(enc_b64)
    return crypt_sm4.crypt_ecb(encrypted_data)
# PGP文件加密
def pgp_encrypt_file(file_data: bytes,filename: str,public_key_text: str):
    temp_dir = tempfile.mkdtemp(dir=GPG_HOME)
    try:
        gpg = gnupg.GPG(gnupghome=temp_dir)
        import_result = gpg.import_keys(public_key_text)
        if not import_result.results:
            raise Exception("PGP公钥导入失败")
        fingerprint = import_result.fingerprints[0]
        encrypted_data = gpg.encrypt(file_data,recipients=[fingerprint],always_trust=True)
        if not encrypted_data.ok:
            raise Exception(encrypted_data.status)
        return encrypted_data.data
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)