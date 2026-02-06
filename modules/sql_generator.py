"""
SQL Generator Module - FIXED VERSION v2.1
Fungsi untuk generate SQL INSERT statements dari DataFrame
PERBAIKAN: NIK, Telepon, NISN, dll sebagai STRING (bukan numeric)
"""

import pandas as pd


def escape_sql_value(value, column_name=''):
    """
    Escape value untuk SQL INSERT
    IMPROVED: Handle NIK, telepon, dll sebagai STRING
    
    Args:
        value: Value yang akan di-escape
        column_name: Nama kolom (untuk special handling)
        
    Returns:
        str: Escaped SQL value
    """
    if pd.isna(value) or value is None:
        return "NULL"
    
    # Convert to string
    value_str = str(value).strip()
    
    # Handle empty string
    if value_str == "":
        return "NULL"
    
    # Remove leading apostrophe from Excel formatting
    if value_str.startswith("'"):
        value_str = value_str[1:]
    
    # Empty after cleaning
    if value_str == "":
        return "NULL"
    
    # CRITICAL: Fields yang HARUS string (jangan convert ke numeric)
    # Ini untuk menghindari kehilangan leading zero atau scientific notation
    string_only_fields = [
        'nik', 'nik_ayah', 'nik_ibu', 'nik_wali',
        'nomor_kk', 'telepon', 'handphone', 
        'telepon_ayah', 'telepon_ibu', 'telepon_wali',
        'telp_ortu', 'nisn', 'nis', 'npsn',
        'nomor_kps', 'nomor_kks', 'nomor_pkh', 
        'nomor_kip', 'nomor_kis', 'nomor_sktm',
        'kodepos', 'rt', 'rw', 'username'
    ]
    
    # Jika kolom harus string, langsung escape tanpa cek numeric
    if column_name.lower() in string_only_fields:
        value_str = value_str.replace("'", "''")
        return f"'{value_str}'"
    
    # Handle tanggal invalid - convert ke NULL
    if value_str in ['0000-00-00', '0000-00-00 00:00:00']:
        return "NULL"
    
    # Untuk kolom lain, coba convert ke numeric
    try:
        # Cek apakah murni angka
        float_val = float(value_str)
        
        # Jika integer, return tanpa .0
        if float_val.is_integer() and column_name not in ['jarak_kesekolah', 'penghasilan_ayah', 'penghasilan_ibu', 'penghasilan_wali']:
            return str(int(float_val))
        
        # Return sebagai float
        return str(float_val)
    except ValueError:
        pass
    
    # Jika bukan numeric, escape sebagai string
    value_str = value_str.replace("'", "''")
    return f"'{value_str}'"


def generate_sql(df, table_name='psb_member', subdomain='hidayatullahbali.sch.id'):
    """
    Generate SQL INSERT statements dari DataFrame
    
    Args:
        df (pandas.DataFrame): Data yang akan di-convert ke SQL
        table_name (str): Nama tabel target
        subdomain (str): Nilai subdomain default
        
    Returns:
        list: List of SQL INSERT statements
    """
    # MAPPING KOLOM YANG BENAR - sesuai dengan HTML table headers
    column_mapping = {
        'No': None,  # Skip
        'Jalur ppdb': 'jalur_ppdb',
        'Nomor pendaftaran': 'nomor_pendaftaran',
        'Jenjang Yg Dipilih ( RA-MI-MTs-MA)': 'jenjang',
        'Nama Lengkap': 'nama',
        'NISN ( Jenjang TK Boleh Di Kosongkan )': 'nisn',
        'Status  ( Mondok / Pulang Pergi ) Khusus  MTs & MA ': 'status_mondok',
        'Bahasa': 'bahasa',
        'Jenjang  ( RA-MI-MTs-MA)': 'email',  # Ini kolom email di HTML!
        'NIK': 'nik',
        'Nomor KK': 'nomor_kk',
        'Kelas': 'kelas',
        'Pilihan kelas': 'pilihan_kelas',
        'Jurusan': 'jurusan',
        'Jurusan dua': 'jurusan_dua',
        'Jurusan tiga': 'jurusan_tiga',
        'Alasan': 'alasan',
        'Tempat Lahir ': 'tempat_lahir',
        'Tanggal Lahir': 'tanggal_lahir',
        'Jenis Kelamin': 'kelamin_jenis',
        'Agama': 'agama',
        'Status anak': 'status_anak',
        'Anak ke': 'anak_ke',
        'Jumlah saudara': 'jumlah_saudara',
        'Jumlah saudara kandung': 'jumlah_saudara_kandung',
        'Jumlah saudara tiri': 'jumlah_saudara_tiri',
        'Jumlah saudara angkat': 'jumlah_saudara_angkat',
        'Tinggi badan': 'tinggi_badan',
        'Berat badan': 'berat_badan',
        'Cacat badan': 'cacat_badan',
        'Golongan darah': 'golongan_darah',
        'Penyakit bawaan': 'penyakit_bawaan',
        'Pernah sakit': 'pernah_sakit',
        'Nama penyakit': 'nama_penyakit',
        'Tanggal sakit': 'tanggal_sakit',
        'Lama sakit': 'lama_sakit',
        'Cita cita': 'cita_cita',
        'Hobi': 'hobi',
        'Alamat Lengkap ': 'alamat',
        'Dusun': 'dusun',
        'Rt': 'rt',
        'Rw': 'rw',
        'Kelurahan': 'kelurahan',
        'Kecamatan': 'kecamatan',
        'Kota': 'kota',
        'Provinsi': 'provinsi',
        'Kodepos': 'kodepos',
        'Sekolah': 'sekolah',
        'Jarak kesekolah': 'jarak_kesekolah',
        'Transportasi kesekolah': 'transportasi_kesekolah',
        'Waktu kesekolah': 'waktu_kesekolah',
        'Jenis tinggal': 'jenis_tinggal',
        'Telepon': 'telepon',
        'No Whatsapp Aktif (WA)': 'handphone',
        'Penerima pkh': 'penerima_pkh',
        'Nomor kps': 'nomor_kps',
        'Jenis ktm': 'jenis_ktm',
        'Nomor sktm': 'nomor_sktm',
        'Nomor kks': 'nomor_kks',
        'Nomor pkh': 'nomor_pkh',
        'Layak pip': 'layak_pip',
        'Alasan pip': 'alasan_pip',
        'Nama kip': 'nama_kip',
        'Nomor kip': 'nomor_kip',
        'Alasan tolak kip': 'alasan_tolak_kip',
        'Penerima kip': 'penerima_kip',
        'Terima fisik kip': 'terima_fisik_kip',
        'Nomor kis': 'nomor_kis',
        'Bujur': 'bujur',
        'Lintang': 'lintang',
        'Lingkar kepala': 'lingkar_kepala',
        'Asal Sekolah ': 'asal_sekolah',
        'Rangking': 'rangking',
        'Peringkat semester 1': 'peringkat_semester_1',
        'Peringkat semester 2': 'peringkat_semester_2',
        'Peringkat semester 3': 'peringkat_semester_3',
        'Peringkat semester 4': 'peringkat_semester_4',
        'Peringkat semester 5': 'peringkat_semester_5',
        'Peringkat semester 6': 'peringkat_semester_6',
        'Alamat sekolah asal': 'alamat_sekolah_asal',
        'Npsn': 'npsn',
        'Tahunlulus': 'tahunlulus',
        'Username ( Maxsimal 10 Huruf )': 'username',
        'Email ortu': 'email_ortu',
        'Telp ortu': 'telp_ortu',
        'Nis': 'nis',
        'Nama Ayah': 'nama_ayah',
        'NIK Ayah': 'nik_ayah',
        'Alamat ayah': 'alamat_ayah',
        'Tempat lahir ayah': 'tempat_lahir_ayah',
        'Tanggal lahir ayah': 'tanggal_lahir_ayah',
        'Usia ayah': 'usia_ayah',
        'Agama ayah': 'agama_ayah',
        'Pendidikan ayah': 'pendidikan_ayah',
        'Pekerjaan  Ayah': 'pekerjaan_ayah',
        'Penghasilan  Ayah': 'penghasilan_ayah',
        'Cacat badan ayah': 'cacat_badan_ayah',
        'Telepon ayah': 'telepon_ayah',
        'Nama Ibu': 'nama_ibu',
        'NIK Ibu ': 'nik_ibu',
        'Alamat ibu': 'alamat_ibu',
        'Tempat lahir ibu': 'tempat_lahir_ibu',
        'Tanggal lahir ibu': 'tanggal_lahir_ibu',
        'Usia ibu': 'usia_ibu',
        'Tahun lahir ayah': 'tahun_lahir_ayah',
        'Tahun lahir ibu': 'tahun_lahir_ibu',
        'Tahun lahir wali': 'tahun_lahir_wali',
        'Agama ibu': 'agama_ibu',
        'Pendidikan Ibu': 'pendidikan_ibu',
        'Pekerjaan Ibu ': 'pekerjaan_ibu',
        'Penghasilan Ibu': 'penghasilan_ibu',
        'Cacat badan ibu': 'cacat_badan_ibu',
        'Telepon ibu': 'telepon_ibu',
        'Nama wali': 'nama_wali',
        'Nik wali': 'nik_wali',
        'Alamat wali': 'alamat_wali',
        'Tempat lahir wali': 'tempat_lahir_wali',
        'Tanggal lahir wali': 'tanggal_lahir_wali',
        'Usia wali': 'usia_wali',
        'Agama wali': 'agama_wali',
        'Pendidikan wali': 'pendidikan_wali',
        'Pekerjaan wali': 'pekerjaan_wali',
        'Penghasilan wali': 'penghasilan_wali',
        'Cacat badan wali': 'cacat_badan_wali',
        'Telepon wali': 'telepon_wali',
        'Prestasi': 'prestasi',
        'Prestasi dua': 'prestasi_dua',
        'Beasiswa': 'beasiswa',
        'Nilai un3': 'nilai_un3',
        'Nilai un': 'nilai_un',
        'Nilai us': 'nilai_us',
        'Nilai un b indo': 'nilai_un_b_indo',
        'Nilai un matematika': 'nilai_un_matematika',
        'Nilai un b ing': 'nilai_un_b_ing',
        'Nilai un ipa': 'nilai_un_ipa',
        'Dari Mana Mendapatkan Informasi Sekolah Kami  ( FB - IG - Tiktok - Google )': 'referensi',
        'Foto': 'foto'
    }
    
    # Kolom database lengkap dengan default values
    db_columns = {
        'subdomain': subdomain,
        'jalur_ppdb': None,
        'gelombang_pendaftaran': None,
        'nomor_pendaftaran': None,
        'nama': None,
        'nama_panggilan': None,
        'link': None,
        'kewarganegaraan': None,
        'bahasa': None,
        'username': None,
        'email': None,
        'password': None,
        'password2': None,
        'nik': None,
        'nomor_kk': None,
        'kelas': None,
        'pilihan_kelas': None,
        'jurusan': None,
        'jurusan_dua': None,
        'jurusan_tiga': None,
        'alasan': None,
        'tempat_lahir': None,
        'tanggal_lahir': None,
        'kelamin_jenis': None,
        'agama': None,
        'status_anak': None,
        'anak_ke': 0,
        'jumlah_saudara': 0,
        'jumlah_saudara_kandung': 0,
        'jumlah_saudara_tiri': 0,
        'jumlah_saudara_angkat': 0,
        'tinggi_badan': None,
        'berat_badan': None,
        'cacat_badan': None,
        'golongan_darah': None,
        'penyakit_bawaan': None,
        'pernah_sakit': None,
        'nama_penyakit': None,
        'tanggal_sakit': None,
        'lama_sakit': None,
        'cita_cita': None,
        'hobi': None,
        'alamat': None,
        'dusun': None,
        'rt': None,
        'rw': None,
        'kelurahan': None,
        'kecamatan': None,
        'kota': None,
        'provinsi': None,
        'kodepos': None,
        'sekolah': None,
        'jarak_kesekolah': 0.0,
        'transportasi_kesekolah': None,
        'waktu_kesekolah': None,
        'jenis_tinggal': None,
        'telepon': None,
        'handphone': None,
        'penerima_pkh': None,
        'nomor_kps': None,
        'jenis_ktm': None,
        'nomor_sktm': None,
        'nomor_kks': None,
        'nomor_pkh': None,
        'layak_pip': None,
        'alasan_pip': None,
        'nama_kip': None,
        'nomor_kip': None,
        'alasan_tolak_kip': None,
        'penerima_kip': None,
        'terima_fisik_kip': None,
        'nomor_kis': None,
        'bujur': None,
        'lintang': None,
        'lingkar_kepala': None,
        'asal_sekolah': None,
        'rangking': 0,
        'peringkat_semester_1': 0,
        'peringkat_semester_2': 0,
        'peringkat_semester_3': 0,
        'peringkat_semester_4': 0,
        'peringkat_semester_5': 0,
        'peringkat_semester_6': 0,
        'alamat_sekolah_asal': None,
        'npsn': None,
        'tahunlulus': 0,
        'nisn': None,
        'email_ortu': None,
        'telp_ortu': None,
        'nis': None,
        'nama_ayah': None,
        'nik_ayah': None,
        'alamat_ayah': None,
        'tempat_lahir_ayah': None,
        'tanggal_lahir_ayah': None,
        'usia_ayah': 0,
        'agama_ayah': None,
        'pendidikan_ayah': None,
        'pekerjaan_ayah': None,
        'penghasilan_ayah': 0.0,
        'cacat_badan_ayah': None,
        'telepon_ayah': None,
        'nama_ibu': None,
        'nik_ibu': None,
        'alamat_ibu': None,
        'tempat_lahir_ibu': None,
        'tanggal_lahir_ibu': None,
        'usia_ibu': 0,
        'tahun_lahir_ayah': 0,
        'tahun_lahir_ibu': 0,
        'tahun_lahir_wali': 0,
        'agama_ibu': None,
        'pendidikan_ibu': None,
        'pekerjaan_ibu': None,
        'penghasilan_ibu': 0.0,
        'cacat_badan_ibu': None,
        'telepon_ibu': None,
        'nama_wali': None,
        'nik_wali': None,
        'alamat_wali': None,
        'tempat_lahir_wali': None,
        'tanggal_lahir_wali': None,
        'usia_wali': 0,
        'agama_wali': None,
        'pendidikan_wali': None,
        'pekerjaan_wali': None,
        'penghasilan_wali': 0.0,
        'cacat_badan_wali': None,
        'telepon_wali': None,
        'prestasi': None,
        'prestasi_dua': None,
        'beasiswa': None,
        'tempuh_kesekolah': None,
        'nilai_un3': None,
        'nilai_un': None,
        'nilai_us': None,
        'nilai_un_b_indo': 0.0,
        'nilai_un_matematika': 0.0,
        'nilai_un_b_ing': 0.0,
        'nilai_un_ipa': 0.0,
        'jenjang': None,
        'tanggal_daftar': 'CURDATE()',
        'tanggal_isi_form': 'NOW()',
        'referensi': None,
        'keputusan': None,
        'tgl': 'NOW()',
        'publish': 1
    }
    
    sql_queries = []
    
    # Generate SQL untuk setiap baris
    for idx, row in df.iterrows():
        # Copy template db_columns
        row_data = db_columns.copy()
        
        # Map data dari HTML ke database columns
        for html_col, db_col in column_mapping.items():
            if db_col and html_col in df.columns:
                value = row[html_col]
                if pd.notna(value) and str(value).strip() != '':
                    row_data[db_col] = value
        
        # Build SQL INSERT
        columns = list(row_data.keys())
        values = []
        
        for col in columns:
            value = row_data[col]
            
            # Handle special columns (functions)
            if col in ['tanggal_daftar', 'tanggal_isi_form', 'tgl']:
                if value in ['CURDATE()', 'NOW()']:
                    values.append(value)
                else:
                    values.append(escape_sql_value(value, col))
            else:
                values.append(escape_sql_value(value, col))
        
        # Generate SQL statement
        sql = f"INSERT INTO `{table_name}` "
        sql += f"(`{'`,`'.join(columns)}`) "
        sql += f"VALUES ({','.join(values)});"
        
        sql_queries.append(sql)
    
    return sql_queries