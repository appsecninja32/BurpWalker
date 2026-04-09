burp_walk_parse.py is a utility that walks through a directory of Burp project files and other HTTP export formats and builds a list of the web paths that have been seen in captured traffic.

When you point it at a folder, it:

looks at all .burp, .xml, .har, and text files under that folder,
finds every URL inside those files,
normalizes each URL to its first path segment (like /api, /login, etc.),
counts how often each path occurs,
updates a persistent JSON database of all paths seen over time, and
lets you export the results as a frequency‑sorted wordlist or CSV.

The result is a dataset of endpoints based on actual requests captured in your Burp history, which you can use to generate more relevant fuzzing or reconnaissance wordlists and improve your workflow efficiency.
