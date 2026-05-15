# TODO - Penyesuaian panel-eye

- [x] Buat plan implementasi penyesuaian panel-eye agar layout/markup mengikuti panel-stunting (tetap 10 field eye).

- [ ] Update `templates/index.html`: samakan struktur form & tombol reset (dan optionally gunakan field layout yang mirip panel-stunting) untuk section `panel-eye`.
- [ ] Update `templates/index.html`: pastikan `clearFormEye()` masih mengosongkan seluruh 10 field eye yang masih dipakai backend.
- [ ] (Jika diperlukan) Update styling di `templates/style.css`/`static/style.css` agar tampilan panel-eye konsisten dengan panel-stunting.
- [ ] Verifikasi logika: submit panel-eye tetap memanggil `/predict_eye` dan mengirim 10 field sesuai `EYE_FEATURES`.
- [ ] Jalankan app dan tes manual: input panel-eye tidak hilang saat berpindah tab dan hasil muncul.

