# bitArticles

## Development

First install pip-tools
```bash
pip install pip-tools
```

For adding libraries and dependencies, use requirements.in for package name and  its version, then do:
```bash
pip-compile requirements.in
```

then install requirements:
```bash
pip install -r requirements.txt
```

## Running
#### With Docker Compose
First time when you want to run the project using docker compose:
```bash
make configs
docker compose up -d
```
Then run below commands:
```bash
docker compose exec -it app bash
make init
```
Now the project is ready for development and testing in local.