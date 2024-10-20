# storeapi

Проект представляет собой API для интернет-магазина, предназначенное для управления основными процессами: от обработки товаров до оформления заказов.

# Технологический стек:
Язык программирования: Python

Фреймворк: Django REST Framework (DRF)

База данных: MySQL для хранения основной информации

Кэширование и брокер сообщений: Redis для кэширования данных и выполнения фоновых задач

Фоновая обработка задач: Celery для асинхронного выполнения задач

# Установка
Клонируйте репозиторий: 
```bash
git clone https://github.com/johnMacClane07/storeapi.git
```
Создаем виртуальное окруение и активируем его 
```bash 
python -m venv venv
source venv/bin/activate 
```
Установите зависимости: 
```bash 
pip install -r requirements.txt
```

Настройте базу данных и Redis в settings.py

Запустите миграции: 
```bash 
python manage.py migrate
```
Запустите сервер: 
```bash 
python manage.py runserver
```
Запустите Celery:
```bash 
celery -A project_name worker -l info
```
### Доступные эндпоинты API

| Метод  | Эндпоинт                           | Описание                                                   |
|--------|-----------------------------------|------------------------------------------------------------|
| `GET`  | `/api/cart/`                      | Просмотр содержимого корзины                                |
| `POST` | `/api/cart/`                      | Добавление товара в корзину                                 |
| `DELETE` | `/api/cart/remove-product/`      | Удаление товара из корзины                                  |
| `DELETE` | `/api/cart/clear-cart/`          | Очистка всей корзины                                        |
| `POST` | `/api/cart/create-order/`         | Создание заказа на основе содержимого корзины               |
| `GET`  | `/api/order/`                     | Получение списка заказов пользователя                      |
| `GET`  | `/api/order/{order_id}/`          | Просмотр деталей заказа по ID                               |
| `GET`  | `/api/products/`                  | Получение списка товаров                                    |
| `GET`  | `/api/products/{product_id}/`     | Просмотр информации о товаре по его ID                      |
| `GET`  | `/api/products/?search={product_name}/` | Поиск товаров по названию                           |
| `GET`  | `/api/products/?filter={product_category}/` | Фильтрация товаров по категории                  |
| `GET`  | `/api/favourites/`                | Просмотр списка избранных товаров                           |
| `POST` | `/api/favourites/`                | Добавление товара в избранное                               |
| `DELETE` | `/api/favourites/{favourite_id}/` | Удаление товара из избранного                    |
| `POST` | `/api/auth/users/`                | Регистрация нового пользователя                             |
| `POST` | `/api/auth/jwt/create/`                | Получение JWT токена                                        |
| `POST` | `/api/auth/jwt/refresh/`               | Обновление JWT токена                                       |

