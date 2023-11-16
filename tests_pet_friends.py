from api import PetFriends
from setting import valid_email, valid_password, invalid_email, invalid_password
import os


pf = PetFriends()


def test_get_api_for_invalid_email(email=invalid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями:
    assert status == 403
    assert 'key'not in result


def test_get_api_for_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиячми:
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_invalid_filter(filter='dogs'):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
       Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
       запрашиваем список всех питомцев и проверяем что список не пустой.
       Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key = auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_add_pet_with_empty_params(name='', animal_type='', age='', pet_photo='Images/IMG_3223.JPG'):
    """Проверяем что можно добавить питомца с незаполненными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца:
    status, result = pf.post_add_a_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200
    assert result['name'] == name


def test_post_add_pet_without_photo(name='Bob', animal_type='dog', age='4', pet_photo=''):
    """   Проверяем, что можно добавить питомца, не заполняя поле 'фото' """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца:
    status, result = pf.post_add_a_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200
    assert result['name'] == name


def test_post_add_pet_with_incorrect_age(name='Jack', animal_type='dog', age='b', pet_photo='Images/IMG_3223.JPG'):
    """Проверяем что можно добавить питомца с некорректным значением в поле 'возраст'   """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца:
    status, result = pf.post_add_a_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200
    assert result['name'] == name


def test_update_inform_with_empty_params(name='', animal_type='', age=''):
    # Проверяем возможность обновления информации о питомце с пустыми параметрами.
    # Получаем ключ auth_key и список своих питомцев:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Есели список не пустой, то пробуем обновить его имя, тип и возраст:
    if len(my_pets) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    # Если список пустой, поднимаем исключение "У меня нет питомцев"
    else:
        raise Exception("There is no my pets")


def test_update_inform_with_incorrect_params(name='1', animal_type='*', age='у'):
    # Проверяем возможность обновления информации о питомце с некорректными параметрами.
    # Получаем ключ auth_key и список своих питомцев:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст:
    if len(my_pets) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    # Если список пустой, поднимаем исключение "У меня нет питомцев"
    else:
        raise Exception("There is no my pets")


def test_create_new_pet_with_empty_params(name='', animal_type='', age=''):
    # Проверяем возможность создания нового питомца с пустыми параметрами.
    # Запрашиваем API-ключ и сохраняем в переменной auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца:
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pet_with_incorrect_format(pet_photo='images/IMG_2425'):
    # Проверяем возможность добавления фото в карточку питомца, указав его формат неверно.
    # Получаем ключ auth_key и список своих питомцев:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Проверяем, есть ли уже фотография у питомца:
    if my_pets['pets'][0]['pet_photo'] == ' ':
        # Добавляем фото:
        status, result = pf.set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        print('У питомца уже есть фото')
