
cmd=./markdown-table-formater.py

rm -rf fixed-py.old
[ ! -d fixed-py ] ||
mv fixed-py fixed-py.old

mkdir fixed-py

find collected/ -type f -name '*.md' |
while read -r f; do
	"$cmd" "$f" > "fixed-py/${f#*collected/}"
done

rm -rf fixed-py.old
