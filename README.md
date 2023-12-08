
- github link :
    - https://github.com/2InfinityN6eyond/PaperClip.git

## Usage

```
# configure database first

# set environment variable
export DB_TO_USE="DB_NAME"
export HOST="URL_TO_DB"
export USER="USERNAME_OF_DATABASE"
export PASSWD="PASSWORD_OF_DATABASE"

git clone https://github.com/2InfinityN6eyond/PaperClip.git
cd PaperClip

pip install -r requirements.txt

cd GUI
python main.py --db_use $DB_TO_USE --host HOST --user USER --passwd PASSWD
```

