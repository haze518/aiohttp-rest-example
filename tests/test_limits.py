import json
import pytest


correct_data = {'client_id': 3,
                'country': 'rrr',
                'currency': 'rrr',
                'max_transfer': 400}
wrong_data = {'client_id': 3,
              'country': 'rrrr',
              'currency': 'rrr',
              'max_transfer': 400}


@pytest.mark.parametrize(('data', 'expected'), [
    [correct_data, 200],
    [wrong_data, 422]
])
async def test_create_limit(data, expected, api_client):
    """
    Создание лимита
    """
    result = await api_client.post('/limits', json=data)
    assert result.status == expected


async def test_get_data(api_client):
    """
    Сбор всех данных с БД лимитов
    """
    await api_client.post('/limits', json=correct_data)
    result = await api_client.get('/limits')
    assert result.status == 200


async def test_get_data_id(api_client):
    """
    Выгрузка данных из таблицы по лимитам,
    по id
    """
    await api_client.post('/limits', json=correct_data)
    result = await api_client.get('/limits/client/1')
    assert result.status == 200
    result = json.loads(await result.text())
    assert result['id'] == 1


async def test_get_data_wrong_id(api_client):
    """
    Проверка ошибки, в случае несуществующего id пользователя
    """
    result = await api_client.get('/limits/client/1')
    assert result.status == 404


async def test_update_limit(api_client):
    """
    Обновление данных в БД
    """
    old_result = await api_client.post('/limits', json=correct_data)
    old_result = json.loads(await old_result.text())
    data = old_result.copy()
    data['max_transfer'] = 1337
    new_result = await api_client.put('/limits', json=data)
    assert new_result.status == 200
    new_result = json.loads(await new_result.text())
    assert new_result != old_result


async def test_delete_limit(api_client):
    """
    Удаление записи
    """
    await api_client.post('/limits', json=correct_data)
    result = await api_client.delete('/limits/client/1')
    assert result.status == 200
    result = json.loads(await result.text())
    assert result['message'] == 'Запись успешно удалена'
