###### http://kim.si-young.org/

# 개발환경
- Python 3.6.5
    - django 2.1.7
    - selenium 3.141.0
    - beautifulsoup4 4.6.0
- phantomjs 2.1.1

# 새 환경에서 시작시
```
python manage.py migrate --run-syncdb
```

# Crontab
```
0 * * * * (...)/python (...)/crawler.py >> (...)/crawler.log
```