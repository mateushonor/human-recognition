import psycopg2
from twilio.rest import Client

# Substitua com suas credenciais do Twilio



client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(phone_number, message):
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=phone_number
        )
        print(f"Message sent to {phone_number}")
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")

def fetch_and_send_messages(Camera_Name):
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="postgres",
        password="engcomp1413",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT telefone FROM telefones LIMIT 1")
    
    
    phone_number = cursor.fetchone()
    if phone_number:
        send_sms(phone_number[0], "Ei tem humano aqui " + Camera_Name)

    conn.close()


