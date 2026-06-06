# Install otomatis library yang dibutuhkan ke Python yang aktif
import sys
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'matplotlib', 'networkx', '--quiet'])
#GUI window tkinter
import tkinter as tk
from tkinter import ttk
from collections import deque #deque = struktur data antrian untuk BFS (lebih efisien dari list biasa)
import networkx as nx #networkx = library untuk membuat dan mengelola graf
# matplotlib = library untuk menggambar visualisasi graf
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches #khusus untuk bikin kotak warna di legend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #jembatan antara matplotlib dan tkinter biar gambar bisa muncul di window
from matplotlib.image import imread #untuk membaca file gambar 

# ── GRAF ─────────────────────
G = nx.DiGraph()
G.add_edges_from([
    ('A','B'),('A','C'),
    ('B','D'),
    ('C','D'),('C','G'),
    ('D','E'),
    ('E','F'),
    ('F','L'),
    ('L','K'),
    ('G','J'),('G','H'),
    ('J','K'),
    ('H','M'),('H','I'),
    ('M','N'),
    ('I','O'),
    ('N','P'),
    ('O','P'),('O','Q'),])

#KOORDINAT NODE
pos  ={'A': (6.4, 10.5),
    'B': (3.9,  9.0), 'C': (6.7,  8.5),
    'D': (5.0,  6.5), 'G': (8.5,  7.5),
    'E': (4.8,  4.0), 'J': (7.7,  4.0), 'H': (9.5, 8.7),
    'F': (4.4,  2.2), 'K': (8.5,  1.6), 'I': (12.5, 8.8), 'M': (9.5, 4.0),
    'L': (5.9,  3.5), 'O': (12.5, 7.0), 'N': (9.5, 1.6),
    'Q': (14.0, 8.0), 'P': (12.5, 4.0),}  

#node terisolasi
isolated_nodes = {
    'R1': (3.7,  3.0),   
    'R2': (2.5,  5.8),   
    'R3': (5.0,  8.8),   
    'R4': (6.3,  6.2),   
    'R5': (12.0, 1.0),}
for r in isolated_nodes:
    G.add_node(r)              # tambah node tanpa edge
    pos[r] = isolated_nodes[r] # tambah posisinya

# ── keadaan/kejadian BFS ───────────────────────────────
state = {
    'visited': set(), 'in_queue': {'A'},#Set berisi node yang SUDAH dikunjungi 'SET', Set berisi node yang SEDANG MENUNGGU di antrian'QUEUE'
    'queue': deque(['A']), 'current': None,#urutan node yang akan dikunjungi berikutnya, deque dipilih karena popleft(), NONE karena awal belum ada yang dikunjungi
    'visit_order': [], 'step': 0, 'done': False,} #List urutan kunjungan untuk ditampilkan di layar, ditampilkan sudah berapa langkah BFS berjalan 'step'

# ── FUNGSI GAMBAR ──────────────────────────────────────
def draw_bfs(ax):
    ax.clear()
    ax.set_facecolor('#F8F9FA')
    # Background peta
    img = imread('peta_desa_kauman.png')
    ax.imshow(img, extent=[0, 15, 0, 11], aspect='auto', alpha=0.35, zorder=0)
    #WARNA node sesuai kejadian
    node_color, edge_color, lw = [], [], []
    for n in G.nodes():
        if n in isolated_nodes:
            node_color.append('#E53935'); edge_color.append('#B71C1C'); lw.append(2.0)
        elif n == state['current']:
            node_color.append('#FAC940'); edge_color.append('#B8860B'); lw.append(2.5)
        elif n in state['visited']:
            node_color.append('#1D9E75'); edge_color.append('#0A5C44'); lw.append(2.0)
        elif n in state['in_queue']:
            node_color.append('#85CAFF'); edge_color.append('#1565C0'); lw.append(2.0)
        else:
            node_color.append('#FFFFFF'); edge_color.append('#555555'); lw.append(1.5)
            
    # MENGATUR WARNA NODE SESUAI DIKUNJUNGI ATAU BELUM
    ec = ['#1D9E75' if (u in state['visited'] and v in state['visited']) else '#BBBBBB'
          for u, v in G.edges()]
    ew = [2.5 if (u in state['visited'] and v in state['visited']) else 1.2
          for u, v in G.edges()]
    #STYLE EDGE DAN NODE
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=ec, width=ew,
                           arrows=True, arrowstyle='-', arrowsize=18,
                           connectionstyle='arc3,rad=0.05', node_size=2200)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_color,
                           edgecolors=edge_color, node_size=2200, linewidths=lw)
    #logika perubahan warna huruf node
    for n in G.nodes():
        if n in isolated_nodes:
            col = '#ffffff'   # teks putih di atas merah
        elif n in state['visited'] and n != state['current']:
            col = '#ffffff' # teks putih di node tellah dikunjungi
        else:
            col = '#1a1a1a' #teks hitam untuk node lainnya
        x, y = pos[n]
        ax.text(x, y, n, ha='center', va='center',
            fontsize=13, fontweight='bold', color=col, zorder=5)
     
    #warna legenda
    legend = [
        mpatches.Patch(fc='#E53935', ec='#B71C1C', lw=1.5, label='Tertimbun puing — tidak terjangkau'),
        mpatches.Patch(fc='#FFFFFF', ec='#555', lw=1.5, label='Belum dilalui'),
        mpatches.Patch(fc='#FAC940', ec='#B8860B', lw=1.5, label='Sedang dikunjungi'),
        mpatches.Patch(fc='#85CAFF', ec='#1565C0', lw=1.5, label='Dalam antrian'),
        mpatches.Patch(fc='#1D9E75', ec='#0A5C44', lw=1.5, label='Sudah diselamatkan'),]
    ax.legend(handles=legend, loc='upper left', fontsize=9, framealpha=0.9)
    
    # pemberitahuan teks di pojok atas tentang progres node
    if state['visit_order']:
        ax.text(0.5, -0.03, 'Urutan: ' + ' -> '.join(state['visit_order']),
                transform=ax.transAxes, ha='center', fontsize=9,
                color='#1D9E75', fontweight='bold')

    if state['current']:
        title = f"Langkah {state['step']} — Mengunjungi node \"{state['current']}\""
    elif state['visit_order']:
        title = 'Selesai! Semua titik Desa Kauman telah dijelajahi BASARNAS.'
    else:
        title = 'BFS Desa Kauman — Siap dimulai dari node A'
    ax.set_title(title, fontsize=12, fontweight='bold', pad=10)
    ax.axis('off')

# ── LOGIKA BFS──
#Maju 1 langkah BFS setiap kali tombol Next Step ditekan
def step_once():
    #Kalau BFS sudah selesai atau antrian kosong, tandai done lalu stop
    if state['done'] or not state['queue']:
        state['done'] = True
        state['current'] = None
        refresh()
        update_info()
        return
    node = state['queue'].popleft() #ambil node paling depan
    state['in_queue'].discard(node) #hapus dari daftar antrian
    state['step'] += 1 #perhitungan langkah +1
    state['current'] = node #menandai node yang sedang dikunjungi
    state['visited'].add(node) #menandai sudah dikunjungi
    state['visit_order'].append(node) #mencatat urutan kunjungan
    # mengecek semua tetangga node 
    for nb in G.successors(node):
        #memasukkan tetangga belum dikunjungi & belum ada diantrian kedalam daftar tunggu
        if nb not in state['visited'] and nb not in state['in_queue']:
            state['queue'].append(nb)
            state['in_queue'].add(nb)
    refresh() #menggabar ulang draf
    update_info() #update teks info

# Jalankan semua langkah BFS sekaligus (tanpa berhenti)
def run_all():
    while not state['done'] and state['queue']: # loop sampai antrian kosong
        node = state['queue'].popleft()
        state['in_queue'].discard(node)
        state['step'] += 1
        state['current'] = node
        state['visited'].add(node)
        state['visit_order'].append(node)
        for nb in G.successors(node):
            if nb not in state['visited'] and nb not in state['in_queue']:
                state['queue'].append(nb)
                state['in_queue'].add(nb)
    state['done'] = True
    state['current'] = None
    refresh()
    update_info()

# Reset semua state ke kondisi awal (mulai ulang dari node A)
def reset():
    state.update({
        'visited': set(), #mengosongkan daftar yang telah dikunjungi
        'in_queue': {'A'}, #A masuk antrian lagi
        'queue': deque(['A']), #dimulai dari antrian A
        'current': None, #tidak ada node yang sedang dikunjungi
        'visit_order': [], #kosongkan urutan kunjungan
        'step': 0, #reset hitungan langkah
        'done': False, }) #bfs belum selesai
    refresh()
    update_info()
    
# ── POPUP MENAMBAHKAN NODE baru─────────────
def popup_add_node():
    win = tk.Toplevel(root)
    win.title('Tambah Node Baru')
    win.configure(bg='#F0F0F0')
    win.geometry('320x260')
    win.resizable(False, False)
    win.grab_set()  # akan berbentuk pop up

    tk.Label(win, text='Tambah Node Baru', font=('Helvetica', 12, 'bold'),
             bg='#6A1B9A', fg='white', pady=8).pack(fill='x')# button tambahakn node akan berwarna ungu

    frm = tk.Frame(win, bg='#F0F0F0', padx=20, pady=10)
    frm.pack(fill='both', expand=True)
    # akan ada kolom pertanyaan: pertama adalah nama node barunya akan apa?
    tk.Label(frm, text='Nama Node:', bg='#F0F0F0', font=('Helvetica', 10)).grid(row=0, column=0, sticky='w', pady=4)
    e_nama = tk.Entry(frm, width=18, font=('Helvetica', 10))
    e_nama.grid(row=0, column=1, pady=4)
    e_nama.focus()
     #kedua koordinat x berapa?
    tk.Label(frm, text='Koordinat X:', bg='#F0F0F0', font=('Helvetica', 10)).grid(row=1, column=0, sticky='w', pady=4)
    e_x = tk.Entry(frm, width=18, font=('Helvetica', 10))
    e_x.grid(row=1, column=1, pady=4)
    # ketiga berapa koordinat y nya?
    tk.Label(frm, text='Koordinat Y:', bg='#F0F0F0', font=('Helvetica', 10)).grid(row=2, column=0, sticky='w', pady=4)
    e_y = tk.Entry(frm, width=18, font=('Helvetica', 10))
    e_y.grid(row=2, column=1, pady=4)
    # akan diberi edge atau disambungkan ke node mana, jika kosong maka otomatis ke node yang sedang dikunjungi sekarang
    tk.Label(frm, text='Sambung ke\n(kosong=otomatis):', bg='#F0F0F0',
             font=('Helvetica', 10), justify='left').grid(row=3, column=0, sticky='w', pady=4)
    e_sambung = tk.Entry(frm, width=18, font=('Helvetica', 10))
    e_sambung.grid(row=3, column=1, pady=4)

    lbl_err = tk.Label(frm, text='', bg='#F0F0F0', font=('Helvetica', 9), fg='#C62828')
    lbl_err.grid(row=4, column=0, columnspan=2)
  # def melakukan penambahan
    def do_add():
        #perlu digaris bawahi untuk nama node baru dan edge sambungannya kemana
        nama    = e_nama.get().strip().upper()
        sambung = e_sambung.get().strip().upper()
        # ada beberapa kondisi eror untuk mengisi pop up 
        if not nama:
            lbl_err.config(text='❌ Nama tidak boleh kosong!'); return #nama ga boleh kososng
        if nama in pos:
            lbl_err.config(text=f'❌ Node {nama} sudah ada!'); return #node baru ga boleh namnya sama dengan node yang sudah ada
        try:
            x, y = float(e_x.get()), float(e_y.get())
        except ValueError:
            lbl_err.config(text='❌ Koordinat harus angka!'); return # koordinat x,y harus angka
    # penambahan node sesuai format nama = x,y seperti format graf sebelumnya diatas
        G.add_node(nama)
        pos[nama] = (x, y)
        # jika bfs nya done maka node baru ini akan jadi node terisolir merah
        if state['done']:
            isolated_nodes[nama] = (x, y)
            lbl_info.config(text=f'⚠️ BFS selesai. Node {nama} jadi titik terisolir (merah).')
        elif not sambung:
            target = state['current'] if state['current'] else 'A'
            G.add_edge(target, nama)
        # otomatis hanya masuk antrian kalau target = current (sedang dikunjungi)
            if target == state['current'] or target in state['visited']:
                state['queue'].append(nama)
                state['in_queue'].add(nama)
            lbl_info.config(text=f'✅ Node {nama} disambung otomatis ke {target}.') # sambungnya kosong maka akan langsung sambung ke node yang sedang dikunjungi
        else:
            if sambung not in pos:
                lbl_err.config(text=f'❌ Node {sambung} tidak ditemukan!') # jika node yang ingin disambung ga ditemukan
                G.remove_node(nama); del pos[nama]; return
            if sambung in state['visited'] and sambung != state['current']:
                lbl_err.config(text=f'❌ {sambung} sudah dikunjungi & terlalu jauh!') # jika node yang dikunjungi terlalu jauh juga tidak boleh(sudah dikunjungi,sedang dikunjungi)
                G.remove_node(nama); del pos[nama]; return
            # hanya masuk antrian kalau node sambungannya sudah/sedang dikunjungi
            G.add_edge(sambung, nama)
            if sambung in state['visited'] or sambung == state['current']:
            # node penghubung sudah dilewati → boleh masuk antrian sekarang
               state['queue'].append(nama)
               state['in_queue'].add(nama)
            # kalau belum → tidak masuk antrian dulu, nanti BFS akan menemukannya
            # secara otomatis saat node penghubungnya dikunjungi
            lbl_info.config(text=f'✅ Node {nama} disambung ke {sambung}.')

        refresh()
        win.destroy()

    tk.Button(frm, text='✅ Tambah', font=('Helvetica', 10, 'bold'),
               bg='#6A1B9A', fg='white', relief='flat', padx=10, pady=4,
               cursor='hand2', command=do_add).grid(row=5, column=0, columnspan=2, pady=8)

# ── POPUP HAPUS NODE yang di inginkan──────────────────────────────────
def popup_del_node():
    win = tk.Toplevel(root)
    win.title('Hapus Node')
    win.configure(bg='#F0F0F0')
    win.geometry('400x220')
    win.resizable(False, False)
    win.grab_set() # berbentuk pop up

    tk.Label(win, text='Hapus Node', font=('Helvetica', 12, 'bold'),
             bg='#E65100', fg='white', pady=8).pack(fill='x') # button akan warna oranye
    
    tk.Label(win, 
         text='⚠️ Hanya node yang belum dikunjungi\ndan belum dalam antrian yang bisa dihapus.',
         font=('Helvetica', 9), bg='#FFF3E0', fg='#E65100',
         pady=6, padx=10, justify='center').pack(fill='x')# pemberitahuan di bagian atas popupnya tentang syarat node yang bisa dihapus

    frm = tk.Frame(win, bg='#F0F0F0', padx=20, pady=10)
    frm.pack(fill='both', expand=True)

    # Daftar node yang boleh dihapus: belum dikunjungi & bukan di antrian
    boleh_hapus = [n for n in G.nodes() 
                   if n not in state['visited'] # node yang telah dikunjungi
                   and n not in state['in_queue'] # node yang dalam antrian
                   and n != state['current']] # node yang sedang dikunjungi

    if not boleh_hapus: #kondisi saat node ga bisa dihapus
        tk.Label(frm, text='Tidak ada node yang bisa dihapus.\n(Semua sudah dikunjungi / dalam antrian)',
                 bg='#F0F0F0', font=('Helvetica', 10), fg='#555').pack(pady=10)
        tk.Button(frm, text='Tutup', command=win.destroy,
                   bg='#ccc', relief='flat', padx=10).pack()
        return

    tk.Label(frm, text='Pilih node yang akan dihapus:', bg='#F0F0F0',
             font=('Helvetica', 10)).grid(row=0, column=0, sticky='w', pady=6) #pemberitahuan node yang akan dihapus

    pilihan = tk.StringVar(value=boleh_hapus[0])
    dropdown = ttk.Combobox(frm, textvariable=pilihan, values=boleh_hapus,
                             state='readonly', width=16, font=('Helvetica', 10))
    dropdown.grid(row=0, column=1, pady=6, padx=6) # list pilihan node yang bisa dihapus

    def do_delete():
        nama = pilihan.get().strip().upper() # node yang akan dihapus
        
        # Hapus node dari graf, pos, dan isolated_nodes kalau ada
        G.remove_node(nama)
        del pos[nama]
        if nama in isolated_nodes:
            del isolated_nodes[nama] # node terisolasi juga bisa dihapus

        lbl_info.config(text=f'🗑 Node {nama} berhasil dihapus.') # notifikasi node yang bisa dihapus
        refresh()
        win.destroy()

    tk.Button(frm, text='🗑 Hapus', font=('Helvetica', 10, 'bold'),
               bg='#E65100', fg='white', relief='flat', padx=10, pady=4,
               cursor='hand2', command=do_delete).grid(row=2, column=0, columnspan=2, pady=8)
    
# Gambar ulang graf di canvas window
def refresh():
    draw_bfs(ax) # memanggil fungsi gambar
    fig.tight_layout(pad=1.5) #merapatkan layout agar tidak terpotong
    canvas.draw() #proses ulang ke window tkinter 

# Update teks info di bawah tombol
def update_info():
    q = list(state['queue'])
    if state['done']:
        #menampilkan urutan lengkap kalau sudah selesai
        lbl_info.config(text='Selesai!  Urutan: ' + ' -> '.join(state['visit_order']))
    else:
        #menampilkan step sekarang, isi antrian, dan node yang sudah dikunjungi
        lbl_info.config(
            text=f"Step {state['step']}  |  Antrian: {q if q else ['kosong']}  |  "
                 f"Dikunjungi: {state['visit_order']}")

# ── GUI WINDOW ─────────────────────────────────────────
root = tk.Tk()
root.title('BFS Navigasi Penyelamatan Korban Gempa — Desa Kauman')
root.configure(bg='#F0F0F0')
root.geometry('900x900')
root.resizable(True, True)

# Header
frm_header = tk.Frame(root, bg='#1D9E75', pady=10) # berwarna hijau
frm_header.pack(fill='x')
tk.Label(frm_header, text='Sistem Navigasi Penyelamatan Korban Gempa — Desa Kauman',# judul header guinya
         font=('Helvetica', 14, 'bold'), bg='#1D9E75', fg='white').pack()
tk.Label(frm_header, text='Algoritma BFS (Breadth-First Search) | BASARNAS',
         font=('Helvetica', 10), bg='#1D9E75', fg='#d0f0e0').pack()

# Tombol stylenya
frm_btn = tk.Frame(root, bg='#F0F0F0', pady=8)
frm_btn.pack(fill='x', padx=20)

style = ttk.Style()
style.configure('Green.TButton',  font=('Helvetica', 11, 'bold'), foreground='white', background='#1D9E75')
style.configure('Blue.TButton',   font=('Helvetica', 11, 'bold'), foreground='white', background='#1565C0')
style.configure('Red.TButton',    font=('Helvetica', 11, 'bold'), foreground='white', background='#C62828')

btn_next  = tk.Button(frm_btn, text='▶  Next Step', font=('Helvetica', 11, 'bold'),
                       bg='#1D9E75', fg='white', relief='flat', padx=16, pady=6,
                       cursor='hand2', command=step_once)
btn_all   = tk.Button(frm_btn, text='⏩  Run All',  font=('Helvetica', 11, 'bold'),
                       bg='#1565C0', fg='white', relief='flat', padx=16, pady=6,
                       cursor='hand2', command=run_all)
btn_reset = tk.Button(frm_btn, text='↺  Reset',     font=('Helvetica', 11, 'bold'),
                       bg='#C62828', fg='white', relief='flat', padx=16, pady=6,
                       cursor='hand2', command=reset)

# ── PANEL TAMBAH & HAPUS NODE ──────────────────────────────────
btn_add_node = tk.Button(frm_btn, text='➕ Add Node', font=('Helvetica', 11, 'bold'),
                          bg='#6A1B9A', fg='white', relief='flat', padx=16, pady=6,
                          cursor='hand2', command=popup_add_node)
btn_del_node = tk.Button(frm_btn, text='🗑 Delete Node', font=('Helvetica', 11, 'bold'),
                          bg='#E65100', fg='white', relief='flat', padx=16, pady=6,
                          cursor='hand2', command=popup_del_node)

btn_next.pack(side='left', padx=6)
btn_all.pack(side='left',  padx=6)
btn_reset.pack(side='left', padx=6)
btn_add_node.pack(side='left', padx=6)
btn_del_node.pack(side='left', padx=6)

# Info bar di pojok kiri atas 
lbl_info = tk.Label(root, text='Tekan Next Step untuk maju 1 langkah, atau Run All untuk selesaikan sekaligus.',
                    font=('Helvetica', 9), bg='#e8f5e9', fg='#1b5e20',
                    anchor='w', padx=10, pady=5)
lbl_info.pack(fill='x', padx=20, pady=(0, 4))

# Canvas matplotlib
fig, ax = plt.subplots(figsize=(12, 9))
fig.patch.set_facecolor('#F8F9FA')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=(0, 10))

# Gambar awal
refresh()
root.mainloop()