<<<<<<< HEAD
<details>
<Summary><b>📃Daftar Anggota Kelompok</b></Summary>
=======
📃Daftar Anggota Kelompok
>>>>>>> f5720cfc12f847a4cafa951a7a85a9cf1b122ba0

1. A. Sheriqa Dewina Ihsan (2406360722)
2. Muhammad Rafi Sugianto (2406357135)
3. Elizabeth Meilanny Sitanggang (2406433522)
4. Vidia Qonita Ahmad (2406345381)
5. Angelo Johenry Apituley (2406428825)
6. Nisriina Wakhdah Haris (2406360445)

<<<<<<< HEAD
</details>

<details>
<Summary><b>⚽ Deskripsi Aplikasi</b></Summary>

=======

⚽ Deskripsi Aplikasi
>>>>>>> f5720cfc12f847a4cafa951a7a85a9cf1b122ba0
Aplikasi "Beyond90" merupakan portal informasi olahraga yang berfokus pada dunia sepak bola profesional. Website ini dirancang untuk menjadi pusat informasi interaktif bagi penggemar sepak bola, dengan menyajikan data dan profil lengkap mengenai pemain, klub, dan statistik pertandingan dalam satu platform yang menarik dan mudah diakses.

Melalui Beyond90, pengguna dapat menjelajahi biodata pemain, melihat perjalanan karier mereka dari klub ke klub, hingga membandingkan performa pemain melalui statistik seperti jumlah gol, assist, dan kartu. Selain itu, pengguna juga dapat mengetahui pencapaian pemain dalam bentuk trofi, penghargaan individu, dan kontribusi mereka di berbagai kompetisi.

Aplikasi ini tidak hanya menyajikan informasi data mentah, tetapi juga dirancang dengan tampilan visual yang rapi dan responsif serta fitur interaktif seperti pencarian pemain, filter berdasarkan klub atau negara, dan kolom komentar bagi pengguna untuk berdiskusi.

<<<<<<< HEAD
Bagi penggemar sepak bola, Beyond90 memberikan pengalaman informatif dan menyenangkan untuk: - Mengenal lebih dekat idola mereka melalui profil pemain. - Melihat perbandingan performa antar pemain atau klub. - Menemukan klub dengan ranking dan statistik terbaik. - Berinteraksi dengan sesama penggemar melalui komentar dan diskusi.

Kebermanfaatan aplikasi ini juga dapat diperluas untuk pelajar, jurnalis olahraga, dan analis data, yang dapat memanfaatkan dataset pemain dan klub sebagai referensi dalam penulisan artikel, riset performa, atau pembuatan konten sepak bola.

</details>

<details>
<Summary><b>🗂️Daftar Modul yang akan diimplementasikan</b></Summary>

1. Manajemen Data Pemain (App: players) (Muhammad Rafi Sugianto)
    - Models:
        1. Player (nama, negara, usia, tinggi, berat, posisi)
        2. CareerHistory (player → Player, klub → Club, tahun_mulai, tahun_selesai)
        3. SeasonStats (player → Player, musim, pertandingan, gol, assist, kartu)
        4. Achievement (player → Player, deskripsi, tahun)
    - Views (CRUD):
        1. player_list →  Daftar pemain
        2. player_detail →  Detail profil pemain
        3. player_create →  Menambahkan pemain
        4. player_update →  Mengedit profil pemain
        5. player_delete →  Menghapus pemain
    - Templates:
        1. players/list.html
        2. players/detail.html
        3. players/form.html

2. Manajemen Data Klub (App: clubs) (Elizabeth Meilanny Sitanggang)
    - Models:
        1. Club (nama, negara, stadion, tahun_berdiri)
        2. ClubRanking (club → Club, musim, peringkat)
    - Views (CRUD):
        1. club_list →  Daftar club
        2. club_detail →  Detail club 
        3. club_create →  Menambahkan club
        4. club_update →  Mengedit info club
        5. club_delete →  Menghapus club
        6. ranking_list →  List ranking club
    - Templates
        1. clubs/list.html 
        2. clubs/detail.html 
        3. clubs/form.html 
        4. clubs/ranking.html

3.  Event Kompetisi (App: events) (Vidia Qonita Ahmad)
    - Models:
        1. Event (nama_event, tipe [liga/turnamen/pertandingan], lokasi, tanggal_mulai, tanggal_selesai)
        2. EventParticipation (event → Event, player/club → Player/Club, peran [pemain, kapten, klub], hasil [menang, kalah, juara])
    - Views (CRUD):
        1. event_list →  Daftar event sepak bola
        2. event_detail →  Detail event
        3. event_create →  Menambahkan event
        4. event_update →  Mengedit info event
        5. event_delete →  Menghapus event
        6. participation_add →  Daftar partisipan yang mengikuti event
        7. participation_update →  Update info partisipan
        8. participation_delete →  Menghapus info partisipan
    - Templates:
        1. events/list.html
        2. events/detail.html
        3. events/form.html
        4. events/participation_form.html


4. Pencarian & Filter (App: search) (A. Sheriqa Dewina Ihsan)
    - Models:
        1. SearchQuery (user, kata_kunci, jenis [pemain/klub], tanggal)
    - Views (CRUD):
        1. search_players →  Mencari pemain berdasarkan nama, posisi, klub, negara
        2. search_clubs →  Mencari klub sepak bola
    - Templates:
        1. search/results.html
        2. search/history.html
        3. search/form.html

5. Halaman Profil Interaktif (App: profiles) (Nisriina Wakhdah Haris)
    - Models:
        1. ProfileWidget (profil → Player/Club, jenis_widget [chart/statistik], konfigurasi JSON)
    - Views (CRUD):
        1. profile_overview → Menampilkan profil pemain/klub interaktif dengan grafik/statistik
        2. widget_create →  Membuat widget baru
        3. widget_update →  Mengupdate widget
        4. widget_delete →  Menghapus widget
    - Templates:
        1. profiles/overview.html
        2. profiles/form.html
        3. profiles/list.html

6.  Komentar & Interaksi Pengguna (App: comments) (Angelo Johenry Apituley)
    - Models:
        1. Comment (user, isi_komentar, tanggal, player/club terkait → bisa pakai GenericForeignKey)
    - Views (CRUD):
        1. comment_add →  Menambahkan komentar
        2. comment_list →  Menampilkan daftar komentar
        3. comment_update →  Mengedit komentar
        4. comment_delete →  Menghapus komentar
    - Templates:
        1. comments/list.html
        2. comments/form.html

7. Galeri Media (App: media_gallery) (Nisriina Wakhdah Haris)
    - Models:
        1. Media (player/club terkait, jenis_media [foto/video], file_url, deskripsi, tanggal_upload)
    - Views (CRUD):
        1. gallery_list →  Menampilkan semua media untuk player/club
        2. gallery_upload →  Upload media (khusus admin) 
        3. gallery_update →  Memperbarui media yang ada
        4. gallery_delete →  Menghapus media
    - Templates:
        1. media/list.html
        2. media/upload.html
        3. media/form.html
        
</details>

<details>
<Summary><b>📚Sumber initial dataset kategori utama produk</b></Summary>

Sumber Dataset: https://www.kaggle.com/datasets/vivovinco/20222023-football-player-stats <br>
Deskripsi Singkat: Dataset ini berisi statistik lengkap pemain sepak bola dari berbagai liga dunia pada musim 2022–2023, mencakup nama pemain, klub, posisi, jumlah pertandingan, gol, assist, dan metrik performa lainnya.

</details>

<details>
<Summary><b>👤 Role Pengguna</b></Summary>

1. Pengunjung (User Biasa)
    - Melihat profil pemain & klub. 
    - Menggunakan fitur pencarian & filter. 
    - Memberikan komentar. 
2. Admin 
    - Mengelola data pemain, klub, dan event
    - Mengelola komentar. 
    - Mengupload media (foto/video).

</details>

<details>
<Summary><b>🖇️Tautan deployment PWS dan link design</b></Summary> 

1. PWS = https://pbp.cs.ui.ac.id/a.sheriqa/beyond-90
2. Link Design = ristek.link/figmaB11

</details>
=======
Bagi penggemar sepak bola, Beyond90 memberikan pengalaman informatif dan menyenangkan untuk:
     - Mengenal lebih dekat idola mereka melalui profil pemain.
     - Melihat perbandingan performa antar pemain atau klub.
     - Menemukan klub dengan ranking dan statistik terbaik.
     - Berinteraksi dengan sesama penggemar melalui komentar dan diskusi.

Kebermanfaatan aplikasi ini juga dapat diperluas untuk pelajar, jurnalis olahraga, dan analis data, yang dapat memanfaatkan dataset pemain dan klub sebagai referensi dalam penulisan artikel, riset performa, atau pembuatan konten sepak bola.

🗂️Daftar Modul yang akan diimplementasikan
1. Manajemen Data Pemain (App: players)
Models:
     - Player (nama, negara, usia, tinggi, berat, posisi)
     - CareerHistory (player, klub, tahun_mulai, tahun_selesai)
     - SeasonStats (player, musim, pertandingan, gol, assist, kartu)
     - Achievement (player, deskripsi, tahun)
Views:
     - player_list → daftar pemain
     - player_detail → detail profil pemain
     - player_search → cari pemain
Templates:
     - players/list.html (daftar pemain + filter)
     - players/detail.html (profil pemain lengkap)

2. Manajemen Data Klub (App: clubs)
Models:
     - Club (nama, negara, stadion, tahun_berdiri)
     - ClubRanking (club, musim, peringkat)
Views:
     - club_list → daftar klub
     - club_detail → detail klub + skuad
     - ranking_list → halaman ranking klub
Templates:
     - clubs/list.html (daftar klub)
     - clubs/detail.html (profil klub)
     - clubs/ranking.html (tabel ranking)

3. Fitur Pencarian & Filter (App: search)
Models: (tidak perlu model baru, pakai dari players & clubs)
Views:
     - search_players → cari pemain berdasarkan nama/posisi/klub/negara
     - search_clubs → cari klub
Templates:
     - search/results.html (menampilkan hasil pencarian)

4. Halaman Profil Interaktif (App: profiles)
(gabungan UI untuk player & club, atau app khusus buat menampilkan dengan layout interaktif)
Models: (tidak perlu baru, pakai Player & Club)
Views:
     - profile_overview → menampilkan profil pemain/klub dengan layout interaktif (chart, grafik, dsb.)
Templates:
     - profiles/overview.html (halaman dengan grafik interaktif, visualisasi statistik)

5. Komentar & Interaksi Pengguna (App: comments)
Models:
     - Comment (user, isi_komentar, tanggal, player/club terkait → pakai GenericForeignKey)
Views:
     - comment_add → tambah komentar
     - comment_list → tampilkan komentar di profil pemain/klub
Templates:
     - comments/list.html (daftar komentar di suatu halaman profil)
     - comments/form.html (form input komentar)

6. Galeri Media (App: media_gallery)
Models:
     - Media (player/club terkait, jenis_media [foto/video], file_url, deskripsi, tanggal_upload)
Views:
     - gallery_list → menampilkan semua media untuk player/club
     - gallery_upload → upload media (khusus admin)
Templates:
     - media/list.html (daftar foto/video dengan grid view)
     - media/upload.html (form upload media)
  

📚Sumber initial dataset kategori utama produk
Sumber Dataset:
          https://www.kaggle.com/datasets/vivovinco/20222023-football-player-stats
Deskripsi Singkat:
Dataset ini berisi statistik lengkap pemain sepak bola dari berbagai liga dunia pada musim 2022–2023, mencakup nama pemain, klub, posisi, jumlah pertandingan, gol, assist, dan metrik performa lainnya.

👤 Role Pengguna
Pengunjung (User Biasa)
          - Melihat profil pemain & klub.
          - Menggunakan fitur pencarian & filter.
          - Memberikan komentar.
Admin
          - Mengelola data pemain & klub.
          - Mengelola komentar.
          - Upload media (foto/video).


🖇️Tautan deployment PWS dan link design
PWS = 
Link Design = ristek.link/figmaB11
>>>>>>> f5720cfc12f847a4cafa951a7a85a9cf1b122ba0
