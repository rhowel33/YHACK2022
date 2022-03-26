# YHACK2022
Yhack code for year 2022
Group: Eli Cox, Christian and Reagan Howell

# Setup and installation
Make sure you have python 3.10.x (use pyenv if you need to). Then run
```bash
git clone https://github.com/rhowel33/YHACK2022.git
cd YHACK2022
python -m venv ../speech_env
source ../speech_env/bin/activate
pip install -r requirements.txt
python -c 'import nltk; nltk.download("punkt"); nltk.download("averaged_perceptron_tagger")'
```
