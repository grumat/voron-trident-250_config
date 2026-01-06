py -3 gen_stats.py --data=.\data\probe_accuracy_superpinda.json --out=.\data\probe_accuracy_superpinda.jpg --title="Prusa Super Pinda" > Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_superpinda_fysetc.json --out=.\data\probe_accuracy_superpinda_fysetc.jpg --title="FYSETC Super Pinda" >> Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_TL-Q5MC2-Z.json --out=.\data\probe_accuracy_TL-Q5MC2-Z.jpg --title="OMRON TL-Q5MC2-Z" >> Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_TL-Q5MC1-Z.json --out=.\data\probe_accuracy_TL-Q5MC1-Z.jpg --title="OMRON TL-Q5MC1-Z" >> Results.txt
py -3 gen_stats.py --data=.\data\probe_accuracy_GX-H15A.json --out=.\data\probe_accuracy_GX-H15A.jpg --title="Panasonic GX-H15A" >> Results.txt
