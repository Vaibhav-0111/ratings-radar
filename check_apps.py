from google_play_scraper import app as gapp

ids = [
    'com.moveinsync.ets',
    'com.moveinsync.driver.lite',
    'com.moveinsync.driver.dco',
    'field.moveinsync.ets',
    'com.workinsync.meeting',
    'com.moveinsync.publictransit',
]

for a in ids:
    try:
        info = gapp(a, lang='en', country='in')
        title = (info.get('title') or '')[:40]
        score = info.get('score')
        installs = info.get('installs')
        ratings = info.get('ratings')
        print(f"{a:55} | {title:40} | rating={score} | installs={installs} | ratings={ratings}")
    except Exception as e:
        print(f"{a:55} | ERROR: {e}")
