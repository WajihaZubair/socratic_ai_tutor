import requests

# This function simply forwards the text to your cloud-hosted model
def generate_response(user_input):
    # REPLACE THIS URL with the unique ngrok address Colab gives you in Step 2!
    colab_url = "https://emu-unsnap-dried.ngrok-free.dev/generate"

    
    try:
        payload = {"prompt": user_input}
        response = requests.post(colab_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json().get("response", "Error parsing tutor response.")
        else:
            return f"Tutor Error: Server responded with status code {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return "The cloud tutor is currently offline. Please ensure your Colab cell is active."
