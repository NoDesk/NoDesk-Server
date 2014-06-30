import hashlib

def hash_content(content):
    return hashlib.sha256(content).hexdigest()
