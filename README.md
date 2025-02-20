# Ollama
Describe Images using Ollama Models 

### Step 1. run docker
```bash 
$ docker run -p 11434:11434 --name ollama-dev [Docker Image]
$ docker exec -it ollama-dev /bin/bash
```

### Step 2. Set env 
Inside the container, set the Ollama API host so the model can connect properly.
```bash
$ export OLLAMA_HOST=http://host.docker.internal:11434
```

### Step 3. Ollama Connection test
Before running image descriptions, test if Ollama is running correctly.
```bash
$ apt-get update -y
$ apt-get install curl -y
$ curl http://host.docker.internal:11434/api/tags
```
### Step 4. run Ollama models 
Now, we can use a Python script to generate descriptions.
``` bash
$ python describe_image.py --file_name 01.jpg
```

### llama3.2-vision model results
![](testfile/01.jpg)
![](testfile/02.jpg)
![](testfile/03.jpg)
![](testfile/04.jpg)
![](testfile/05.png)
