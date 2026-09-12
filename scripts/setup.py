import sys

from app.config import EMBEDDING_MODEL, MODEL_DIR
from app.core.embeddings import embed_texts

def main():
    print(f"Downloading embedding model: {EMBEDDING_MODEL} ...")
    vectors = embed_texts(["health test sentence"])
    print(f"Embedding model ready (dim={vectors.shape[1]})")

    print(f"Downloading language detection model: lid.176.bin ...")
    import fasttext
    try:
        fasttext.download_model("lid.176.bin")
    except Exception as e:
        print(f"fasttext download failed: {e}")
        return
    import shutil
    target = MODEL_DIR / "lid.176.bin"
    shutil.move("lid.176.bin", str(target))
    print(f"Language model ready at {target}")
    print("SETUP COMPLETE")

if __name__ == "__main__":
    sys.exit(main())
