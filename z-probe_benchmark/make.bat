py -3 gen_stats.py --data=.\data\probe_accuracy_superpinda.json --out=.\data\probe_accuracy_superpinda.jpg --title="Prusa Super Pinda" > Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_superpinda_fysetc.json --out=.\data\probe_accuracy_superpinda_fysetc.jpg --title="FYSETC Super Pinda" >> Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_TL-Q5MC2-Z.json --out=.\data\probe_accuracy_TL-Q5MC2-Z.jpg --title="OMRON TL-Q5MC2-Z" >> Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_TL-Q5MC1-Z.json --out=.\data\probe_accuracy_TL-Q5MC1-Z.jpg --title="OMRON TL-Q5MC1-Z" >> Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_GX-H15A.json --out=.\data\probe_accuracy_GX-H15A.jpg --title="Panasonic GX-H15A" >> Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_GX-H12A.json --out=.\data\probe_accuracy_GX-H12A.jpg --title="Panasonic GX-H12A" >> Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_N3F-H4NB.json --out=.\data\probe_accuracy_N3F-H4NB.jpg --title="BAOLSEN N3F-H4NB" >> Results.txt

IF EXIST ".\data\probe_accuracy.json" (
	py -3 gen_stats.py --data=.\data\probe_accuracy.json --out=.\data\probe_accuracy.jpg --title="Fresh Test" >> Results.txt
)

py -3 mk_tables.py > Tables.md
