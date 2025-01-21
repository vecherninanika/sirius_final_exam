from pathlib import Path

import pytest
from httpx import AsyncClient
from starlette import status

from tests.const import URLS

from webapp.db.models import Post

BASE_DIR = Path(__file__).parent

FIXTURES_PATH = BASE_DIR / "fixtures"


@pytest.mark.parametrize(
    ("username", "password", "fixtures", "expected_status"),
    [
        (
            "test_client",
            "secret",
            [
                FIXTURES_PATH / "post.json",
            ],
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.asyncio()
@pytest.mark.usefixtures("_common_api_fixture")
async def test_get_post(
    client: AsyncClient,
    access_token: str,
    expected_status,
) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await client.get("/api/ingredient", headers=headers)
    assert response.status_code == expected_status
    assert len(response.json()) >= 1

