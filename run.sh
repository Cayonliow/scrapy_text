rm -r scrapying/output/
rm -r frequent_single_word/output/
rm -r output/
python3 frequent_single_word/fsw_main.py -p 'False'
python3 scrapying/scr_main.py -p 'False'
python3 main.py
