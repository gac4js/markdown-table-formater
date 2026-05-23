# markdown-table-formater.py

Formate les tableaux markdown en alignant les colonnes, sans dépendance externe.

## Usage

```bash
# aperçu sur stdout
python3 markdown-table-formater.py fichier.md

# modification en place
python3 markdown-table-formater.py -i fichier.md

# plusieurs fichiers
python3 markdown-table-formater.py -i *.md
```

## Fonctionnement

Le script parcourt le fichier ligne par ligne, accumule les blocs de tableau (lignes commençant par `|`) puis les formate :

1. Calcul de la largeur maximale de chaque colonne (en largeur d'affichage, pas en nombre de caractères)
2. Padding de chaque cellule à cette largeur
3. Régénération des lignes séparateur (`|---|---|`) avec des tirets pleine largeur, en préservant les marqueurs d'alignement (`:---`, `:---:`, `---:`)

Le `|` final de chaque ligne est préservé ou absent selon l'original.

## Cas gérés

- **Caractères larges** (emoji `✅`, `❌`, CJK…) : comptés sur 2 colonnes d'affichage
- **Pipe échappé** (`\|`) : traité comme caractère littéral, pas comme séparateur de colonne
- **Tableau sans `|` final** : la dernière colonne n'est pas paddée (comportement identique à `column(1)`)
- **Tableau mixte** : lignes sans `|` final dans un tableau qui en a — paddées et alignées avec les autres

## Tests

```bash
tests/run.sh          # lance pytest
tests/run.sh -v       # mode verbeux
```

Les fichiers d'exemple sont dans `sample/` (paires `*.input.md` / `*.expected.md`).
