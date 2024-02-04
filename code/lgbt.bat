@echo on

c:
cd C:\Users\wimer\github\4chan-cca\code

git fetch

git pull

python.exe 4chan_scrape.py

git add logs.txt

git add ../data/lgbt_week_1.csv

git commit -m "routine update"

git push
