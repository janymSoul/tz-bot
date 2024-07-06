from oauth2client.service_account import ServiceAccountCredentials
import gspread
BOT_TOKEN = "7130994236:AAGy4YaYg795CB6U7oKhTNSVGifvai5aYsg"
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("гугл таблички").sheet1
YOOKASSA_API_URL = 'https://api.yookassa.ru/v3/payments'
YOOKASSA_SECRET_KEY = 'test_5szewN8JlQ1dJMupmvvCJaz7pyVl89p1P2mYNonsNa8'
YOOKASSA_SHOP_ID = '414739'