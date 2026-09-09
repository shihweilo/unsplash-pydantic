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
- **Resource Oriented**: Clean API design mirroring the Unsplash documentation (Photos, Users, Collections, Search, Topics).

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

# Release the connection pool when you are done
client.close()
```

The client can also be used as a context manager, which closes the underlying
connection pool on exit:

```python
with UnsplashClient(access_key=os.getenv("UNSPLASH_ACCESS_KEY")) as client:
    photo = client.photos.random(query="nature")
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

If you cannot use `async with`, call `await client.aclose()` to release the
connection pool explicitly.

### Topics

Topics are Unsplash's editorial categories. Accepted by id or slug:

```python
# Browse topics (order_by: featured, latest, oldest, position)
for topic in client.topics.list(order_by="featured"):
    print(f"{topic.slug}: {topic.total_photos} photos")

# A single topic, and its photos
topic = client.topics.get("wallpapers")
photos = client.topics.photos("wallpapers", orientation="landscape", per_page=5)
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

### Optional Fields

Unsplash returns **abbreviated objects** when a resource is embedded in another
one. A user nested inside a photo, for example, omits `profile_image` and most
`total_*` counters, and its `links` may carry only `self`, `html` and `photos`.

The models mirror that reality: only fields present in *every* representation
are required. On `User` that is `id` and `username`; on `Photo` it is `id`,
`created_at`, `width`, `height`, `urls`, `links` and `user`. Everything else is
`Optional` and defaults to `None`.

```python
photo = client.photos.get("Dwu85P9SOIk")

photo.urls.full          # always present
photo.user.username      # always present

if photo.user.profile_image:          # may be omitted on an embedded user
    print(photo.user.profile_image.large)
```

This means a type checker will point at the `None` cases for you, instead of the
client raising a `ValidationError` from deep inside a response you cannot see.

### Retries

Transport errors (connection resets, DNS failures, timeouts) and `5xx` responses
are retried automatically with exponential backoff, up to `max_retries` times
(default `3`, so up to 4 attempts total). A `Retry-After` header is honored when
the server sends one.

Rate limits (`429`) are deliberately **not** retried unless the response carries
a short `Retry-After`. Unsplash's quota resets hourly, so retrying a rate-limited
request would only delay the `RateLimitError` you need to handle:

```python
from unsplash import RateLimitError, UnsplashClient

# Disable retries entirely
client = UnsplashClient(access_key="...", max_retries=0)

try:
    photo = client.photos.random()
except RateLimitError as exc:
    print(f"Quota exhausted: {exc.remaining}/{exc.limit} remaining")
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