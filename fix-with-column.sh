
cmd=./markdown-table-formater.with-column.py

rm -rf fixed-column.old
[ ! -d fixed-column ] ||
mv fixed-column fixed-column.old

mkdir fixed-column

find collected/ -type f -name '*.md' |
while read -r f; do
	"$cmd" "$f" > "fixed-column/${f#*collected/}"
done

rm -rf fixed-column.old
