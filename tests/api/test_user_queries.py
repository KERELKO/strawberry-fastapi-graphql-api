import httpx
import pytest

from .common import BASE_GRAPHQL_URL

GET_USER_QUERY = """
query Query($id: ID!) {
  user(id: $id) {
    username
    id
  }
}
"""


@pytest.mark.asyncio
async def test_can_get_single_user():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            BASE_GRAPHQL_URL,
            json={'query': GET_USER_QUERY, 'variables': {'id': 1}},
        )

        data = response.json()['data']

        assert (u := data.get('user', None)) is not None

        assert u['username']
        assert u['id']
