# Ollama
Describe Images using Ollama Models 

### Step 1. run docker
```
$ docker run -p 11434:11434 --name ollama-dev [Docker Image]
$ docker exec -it ollama-dev /bin/bash
```

### Step 2. Set env 
```bash
$ export OLLAMA_HOST=http://host.docker.internal:11434
```

### Step 3. Ollama Connection test
we can test connection using 'curl'
```bash
$ apt-get update -y
$ apt-get install curl -y
$ curl http://host.docker.internal:11434/api/tags
```
### Step 4. run Ollama models 
we can select ollama models (config/llm_configs  -> ollama model, ollama model tags (e.g latest, 3b)
``` bash
$ python describe_image.py --file_name 01.jpg
```

### llama3.2-vision model results 
