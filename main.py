import requests
from datetime import datetime
import smtplib
import time

YOUR_EMAIL = None
EMAIL_PASSWORD = None
DESTINATION_EMAIL = None


# Warsaw position
MY_LAT = 52.229675 # Your latitude
MY_LONG = 21.012230 # Your longitude

# ISS position
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()
iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# sunrise-sunset time

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

while True:
    time.sleep(60)
    if MY_LONG-5 < iss_longitude < MY_LONG+5 and MY_LAT-5 < iss_latitude < MY_LAT+5:
        print(sunrise, time_now.hour, sunset)
        if time_now.hour >= sunset or time_now.hour <= sunrise:
            mail = smtplib.SMTP("smtp.gmail.com")
            mail.starttls()
            mail.login(password=EMAIL_PASSWORD, user=YOUR_EMAIL)
            mail.sendmail(YOUR_EMAIL, DESTINATION_EMAIL, msg="Subject:ISS\n\nLook up")
            print("done")
        else:
            print("bad time")
    else:
        print("bad iss station position")


# BONUS: run the code every 60 seconds.



