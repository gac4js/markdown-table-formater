# fmt_tables.py — contexte et conception

## Problème

Les fichiers markdown du projet contiennent des tableaux syntaxiquement valides mais non alignés, difficiles à lire directement dans un éditeur de texte.

## Solution envisagée

Utiliser la commande système `column` pour réaligner chaque tableau :

```bash
column -s '|' -o '|' -t
```

La commande prend `|` comme séparateur d'entrée et de sortie, et active le mode tableau pour aligner les colonnes.

## Point délicat identifié

La ligne séparateur markdown (ex: `|---|---|`) est transformée par `column` en `| ---   | ---   |` — les tirets ne remplissent plus toute la largeur de colonne. Le script doit détecter ces lignes et régénérer les tirets pour qu'ils occupent toute la largeur, en préservant les marqueurs d'alignement (`:---`, `:---:`, `---:`).

## Approche retenue

Script Python (`fmt_tables.py`) qui :

1. Parcourt le fichier ligne par ligne
2. Accumule les lignes de tableau (commençant par `|`) dans un tampon
3. À la fin de chaque bloc de tableau, envoie le tampon à `column` via `subprocess`
4. Détecte les lignes séparateur et remplace leur contenu par des tirets pleine largeur
5. Réassemble le fichier et préserve le newline final

## Usage

```bash
# aperçu sur stdout
python3 fmt_tables.py fichier.md

# modification en place
python3 fmt_tables.py -i fichier.md

# plusieurs fichiers
python3 fmt_tables.py -i *.md
```
