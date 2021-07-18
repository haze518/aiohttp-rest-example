import pytest


data = {'client_id': 1,
        'country': 'rrr',
        'currency': 'rrr',
        'max_transfer': 400}


async def test_not_found_limit(api_client):
    """
    Проверка случая, когда id не существует БД
    """
    data = {'limit_id': 1, 'amount': 1337}
    result = await api_client.post('/transcation', json=data)
    assert result.status == 404


async def test_amount_greater_max_transfer(api_client):
    """
    Проверить случай, когда остаток за месяц меньше, чем
    сумма, которую пытаются внести в историю
    """
    await api_client.post('/limits', json=data)
    new_data = {'limit_id': 1, 'amount': 1337}
    result = await api_client.post('/transaction', json=new_data)
    assert result.status == 400


@pytest.mark.parametrize(('amount', 'expected', 'limit_status'), [
    [400, 200, 404],
    [300, 200, 200]
])
async def test_bank_amount(amount, expected, limit_status, api_client):
    """
    При внесении средств в историю, количество средств на лимите
    уменьшается соразмерно с указанной суммой
    """
    new_data = {'limit_id': 1, 'amount': amount}
    await api_client.post('/limits', json=data)
    result = await api_client.post('/transaction', json=new_data)
    assert result.status == expected
    check_limits = await api_client.get('/limits/client/1')
    assert check_limits.status == limit_status


async def test_all_table_data(api_client):
    """
    Выгрузить все данные из таблицы по историям
    """
    await api_client.post('/limits', json=data)
    await api_client.post('/transaction', json=data)
    result = await api_client.get('/transaction')
    return result.status == 200
