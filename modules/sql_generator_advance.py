"""
Advanced SQL Generator - Complete psb_member table structure
Matches all 268 columns from the original table
Only accepts valid columns, skips unknown columns
"""
import pandas as pd
import numpy as np
import re
from datetime import datetime


# Valid columns in psb_member table (for validation)
VALID_COLUMNS = {
    'no', 'subdomain', 'jalur_ppdb', 'gelombang_pendaftaran', 'nomor_pendaftaran',
    'nama', 'nama_panggilan', 'link', 'kewarganegaraan', 'bahasa', 'username',
    'email', 'password', 'password2', 'nik', 'nomor_kk', 'kelas', 'pilihan_kelas',
    'jurusan', 'jurusan_dua', 'jurusan_tiga', 'alasan', 'tempat_lahir', 'tanggal_lahir',
    'kelamin_jenis', 'agama', 'status_anak', 'anak_ke', 'jumlah_saudara',
    'jumlah_saudara_kandung', 'jumlah_saudara_tiri', 'jumlah_saudara_angkat',
    'tinggi_badan', 'berat_badan', 'cacat_badan', 'golongan_darah', 'penyakit_bawaan',
    'pernah_sakit', 'nama_penyakit', 'tanggal_sakit', 'lama_sakit', 'cita_cita',
    'hobi', 'alamat', 'dusun', 'rt', 'rw', 'kelurahan', 'kecamatan', 'kota',
    'provinsi', 'kodepos', 'sekolah', 'jarak_kesekolah', 'transportasi_kesekolah',
    'waktu_kesekolah', 'jenis_tinggal', 'telepon', 'handphone', 'penerima_pkh',
    'nomor_kps', 'jenis_ktm', 'nomor_sktm', 'nomor_kks', 'nomor_pkh', 'layak_pip',
    'alasan_pip', 'nama_kip', 'nomor_kip', 'alasan_tolak_kip', 'penerima_kip',
    'terima_fisik_kip', 'nomor_kis', 'bujur', 'lintang', 'lingkar_kepala',
    'asal_sekolah', 'rangking', 'peringkat_semester_1', 'peringkat_semester_2',
    'peringkat_semester_3', 'peringkat_semester_4', 'peringkat_semester_5',
    'peringkat_semester_6', 'alamat_sekolah_asal', 'npsn', 'tahunlulus', 'nisn',
    'email_ortu', 'telp_ortu', 'nis', 'nama_ayah', 'nik_ayah', 'alamat_ayah',
    'tempat_lahir_ayah', 'tanggal_lahir_ayah', 'usia_ayah', 'agama_ayah',
    'pendidikan_ayah', 'pekerjaan_ayah', 'penghasilan_ayah', 'cacat_badan_ayah',
    'telepon_ayah', 'nama_ibu', 'nik_ibu', 'alamat_ibu', 'tempat_lahir_ibu',
    'tanggal_lahir_ibu', 'usia_ibu', 'tahun_lahir_ayah', 'tahun_lahir_ibu',
    'tahun_lahir_wali', 'agama_ibu', 'pendidikan_ibu', 'pekerjaan_ibu',
    'penghasilan_ibu', 'cacat_badan_ibu', 'telepon_ibu', 'nama_wali', 'nik_wali',
    'alamat_wali', 'tempat_lahir_wali', 'tanggal_lahir_wali', 'usia_wali',
    'agama_wali', 'pendidikan_wali', 'pekerjaan_wali', 'penghasilan_wali',
    'cacat_badan_wali', 'telepon_wali', 'prestasi', 'prestasi_dua', 'beasiswa',
    'tempuh_kesekolah', 'nilai_un3', 'nilai_un', 'nilai_us', 'nilai_un_b_indo',
    'nilai_un_matematika', 'nilai_un_b_ing', 'nilai_un_ipa',
    'rata_rata_rapor_semester_1', 'rata_rata_rapor_semester_2',
    'rata_rata_rapor_semester_3', 'rata_rata_rapor_semester_4',
    'rata_rata_rapor_semester_5', 'rata_rata_rapor_semester_6',
    'agama_rapor_semester_1', 'agama_rapor_semester_2', 'agama_rapor_semester_3',
    'agama_rapor_semester_4', 'agama_rapor_semester_5', 'agama_rapor_semester_6',
    'ips_rapor_semester_1', 'ips_rapor_semester_2', 'ips_rapor_semester_3',
    'ips_rapor_semester_4', 'ips_rapor_semester_5', 'ips_rapor_semester_6',
    'b_indo_rapor_semester_1', 'matematika_rapor_semester_1', 'b_ing_rapor_semester_1',
    'ipa_rapor_semester_1', 'b_indo_rapor_semester_2', 'matematika_rapor_semester_2',
    'b_ing_rapor_semester_2', 'ipa_rapor_semester_2', 'b_indo_rapor_semester_3',
    'matematika_rapor_semester_3', 'b_ing_rapor_semester_3', 'ipa_rapor_semester_3',
    'b_indo_rapor_semester_4', 'matematika_rapor_semester_4', 'b_ing_rapor_semester_4',
    'ipa_rapor_semester_4', 'b_indo_rapor_semester_5', 'matematika_rapor_semester_5',
    'b_ing_rapor_semester_5', 'ipa_rapor_semester_5', 'b_indo_rapor_semester_6',
    'matematika_rapor_semester_6', 'b_ing_rapor_semester_6', 'ipa_rapor_semester_6',
    'b_indo_rapor_semester_7', 'matematika_rapor_semester_7', 'b_ing_rapor_semester_7',
    'ipa_rapor_semester_7', 'b_indo_rapor_semester_8', 'matematika_rapor_semester_8',
    'b_ing_rapor_semester_8', 'ipa_rapor_semester_8', 'b_indo_rapor_semester_9',
    'matematika_rapor_semester_9', 'b_ing_rapor_semester_9', 'ipa_rapor_semester_9',
    'b_indo_rapor_semester_10', 'matematika_rapor_semester_10', 'b_ing_rapor_semester_10',
    'ipa_rapor_semester_10', 'b_indo_rapor_semester_11', 'matematika_rapor_semester_11',
    'b_ing_rapor_semester_11', 'ipa_rapor_semester_11', 'b_indo_rapor_semester_12',
    'matematika_rapor_semester_12', 'ipa_rapor_semester_12', 'pkn_rapor_semester_5',
    'rata_rata_us', 'jmlh_nilai_un', 'rata_rata_un', 'nomor_ijazah', 'nomor_skhu',
    'nomor_peserta_un', 'nomor_akta_lahir', 'domisili', 'jenjang', 'pembayaran',
    'tanggal_daftar', 'data_periodik', 'tanggal_isi_form', 'pernah_paud', 'pernah_tk',
    'referensi', 'keputusan', 'status_rumah_ayah', 'status_rumah_ibu',
    'alamat_kerja_ayah', 'alamat_kerja_ibu', 'jarak_kekantor_ayah',
    'jarak_kekantor_ibu', 'transportasi_ayah', 'transportasi_ibu', 'suku_ayah',
    'suku_ibu', 'bahasa_ayah', 'bahasa_ibu', 'pendidikan_agama_ayah',
    'pendidikan_agama_ibu', 'bacaan_quran_ayah', 'bacaan_quran_ibu', 'status_ayah',
    'status_ibu', 'organisasi_islam_ayah', 'organisasi_islam_ibu', 'bacaan_ayah',
    'bacaan_ibu', 'tgl', 'publish', 'penghasilan', 'nsm', 'keterangan_beasiswa',
    'tahun_mulai_beasiswa', 'tahun_selesai_beasiswa', 'jenis_kesejahteraan',
    'nomor_bpjs', 'panjang_lengan', 'panjang_tungkai', 'tingkat_kec', 'tingkat_kab',
    'tingkat_prov', 'tingkat_nas', 'tingkat_inter', 'prestasi_kec1', 'prestasi_kec2',
    'prestasi_kec3', 'prestasi_kab1', 'prestasi_kab2', 'prestasi_prov1',
    'prestasi_nas1', 'prestasi_inter1', 'jumlah_rapor_semester_1',
    'jumlah_rapor_semester_2', 'jumlah_rapor_semester_3', 'jumlah_rapor_semester_4',
    'jumlah_rapor_semester_5', 'jumlah_rapor_semester_6', 'foto', 'ukuran_pakaian',
    'jurusan_diterima', 'penerima_kps', 'nama_rekening_pembayaran',
    'telepon_pembayaran', 'bank_asal', 'bank_tujuan', 'nominal_transfer',
    'tanggal_transfer', 'bukti_pembayaran', 'konfirmasi_pembayaran'
}


# Complete column type mapping for psb_member table
COLUMN_TYPES = {
    # === IDENTIFIERS ===
    'no': 'INT(11) NOT NULL AUTO_INCREMENT',
    'subdomain': "VARCHAR(75) NOT NULL DEFAULT ''",
    'link': "VARCHAR(100) NOT NULL DEFAULT ''",
    'username': "VARCHAR(20) NOT NULL DEFAULT ''",
    'password': "VARCHAR(50) NOT NULL DEFAULT ''",
    'password2': "VARCHAR(20) NOT NULL DEFAULT ''",
    
    # === REGISTRATION INFO ===
    'jalur_ppdb': "VARCHAR(30) NOT NULL DEFAULT ''",
    'gelombang_pendaftaran': "VARCHAR(100) NOT NULL DEFAULT ''",
    'nomor_pendaftaran': "VARCHAR(30) NOT NULL DEFAULT ''",
    'tanggal_daftar': "DATE NOT NULL",
    'tanggal_isi_form': "DATETIME NOT NULL",
    'keputusan': "VARCHAR(30) NOT NULL DEFAULT ''",
    'publish': "ENUM('0','1') NOT NULL DEFAULT '1'",
    
    # === PERSONAL INFO ===
    'nama': "VARCHAR(100) NOT NULL DEFAULT ''",
    'nama_panggilan': "VARCHAR(100) NOT NULL DEFAULT ''",
    'kewarganegaraan': "VARCHAR(50) NOT NULL DEFAULT ''",
    'bahasa': "VARCHAR(32) NOT NULL DEFAULT ''",
    'email': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nik': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nomor_kk': "VARCHAR(20) NOT NULL DEFAULT ''",
    'nisn': "VARCHAR(50) NOT NULL DEFAULT '123'",
    'nis': "VARCHAR(50) NOT NULL DEFAULT ''",
    
    # === CLASS/MAJOR ===
    'kelas': "VARCHAR(20) NOT NULL DEFAULT ''",
    'pilihan_kelas': "VARCHAR(32) NOT NULL DEFAULT ''",
    'jurusan': "VARCHAR(50) NOT NULL DEFAULT ''",
    'jurusan_dua': "VARCHAR(100) NOT NULL DEFAULT ''",
    'jurusan_tiga': "VARCHAR(100) NOT NULL DEFAULT ''",
    'jurusan_diterima': "VARCHAR(50) NOT NULL DEFAULT ''",
    'alasan': "TEXT NOT NULL",
    'jenjang': "VARCHAR(20) NOT NULL DEFAULT ''",
    
    # === BIRTH INFO ===
    'tempat_lahir': "VARCHAR(50) NOT NULL DEFAULT ''",
    'tanggal_lahir': "DATE NOT NULL",
    'kelamin_jenis': "ENUM('L','P') NOT NULL DEFAULT 'L'",
    'agama': "VARCHAR(50) NOT NULL DEFAULT ''",
    
    # === FAMILY INFO ===
    'status_anak': "VARCHAR(50) NOT NULL DEFAULT ''",
    'anak_ke': "INT(11) NOT NULL DEFAULT 0",
    'jumlah_saudara': "INT(11) NOT NULL DEFAULT 0",
    'jumlah_saudara_kandung': "INT(11) NOT NULL DEFAULT 0",
    'jumlah_saudara_tiri': "INT(11) NOT NULL DEFAULT 0",
    'jumlah_saudara_angkat': "INT(11) NOT NULL DEFAULT 0",
    
    # === PHYSICAL ===
    'tinggi_badan': "VARCHAR(50) NOT NULL DEFAULT ''",
    'berat_badan': "VARCHAR(50) NOT NULL DEFAULT ''",
    'cacat_badan': "VARCHAR(100) NOT NULL DEFAULT ''",
    'golongan_darah': "VARCHAR(2) NOT NULL DEFAULT ''",
    'lingkar_kepala': "VARCHAR(30) NOT NULL DEFAULT ''",
    'panjang_lengan': "VARCHAR(50) NOT NULL DEFAULT ''",
    'panjang_tungkai': "VARCHAR(50) NOT NULL DEFAULT ''",
    'ukuran_pakaian': "VARCHAR(100) NOT NULL DEFAULT ''",
    
    # === HEALTH ===
    'penyakit_bawaan': "VARCHAR(75) NOT NULL DEFAULT ''",
    'pernah_sakit': "ENUM('Ya','Tidak') NOT NULL DEFAULT 'Tidak'",
    'nama_penyakit': "VARCHAR(100) NOT NULL DEFAULT ''",
    'tanggal_sakit': "VARCHAR(100) NOT NULL DEFAULT ''",
    'lama_sakit': "VARCHAR(100) NOT NULL DEFAULT ''",
    
    # === INTERESTS ===
    'cita_cita': "VARCHAR(50) NOT NULL DEFAULT ''",
    'hobi': "VARCHAR(50) NOT NULL DEFAULT ''",
    
    # === ADDRESS ===
    'alamat': "TEXT NOT NULL",
    'dusun': "VARCHAR(100) NOT NULL DEFAULT ''",
    'rt': "VARCHAR(20) NOT NULL DEFAULT ''",
    'rw': "VARCHAR(20) NOT NULL DEFAULT ''",
    'kelurahan': "VARCHAR(100) NOT NULL DEFAULT ''",
    'kecamatan': "VARCHAR(50) NOT NULL DEFAULT ''",
    'kota': "VARCHAR(50) NOT NULL DEFAULT ''",
    'provinsi': "VARCHAR(50) NOT NULL DEFAULT ''",
    'kodepos': "VARCHAR(5) NOT NULL DEFAULT ''",
    'domisili': "VARCHAR(75) NOT NULL DEFAULT ''",
    'bujur': "VARCHAR(30) NOT NULL DEFAULT ''",
    'lintang': "VARCHAR(30) NOT NULL DEFAULT ''",
    
    # === SCHOOL COMMUTE ===
    'sekolah': "VARCHAR(32) NOT NULL DEFAULT ''",
    'jarak_kesekolah': "VARCHAR(24) NOT NULL DEFAULT ''",
    'transportasi_kesekolah': "VARCHAR(100) NOT NULL DEFAULT ''",
    'waktu_kesekolah': "INT(11) NOT NULL DEFAULT 0",
    'tempuh_kesekolah': "INT(11) NOT NULL DEFAULT 0",
    'jenis_tinggal': "VARCHAR(100) NOT NULL DEFAULT ''",
    
    # === CONTACT ===
    'telepon': "VARCHAR(50) NOT NULL DEFAULT ''",
    'handphone': "VARCHAR(50) NOT NULL DEFAULT ''",
    'email_ortu': "VARCHAR(100) NOT NULL DEFAULT ''",
    'telp_ortu': "VARCHAR(20) NOT NULL DEFAULT ''",
    
    # === FINANCIAL AID ===
    'penerima_pkh': "ENUM('YA','TIDAK') NOT NULL",
    'penerima_kps': "ENUM('YA','TIDAK') NOT NULL",
    'nomor_kps': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nomor_kks': "VARCHAR(20) NOT NULL DEFAULT ''",
    'nomor_pkh': "VARCHAR(50) NOT NULL DEFAULT ''",
    'jenis_ktm': "VARCHAR(32) NOT NULL DEFAULT ''",
    'nomor_sktm': "VARCHAR(30) NOT NULL DEFAULT ''",
    'layak_pip': "VARCHAR(20) NOT NULL DEFAULT ''",
    'alasan_pip': "VARCHAR(20) NOT NULL DEFAULT ''",
    'penerima_kip': "VARCHAR(10) NOT NULL DEFAULT ''",
    'nama_kip': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nomor_kip': "VARCHAR(30) NOT NULL DEFAULT ''",
    'terima_fisik_kip': "VARCHAR(10) NOT NULL DEFAULT ''",
    'alasan_tolak_kip': "VARCHAR(100) NOT NULL DEFAULT ''",
    'nomor_kis': "VARCHAR(20) NOT NULL DEFAULT ''",
    'nomor_bpjs': "VARCHAR(50) NOT NULL DEFAULT ''",
    'jenis_kesejahteraan': "VARCHAR(50) NOT NULL DEFAULT ''",
    'beasiswa': "TEXT NOT NULL",
    'keterangan_beasiswa': "VARCHAR(50) NOT NULL DEFAULT ''",
    'tahun_mulai_beasiswa': "VARCHAR(50) NOT NULL DEFAULT ''",
    'tahun_selesai_beasiswa': "VARCHAR(50) NOT NULL DEFAULT ''",
    
    # === PREVIOUS SCHOOL ===
    'asal_sekolah': "VARCHAR(100) NOT NULL DEFAULT ''",
    'alamat_sekolah_asal': "VARCHAR(150) NOT NULL DEFAULT ''",
    'npsn': "VARCHAR(25) NOT NULL DEFAULT ''",
    'nsm': "VARCHAR(50) NOT NULL DEFAULT ''",
    'tahunlulus': "VARCHAR(20) NOT NULL DEFAULT ''",
    'pernah_paud': "VARCHAR(8) NOT NULL DEFAULT ''",
    'pernah_tk': "VARCHAR(8) NOT NULL DEFAULT ''",
    
    # === RANKINGS ===
    'rangking': "INT(11) NOT NULL DEFAULT 0",
    'peringkat_semester_1': "INT(11) NOT NULL DEFAULT 0",
    'peringkat_semester_2': "INT(11) NOT NULL DEFAULT 0",
    'peringkat_semester_3': "INT(11) NOT NULL DEFAULT 0",
    'peringkat_semester_4': "INT(11) NOT NULL DEFAULT 0",
    'peringkat_semester_5': "INT(11) NOT NULL DEFAULT 0",
    'peringkat_semester_6': "INT(11) NOT NULL DEFAULT 0",
    
    # === EXAM SCORES ===
    'nilai_un3': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nilai_un': "DECIMAL(5,2) NOT NULL DEFAULT 0.00",
    'nilai_us': "DECIMAL(6,2) NOT NULL DEFAULT 0.00",
    'nilai_un_b_indo': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'nilai_un_matematika': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'nilai_un_b_ing': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'nilai_un_ipa': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'rata_rata_us': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'jmlh_nilai_un': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'rata_rata_un': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'nomor_ijazah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nomor_skhu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nomor_peserta_un': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nomor_akta_lahir': "VARCHAR(50) NOT NULL DEFAULT ''",
    
    # === REPORT CARDS - AVERAGES ===
    'rata_rata_rapor_semester_1': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'rata_rata_rapor_semester_2': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'rata_rata_rapor_semester_3': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'rata_rata_rapor_semester_4': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'rata_rata_rapor_semester_5': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'rata_rata_rapor_semester_6': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    
    # === REPORT CARDS - TOTALS ===
    'jumlah_rapor_semester_1': "INT(11) NOT NULL DEFAULT 0",
    'jumlah_rapor_semester_2': "INT(11) NOT NULL DEFAULT 0",
    'jumlah_rapor_semester_3': "INT(11) NOT NULL DEFAULT 0",
    'jumlah_rapor_semester_4': "INT(11) NOT NULL DEFAULT 0",
    'jumlah_rapor_semester_5': "INT(11) NOT NULL DEFAULT 0",
    'jumlah_rapor_semester_6': "INT(11) NOT NULL DEFAULT 0",
    
    # === REPORT CARDS - RELIGION ===
    'agama_rapor_semester_1': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'agama_rapor_semester_2': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'agama_rapor_semester_3': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'agama_rapor_semester_4': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'agama_rapor_semester_5': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'agama_rapor_semester_6': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    
    # === REPORT CARDS - IPS ===
    'ips_rapor_semester_1': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ips_rapor_semester_2': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ips_rapor_semester_3': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ips_rapor_semester_4': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ips_rapor_semester_5': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ips_rapor_semester_6': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    
    # === REPORT CARDS - PKN ===
    'pkn_rapor_semester_5': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    
    # === REPORT CARDS - BAHASA INDONESIA (Semesters 1-12) ===
    'b_indo_rapor_semester_1': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_2': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_3': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_4': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_5': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_6': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_7': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_8': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_9': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_10': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_11': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_indo_rapor_semester_12': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    
    # === REPORT CARDS - MATEMATIKA (Semesters 1-12) ===
    'matematika_rapor_semester_1': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_2': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_3': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_4': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_5': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_6': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_7': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_8': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_9': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_10': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_11': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'matematika_rapor_semester_12': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    
    # === REPORT CARDS - BAHASA INGGRIS (Semesters 1-10) ===
    'b_ing_rapor_semester_1': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_ing_rapor_semester_2': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_ing_rapor_semester_3': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_ing_rapor_semester_4': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_ing_rapor_semester_5': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_ing_rapor_semester_6': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_ing_rapor_semester_7': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_ing_rapor_semester_8': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_ing_rapor_semester_9': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'b_ing_rapor_semester_10': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    
    # === REPORT CARDS - IPA (Semesters 1-12) ===
    'ipa_rapor_semester_1': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_2': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_3': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_4': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_5': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_6': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_7': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_8': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_9': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_10': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_11': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    'ipa_rapor_semester_12': "DECIMAL(4,2) NOT NULL DEFAULT 0.00",
    
    # === FATHER INFO ===
    'nama_ayah': "VARCHAR(100) NOT NULL DEFAULT ''",
    'nik_ayah': "VARCHAR(20) NOT NULL DEFAULT ''",
    'alamat_ayah': "TEXT NOT NULL",
    'tempat_lahir_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'tanggal_lahir_ayah': "DATE NOT NULL",
    'usia_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'tahun_lahir_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'agama_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'pendidikan_ayah': "VARCHAR(100) NOT NULL DEFAULT ''",
    'pekerjaan_ayah': "VARCHAR(100) NOT NULL DEFAULT ''",
    'penghasilan_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'cacat_badan_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'telepon_ayah': "VARCHAR(20) NOT NULL DEFAULT ''",
    'status_rumah_ayah': "ENUM('sendiri','kontrak','dinas') NOT NULL DEFAULT 'sendiri'",
    'alamat_kerja_ayah': "VARCHAR(1000) NOT NULL DEFAULT ''",
    'jarak_kekantor_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'transportasi_ayah': "VARCHAR(100) NOT NULL DEFAULT ''",
    'suku_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'bahasa_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'pendidikan_agama_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'bacaan_quran_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'status_ayah': "VARCHAR(100) NOT NULL DEFAULT ''",
    'organisasi_islam_ayah': "VARCHAR(50) NOT NULL DEFAULT ''",
    'bacaan_ayah': "VARCHAR(100) NOT NULL DEFAULT ''",
    
    # === MOTHER INFO ===
    'nama_ibu': "VARCHAR(100) NOT NULL DEFAULT ''",
    'nik_ibu': "VARCHAR(20) NOT NULL DEFAULT ''",
    'alamat_ibu': "TEXT NOT NULL",
    'tempat_lahir_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'tanggal_lahir_ibu': "DATE NOT NULL",
    'usia_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'tahun_lahir_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'agama_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'pendidikan_ibu': "VARCHAR(100) NOT NULL DEFAULT ''",
    'pekerjaan_ibu': "VARCHAR(100) NOT NULL DEFAULT ''",
    'penghasilan_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'cacat_badan_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'telepon_ibu': "VARCHAR(20) NOT NULL DEFAULT ''",
    'status_rumah_ibu': "ENUM('sendiri','kontrak','dinas') NOT NULL DEFAULT 'sendiri'",
    'alamat_kerja_ibu': "VARCHAR(100) NOT NULL DEFAULT ''",
    'jarak_kekantor_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'transportasi_ibu': "VARCHAR(100) NOT NULL DEFAULT ''",
    'suku_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'bahasa_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'pendidikan_agama_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'bacaan_quran_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'status_ibu': "VARCHAR(100) NOT NULL DEFAULT ''",
    'organisasi_islam_ibu': "VARCHAR(50) NOT NULL DEFAULT ''",
    'bacaan_ibu': "VARCHAR(100) NOT NULL DEFAULT ''",
    
    # === GUARDIAN INFO ===
    'nama_wali': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nik_wali': "VARCHAR(20) NOT NULL DEFAULT ''",
    'alamat_wali': "TEXT NOT NULL",
    'tempat_lahir_wali': "VARCHAR(50) NOT NULL DEFAULT ''",
    'tanggal_lahir_wali': "DATE NOT NULL",
    'usia_wali': "INT(11) NOT NULL DEFAULT 0",
    'tahun_lahir_wali': "VARCHAR(50) NOT NULL DEFAULT ''",
    'agama_wali': "VARCHAR(100) NOT NULL DEFAULT ''",
    'pendidikan_wali': "VARCHAR(50) NOT NULL DEFAULT ''",
    'pekerjaan_wali': "VARCHAR(50) NOT NULL DEFAULT ''",
    'penghasilan_wali': "VARCHAR(50) NOT NULL DEFAULT ''",
    'cacat_badan_wali': "VARCHAR(50) NOT NULL DEFAULT ''",
    'telepon_wali': "VARCHAR(20) NOT NULL DEFAULT ''",
    
    # === ACHIEVEMENTS ===
    'prestasi': "TEXT NOT NULL",
    'prestasi_dua': "TEXT NOT NULL",
    'tingkat_kec': "ENUM('tidak','ya') NOT NULL",
    'tingkat_kab': "ENUM('tidak','ya') NOT NULL",
    'tingkat_prov': "ENUM('tidak','ya') NOT NULL",
    'tingkat_nas': "ENUM('tidak','ya') NOT NULL",
    'tingkat_inter': "ENUM('tidak','ya') NOT NULL",
    'prestasi_kec1': "VARCHAR(100) NOT NULL DEFAULT ''",
    'prestasi_kec2': "VARCHAR(100) NOT NULL DEFAULT ''",
    'prestasi_kec3': "VARCHAR(100) NOT NULL DEFAULT ''",
    'prestasi_kab1': "VARCHAR(100) NOT NULL DEFAULT ''",
    'prestasi_kab2': "VARCHAR(100) NOT NULL DEFAULT ''",
    'prestasi_prov1': "VARCHAR(100) NOT NULL DEFAULT ''",
    'prestasi_nas1': "VARCHAR(100) NOT NULL DEFAULT ''",
    'prestasi_inter1': "VARCHAR(100) NOT NULL DEFAULT ''",
    
    # === PAYMENT INFO ===
    'pembayaran': "VARCHAR(255) NOT NULL DEFAULT ''",
    'penghasilan': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nama_rekening_pembayaran': "VARCHAR(100) NOT NULL DEFAULT ''",
    'telepon_pembayaran': "INT(11) NOT NULL DEFAULT 0",
    'bank_asal': "VARCHAR(50) NOT NULL DEFAULT ''",
    'bank_tujuan': "VARCHAR(50) NOT NULL DEFAULT ''",
    'nominal_transfer': "INT(11) NOT NULL DEFAULT 0",
    'tanggal_transfer': "DATE NOT NULL",
    'bukti_pembayaran': "VARCHAR(255) NOT NULL DEFAULT ''",
    'konfirmasi_pembayaran': "ENUM('0','1') NOT NULL",
    
    # === MISC ===
    'data_periodik': "TEXT NOT NULL",
    'referensi': "VARCHAR(32) NOT NULL DEFAULT ''",
    'foto': "VARCHAR(100) NOT NULL DEFAULT ''",
    'tgl': "DATETIME NOT NULL",
}


def sanitize_column_name(col_name):
    """Clean column name to match DB convention"""
    s = str(col_name).lower()
    s = s.replace(' ', '_').replace('/', '_').replace('(', '').replace(')', '')
    s = s.replace('-', '_').replace('.', '_')
    s = ''.join(c for c in s if c.isalnum() or c == '_')
    while '__' in s:
        s = s.replace('__', '_')
    return s.strip('_')


def get_column_type(col_name):
    """Get column type from mapping or infer it"""
    clean_name = sanitize_column_name(col_name)
    
    # Check exact match
    if clean_name in COLUMN_TYPES:
        return COLUMN_TYPES[clean_name]
    
    # Pattern matching for unmapped columns
    if 'rapor_semester' in clean_name:
        return "DECIMAL(4,2) NOT NULL DEFAULT 0.00"
    if clean_name.startswith('peringkat_'):
        return "INT(11) NOT NULL DEFAULT 0"
    if clean_name.startswith('jumlah_'):
        return "INT(11) NOT NULL DEFAULT 0"
    if 'tanggal' in clean_name and 'sakit' not in clean_name:
        return "DATE NOT NULL"
    if clean_name in ['tgl', 'tanggal_isi_form']:
        return "DATETIME NOT NULL"
    
    # Default
    return "VARCHAR(255) NOT NULL DEFAULT ''"


def escape_value(val, col_type):
    """Escape value based on column type"""
    # Handle Series
    if isinstance(val, pd.Series):
        if len(val) == 0:
            return get_default_value(col_type)
        val = val.iloc[0]
    
    # Handle None/NaN
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return get_default_value(col_type)
    
    try:
        if pd.isna(val):
            return get_default_value(col_type)
    except:
        pass
    
    # Convert to string
    s = str(val).strip()
    if s == '' or s == 'nan' or s == 'None':
        return get_default_value(col_type)
    
    # Handle by type
    if 'INT' in col_type:
        try:
            return str(int(float(s)))
        except:
            return get_default_value(col_type)
    
    elif 'DECIMAL' in col_type:
        try:
            return str(float(s))
        except:
            return get_default_value(col_type)
    
    elif 'DATE' in col_type:
        if s == '0000-00-00' or s == '0000-00-00 00:00:00':
            return "'0000-00-00'"
        # Remove time if exists
        s = s.split(' ')[0]
        return f"'{s}'"
    
    elif 'ENUM' in col_type:
        # Extract valid values from ENUM definition
        match = re.search(r"ENUM\((.*?)\)", col_type)
        if match:
            valid = [v.strip("'") for v in match.group(1).split(',')]
            if s in valid:
                return f"'{s}'"
        return get_default_value(col_type)
    
    else:
        # String - escape quotes
        s = s.replace("'", "''")
        s = s.replace("\\", "\\\\")
        return f"'{s}'"


def get_default_value(col_type):
    """Get default value for NULL fields"""
    if 'INT' in col_type:
        return '0'
    elif 'DECIMAL' in col_type:
        return '0.00'
    elif 'DATE' in col_type:
        return "'0000-00-00'"
    elif 'DATETIME' in col_type:
        return "'0000-00-00 00:00:00'"
    elif 'ENUM' in col_type:
        # Extract first ENUM value
        match = re.search(r"ENUM\('([^']+)'", col_type)
        if match:
            return f"'{match.group(1)}'"
        return "''"
    else:
        return "''"


def generate_sql_advanced(df, table_name="psb_member"):
    """Generate SQL matching psb_member structure"""
    print(f"\n🔧 Generating SQL for table: {table_name}")
    print(f"📊 DataFrame: {len(df)} rows × {len(df.columns)} columns\n")
    
    # Sanitize column names
    cols = [sanitize_column_name(c) for c in df.columns]
    
    # Filter: Only keep columns that exist in VALID_COLUMNS
    print("🔍 Filtering columns...")
    valid_cols = []
    valid_indices = []
    skipped_cols = []
    seen_cols = set()  # Track duplicates
    duplicate_cols = []
    
    for i, col in enumerate(cols):
        if col in VALID_COLUMNS:
            # Check for duplicates
            if col in seen_cols:
                duplicate_cols.append(col)
                continue  # Skip duplicate
            
            seen_cols.add(col)
            valid_cols.append(col)
            valid_indices.append(i)
        else:
            skipped_cols.append(col)
    
    if duplicate_cols:
        print(f"⚠️  Removed {len(duplicate_cols)} duplicate columns:")
        for col in set(duplicate_cols):  # Show unique duplicates
            print(f"   - {col}")
    
    if skipped_cols:
        print(f"⚠️  Skipped {len(skipped_cols)} unknown columns:")
        for col in skipped_cols[:10]:  # Show first 10
            print(f"   - {col}")
        if len(skipped_cols) > 10:
            print(f"   ... and {len(skipped_cols) - 10} more")
    
    print(f"✅ Using {len(valid_cols)} valid columns\n")
    
    # Filter DataFrame to only valid columns
    df = df.iloc[:, valid_indices]
    cols = valid_cols
    col_types = [get_column_type(c) for c in cols]
    
    # CREATE TABLE statement
    create = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
    create += "  `no` INT(11) NOT NULL AUTO_INCREMENT,\n"
    
    for col, col_type in zip(cols, col_types):
        if col != 'no':  # Skip if 'no' already exists
            create += f"  `{col}` {col_type},\n"
    
    create += "  PRIMARY KEY (`no`),\n"
    create += "  KEY `subdomain` (`subdomain`)\n"
    create += ") ENGINE=MyISAM DEFAULT CHARSET=latin1;\n\n"
    
    # INSERT statements
    inserts = []
    for idx, row in enumerate(df.itertuples(index=False), 1):
        values = []
        for i, cell in enumerate(row):
            col_type = col_types[i]
            values.append(escape_value(cell, col_type))
        
        cols_str = ', '.join([f'`{c}`' for c in cols])
        vals_str = ', '.join(values)
        sql = f"INSERT INTO `{table_name}` ({cols_str}) VALUES ({vals_str});\n"
        inserts.append(sql)
        
        # Progress indicator
        if idx % 50 == 0:
            print(f"  ✓ Generated {idx}/{len(df)} INSERT statements...")
    
    print(f"\n✅ Done! Generated {len(inserts)} INSERT statements\n")
    
    return {
        'create_table': create,
        'inserts': inserts,
        'full_sql': create + '\n'.join(inserts)
    }


def save_sql(sql_dict, filename="output.sql"):
    """Save SQL to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(sql_dict['full_sql'])
        print(f"✅ SQL saved to: {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False