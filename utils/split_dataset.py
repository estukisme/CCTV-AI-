import os
import shutil
import random

# ==============================================
# KONFIGURASI (SUDAH DISESUAIKAN UNTUK KAK JUN)
# ==============================================
SOURCE_DIR = r"D:\2026\PHONSKA 1\CCTV\dataset"       # folder yang berisi merah/putih
OUTPUT_DIR = r"D:\2026\PHONSKA 1\CCTV\dataset_split" # hasil split
SPLIT = (0.7, 0.2, 0.1)
CLASSES = ["merah", "putih"]

# ==============================================
# BUAT FOLDER OUTPUT
# ==============================================
def prepare_folders():
    for split_name in ["train", "val", "test"]:
        for cls in CLASSES:
            path = os.path.join(OUTPUT_DIR, split_name, cls)
            os.makedirs(path, exist_ok=True)

# ==============================================
# SPLIT DATASET
# ==============================================
def split_data():
    for cls in CLASSES:
        src_folder = os.path.join(SOURCE_DIR, cls)
        if not os.path.exists(src_folder):
            print(f"❌ Folder tidak ditemukan: {src_folder}")
            continue

        files = [
            f for f in os.listdir(src_folder)
            if os.path.isfile(os.path.join(src_folder, f))
        ]

        random.shuffle(files)

        total = len(files)
        n_train = int(total * SPLIT[0])
        n_val = int(total * SPLIT[1])

        train_files = files[:n_train]
        val_files = files[n_train:n_train + n_val]
        test_files = files[n_train + n_val:]

        for f in train_files:
            shutil.copy(os.path.join(src_folder, f),
                        os.path.join(OUTPUT_DIR, "train", cls, f))

        for f in val_files:
            shutil.copy(os.path.join(src_folder, f),
                        os.path.join(OUTPUT_DIR, "val", cls, f))

        for f in test_files:
            shutil.copy(os.path.join(src_folder, f),
                        os.path.join(OUTPUT_DIR, "test", cls, f))

        print(f"[{cls}] total={total} → train={len(train_files)}, val={len(val_files)}, test={len(test_files)}")

# ==============================================
# MAIN
# ==============================================
if __name__ == "__main__":
    prepare_folders()
    split_data()
    print("\n🎉 Data berhasil di-split ke folder dataset_split/ !")
