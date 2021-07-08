# Orchestration

## How to run

```bash
docker-compose up -d
```

You can watch the output of the containers witch `docker-compose logs`:

```bash
docker-compose logs --follow 
```

## Additional step UFZ developer for Frontend local development - Identity Provider

You can't use `localhost` for local development to authenticate against an Identity Provider, but you can use `localhost.localdomain`
Here's how you can do this on a Linux (Ubuntu) machine (feel free to search for your own operation system):
- Adjust `hosts` file:
    - sudo nano /etc/hosts
    - add the following line: 127.0.0.1 localhost.localdomain
    - save 
      
Application url: https://localhost.localdomain:3000/