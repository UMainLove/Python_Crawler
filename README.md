# DATA CRAWLER

Here you have 3 python scripts to crawl data from different sources:

- `website_short_c.py`: This script crawls data from a website using a recursive approach. Faster solution to crawl short-size or mid-size websites.
- `website_long_c.py`: This script crawls data from a website using an iterative approach. This prevents stack overflow and allows you to crawl a large-size websites.
- `github_c.py`: This script crawls data from a GitHub repository.


## Installation

To run the scripts, you need to install the required libraries. You can install them using pip:

```bash
pip install 
attrs==24.2.0
beautifulsoup4==4.12.3
certifi==2024.8.30
cffi==1.17.1
charset-normalizer==3.4.0
cryptography==43.0.3
Deprecated==1.2.14
gitdb==4.0.11
GitPython==3.1.43
h11==0.14.0
html2text==2024.2.26
idna==3.10
outcome==1.3.0.post0
pycparser==2.22
PyGithub==2.5.0
PyJWT==2.9.0
PyNaCl==1.5.0
PySocks==1.7.1
python-dotenv==1.0.1
requests==2.32.3
selenium==4.26.1
smmap==5.0.1
sniffio==1.3.1
sortedcontainers==2.4.0
soupsieve==2.6
tqdm==4.67.0
trio==0.27.0
trio-websocket==0.11.1
typing_extensions==4.12.2
urllib3==2.2.3
websocket-client==1.8.0
wrapt==1.16.0
wsproto==1.2.0
```


## Usage

```bash
python3 website_short_c.py

python3 website_long_c.py

python3 github_c.py
```


## Contributing 

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.