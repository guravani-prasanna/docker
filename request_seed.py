import requests

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    """
    Request encrypted seed from instructor API
    """

    # Step 1: Read student public key from PEM file
    with open("student_public.pem", "r") as f:
        public_key = f.read().strip()

    # Convert to single line with \n for line breaks
    public_key_single_line = public_key.replace("\n", "\n")

    # Step 2: Prepare HTTP POST request payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key_single_line
    }

    headers = {"Content-Type": "application/json"}

    try:
        # Step 3: Send POST request
        print(payload)
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        # Step 4: Parse JSON response
        data = response.json()
        if data.get("status") == "success":
            encrypted_seed = data.get("encrypted_seed")

            # Step 5: Save encrypted seed to file (DO NOT commit this file)
            with open("encrypted_seed.txt", "w") as f:
                f.write(encrypted_seed)

            print("Encrypted seed saved to encrypted_seed.txt")
            return encrypted_seed
        else:
            print("Error from API:", data)
            return None

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None


if __name__ == "__main__":
    api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
    student_id = "23p31a4471"  # Replace with your actual ID
    github_repo_url = "https://github.com/guravani-prasanna/docker"  # EXACT repo URL
    request_seed(student_id, github_repo_url, api_url)