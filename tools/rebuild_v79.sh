cd /home/claude/v7/tools; D=/home/claude/v7/b79f; R=/home/claude/b79/ALT_V79_Equipment_Register.xlsx
rm -f $D/v79.bog $D/v79_fpt.bog
python3 make_v79.py /home/claude/work/c_v5.bog /home/claude/work/c_v5.tsv $D/v79_fpt.bog --regdir $D/reg_fpt --timing fpt --register $R > $D/build_fpt.log 2>&1 &
python3 make_v79.py /home/claude/work/c_v5.bog /home/claude/work/c_v5.tsv $D/v79.bog --regdir $D/reg --timing site --register $R > $D/build_site.log 2>&1 &
wait
