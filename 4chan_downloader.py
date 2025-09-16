import os
import requests
import argparse

def download_thread_media(board, thread_id, output_dir):
    # 4chan JSON API URL for the thread
    api_url = f"https://a.4cdn.org/{board}/thread/{thread_id}.json"
    base_media_url = f"https://i.4cdn.org/{board}/"

    # Get thread data
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Error: Unable to fetch thread {thread_id} from /{board}/")
        return

    thread_data = response.json()

    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Download media files
    count = 0
    for post in thread_data.get("posts", []):
        if "tim" in post and "ext" in post:
            file_name = f"{post['tim']}{post['ext']}"
            file_url = base_media_url + file_name
            file_path = os.path.join(output_dir, file_name)

            if not os.path.exists(file_path):  # Skip if already downloaded
                print(f"Downloading {file_name}...")
                media_response = requests.get(file_url, stream=True)
                if media_response.status_code == 200:
                    with open(file_path, "wb") as f:
                        for chunk in media_response.iter_content(1024):
                            f.write(chunk)
                    count += 1
                else:
                    print(f"Failed to download {file_name}")
            else:
                print(f"Skipping {file_name} (already exists)")

    print(f"\nDone! Downloaded {count} new files to {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Download media from a 4chan thread")
    parser.add_argument("board", help="Board name (e.g., g, wg, pol, etc.)")
    parser.add_argument("thread_id", help="Thread ID")
    parser.add_argument("-o", "--output", default="downloads", help="Output directory")

    args = parser.parse_args()

    download_thread_media(args.board, args.thread_id, args.output)


if __name__ == "__main__":
    main()
