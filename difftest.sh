

./fix-with-column.sh
./fix-with-py.sh
diff -r "${@:--u}" fixed-column/ fixed-py/
