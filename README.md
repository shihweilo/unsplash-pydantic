# Unsplash Python SDK

[![PyPI version](https://badge.fury.io/py/unsplash-pydantic.svg)](https://badge.fury.io/py/unsplash-pydantic)
[![Python Versions](https://img.shields.io/pypi/pyversions/unsplash-pydantic.svg)](https://pypi.org/project/unsplash-pydantic/)
[![Test](https://github.com/shihweilo/unsplash-pydantic/actions/workflows/test.yml/badge.svg)](https://github.com/shihweilo/unsplash-pydantic/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

> [!WARNING]
> This is an unofficial SDK and is currently under active development.

A modern, type-safe Python client for the [Unsplash API](https://unsplash.com/developers). Built with **Pydantic v2** for robust data validation and **httpx** for high-performance sync and async support.

## ✨ Features

- **Type Safe**: Fully typed response models using Pydantic v2.
- **Async Native**: First-class `async`/`await` support with `AsyncUnsplashClient`.
- **Modern**: Built on `httpx` (HTTP/2 support, connection pooling).
- **Developer Friendly**: IDE auto-completion, detailed error messages, and fully documented resources.
- **Resource Oriented**: Clean API design mirroring the Unsplash documentation (Photos, Users, Collections, Search).

## 🛠️ Installation

Install usage **pip**:

```bash
pip install unsplash-pydantic
```

Or using **Poetry**:

```bash
poetry add unsplash-pydantic
```

## 🚀 Quick Start

### Synchronous Client

Perfect for scripts and standard applications.

```python
import os
from unsplash import UnsplashClient

# Initialize the client
client = UnsplashClient(access_key=os.getenv("UNSPLASH_ACCESS_KEY"))

# Get a random photo of nature
photo = client.photos.random(query="nature", orientation="landscape")

# Access typed fields
print(f"Photo by: {photo.user.name}")
print(f"Description: {photo.description}")
print(f"Download URL: {photo.urls.full}")

# Search for photos
results = client.search.photos("mountains", page=1, per_page=10)
print(f"Found {results.total} photos")
```

### Asynchronous Client

Ideal for high-concurrency applications (FastAPI, etc).

```python
import asyncio
import os
from unsplash import AsyncUnsplashClient

async def main():
    async with AsyncUnsplashClient(access_key=os.getenv("UNSPLASH_ACCESS_KEY")) as client:
        # Fetch user profile asynchronously
        user = await client.users.get("ousplash")
        print(f"{user.name} has {user.total_photos} photos")

        # Get their latest photos
        photos = await client.users.photos(user.username, per_page=5)
        for photo in photos:
            print(f"- {photo.id}: {photo.urls.regular}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 📚 Core Concepts

### Error Handling

All specific errors catch a base `UnsplashError`. Common HTTP errors (401, 404, 429) are mapped to specific exceptions.

```python
from unsplash import UnsplashClient, UnsplashError, RateLimitError

try:
    client.photos.get("invalid-id")
except RateLimitError as e:
    print(f"Rate limited! Limit: {e.limit}, Remaining: {e.remaining}")
except UnsplashError as e:
    print(f"API Error: {e.message}")
```

### Unsplash Guidelines

This SDK helps you follow Unsplash API Guidelines:

1.  **Attribution**: The `Photo` model includes the `user` object with `name` and `links` to properly credit photographers.
2.  **Download Tracking**: Use `client.photos.track_download(id)` or `client.photos.download(id)` to trigger the download event required by the API.
3.  **Hotlinking**: `photo.urls` provides hotlinkable URLs directly.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1.  Fork the repository
2.  Create your feature branch (`git checkout -b feature/amazing-feature`)
3.  Commit your changes (`git commit -m 'Add some amazing feature'`)
4.  Push to the branch (`git push origin feature/amazing-feature`)
5.  Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*This library is not officially affiliated with Unsplash.*