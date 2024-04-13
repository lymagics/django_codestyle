## Project setup
Document contains steps to setup project.

1. Install [mkcert](https://github.com/FiloSottile/mkcert) and run:
```console
mkcert -install
```

2. Generate ssl certificates:
```console
make certs
```

3. Create .env file with env-example file. Fill .env file with environment variables.

4. Build project:
```console
make build
```

5. Run project:
```console
make start
```
