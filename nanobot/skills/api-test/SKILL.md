---
name: api-test
description: "Test REST APIs with curl/httpie. Support GET, POST, PUT, DELETE, authentication, headers, and JSON payloads."
metadata: {"nanobot":{"emoji":"🔌","requires":{"bins":["curl"]}}}
---

# API Testing Skill

Test and debug REST APIs using curl or httpie.

## Basic Requests

### GET Request
```bash
curl -s "https://api.example.com/users" | jq '.'
```

### GET with Headers
```bash
curl -s -H "Accept: application/json" -H "Authorization: Bearer TOKEN" "https://api.example.com/protected"
```

### POST with JSON
```bash
curl -s -X POST "https://api.example.com/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'
```

### PUT/PATCH Update
```bash
curl -s -X PUT "https://api.example.com/users/123" \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Updated"}'
```

### DELETE Request
```bash
curl -s -X DELETE "https://api.example.com/users/123"
```

## Authentication

### Basic Auth
```bash
curl -s -u "username:password" "https://api.example.com/users"
```

### Bearer Token
```bash
curl -s -H "Authorization: Bearer $TOKEN" "https://api.example.com/users"
```

### API Key in Header
```bash
curl -s -H "X-API-Key: your-api-key" "https://api.example.com/users"
```

### API Key in Query
```bash
curl -s "https://api.example.com/users?api_key=your-api-key"
```

## Advanced Usage

### Save Response to File
```bash
curl -s "https://api.example.com/large-data" -o response.json
```

### Download with Progress
```bash
curl -L "https://example.com/file.zip" -o file.zip --progress-bar
```

### Test with Timing
```bash
curl -s -w "@curl-format.txt" -o /dev/null "https://api.example.com/users"
```

curl-format.txt:
```
time_namelookup:  %{time_namelookup}s
   time_connect:  %{time_connect}s
time_appconnect:  %{time_appconnect}s
  time_pretransfer:  %{time_pretransfer}s
time_starttransfer:  %{time_starttransfer}s
                   ----------
      time_total:  %{time_total}s
```

### Upload File
```bash
curl -s -X POST "https://api.example.com/upload" \
  -F "file=@/path/to/file.pdf" \
  -F "description=Test upload"
```

### Multipart Form Data
```bash
curl -s -X POST "https://api.example.com/data" \
  -F "name=value" \
  -F "file=@data.json;type=application/json"
```

## Debugging

### Verbose Output
```bash
curl -v "https://api.example.com/users"
```

### See Request Headers
```bash
curl -s -D - "https://api.example.com/users" -o /dev/null
```

### Test with Different Methods
```bash
# OPTIONS to see allowed methods
curl -s -X OPTIONS "https://api.example.com/users" -i
```

## Using httpie (alternative)

Install: `pip install httpie`

```bash
# GET request
http GET api.example.com/users

# POST with JSON
http POST api.example.com/users name=John email=john@example.com

# With auth
http --auth username:password GET api.example.com/protected

# Download file
http --download GET api.example.com/file.zip
```

## Tips

- Use `jq` to format JSON: `curl -s "url" | jq '.'`
- Chain commands: `curl -s "url" | jq '.data[] | .name'`
- Test endpoints in parallel for batch operations
- Save common requests as shell functions
- Use environment variables for tokens: `export API_TOKEN=xxx`
