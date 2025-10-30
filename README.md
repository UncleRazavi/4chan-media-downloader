## 4chan Media Downloader

A simple Python script to download all media (images, videos, etc.) from one or more 4chan threads.

---
##

## Features

This script provides flexible options for batch downloading media from 4chan:

- **Media Download:** Downloads **all** images, videos, and other media files from the specified threads.
 
- **Batch Downloading:** Supports downloading media from **multiple threads** in a single run.
  
- **File Input Support (`-f` / `--file`):** Easily input a list of thread links or board/thread\_id pairs from a `.txt` file.
 
-  **Improved Link Parsing:** Accepts various input formats for better flexibility:
    * Full URL (e.g., `https://boards.4chan.org/g/thread/12345678`)
    * Short board/thread\_id format (e.g., `g/12345678`)
      
- **Folder Organization:** Downloads are neatly organized into separate, dedicated subfolders within the output directory (e.g., `my_downloads/g_12345678/`).
  
- **Combined Input:** Allows mixing direct command-line arguments and file input in the same command.
  
- **User-Friendly CLI:** Clear command-line interface with detailed console messages and improved **error handling**.

---

## Requirements

* **Python 3.7+**
* The `requests` library

### Installation

1.  Clone the repository (if applicable).
2.  Install the dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

The script offers two primary methods for specifying threads: direct command-line arguments and batch file input.

### 1. Single or Multiple Threads (CLI Arguments)

Use the basic structure to specify the thread by its board and ID.

```bash
# Basic format for a single thread
python download_4chan.py <board> <thread_id> -o <output_directory>

# Example: Downloading thread 12345678 from the /g/ board to the 'downloads' folder
python download_4chan.py g 12345678 -o downloads
