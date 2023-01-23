# No. 3: Observasi Koloni Vibrio
Skill Task - ML Engineer RnD. Ini adalah cara saya mengetahui jumlah koloni vibrio, ekstraksi warna, dan luas masing-masing koloni.

## Metodologi saya
Algoritma yang saya gunakan adalah yang tertuang di jurnal [OpenCFU, a New Free and Open-Source Software to Count Cell Colonies and Other Circular Objects - PLOS One](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0054072). Alasan memilih menggunakan OpenCFU adalah algoritma (formula matematik) yang digunakan sudah kompleks, teruji, dan ada kode implementasinya. Walau belum menggunakan deep learning dan masih banyak false cases (false negative terutama), tapi sebagai tahap awal kebutuhan ini menurut saya sudah cukup.

## Cara menjalankan
1. build docker
2. run docker dengan port forwarding dari localhost:8501
3. Isi parameter-parameter yang dibutuhkan (image file path, threshold, radius min-max, cluster params, jumlah variasi spesies/warna, dll.
4. Akan disajikan summary sebagai berikut di browser
![enter image description here](https://images2.imgbox.com/fe/74/gYzMIjVm_o.png)

## Possibility next update
1. Perbandingan kualitatif dan kuantitatif terhadap ground-truth
2. Untuk data detil seperti di setiap cluster/koloni, koordinatnya berapa dan ada berapa koloni aproksimasinya, sudah disajikan dalam `results.csv`, sedangkan tabel di streamlit belum.