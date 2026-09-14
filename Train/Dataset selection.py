# download_tartanground.py
import os
from pathlib import Path
from huggingface_hub import snapshot_download, HfApi

# ── Chemin de destination ABSOLU (évite les problèmes Windows) ─────
SCRIPT_DIR = Path(__file__).parent.resolve()
SAVE_DIR   = SCRIPT_DIR / "data" / "tartanground"
SAVE_DIR.mkdir(parents=True, exist_ok=True)
print(f"📁 Destination : {SAVE_DIR}")

# ── Lister les environnements disponibles sur HuggingFace ─────────
print("\n🔍 Vérification des fichiers disponibles sur HuggingFace...")
api  = HfApi()
try:
    files = api.list_repo_files(
        "theairlabcmu/TartanGround",
        repo_type="dataset"
    )
    envs_available = set()
    for f in files:
        parts = f.split("/")
        if len(parts) >= 1:
            envs_available.add(parts[0])
    print(f"  Environnements disponibles : {sorted(envs_available)}")
except Exception as e:
    print(f"  ⚠ Impossible de lister : {e}")
    envs_available = {
        "ForestEnv_Easy", "UrbanCity_Easy",
        "IndoorCorridor_Easy", "GrasslandPlain_Easy"
    }

# ── Téléchargement d'un petit sous-ensemble ────────────────────────
# Commencer par 1 seul environnement pour tester (~2–5 Go)
TARGET_ENVS = ["Office"]

# Garder uniquement les envs réellement disponibles
to_download = [e for e in TARGET_ENVS if e in envs_available]
if not to_download:
    print("⚠ Aucun des environnements cibles trouvé.")
    print(f"  Disponibles : {sorted(envs_available)}")
    print("  → Changer TARGET_ENVS avec un nom de la liste ci-dessus")
    exit(1)

patterns = [f"{e}/*" for e in to_download]
print(f"\n⬇  Téléchargement : {to_download}")
print(f"   Vers : {SAVE_DIR}\n")

try:
    path = snapshot_download(
        repo_id="theairlabcmu/TartanGround",
        repo_type="dataset",
        allow_patterns=patterns,
        local_dir=str(SAVE_DIR),
        local_dir_use_symlinks=False,   # important sur Windows
        ignore_patterns=["*.git*"],
    )
    print(f"\n✅ Téléchargement terminé → {path}")
except Exception as e:
    print(f"\n❌ Erreur : {e}")
    print("→ Vérifier la connexion internet et réessayer")