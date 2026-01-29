import requests
import base64
from django.conf import settings
from datetime import datetime
import os

class DarajaClient:
    def __init__(self):
        self.consumer_key = os.getenv('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
        self.shortcode = os.getenv('MPESA_SHORTCODE', '174379')
        self.passkey = os.getenv('MPESA_PASSKEY')
        self.base_url = "https://sandbox.safaricom.co.ke"

    def get_access_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        try:
            response = requests.get(url, auth=(self.consumer_key, self.consumer_secret), timeout=30)
            if response.status_code == 200:
                return response.json()['access_token']
        except Exception as e:
            print(f"Token Error: {e}")
        return None

    def format_phone(self, phone):
        """Format phone to 2547XXXXXXXX or 2541XXXXXXXX"""
        if not phone:
            return ""
        phone = str(phone).strip().replace("+", "")
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif phone.startswith('254'):
            return phone
        elif len(phone) == 9: # handles 7XXXXXXXX
            phone = '254' + phone
        return phone

    def generate_password(self, timestamp):
        # Note: Password uses the RAW shortcode, but PartyB usually uses formatted phone if it's a phone-based shortcode
        data_to_encode = f"{self.shortcode}{self.passkey}{timestamp}"
        encoded_string = base64.b64encode(data_to_encode.encode())
        return encoded_string.decode('utf-8')

    def stk_push(self, phone_number, amount, callback_url, account_ref="HomeKare", desc="Service Payment"):
        access_token = self.get_access_token()
        if not access_token:
            return {"status": "error", "message": "Failed to generate access token"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)
        
        formatted_phone = self.format_phone(phone_number)
        formatted_shortcode = self.shortcode # Usually stays as is for paybills

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": formatted_phone,
            "PartyB": self.shortcode,
            "PhoneNumber": formatted_phone,
            "CallBackURL": callback_url,
            "AccountReference": account_ref,
            "TransactionDesc": desc
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        
        try:
            print(f"STK Push Payload: {payload}")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            print(f"STK Push Response: {response.status_code} - {response.text}")
            return response.json()
        except Exception as e:
            print(f"STK Push Exception: {str(e)}")
            return {"status": "error", "message": str(e)}

    def query_stk_status(self, checkout_request_id):
        access_token = self.get_access_token()
        if not access_token:
            return {"status": "error", "message": "Failed to generate access token"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = self.generate_password(timestamp)

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        url = f"{self.base_url}/mpesa/stkpushquery/v1/query"

        try:
            print(f"STK Query Payload: {payload}")
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            print(f"STK Query Response: {response.status_code} - {response.text}")
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
