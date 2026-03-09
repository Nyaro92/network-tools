from rembg import remove
from PIL import Image

# Ouvrir l'image
input_path = "/home/nyaro/projet/test_connexion/static/logo.png"
     # Remplace par ton image
output_path = "/home/nyaro/projet/test_connexion/static/logo2.png"


input_image = Image.open(input_path)

# Supprimer le background
output_image = remove(input_image)

# Sauvegarder en PNG (important pour garder la transparence)
output_image.save(output_path)

print("Background supprimé avec succès !")
 