

rm -rf collected.old
[ ! -d collected ] ||
mv collected collected.old

mkdir collected

find .. -type f -name '*.md' |
grep -v /basy/ |
grep -v '/markdown-table-formater/' |
xargs grep -H '^|.*|$' | cut -d: -f1 |sort -u |
{
	i=1
	while read -r f; do
		i=$(($i+1))
		cp -a "$f" "collected/$i.md"
	done
}

rm -rf collected.old
