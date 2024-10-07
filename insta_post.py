import requests
import os
import webbrowser
from requests_toolbelt.multipart.encoder import MultipartEncoder
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

class InstaPost:

    def __init__(self):
        # **Important:** Replace these with your actual credentials
        load_dotenv()
        self.INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')

        self.graph_url = 'https://graph.instagram.com/v21.0/'

    def mypost(self, image_path, caption = ''):

        """Posts an image to Instagram using the v21.0 Graph API.

        Args:
            image_path (str): The path to the image file.
            caption (str, optional): The caption for the image. Defaults to ''.
        """

        # 1. Encode the image to Data URI
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                #image_base64 = base64.b64encode(image_data).decode('utf-8')
                image_uri = image_data.hex() #f"data:image/jpeg;base64,{image_base64}" 
        except FileNotFoundError:
            print(f"Error: Image file not found at '{image_path}'")
            return

        # 2. Use the Data URI in the API request
        upload_url = f"{self.graph_url}{self.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"

        headers = {
            "Authorization": f"Bearer {self.INSTAGRAM_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        upload_data = {
            "image_url": image_uri,  # Use the Data URI here
            "caption": caption,
            "access_token": self.INSTAGRAM_ACCESS_TOKEN
        }

        response = requests.post(upload_url, headers=headers, json=upload_data)

        response.raise_for_status()
        upload_response = response.json()
        media_id = upload_response["id"]

        publish_url = f"{self.graph_url}{self.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"

        publish_data = {
            "creation_id": media_id,
            "access_token": self.INSTAGRAM_ACCESS_TOKEN
        }
    
        publish_resp = requests.post(publish_url,headers=headers,json=publish_data)
        publish_resp.raise_for_status()

        print("Image posted successfully!")


    def post_image_to_instagram(self, image_path, caption=''):
        """Posts an image to Instagram using the v21.0 Graph API.

        Args:
            image_path (str): The path to the image file.
            caption (str, optional): The caption for the image. Defaults to ''.
        """

        # 1. Read the image file into memory
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
        except FileNotFoundError:
            print(f"Error: Image file not found at '{image_path}'")
            return

        # 2. Upload the image data
        upload_url = f"{self.graph_url}{self.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"

        headers = {
            "Authorization": f"Bearer {self.INSTAGRAM_ACCESS_TOKEN}",
            "Content-Type": "multipart/form-data"
        }

        files = {"file": ("image.jpg", image_data)}
        response = requests.post(
            upload_url, headers=headers, files=files
        )

        response.raise_for_status()
        upload_response = response.json()
        media_id = upload_response["id"]

        # 3. Publish the image to Instagram
        publish_url = f"{self.graph_url}{self.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
        response = requests.post(
            publish_url, headers=headers, params={"creation_id": media_id}
        )
        response.raise_for_status()

        print("Image posted successfully!")

    def post_text_to_instagram(self, text):
        """Posts a text post to Instagram using the v21.0 Graph API.

        Args:
            access_token (str): Your Instagram Business Account's access token.
            instagram_business_account_id (str): Your Instagram Business Account ID.
            text (str): The text for the post.
        """

        graph_url = 'https://graph.instagram.com/v21.0/'
        post_url = f"{graph_url}{self.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"

        headers = {
            "Authorization": f"Bearer {self.INSTAGRAM_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        data = {
            "caption": text,
            "access_token": self.INSTAGRAM_ACCESS_TOKEN,
        }

        response = requests.post(post_url, headers=headers, json=data)
        response.raise_for_status()

        print("Text posted successfully!")

    def get_imgur_access_token(self):
        """Guides the user through the OAuth 2.0 flow to get an Imgur access token."""

        load_dotenv()
        client_id = os.getenv('IMGUR_Client_ID')
        client_secret = os.getenv('IMGUR_Client_Secret')
        redirect_uri = 'http://127.0.0.1:8080'  # Replace with your actual redirect URI

        # 1. Authorization Phase
        oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
        authorization_url, state = oauth.authorization_url('https://api.imgur.com/oauth2/authorize')
        print('Please go to this URL and authorize the app:', authorization_url)
        #webbrowser.open(authorization_url)

        authorization_response = 'http://127.0.0.1:8080/?state=6AclwoYJ8Vz8fRCCwEiJgQjX9SY3w9&code=29e4e2d49d59e1719c8663713ec426796a446012' #input('Enter the full callback URL you were redirected to: ')

        # 2. Token Exchange Phase
        try:
            token = oauth.fetch_token(
                'https://api.imgur.com/oauth2/token',
                authorization_response=authorization_response,
                client_secret=client_secret,
            )
            return token['access_token']
        except Exception as e:
            print(f"Error during token exchange: {e}")
            return None

    def upload_to_imgur(self, image_path, access_token):
        """Uploads an image to Imgur using the provided access token."""
        url = "https://api.imgur.com/3/image"
        headers = {"Authorization": f"Bearer {access_token}"}
        with open(image_path, "rb") as image_file:
            response = requests.post(url, headers=headers, files={"image": image_file})
        response.raise_for_status()
        return response.json()["data"]["link"]

if __name__ == "__main__":
    # Example usage:
    image_path = "image.jpeg"  # Replace with your image path
    caption = "This is a test image upload using the Meta Graph API!"
    insta = InstaPost()

    imgur_access_token = insta.get_imgur_access_token() # Get the token once

    imgur_url = insta.upload_to_imgur(image_path)

    print("Imgur URL:", imgur_url) 

    text_to_post = "This is a test text post using the Meta Graph API!"

    #insta.post_text_to_instagram(text_to_post)
    insta.mypost(image_path, caption)
    #insta.post_image_to_instagram(image_path, caption)
