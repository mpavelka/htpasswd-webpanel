Htpasswd Webpanel
===

Web UI for htpasswd user management.

## Run via Docker

```
docker run -d --name htpanel -v $(pwd):/etc/apache2 -p 8080:8080 mpavelka/htpanel
```

Navigate to [http://localhost:8080]() in your browser.

## TODOS
- Implement session alerts and redirects instead of BadRequest errors returned on invalid POST requests
