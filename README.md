# Sistem Navigasi Penyelamatan Korban Gempa — Desa Kauman
### Breadth-First Search (BFS) | Struktur Data & Algoritma

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![NetworkX](https://img.shields.io/badge/NetworkX-3.x-orange?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-green?style=flat-square)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-yellow?style=flat-square)

---

## 📌 Deskripsi Proyek

Proyek ini merupakan simulasi sistem navigasi penyelamatan korban gempa bumi di **Desa Kauman, Bojonegoro** menggunakan algoritma **Breadth-First Search (BFS)**. Sistem ini dirancang untuk membantu tim **BASARNAS** dalam menelusuri titik-titik lokasi secara sistematis dan efisien pasca gempa bumi.Graf yang digunakan merepresentasikan titik-titik lokasi nyata di Desa Kauman dengan latar belakang peta Google Maps sebagai referensi visual.

## 🗺️ Studi Kasus
> Tim BASARNAS perlu menelusuri seluruh titik lokasi di Desa Kauman untuk menyelamatkan korban gempa. Beberapa titik tidak dapat dijangkau karena tertimbun puing-puing bangunan. Tim harus bergerak secara sistematis dari titik terdekat ke titik yang lebih jauh.


## 📍 Daftar Vertex (Titik Lokasi)

| Vertex | Lokasi |
|--------|--------|
| A | Jalan Utama Jl. MH Thamrin *(Titik Awal / Root)* |
| B | Musholla Al-Hidayah |
| C | SMPN 1 Bojonegoro |
| D | Warung Kopi Mak Bah |
| E | Hi Food Thamrin - Korean Asia Cafe |
| F | Nasi Tempong Banyuwangi |
| G | KB RA Nurul Ummah Kauman Bojonegoro |
| H | Sky Pool Cafe |
| I | TK Kartika IV-47 & KB Tunas Kartika |
| J | Sekretariat PC Ikatan Bidan Indonesia |
| K | Applestar Bojonegoro |
| L | Kantor Kepala Desa Kauman |
| M | Airlangga Education Center |
| N | Panti Asuhan Muslimat NU Nurur Rohmah 01 |
| O | Masjid Agung Darussalam Bojonegoro |
| P | Rumah Sakit Aisyiyah Bojonegoro |
| Q | Alun-Alun Kabupaten Bojonegoro |
TERISOLASI
| R1|: Kost Karyawan Single 
  R2| : Danu Arta Phone 
  R3| : Warung Sicin Sego Bancaan 
  R4| : Pengadilan Agama Kelas IA Bojonegoro
  R5| : PT Positif Media Citra

## 🔗 Struktur Graf (Edge)

```
A → B, C          B → D
C → D, G          D → E
E → F             F → L
L → K             G → J, H
J → K             H → I, M
M → N             I → O
O → Q, P          N → P

Urutan BFS dari Root A:
A-B-C-D-G-E-J-H-F-K-M-I-L-N-O-P-Q


## ✨ Fitur

- 🗺️ Visualisasi graf di atas peta nyata Desa Kauman
- 🎨 Warna node dinamis sesuai status BFS:
  - ⚪ Putih → Belum dilalui
  - 🟡 Kuning → Sedang dikunjungi
  - 🔵 Biru muda → Dalam antrian
  - 🟢 Hijau tosca → Sudah diselamatkan
  - 🔴 Merah → Tertimbun puing (tidak terjangkau)
- ▶️ Next Step — maju satu langkah BFS
- ⏩ Run All — selesaikan semua langkah sekaligus
- ↺ Reset — mulai ulang dari node A
- ➕ Add Node — tambah titik baru saat BFS belum/sedang/sudah berjalan
- 🗑️ Delete Node — hapus titik yang belum dikunjungi

## 🛠️ Teknologi
| Library | Fungsi |
|---------|--------|
| `networkx` | Membuat dan mengelola struktur graf |
| `matplotlib` | Visualisasi graf dan background peta |
| `tkinter` | GUI window interaktif |
| `collections.deque` | Struktur data antrian BFS |


## 🚀 Cara Menjalankan

### Versi Desktop (VS Code)
```bash
# Clone repository
git clone https://github.com/username/bfs-basarnas-kauman.git
cd bfs-basarnas-kauman

# Install dependencies
pip install matplotlib networkx

# Jalankan
python bfs_kauman.py

> ⚠️ Pastikan file `peta_desa_kauman.png` berada di folder yang sama dengan `import sys DESA KAUMAN VERSI.py`

## 📊 Kenapa BFS?

| Kriteria | BFS | DFS | Dijkstra | Ant Colony |
|----------|-----|-----|----------|------------|
| Jalur terpendek (tak berbobot) | ✅ | ❌ | ✅ | ✅ |
| Sistematis level per level | ✅ | ❌ | ❌ | ❌ |
| Jamin semua titik terjangkau | ✅ | ✅ | ❌ | ✅ |
| Cocok graf kecil tak berbobot | ✅ | ✅ | ❌ | ❌ |
| Kompleksitas | Rendah | Rendah | Sedang | Tinggi |

> BFS dipilih karena graf Desa Kauman berskala kecil, tidak berbobot, dan tujuannya menelusuri semua titik secara sistematis dari yang terdekat — sesuai cara kerja tim SAR di lapangan.

## 📁 Struktur File
bfs-basarnas-kauman/
│
├── import sys DESA KAUMAN VERSI.py      # Versi desktop (VS Code + Tkinter)
├── peta_desa_kauman.png                 # Background peta Desa Kauman
├── keterangan_vertex.txt                # Keterangan lengkap tiap vertex
└── README.md

## 👩‍💻 Dibuat Oleh

> Ummul Lutfiah (NIM : 25031554167| KELAS : 2025E| PRODI : SAINS DATA FMIPA UNESA)
*"Setiap detik berarti dalam penyelamatan. BFS memastikan tidak ada satu titik pun yang terlewat."* 🚒