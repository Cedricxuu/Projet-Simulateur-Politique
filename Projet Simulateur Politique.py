import subprocess
import random
import time
from datetime import datetime

modele = "llama2:chat"  # Change selon ce que tu as
nb_tours = 10
log = []

# Jauges
etat = {
    "Politique": 100,
    "Population": 100,
    "Économie": 100,
}

def afficher_jauges():
    print("\n📊 ÉTAT DU PAYS :")
    for nom, valeur in etat.items():
        barres = int(valeur / 10)
        print(f"{nom:10} : [{'#' * barres}{'-' * (10 - barres)}] {valeur}/100")

def appel_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", modele],
        input=prompt.encode(),
        capture_output=True
    )
    return result.stdout.decode().strip()

# Scénario initial avec pays aléatoire choisi par l'IA
prompt_intro = """
Invente un pays (réel ou fictif), nomme-le, et propose un scénario de crise crédible.
3 phrases max. Termine par : "Que faites-vous ?"
Ne donne que le texte du scénario.
"""
intro = appel_ollama(prompt_intro)
print("\n🌍 SCÉNARIO INITIAL :")
print(intro)
log.append("🌍 SCÉNARIO INITIAL :\n" + intro)

# Essai d'extraction du nom du pays
nom_pays = intro.split('.')[0].split()[-1].replace(",", "").strip()

# Affichage initial des jauges
afficher_jauges()

# Boucle principale
for tour in range(nb_tours):
    print(f"\n--- TOUR {tour + 1} ---")
    action = input("➡️ Votre action ?\n> ")
    log.append(f"\n[TOUR {tour + 1}] Action du joueur : {action}")

    prompt_reaction = f"""
Contexte : crise dans le pays nommé {nom_pays}.
Le joueur propose l'action suivante : "{action}".
En 2 phrases max, donne la suite de l'histoire suivant les décisions du joueur, il faut aussi ajouter un mini résumé de l'ensemble de la situation ensuite.
Termine toujours par : "Que faites-vous ensuite ?"
"""
    reaction = appel_ollama(prompt_reaction)
    print(f"\n🤖 Narrateur : {reaction}")
    log.append(f"Réaction Narrateur : {reaction}")

    # Modification des jauges (chaque tour est imprévisible)
    for jauge in etat:
        variation = random.randint(-25, 10)  # Plus de chances de perdre que de gagner
        etat[jauge] = max(0, min(100, etat[jauge] + variation))

    afficher_jauges()
    log.append(f"État du pays : {etat}")

    # Vérification de défaite
    if any(valeur <= 0 for valeur in etat.values()):
        print("\n💥 Une des structures du pays s’effondre. GAME OVER.")
        log.append("💥 ÉCHEC : Une jauge est tombée à 0.")
        break
else:
    print("\n✅ Vous avez évité l'effondrement... cette fois.")
    log.append("✅ SUCCÈS : Fin de simulation sans effondrement.")

# Sauvegarde
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nom_fichier = f"crise_{nom_pays}_{timestamp}.txt"
with open(nom_fichier, "w", encoding="utf-8") as f:
    f.write("\n".join(log))

print(f"\n🗃️ Rapport enregistré : {nom_fichier}")
print("Merci d'avoir joué !")
