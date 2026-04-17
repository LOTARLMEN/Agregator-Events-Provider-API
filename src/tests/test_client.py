import uuid

import httpx
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.application.exceptions import ProviderTimeout
from src.infrastructure.clients.events.provider import EventProviderClient


@pytest.mark.asyncio
async def test_events_success():
    service = EventProviderClient()

    expected_response = {
        "items": [{"id": "1", "name": "Concert"}],
        "cursor": None,
    }

    with patch(
        "src.infrastructure.clients.events.provider.httpx.AsyncClient"
    ) as mock_client_class:
        mock_client_instance = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        mock_client_instance.get.return_value = mock_response

        result = await service.events(changed_at="2024-01-01")

        assert result == expected_response

        mock_client_instance.get.assert_called_once()

        args, kwargs = mock_client_instance.get.call_args
        assert kwargs["params"] == {"changed_at": "2024-01-01"}
        assert "x-api-key" in kwargs["headers"]


@pytest.mark.asyncio
async def test_events_with_cursor_logic():
    service = EventProviderClient()

    my_cursor = "https://external-provider.com/api/v2/events/?next=abc"

    fake_response_data = {"items": []}

    with patch(
        "src.infrastructure.clients.events.provider.httpx.AsyncClient"
    ) as mock_client_class:
        mock_client_instance = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = fake_response_data
        mock_client_instance.get.return_value = mock_response

        await service.events(cursor=my_cursor)

        args, kwargs = mock_client_instance.get.call_args

        called_url = args[0]

        assert called_url == my_cursor

        assert kwargs["params"] is None


@pytest.mark.asyncio
async def test_events_server_error():
    service = EventProviderClient()

    with patch(
        "src.infrastructure.clients.events.provider.httpx.AsyncClient"
    ) as mock_client_class:
        mock_client_instance = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance

        mock_client_instance.get.side_effect = httpx.ConnectTimeout(
            "Connection timeout"
        )

        with pytest.raises(ProviderTimeout):
            await service.events()

        mock_client_instance.get.assert_called_once()


@pytest.mark.asyncio
async def test_register_success():
    service = EventProviderClient()
    mock_event_id = uuid.uuid4()
    mock_user_body = {"user_id": str(uuid.uuid4())}
    fake_response_data = {"success": True}

    with patch(
        "src.infrastructure.clients.events.provider.httpx.AsyncClient"
    ) as mock_client_class:
        mock_client_instance = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = fake_response_data

        mock_client_instance.post.return_value = mock_response

        result = await service.register(mock_event_id, mock_user_body)

        mock_client_instance.post.assert_called_once()

        args, kwargs = mock_client_instance.post.call_args
        called_url = args[0]

        assert str(mock_event_id) in called_url

        assert kwargs["data"] == mock_user_body
        assert result == fake_response_data


@pytest.mark.asyncio
async def test_unregister_success():
    service = EventProviderClient()
    mock_event_id = uuid.uuid4()
    mock_ticket_id = uuid.uuid4()

    with patch(
        "src.infrastructure.clients.events.provider.httpx.AsyncClient"
    ) as mock_client_class:
        mock_client_instance = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance

        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_client_instance.request.return_value = mock_response

        await service.unregister(mock_event_id, mock_ticket_id)

        mock_client_instance.request.assert_called_once()

        args, kwargs = mock_client_instance.request.call_args

        called_method = args[0]
        called_url = args[1]

        assert called_method == "DELETE"
        assert str(mock_event_id) in called_url
        assert "unregister" in called_url

        assert kwargs["json"] == {"ticket_id": str(mock_ticket_id)}


@pytest.mark.asyncio
async def test_seats():
    service = EventProviderClient()
    mock_event_id = uuid.uuid4()
    mock_response_data = {"seats": []}

    with patch(
        "src.infrastructure.clients.events.provider.httpx.AsyncClient"
    ) as mock_client_class:
        mock_client_instance = AsyncMock()
        mock_client_class.return_value.__aenter__.return_value = mock_client_instance

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data
        mock_client_instance.get.return_value = mock_response

        service.seats.cache_clear()
        seats = await service.seats(mock_event_id)

        mock_client_instance.get.assert_called_once()

        args, kwargs = mock_client_instance.get.call_args
        called_url = args[0]

        assert str(mock_event_id) in called_url
        assert "/seats/" in called_url
        assert seats == mock_response_data
