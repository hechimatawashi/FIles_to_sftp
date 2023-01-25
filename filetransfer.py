import os
import datetime
import paramiko
import logging
import keyring

# ログ設定
logging.basicConfig(level=logging.INFO, filename='mylog.log', filemode='w')
logger = logging.getLogger(__name__)

# 共有フォルダのルートパス
root_path = ['/mnt/shared/A', '/mnt/shared/B', '/mnt/shared/C']

# 接続情報
hostname = 'sftp.example.com'
username = 'username'
private_key = '/path/to/.ssh/key.pem'
password = keyring.get_password("pemfile", "username")

# n時間以内に変更、新規作成が行われたファイルを取得
now = datetime.datetime.now()
one_hour_ago = now - datetime.timedelta(hours=n)
files = []
for root in root_path:
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            st = os.stat(file_path)
            mtime = datetime.datetime.fromtimestamp(st.st_mtime)
            if mtime > one_hour_ago:
                files.append(file_path)

# SFTP接続
key = paramiko.RSAKey.from_private_key_file(private_key, password=password)
transport = paramiko.Transport((hostname, 22))
transport.connect(username=username, pkey=key)
sftp = transport.open_sftp()

# アップロード
for file_path in files:
    dir_name = os.path.basename(dirpath)
    for subdir in os.path.relpath(dirpath,root).split(os.sep)[1:]:
        dir_name = dir_name + '_' + subdir
    file_name = os.path.basename(file_path)
    renamed_file_name = dir_name + '_' + file_name
    sftp.put(file_path, renamed_file_name)
    # アップロードしたファイル名をログに出力
    logger.info(renamed_file_name)

# SFTP切断
sftp.close()
transport.close()
