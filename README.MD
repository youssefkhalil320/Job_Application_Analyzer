# Job Application Analyzer
description 

# Usage 
- create virtual python environment 

```
conda create -n job_application python=3.8
```

- activate the environment
```
conda activate job_application
```

- install the requirements 
```
pip install -r requirements.txt
```

-install NLTK stop words
```
cd nltk_scripts
python stop_words_downloader.py
```
### Only do the the following two steps if you wish to try using Ollama models
- Download Ollama Docker image
```
docker run -d -v ollama:/root/.ollama -p 11435:11434 --name ollama ollama/ollama
```

- Run llama3 model locally
```
docker exec -it ollama ollama run llama3
```