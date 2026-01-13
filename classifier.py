import os
import shutil

def classify_images(image_paths):
    essential = []
    decorative = []

    for path in image_paths:
        filename = os.path.basename(path).lower()
        try:
            size_kb = os.path.getsize(path) / 1024
        except:
            size_kb = 0

        # Decorative rules
        if any(word in filename for word in ["logo", "icon", "sprite", "thumbnail", "banner", "ads"]):
            decorative.append(path)
        elif size_kb < 5:  # very small (spacers/icons)
            decorative.append(path)
        elif filename.endswith((".svg", ".gif")) and size_kb < 30:
            decorative.append(path)

        # Essential rules
        elif size_kb > 30:  
            essential.append(path)
        elif any(word in filename for word in ["map", "chart", "diagram", "photo", "figure", "cover"]):
            essential.append(path)
        else:
            decorative.append(path)

    # --- Fallback: if everything goes decorative, force some into essential ---
    if len(essential) == 0 and len(decorative) > 0:
        sorted_by_size = sorted(decorative, key=lambda p: os.path.getsize(p), reverse=True)
        cutoff = max(1, len(sorted_by_size) // 5)  # largest 20% → essential
        essential = sorted_by_size[:cutoff]
        decorative = sorted_by_size[cutoff:]

    # ✅ Save copies instead of moves
    os.makedirs("images/essential", exist_ok=True)
    os.makedirs("images/decorative", exist_ok=True)

    for path in essential:
        dest = os.path.join("images/essential", os.path.basename(path))
        if not os.path.exists(dest):
            shutil.copy(path, dest)

    for path in decorative:
        dest = os.path.join("images/decorative", os.path.basename(path))
        if not os.path.exists(dest):
            shutil.copy(path, dest)

    return {
        "essential": essential,
        "decorative": decorative
    }
