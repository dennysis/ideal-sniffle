import requests
import base64
from datetime import datetime
from flask import current_app

class PaymentGateway:
    def __init__(self):
        self.mpesa_consumer_key = current_app.config.get('MPESA_CONSUMER_KEY')
        self.mpesa_consumer_secret = current_app.config.get('MPESA_CONSUMER_SECRET')
        self.mpesa_shortcode = current_app.config.get('MPESA_SHORTCODE')
        self.mpesa_passkey = current_app.config.get('MPESA_PASSKEY')
    
    def get_mpesa_access_token(self):
        """Get M-Pesa access token"""
        try:
            api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
            
            # Create credentials
            credentials = base64.b64encode(
                f"{self.mpesa_consumer_key}:{self.mpesa_consumer_secret}".encode()
            ).decode('utf-8')
            
            headers = {
                'Authorization': f'Basic {credentials}'
            }
            
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            
            return response.json().get('access_token')
        except Exception as e:
            current_app.logger.error(f"Failed to get M-Pesa token: {str(e)}")
            return None
    
    def initiate_mpesa_payment(self, phone_number, amount, account_reference, transaction_desc):
        """Initiate M-Pesa STK Push payment"""
        access_token = self.get_mpesa_access_token()
        if not access_token:
            return {'success': False, 'error': 'Failed to get access token'}
        
        try:
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode(
                f"{self.mpesa_shortcode}{self.mpesa_passkey}{timestamp}".encode()
            ).decode('utf-8')
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "BusinessShortCode": self.mpesa_shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone_number,
                "PartyB": self.mpesa_shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": "https://your-domain.com/mpesa/callback",
                "AccountReference": account_reference,
                "TransactionDesc": transaction_desc
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            return {'success': True, 'data': response.json()}
        except Exception as e:
            current_app.logger.error(f"M-Pesa payment failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def process_card_payment(self, card_details, amount):
        """Process card payment (placeholder for actual payment processor)"""
        # This would integrate with actual payment processors like Stripe, PayPal, etc.
        # For now, return a mock successful response
        return {
            'success': True,
            'transaction_id': f"CARD_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'message': 'Payment processed successfully'
        }
    
    def process_paypal_payment(self, amount, currency='USD'):
        """Process PayPal payment (placeholder)"""
        # This would integrate with PayPal API
        return {
            'success': True,
            'transaction_id': f"PP_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'message': 'PayPal payment processed successfully'
        }