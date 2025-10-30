import os
import requests
import argparse

def download_thread_media(board, thread_id, output_dir):
    api_url = f"https://a.4cdn.org/{board}/thread/{thread_id}.json"
    base_media_url = f"https://i.4cdn.org/{board}/"

    response = requests.get(api_url)
    if response.status_code != 200:
        print(f" Error: Unable to fetch thread {thread_id} from /{board}/")
        return

    thread_data = response.json()
    os.makedirs(output_dir, exist_ok=True)

    count = 0
    for post in thread_data.get("posts", []):
        if "tim" in post and "ext" in post:
            file_name = f"{post['tim']}{post['ext']}"
            file_url = base_media_url + file_name
            file_path = os.path.join(output_dir, file_name)

            if not os.path.exists(file_path):
                print(f" Downloading {file_name}...")
                media_response = requests.get(file_url, stream=True)
                if media_response.status_code == 200:
                    with open(file_path, "wb") as f:
                        for chunk in media_response.iter_content(1024):
                            f.write(chunk)
                    count += 1
                else:
                    print(f" Failed to download {file_name}")
            else:
                print(f" Skipping {file_name} (already exists)")

    print(f"\n Done! Downloaded {count} new files to {output_dir}\n")


def parse_thread_link(link):
    """
    Extracts board and thread_id from either a full 4chan URL or board/thread format.
    Examples:
        https://boards.4chan.org/g/thread/12345678  -> ('g', '12345678')
        g/12345678                                  -> ('g', '12345678')
    """
    link = link.strip()
    if not link:
        return None

    if "4chan.org" in link:
        try:
            parts = link.split("/")
            board = parts[3]
            thread_id = parts[5]
            return board, thread_id
        except IndexError:
            print(f" Invalid 4chan URL format: {link}")
            return None
    elif "/" in link:
        board, thread_id = link.split("/", 1)
        return board, thread_id
    else:
        print(f"❌ Invalid format: {link}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Download media from one or more 4chan threads")
    parser.add_argument("inputs", nargs="*", help="Thread links or board/thread_id pairs (e.g., g/12345678)")
    parser.add_argument("-f", "--file", help="Text file containing thread links (one per line)")
    parser.add_argument("-o", "--output", default="downloads", help="Base output directory")

    args = parser.parse_args()

    threads = []

    # Add threads from command line
    for input_item in args.inputs:
        parsed = parse_thread_link(input_item)
        if parsed:
            threads.append(parsed)

    # Add threads from file
    if args.file:
        if os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8") as f:
                for line in f:
                    parsed = parse_thread_link(line)
                    if parsed:
                        threads.append(parsed)
        else:
            print(f" File not found: {args.file}")
            return

    if not threads:
        print(" No valid threads provided!")
        return

    # Process all threads
    for board, thread_id in threads:
        thread_output = os.path.join(args.output, f"{board}_{thread_id}")
        print(f"\n Processing /{board}/ thread {thread_id}...")
        download_thread_media(board, thread_id, thread_output)


if __name__ == "__main__":
    main()
