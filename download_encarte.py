import requests
import os


def save_file(dir_name: str, filename: str, content: bytes) -> None:
    """Save file content to disk."""
    os.makedirs(dir_name, exist_ok=True)
    with open(os.path.join(dir_name, filename), "wb") as f:
        f.write(content)
    print(f"Downloaded: {filename}")


def download_files(url: str, dir_name: str, filename: str) -> None:
    """Download PDF files from the given URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        if response.status_code == 200:
            save_file(dir_name, filename, response.content)
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    file_name = "encarte.pdf"
    url = "https://supermercadosguanabara.com.br/encarte/baixe"
    dir_name = "./encartes/"
    download_files(url, dir_name, file_name)
