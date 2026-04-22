# Burp Walker
<p align="center"\>
  <a href="https://buymeacoffee.com/appsecninja32" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" ></a>
</p>

<p align="center"\>
<img src="images/burpWalker.png" alt="Burp Walker Logo" width="250">
</p>

**Burp Walker** (`burp_walk_parse.py`) is a reconnaissance utility designed to transform stagnant HTTP exports into actionable intelligence. By recursively scanning directories of project files and traffic captures, it extracts, normalizes, and categorizes endpoints to build frequency-based wordlists tailored to your target's actual architecture.

## 🚀 Key Features

  * **Multi-Format Ingestion**: Recursively parses `.burp`, `.xml`, `.har`, and raw `.txt` files.
  * **Path Normalization**: Intelligently strips URLs to their first path segment (e.g., `/api`, `/admin`, `/v1`) to identify core application entry points.
  * **Persistent Intelligence**: Maintains a local JSON database to track endpoints across multiple sessions and projects.
  * **Frequency Analysis**: Automatically counts occurrences so you can prioritize the most active endpoints for fuzzing.
  * **Flexible Export**: Generate sorted wordlists or CSV files for seamless integration into tools like `ffuf`, `dirsearch`, or `gobuster`.

## 🛠️ How It Works

1.  **Walk**: It crawls through a specified folder, looking for any supported traffic capture files.
2.  **Extract**: It extracts every URL found within those files.
3.  **Parse & Normalize**: Each URL is shortened to its primary path (the first segment), cleaning up the noise.
4.  **Database Update**: It updates a persistent local database with the new findings and incremented counts.
5.  **Output**: It provides a frequency-sorted dataset, giving you a map of the application's most common routes.

## 📖 Usage

### Installation

```bash
git clone https://github.com/appsecninja32/BurpWalker.git
cd BurpWalker
pip install -r requirements.txt
```

### Basic Scan

Point the script at a folder containing your Burp exports:

```bash
python burp_walk_parse.py --path ./my_project_exports/
```

### Exporting a Wordlist

To generate a wordlist for reconnaissance based on frequency:

```bash
python burp_walk_parse.py --export wordlist --output top_paths.txt
```

## 🎯 Use Cases

  * **Custom Wordlist Generation**: Create fuzzing lists that are specific to the environment you are testing rather than using generic wordlists.
  * **Attack Surface Mapping**: Quickly identify the main functional areas of a large-scale web application.
  * **Historical Analysis**: Keep a running database of every path you've ever seen across all client engagements.

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

-----

*Maintained by [appsecninja32](https://www.google.com/search?q=https://github.com/appsecninja32)*
