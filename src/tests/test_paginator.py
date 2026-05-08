from unittest.mock import AsyncMock

import pytest

from src.infrastructure.clients.events.paginator import EventsPaginator


@pytest.mark.asyncio
async def test_events_paginator_iteration():
    mock_client = AsyncMock()

    page_1 = {
        "results": [{"id": 1}],
        "next": "https://api.com/page2",
    }
    page_2 = {"results": [{"id": 2}], "next": None}

    mock_client.events.side_effect = [page_1, page_2]

    paginator = EventsPaginator(client=mock_client, start_changed_at="2024-01-01")

    collected_results = []
    async for batch in paginator:
        collected_results.append(batch)

    assert mock_client.events.call_count == 2

    calls = mock_client.events.call_args_list

    args_1, kwargs_1 = calls[0]
    assert kwargs_1["cursor"] is None
    assert kwargs_1["changed_at"] == "2024-01-01"

    args_2, kwargs_2 = calls[1]
    assert kwargs_2["cursor"] == "https://api.com/page2"

    assert collected_results == [[{"id": 1}], [{"id": 2}]]


@pytest.mark.asyncio
async def test_events_paginator_single_page():
    mock_client = AsyncMock()

    page = {
        "results": [{"id": 1}],
        "next": None,
    }

    mock_client.events.return_value = page

    paginator = EventsPaginator(client=mock_client)

    collected_results = []
    async for batch in paginator:
        collected_results.append(batch)

    assert mock_client.events.call_count == 1

    mock_client.events.assert_awaited_once_with(
        cursor=None,
        changed_at="2000-01-01",
    )

    assert collected_results == [[{"id": 1}]]


@pytest.mark.asyncio
async def test_events_paginator_empty_results():
    mock_client = AsyncMock()

    page = {
        "results": [],
        "next": None,
    }

    mock_client.events.return_value = page

    paginator = EventsPaginator(client=mock_client)

    collected_results = []
    async for batch in paginator:
        collected_results.append(batch)

    assert mock_client.events.call_count == 1

    assert collected_results == [[]]
