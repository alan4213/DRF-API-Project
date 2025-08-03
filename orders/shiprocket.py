import requests

EMAIL = "aleenabenny33@gmail.com"
PASSWORD = "JCCzVwpTD0f^pke5"

# Shiprocket Auth API Endpoint

AUTH_URL = "https://apiv2.shiprocket.in/v1/external/auth/login"


def get_shiprocket_token():


    payload = {



    "email": EMAIL,

    "password": PASSWORD

    }

    headers= {


    "Content-Type": "application/json"}

    try:

        response=requests.post(AUTH_URL, json=payload, headers=headers) 
        response.raise_for_status() # raise error if response is not

        data = response.json() 
        token =data.get("token")

        if token:

            print(" Shiprocket Token:", token)
            return token
        else:
            print("X Failed to get token. Check credentials.") 
            return  None

    except requests.exceptions.RequestException as e:

        print("X Request failed:", e)

        return None

# Execute the function when the script is run directly
if __name__ == "__main__":
     get_shiprocket_token()
  