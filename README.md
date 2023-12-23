# iCV Parser 🏴‍☠️ 🧲

Dockerized Streamlit app to parse collections and magnet links from iCV [icv-crew.com](https://icv-crew.com)

</br>

## Deploy with Docker

### Docker run

Easily deploy with `docker run`:

```
docker run
  --name icvparser
  -p 8051:8501
  -e ICV_USERNAME=<your iCV username>
  -e ICV_PASSWORD=<your iCV password>
  ghcr.io/arseniov/icv-parser/icv-parser:<tag>
```

</br>

### Docker compose

Run with `docker compose`:

```text
# Example docker-compose.yml file

version: '3'
services:
  icvparser:
    container_name: icvparser # Container name
    image: ghcr.io/arseniov/icv-parser/icv-parser:<tag> # Replace <tag> with tag for your architecture. See details below.
    ports:
      - "8051:8501" # Expose TCP port 8051 against the default Streamlit 8501
    environment:
        ICV_USERNAME: <your iCV username> # Replace <your iCV username> with your iCV username
        ICV_PASSWORD: <your iCV password> # Replace <your iCV password> with your iCV password
    healthcheck:
      test: python -c "import requests; print(requests.get('http://localhost:8501/_stcore/health').text)" || exit 1
      interval: 60s
      retries: 5
      start_period: 20s
      timeout: 10s
```

</br>

## Architecture tags

Current available image architectures:

* `amd64`
* `arm64`
