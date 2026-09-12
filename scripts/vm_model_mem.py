import os
os.environ["PYTHONPATH"] = "/opt/healthbot"
import sys
sys.path.insert(0, "/opt/healthbot")

import psutil
from app.core import embeddings

proc = psutil.Process()
print("RSS before load (MB):", proc.memory_info().rss // (1024 * 1024))

tok, model = embeddings.get_model()
print("model dtype:", model.dtype)
try:
    print("memory footprint (MB):", model.get_memory_footprint() // (1024 * 1024))
except Exception as e:
    print("footprint err:", e)

print("RSS after load (MB):", proc.memory_info().rss // (1024 * 1024))