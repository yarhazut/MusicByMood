from googletrans import Translator
import string
# encoding=utf8
import sys
from bs4 import BeautifulSoup
# reload(sys)
# sys.setdefaultencoding('utf8')


translator = Translator()

text = "השתמש בכלי זה להתקנת עותק נקי של הגירסה החדשה ביותר של Windows 10 Home או Windows 10 Pro, ולהסרת אפליקציות שהתקנת או שהגיעו מותקנות מראש במחשב. תהיה לך אפשרות לשמור את הקבצים האישיים שלך. אם ברצונך לשדרג את המחשב הנוכחי שלך שמותקן בו Windows 7 או Windows 8.1 PC, עבור אל קבל את Windows 10 לקבלת מידע נוסף על אפשרויות השדרוג. אם במחשב מותקנת מהדורת Enterprise או Education, הכלי לא יעבוד עבור התקנה נקייה. לקבלת מידע נוסף, בקר במרכז השירות של רישוי רב משתמשים."
soup = BeautifulSoup(text)
print(translator.translate(soup.get_text()).text)

def translate_text(text):
    soup = BeautifulSoup(text)
    return(translator.translate(soup.get_text()).text)

