import sys
sys.path.append("/")

from flask import Flask, jsonify, request, make_response
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
from protobuf import my_pb2, output_pb2

import os
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

app = Flask(__name__)

def get_token(password, uid):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"

    headers = {
        "User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }

    r = requests.post(url, headers=headers, data=data)

    try:
        j = r.json()
    except:
        return {
            "error": "OAuth non JSON",
            "raw": r.text
        }

    token = (
        j.get("access_token")
        or j.get("token")
        or j.get("session_key")
        or j.get("jwt")
        or (j.get("data") or {}).get("token")
    )

    if token:
        j["access_token"] = token

    return {
        "access_token": j.get("access_token"),
        "open_id": j.get("open_id"),
        "uid": j.get("uid"),
        "raw": j
    }

def encrypt_message(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    return cipher.encrypt(padded_message)

def parse_response(response_content):
    response_dict = {}
    lines = response_content.split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            response_dict[key.strip()] = value.strip().strip('"')
    return response_dict

def process_token(uid, password):
    token_data = get_token(password, uid)

    if not token_data:
        return {"error": "Failed to retrieve token"}

    if "raw" in token_data:
        oauth_raw = token_data["raw"]
    else:
        oauth_raw = token_data

    # ---- GAME DATA ----
    game_data = my_pb2.GameData()
    game_data.timestamp = "2024-12-05 18:15:32"
    game_data.game_name = "free fire"
    game_data.game_version = 1
    game_data.version_code = "1.108.3"
    game_data.os_info = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
    game_data.device_type = "Handheld"
    game_data.network_provider = "Verizon Wireless"
    game_data.connection_type = "WIFI"
    game_data.screen_width = 1280
    game_data.screen_height = 960
    game_data.dpi = "240"
    game_data.cpu_info = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
    game_data.total_ram = 5951
    game_data.gpu_name = "Adreno (TM) 640"
    game_data.gpu_version = "OpenGL ES 3.0"
    game_data.user_id = "Google|74b585a9-0268-4ad3-8f36-ef41d2e53610"
    game_data.ip_address = "172.190.111.97"
    game_data.language = "en"
    game_data.open_id = token_data.get('open_id', '')
    game_data.access_token = token_data.get('access_token', '')
    game_data.platform_type = 4
    game_data.device_form_factor = "Handheld"
    game_data.device_model = "Asus ASUS_I005DA"
    game_data.field_60 = 32968
    game_data.field_61 = 29815
    game_data.field_62 = 2479
    game_data.field_63 = 914
    game_data.field_64 = 31213
    game_data.field_65 = 32968
    game_data.field_66 = 31213
    game_data.field_67 = 32968
    game_data.field_70 = 4
    game_data.field_73 = 2
    game_data.library_path = "/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/lib/arm"
    game_data.field_76 = 1
    game_data.apk_info = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/base.apk"
    game_data.field_78 = 6
    game_data.field_79 = 1
    game_data.os_architecture = "32"
    game_data.build_number = "2019117877"
    game_data.field_85 = 1
    game_data.graphics_backend = "OpenGLES2"
    game_data.max_texture_units = 16383
    game_data.rendering_api = 4
    game_data.encoded_field_89 = "\u0017T\u0011\u0017\u0002\b\u000eUMQ\bEZ\u0003@ZK;Z\u0002\u000eV\ri[QVi\u0003\ro\t\u0007e"
    game_data.field_92 = 9204
    game_data.marketplace = "3rd_party"
    game_data.encryption_key = "KqsHT2B4It60T/65PGR5PXwFxQkVjGNi+IMCK3CFBCBfrNpSUA1dZnjaT3HcYchlIFFL1ZJOg0cnulKCPGD3C3h1eFQ="
    game_data.total_storage = 111107
    game_data.field_97 = 1
    game_data.field_98 = 1
    game_data.field_99 = "4"
    game_data.field_100 = "4"

    serialized_data = game_data.SerializeToString()
    encrypted_data = encrypt_message(AES_KEY, AES_IV, serialized_data)

    url = "https://loginbp.ggblueshark.com/MajorLogin"
    headers = {
        'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Content-Type': "application/octet-stream",
        'Expect': "100-continue",
        'X-GA': "v1 1",
        'X-Unity-Version': "2018.4.11f1",
        'ReleaseVersion': "OB52"
    }

    try:
        response = requests.post(url, data=encrypted_data, headers=headers, verify=False)

        if response.status_code == 200:
            example_msg = output_pb2.Garena_420()
            example_msg.ParseFromString(response.content)

            parsed_resp = parse_response(str(example_msg))

            return {
                "token": parsed_resp.get("token", "N/A"),
                "oauth_raw": oauth_raw,
                "api": parsed_resp.get("api", "N/A"),
                "region": parsed_resp.get("region", "N/A"),
                "status": parsed_resp.get("status", "live")
            }
        else:
            return {"error": f"HTTP {response.status_code} - {response.reason}"}

    except Exception as e:
        return {"error": f"Request error: {e}"}

def parse_protobuf_raw(data):
    result = {}
    pos = 0
    
    def read_varint():
        nonlocal pos
        value = 0
        shift = 0
        while True:
            if pos >= len(data):
                break
            byte_val = data[pos]
            pos += 1
            value |= (byte_val & 0x7F) << shift
            if not (byte_val & 0x80):
                break
            shift += 7
        return value
    
    while pos < len(data):
        try:
            first_byte = data[pos]
            pos += 1
            field_number = first_byte >> 3
            wire_type = first_byte & 0x07
            
            if wire_type == 0:
                value = read_varint()
                result.setdefault(field_number, []).append(value)
            elif wire_type == 2:
                length = read_varint()
                chunk = data[pos:pos+length]
                pos += length
                try:
                    string_value = chunk.decode('utf-8')
                    result.setdefault(field_number, []).append(string_value)
                except:
                    nested = parse_protobuf_raw(chunk)
                    result.setdefault(field_number, []).append(nested)
        except:
            break
    
    for k, v in list(result.items()):
        if isinstance(v, list) and len(v) == 1:
            result[k] = v[0]
    
    return result

def get_friends_from_token(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "UnityPlayer/2022.3.47f1",
        "ReleaseVersion": "OB52",
        "X-Unity-Version": "2022.3.47f1",
        "X-GA": "v1 1"
    }
    
    payload = bytes.fromhex('362b36f221ac9ed98b104f7b53c858dc')
    
    try:
        response = requests.post(
            "https://client.ind.freefiremobile.com/GetFriend",
            headers=headers,
            data=payload,
            timeout=10
        )
        
        raw_data = response.content
        
        try:
            text = raw_data.decode('utf-8')
            if text.isascii() and ('token' in text.lower() or 'error' in text.lower()):
                return {
                    "success": False,
                    "error": text.strip()
                }
        except:
            pass
        
        parsed_data = parse_protobuf_raw(raw_data)
        
        result = {
            "success": True,
            "total_size_bytes": len(raw_data),
            "friends_count": 0,
            "friends_list": []
        }
        
        if 1 in parsed_data and isinstance(parsed_data[1], list):
            result["friends_count"] = len(parsed_data[1])
            for friend in parsed_data[1]:
                if isinstance(friend, dict):
                    result["friends_list"].append({
                        "user_id": friend.get(1, "unknown"),
                        "nickname": friend.get(3, "unknown")
                    })
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ========== ENDPOINTS ==========

@app.route('/token', methods=['GET'])
def get_token_response():
    """Original endpoint - Get JWT token from UID/PASS"""
    uid = request.args.get('uid')
    password = request.args.get('password')

    if not uid or not password:
        return jsonify({"error": "Missing parameters: uid and password are required"}), 400

    result = process_token(uid, password)

    if "error" in result:
        return jsonify(result), 500

    response = make_response(jsonify(result))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/friend', methods=['GET'])
def get_friends():
    """Get friend list - UID/PASS → OAuth → MajorLogin → Friends"""
    uid = request.args.get('uid')
    password = request.args.get('pass')
    access_token = request.args.get('access')
    jwt_token = request.args.get('jwt')
    
    method = None
    token = None
    
    # Method 1: UID + PASS
    if uid and password:
        method = "UID_PASS"
        
        # Step 1: Get JWT using existing process_token function
        token_result = process_token(uid, password)
        
        if "error" in token_result:
            return jsonify({
                "success": False,
                "error": token_result["error"]
            }), 401
        
        token = token_result.get("token")
        if not token or token == "N/A":
            return jsonify({
                "success": False,
                "error": "Failed to get JWT token"
            }), 401
            
    # Method 2: Access Token (need to convert to JWT)
    elif access_token:
        method = "ACCESS_TOKEN"
        
        # Build GameData and call MajorLogin
        game_data = my_pb2.GameData()
        game_data.timestamp = "2024-12-05 18:15:32"
        game_data.game_name = "free fire"
        game_data.game_version = 1
        game_data.version_code = "1.108.3"
        game_data.os_info = "Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)"
        game_data.device_type = "Handheld"
        game_data.network_provider = "Verizon Wireless"
        game_data.connection_type = "WIFI"
        game_data.screen_width = 1280
        game_data.screen_height = 960
        game_data.dpi = "240"
        game_data.cpu_info = "ARMv7 VFPv3 NEON VMH | 2400 | 4"
        game_data.total_ram = 5951
        game_data.gpu_name = "Adreno (TM) 640"
        game_data.gpu_version = "OpenGL ES 3.0"
        game_data.user_id = "Google|74b585a9-0268-4ad3-8f36-ef41d2e53610"
        game_data.ip_address = "172.190.111.97"
        game_data.language = "en"
        game_data.open_id = ""
        game_data.access_token = access_token
        game_data.platform_type = 4
        game_data.device_form_factor = "Handheld"
        game_data.device_model = "Asus ASUS_I005DA"
        game_data.field_60 = 32968
        game_data.field_61 = 29815
        game_data.field_62 = 2479
        game_data.field_63 = 914
        game_data.field_64 = 31213
        game_data.field_65 = 32968
        game_data.field_66 = 31213
        game_data.field_67 = 32968
        game_data.field_70 = 4
        game_data.field_73 = 2
        game_data.library_path = "/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/lib/arm"
        game_data.field_76 = 1
        game_data.apk_info = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-QPvBnTUhYWE-7DMZSOGdmA==/base.apk"
        game_data.field_78 = 6
        game_data.field_79 = 1
        game_data.os_architecture = "32"
        game_data.build_number = "2019117877"
        game_data.field_85 = 1
        game_data.graphics_backend = "OpenGLES2"
        game_data.max_texture_units = 16383
        game_data.rendering_api = 4
        game_data.encoded_field_89 = "\u0017T\u0011\u0017\u0002\b\u000eUMQ\bEZ\u0003@ZK;Z\u0002\u000eV\ri[QVi\u0003\ro\t\u0007e"
        game_data.field_92 = 9204
        game_data.marketplace = "3rd_party"
        game_data.encryption_key = "KqsHT2B4It60T/65PGR5PXwFxQkVjGNi+IMCK3CFBCBfrNpSUA1dZnjaT3HcYchlIFFL1ZJOg0cnulKCPGD3C3h1eFQ="
        game_data.total_storage = 111107
        game_data.field_97 = 1
        game_data.field_98 = 1
        game_data.field_99 = "4"
        game_data.field_100 = "4"

        serialized_data = game_data.SerializeToString()
        encrypted_data = encrypt_message(AES_KEY, AES_IV, serialized_data)

        url = "https://loginbp.ggblueshark.com/MajorLogin"
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/octet-stream",
            'Expect': "100-continue",
            'X-GA': "v1 1",
            'X-Unity-Version': "2018.4.11f1",
            'ReleaseVersion': "OB52"
        }

        try:
            response = requests.post(url, data=encrypted_data, headers=headers, verify=False, timeout=10)
            if response.status_code == 200:
                garena_msg = output_pb2.Garena_420()
                garena_msg.ParseFromString(response.content)
                parsed = parse_response(str(garena_msg))
                token = parsed.get("token")
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"MajorLogin failed: {str(e)}"
            }), 401
            
        if not token:
            return jsonify({
                "success": False,
                "error": "Failed to convert access token to JWT"
            }), 401
        
    # Method 3: Direct JWT
    elif jwt_token:
        method = "JWT_TOKEN"
        token = jwt_token
        
    else:
        return jsonify({
            "success": False,
            "error": "Missing parameters. Use: ?uid=UID&pass=PASS or ?access=TOKEN or ?jwt=TOKEN"
        }), 400
    
    # Get friends
    result = get_friends_from_token(token)
    result["METHOD"] = method
    
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
