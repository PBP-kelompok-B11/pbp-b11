📃Daftar Anggota Kelompok

1. A. Sheriqa Dewina Ihsan (2406360722)
2. Muhammad Rafi Sugianto (2406357135)
3. Elizabeth Meilanny Sitanggang (2406433522)
4. Vidia Qonita Ahmad (2406345381)
5. Angelo Johenry Apituley (2406428825)
6. Nisriina Wakhdah Haris (2406360445)


⚽ Deskripsi Aplikasi
Aplikasi "[nama aplikasi]" merupakan portal informasi olahraga yang berfokus pada dunia sepak bola profesional. Website ini dirancang untuk menjadi pusat informasi interaktif bagi penggemar sepak bola, dengan menyajikan data dan profil lengkap mengenai pemain, klub, dan statistik pertandingan dalam satu platform yang menarik dan mudah diakses.

Melalui [nama aplikasi], pengguna dapat menjelajahi biodata pemain, melihat perjalanan karier mereka dari klub ke klub, hingga membandingkan performa pemain melalui statistik seperti jumlah gol, assist, dan kartu. Selain itu, pengguna juga dapat mengetahui pencapaian pemain dalam bentuk trofi, penghargaan individu, dan kontribusi mereka di berbagai kompetisi.

Aplikasi ini tidak hanya menyajikan informasi data mentah, tetapi juga dirancang dengan tampilan visual yang rapi dan responsif serta fitur interaktif seperti pencarian pemain, filter berdasarkan klub atau negara, dan kolom komentar bagi pengguna untuk berdiskusi.

Bagi penggemar sepak bola, [nama aplikasi] memberikan pengalaman informatif dan menyenangkan untuk:
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
Link Design =
