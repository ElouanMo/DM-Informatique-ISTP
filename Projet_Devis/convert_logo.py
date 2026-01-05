from PIL import Image
import os

def convertir():
    # CORRECTION ICI : .png au lieu de .jpg
    source = "logo_source.png"
    cible = "logo.ico"

    if not os.path.exists(source):
        print(f"❌ Erreur : Je ne trouve pas le fichier {source}")
        print("Vérifiez que le nom est exact (attention aux .png / .jpg)")
        return

    try:
        img = Image.open(source)
        # On sauvegarde en .ico
        img.save(cible, format='ICO', sizes=[(256, 256)])
        print(f"✅ Succès ! L'icône {cible} a été créée.")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    convertir()