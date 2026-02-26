# Simple HTTP Server

A lightweight HTTP server built with Python's built-in modules. Perfect for development, testing, and learning purposes.

## Features

- 🚀 **Built-in Python modules** - No external dependencies required
- 📁 **File serving** - Serves static files from the current directory
- 🌐 **CORS enabled** - Cross-origin requests allowed for development
- 📝 **Enhanced logging** - Better request logging with timestamps
- 🔍 **File detection** - Automatically detects HTML and web assets
- 📂 **Directory listing** - Browse files in the current directory

## Quick Start

### 1. Run the server
```bash
python simple_server.py
```

### 2. Access your server
- **Main page**: http://localhost:8000/index.html
- **File browser**: http://localhost:8000/
- **Any HTML file**: http://localhost:8000/yourfile.html

### 3. Stop the server
Press `Ctrl+C` in the terminal

## Server Details

- **Port**: 8000 (configurable in the code)
- **Protocol**: HTTP/1.1
- **Handler**: Custom SimpleHTTPRequestHandler
- **CORS**: Enabled for all origins (development only)
- **File Detection**: Automatically scans for HTML and web assets

## File Structure

```
SecurityLearnings/
├── simple_server.py      # Main server script
├── index.html           # Sample HTML page (external file)
├── requirements.txt     # Dependencies (none required)
└── README.md           # This file
```

## Customization

### Change Port
Edit the `PORT` variable in `simple_server.py`:
```python
PORT = 8080  # Change to your preferred port
```

### Add Custom Endpoints
Extend the `SimpleHTTPServer` class to add custom routing logic.

### Modify Content
Edit any HTML, CSS, or JavaScript files in your directory. The server will serve them as-is.

## Security Notes

⚠️ **This server is for development and learning purposes only!**

- CORS is enabled for all origins
- No authentication or rate limiting
- Serves files from the current directory
- Not suitable for production use

## Troubleshooting

### Port Already in Use
If you get "Address already in use" error:
1. Stop other services using port 8000
2. Change the port number in the code
3. Use `lsof -i :8000` to find what's using the port

### Permission Denied
Make sure you have write permissions in the current directory for creating sample files.

## Requirements

- Python 3.6 or higher
- No external packages required
- Works on Windows, macOS, and Linux

## License

This is a simple learning project. Feel free to modify and use as needed.
