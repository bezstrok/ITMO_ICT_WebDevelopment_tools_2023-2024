### Документация API

Этот API предоставляет функционал для работы с авторизацией, пользователями, бюджетами, категориями и транзакциями в рамках
системы управления личными финансами. Он использует **JWT** для аутентификации пользователей и содержит следующие основные
разделы:

1. **Авторизация**
2. **Пользователи**
3. **Бюджеты**
4. **Категории**
5. **Транзакции**
6. **Связи между категориями и транзакциями**

---

## **1. Авторизация**

### **Регистрация пользователя**

**POST /auth/register**

Регистрирует нового пользователя в системе.

- **Тело запроса:**
  - `username` (string, required): Имя пользователя.
  - `password` (string, required): Пароль пользователя.

- **Ответ:**
  - `200 OK`: Успешная регистрация.
    ```json
    {
      "id": 1,
      "username": "string",
      "email": "string"
    }
    ```
  - `422 Validation Error`: Ошибка валидации данных.

---

### **Вход пользователя**

**POST /auth/login**

Аутентифицирует пользователя и выдает JWT токен.

- **Тело запроса:**
  - `username` (string, required): Имя пользователя.
  - `password` (string, required): Пароль пользователя.

- **Ответ:**
  - `200 OK`: Успешная аутентификация.
    ```json
    {
      "access_token": "string"
    }
    ```
  - `422 Validation Error`: Ошибка валидации данных.

---

### **Обновление токена доступа**

**POST /auth/refreshToken**

Обновляет токен доступа с использованием `refresh_token`.

- **Параметры запроса:**
  - `refresh_token` (cookie, optional): Токен обновления.

- **Ответ:**
  - `200 OK`: Успешное обновление токена.
    ```json
    {
      "access_token": "string"
    }
    ```
  - `422 Validation Error`: Ошибка валидации данных.

---

### **Смена пароля**

**POST /auth/changePassword**

Изменяет пароль пользователя.

- **Тело запроса:**
  - `old_password` (string, required): Старый пароль.
  - `new_password` (string, required): Новый пароль.

- **Ответ:**
  - `200 OK`: Успешная смена пароля.
  - `422 Validation Error`: Ошибка валидации данных.

---

## **2. Пользователи**

### **Получение информации о пользователе**

**GET /user**

Возвращает информацию о текущем пользователе.

- **Ответ:**
  - `200 OK`: Информация о пользователе.
    ```json
    {
      "id": 1,
      "username": "string",
      "email": "string"
    }
    ```

---

### **Обновление пользователя**

**PUT /user**

Обновляет информацию о пользователе.

- **Тело запроса:**
  - `email` (string, required): Новый email пользователя.

- **Ответ:**
  - `200 OK`: Обновленная информация о пользователе.
    ```json
    {
      "id": 1,
      "username": "string",
      "email": "string"
    }
    ```
  - `422 Validation Error`: Ошибка валидации данных.

---

## **3. Бюджеты**

### **Получение всех бюджетов**

**GET /budgets**

Возвращает список бюджетов, привязанных к пользователю.

- **Параметры запроса:**
  - `page` (integer, optional): Номер страницы (по умолчанию 1).
  - `start_date` (datetime, optional): Начальная дата фильтрации.
  - `end_date` (datetime, optional): Конечная дата фильтрации.
  - `orders` (array, optional): Сортировка по `start_date`, `end_date`, `amount`.

- **Ответ:**
  - `200 OK`: Список бюджетов.
    ```json
    {
      "count": 1,
      "next": null,
      "previous": null,
      "results": [
        {
          "id": 1,
          "amount": 1000.00,
          "start_date": "2024-01-01T00:00:00",
          "end_date": "2024-01-31T23:59:59"
        }
      ]
    }
    ```
  - `422 Validation Error`: Ошибка валидации данных.

---

### **Создание нового бюджета**

**POST /budgets**

Создает новый бюджет для пользователя.

- **Тело запроса:**
  - `amount` (float, required): Сумма бюджета.
  - `start_date` (datetime, required): Начальная дата бюджета.
  - `end_date` (datetime, required): Конечная дата бюджета.

- **Ответ:**
  - `200 OK`: Созданный бюджет.
    ```json
    {
      "id": 1,
      "amount": 1000.00,
      "start_date": "2024-01-01T00:00:00",
      "end_date": "2024-01-31T23:59:59"
    }
    ```
  - `422 Validation Error`: Ошибка валидации данных.

---

### **Получение бюджета по ID**

**GET /budgets/{budget_id}**

Возвращает бюджет по его ID.

- **Параметры пути:**
  - `budget_id` (integer, required): ID бюджета.

- **Ответ:**
  - `200 OK`: Информация о бюджете.
    ```json
    {
      "id": 1,
      "amount": 1000.00,
      "start_date": "2024-01-01T00:00:00",
      "end_date": "2024-01-31T23:59:59"
    }
    ```

---

### **Обновление бюджета**

**PUT /budgets/{budget_id}**

Обновляет информацию о бюджете.

- **Параметры пути:**
  - `budget_id` (integer, required): ID бюджета.

- **Тело запроса:**
  - `amount` (float, required): Новая сумма бюджета.
  - `start_date` (datetime, required): Новая начальная дата бюджета.
  - `end_date` (datetime, required): Новая конечная дата бюджета.

- **Ответ:**
  - `200 OK`: Обновленный бюджет.
    ```json
    {
      "id": 1,
      "amount": 1500.00,
      "start_date": "2024-02-01T00:00:00",
      "end_date": "2024-02-28T23:59:59"
    }
    ```

---

### **Удаление бюджета**

**DELETE /budgets/{budget_id}**

Удаляет бюджет по его ID.

- **Параметры пути:**
  - `budget_id` (integer, required): ID бюджета.

- **Ответ:**
  - `200 OK`: Успешное удаление бюджета.

---

## **4. Категории**

### **Получение всех категорий**

**GET /categories**

Возвращает список категорий пользователя.

- **Параметры запроса:**
  - `page` (integer, optional): Номер страницы.
  - `parent_id` (integer, optional): ID родительской категории.
  - `budget_id` (integer, optional): ID бюджета.

- **Ответ:**
  - `200 OK`: Список категорий.
    ```json
    {
      "count": 1,
      "results": [
        {
          "id": 1,
          "title": "Food",
          "parent_id": null,
          "budget_id": 1
        }
      ]
    }
    ```

---

### **Создание новой категории**

**POST /categories**

Создает новую категорию.

- **Тело запроса:**
  - `title` (string, required): Название категории.
  - `parent_id` (integer, optional): ID родительской категории.
  - `budget_id` (integer, optional): ID бюджета.

- **Ответ:**
  - `200 OK`: Созданная категория.
    ```json
    {
      "id": 1,
      "title": "Food",
      "parent_id": null,
      "budget_id": 1
    }
    ```

---

### **Получение категории по ID**

**GET /categories/{category_id}**

Возвращает категорию по ее ID.

- **Параметры пути:**
  - `category_id` (integer, required): ID категории.

- **Ответ:**
  - `200 OK`: Информация о категории.
    ```json
    {
      "id": 1,
      "title": "Food",
      "parent": null,
      "children": [],
      "budget": {
        "id": 1,
        "amount": 1000.00
      }
    }
    ```

---

### **Обновление категории**

**PUT /categories/{category_id}**

Обновляет информацию о категории.

- **Параметры пути:**
  - `category_id` (integer, required): ID категории.

- **Тело запроса:**
  - `title` (string, required): Новое название категории.
  - `parent_id` (integer, optional): ID родительской категории.
  - `budget_id` (integer, optional): ID бюджета.

- **Ответ:**
  - `200 OK`: Обновленная категория.

---

### **Удаление категории**

**DELETE /categories/{category_id}**

Удаляет категорию по ее ID.

- **Параметры пути:**
  - `category_id` (integer, required): ID категории.

- **Ответ:**
  - `200 OK`: Успешное удаление категории.

---

## **5. Транзакции**

### **Получение всех транзакций**

**GET /transactions**

Возвращает список транзакций пользователя.

- **Параметры запроса:**
  - `page` (integer, optional): Номер страницы.
  - `transaction_type` (string, optional): Тип транзакции (`deposit`, `withdraw`).
  - `orders` (array, optional): Сортировка по `amount`.

- **Ответ:**
  - `200 OK`: Список транзакций.
    ```json
    {
      "count": 1,
      "results": [
        {
          "id": 1,
          "amount": 100.00,
          "transaction_type": "withdraw"
        }
      ]
    }
    ```

---

### **Создание новой транзакции**

**POST /transactions**

Создает новую транзакцию.

- **Тело запроса:**
  - `amount` (float, required): Сумма транзакции.
  - `transaction_type` (string, required): Тип транзакции (`deposit`, `withdraw`).

- **Ответ:**
  - `200 OK`: Созданная транзакция.
    ```json
    {
      "id": 1,
      "amount": 100.00,
      "transaction_type": "withdraw"
    }
    ```

---

### **Получение транзакции по ID**

**GET /transactions/{transaction_id}**

Возвращает транзакцию по ее ID.

- **Параметры пути:**
  - `transaction_id` (integer, required): ID транзакции.

- **Ответ:**
  - `200 OK`: Информация о транзакции.

---

### **Обновление транзакции**

**PUT /transactions/{transaction_id}**

Обновляет информацию о транзакции.

- **Параметры пути:**
  - `transaction_id` (integer, required): ID транзакции.

- **Тело запроса:**
  - `amount` (float, required): Новая сумма транзакции.
  - `transaction_type` (string, required): Новый тип транзакции.

- **Ответ:**
  - `200 OK`: Обновленная транзакция.

---

### **Удаление транзакции**

**DELETE /transactions/{transaction_id}**

Удаляет транзакцию по ее ID.

- **Параметры пути:**
  - `transaction_id` (integer, required): ID транзакции.

- **Ответ:**
  - `200 OK`: Успешное удаление транзакции.

---

## **6. Связи между категориями и транзакциями**

### **Создание связи между категорией и транзакцией**

**POST /relationships/categoryToTransaction**

Создает связь между категорией и транзакцией.

- **Тело запроса:**
  - `category_id` (integer, required): ID категории.
  - `transaction_id` (integer, required): ID транзакции.

- **Ответ:**
  - `200 OK`: Успешное создание связи.

---
