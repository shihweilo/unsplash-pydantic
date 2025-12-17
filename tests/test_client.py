import httpx
import respx
import pytest
from unsplash import UnsplashClient, UnsplashError

def test_get_photo_success(respx_mock):
    respx_mock.get("https://api.unsplash.com/photos/foo").mock(
        return_value=httpx.Response(
            200, 
            json={
                "id": "foo",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "width": 100,
                "height": 100,
                "color": "#000",
                "likes": 0,
                "urls": {
                    "raw": "http://e.com/raw",
                    "full": "http://e.com/full",
                    "regular": "http://e.com/reg",
                    "small": "http://e.com/small",
                    "thumb": "http://e.com/thumb"
                },
                "links": {
                    "self": "http://e.com",
                    "html": "http://e.com",
                    "download": "http://e.com/dl",
                    "download_location": "http://e.com/dl_loc"
                },
                "user": {
                    "id": "u1",
                    "username": "u1",
                    "name": "User 1",
                    "total_likes": 0,
                    "total_photos": 0,
                    "total_collections": 0,
                    "profile_image": {
                        "small": "http://e.com/s",
                        "medium": "http://e.com/m",
                        "large": "http://e.com/l"
                    },
                    "links": {
                        "self": "http://e.com",
                        "html": "http://e.com",
                        "photos": "http://e.com",
                        "likes": "http://e.com",
                        "portfolio": "http://e.com",
                        "following": "http://e.com",
                        "followers": "http://e.com"
                    }
                }
            }
        )
    )
    
    client = UnsplashClient(access_key="test_key")
    photo = client.photos.get("foo")
    assert photo.id == "foo"
    
def test_get_photo_not_found(respx_mock):
    respx_mock.get("https://api.unsplash.com/photos/missing").mock(
        return_value=httpx.Response(404, json={"errors": ["Not Found"]})
    )
    
    client = UnsplashClient(access_key="test_key")
    with pytest.raises(UnsplashError) as exc_info:
        client.photos.get("missing")
    
    assert exc_info.value.http_status == 404
