import base64
import gzip

def read_file(filename):
    temp_file = open(filename, 'r')
    result = temp_file.read()
    temp_file.close()
    return result

def write_file(filename, content):
    temp_file = open(filename, 'w')
    temp_file.write(content)
    temp_file.close()

def encode_level(level_string: str, is_official_level: bool) -> str:
    gzipped = gzip.compress(level_string.encode())
    base64_encoded = base64.urlsafe_b64encode(gzipped)
    if is_official_level:
        base64_encoded = base64_encoded[13:]
    return base64_encoded.decode()


def make_plist(data):
    result = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
 <dict>
'''
    for i in data:
        result += f'  <key>{i}</key>\n  <string>{data[i]}</string>\n'
    result += ''' </dict>
</plist>
'''
    return result


all_data = read_file('Resources/LevelData.plist')
write_file('LevelData_backup.plist', all_data)


temp_data = all_data.strip().split('\n')[5:-2]
decoded_data = {}
encoded_data = {}
last = 1


for i in temp_data:
    cur = i.strip()
    if cur.startswith('<key>'):
        last = int(cur.replace('<key>', '').replace('</key>', '').strip())
    elif cur.startswith('<string>'):
        decoded_data[last] = cur.replace('<string>', '').replace('</string>', '').strip()


for i in decoded_data:
    cur = decoded_data[i]
    encoded_level = encode_level(cur, True)
    encoded_data[i] = encoded_level


encoded_data = make_plist(encoded_data)
write_file('Resources/LevelData.plist', encoded_data)
print('ok')
