# Структура базы данных PostgreSQL - Ronix Inventory System

## Диаграмма связей

```
users_user (Пользователи)
    ↓
    ├─→ orders_order (Заявки) - client_id
    ├─→ orders_order (Заявки) - assigned_to_id
    ├─→ inventory_stockmovement (Движения) - user_id
    └─→ auth_group (Группы) - через users_user_groups

inventory_category (Категории)
    ↓
    └─→ inventory_component (Комплектующие) - category_id

inventory_supplier (Поставщики) - независимая таблица

inventory_component (Комплектующие)
    ↓
    ├─→ orders_orderitem (Позиции заявок) - component_id
    └─→ inventory_stockmovement (Движения) - component_id

inventory_service (Услуги)
    ↓
    └─→ orders_orderitem (Позиции заявок) - service_id

orders_order (Заявки)
    ↓
    ├─→ orders_orderitem (Позиции заявок) - order_id
    └─→ orders_receipt (Чеки) - order_id
```

---

## 1. Таблица: users_user (Пользователи)

**Описание:** Расширенная модель пользователя Django

| Колонка | Тип | Ограничения | Описание |
|---------|-----|-------------|----------|
| id | INTEGER | PRIMARY KEY | Уникальный идентификатор |
| username | VARCHAR(150) | UNIQUE, NOT NULL | Имя пользователя |
| email | VARCHAR(254) | | Email адрес |
| password | VARCHAR(128) | NOT NULL | Хеш пароля |
| first_name | VARCHAR(150) | | Имя |
| last_name | VARCHAR(150) | | Фамилия |
| role | VARCHAR(20) | DEFAULT 'client' | Роль: 'client' или 'worker' |
| phone | VARCHAR(20) | | Телефон |
| address | TEXT | | Адрес |
| is_staff | BOOLEAN | DEFAULT FALSE | Доступ к админ-панели |
| is_superuser | BOOLEAN | DEFAULT FALSE | Суперпользователь |
| is_active | BOOLEAN | DEFAULT TRUE | Активен |
| created_at | TIMESTAMP | AUTO | Дата регистрации |
| updated_at | TIMESTAMP | AUTO | Дата обновления |
| last_login | TIMESTAMP | NULL | Последний вход |
| date_joined | TIMESTAMP | AUTO | Дата присоединения |

**Связи:**
- orders_order.client_id → users_user.id (ForeignKey)
- orders_order.assigned_to_id → users_user.id (ForeignKey)
- inventory_stockmovement.user_id → users_user.id (ForeignKey)

---

## 2. Таблица: inventory_category (Категории комплектующих)

| Колонка | Тип | Ограничения | Описание |
|---------|-----|-------------|----------|
| id | INTEGER | PRIMARY KEY | ID категории |
| name | VARCHAR(200) | NOT NULL | Название категории |
| description | TEXT | | Описание |
| created_at | TIMESTAMP | AUTO | Дата создания |

**Связи:**
- inventory_component.category_id → inventory_category.id (ForeignKey)

---

## 3. Таблица: inventory_component (Комплектующие)

| Колонка | Тип | Ограничения | Описание |
|---------|-----|-------------|----------|
| id | INTEGER | PRIMARY KEY | ID комплектующей |
| name | VARCHAR(200) | NOT NULL | Название |
| category_id | INTEGER | FOREIGN KEY | → inventory_category.id |
| description | TEXT | | Описание |
| article_number | VARCHAR(100) | UNIQUE, NOT NULL | Артикул |
| manufacturer | VARCHAR(200) | | Производитель |
| price | DECIMAL(10,2) | NOT NULL | Цена за единицу |
| quantity | INTEGER | DEFAULT 0 | Количество на складе |
| min_quantity | INTEGER | DEFAULT 5 | Минимальный остаток |
| image | VARCHAR(100) | NULL | Путь к изображению |
| created_at | TIMESTAMP | AUTO | Дата добавления |
| updated_at | TIMESTAMP | AUTO | Дата обновления |

**Связи:**
- orders_orderitem.component_id → inventory_component.id (ForeignKey)
- inventory_stockmovement.component_id → inventory_component.id (ForeignKey)

---

## 4. Таблица: inventory_supplier (Поставщики)

| Колонка | Тип | Ограничения | Описание |
|---------|-----|-------------|----------|
| id | INTEGER | PRIMARY KEY | ID поставщика |
| name | VARCHAR(200) | NOT NULL | Название компании |
| contact_person | VARCHAR(200) | | Контактное лицо |
| email | VARCHAR(254) | | Email |
| phone | VARCHAR(20) | | Телефон |
| address | TEXT | | Адрес |
| created_at | TIMESTAMP | AUTO | Дата добавления |

**Связи:** Независимая таблица (справочник)

---

## 5. Таблица: inventory_stockmovement (Движения товаров)

| Колонка | Тип | Ограничения | Описание |
|---------|-----|-------------|----------|
| id | INTEGER | PRIMARY KEY | ID движения |
| component_id | INTEGER | FOREIGN KEY | → inventory_component.id |
| movement_type | VARCHAR(20) | NOT NULL | Тип: supply, sale, write_off, return_supplier, inventory, transfer |
| quantity | INTEGER | NOT NULL | Количество |
| note | TEXT | | Примечание |
| user_id | INTEGER | FOREIGN KEY NULL | → users_user.id |
| created_at | TIMESTAMP | AUTO | Дата операции |

**Связи:**
- inventory_component.id ← inventory_stockmovement.component_id
- users_user.id ← inventory_stockmovement.user_id

---

## 6. Таблица: inventory_service (Услуги)

| Колонка | Тип | Ограничения | Описание |
|---------|-----|-------------|----------|
| id | INTEGER | PRIMARY KEY | ID услуги |
| name | VARCHAR(300) | NOT NULL | Название услуги |
| category | VARCHAR(20) | DEFAULT 'other' | Категория: repair, replacement, diagnostics, maintenance, installation, other |
| description | TEXT | | Описание |
| price | DECIMAL(10,2) | NOT NULL | Цена |
| duration | INTEGER | DEFAULT 30 | Длительность (минуты) |
| is_active | BOOLEAN | DEFAULT TRUE | Активна |
| created_at | TIMESTAMP | AUTO | Дата создания |
| updated_at | TIMESTAMP | AUTO | Дата обновления |

**Связи:**
- orders_orderitem.service_id → inventory_service.id (ForeignKey)

---

## 7. Таблица: orders_order (Заявки)

| Колонка | Тип | Ограничения | Описание |
|---------|-----|-------------|----------|
| id | INTEGER | PRIMARY KEY | ID заявки |
| client_id | INTEGER | FOREIGN KEY | → users_user.id (клиент) |
| order_type | VARCHAR(20) | NOT NULL | Тип: 'service' или 'components' |
| status | VARCHAR(20) | DEFAULT 'new' | Статус: new, in_progress, completed, cancelled |
| description | TEXT | NOT NULL | Описание проблемы/запроса |
| assigned_to_id | INTEGER | FOREIGN KEY NULL | → users_user.id (работник) |
| total_amount | DECIMAL(10,2) | DEFAULT 0.00 | Общая сумма |
| created_at | TIMESTAMP | AUTO | Дата создания |
| updated_at | TIMESTAMP | AUTO | Дата обновления |
| completed_at | TIMESTAMP | NULL | Дата выполнения |

**Связи:**
- users_user.id ← orders_order.client_id
- users_user.id ← orders_order.assigned_to_id
- orders_orderitem.order_id → orders_order.id (обратная связь)
- orders_receipt.order_id → orders_order.id (обратная связь)

---

## 8. Таблица: orders_orderitem (Позиции заявок)

| Колонка | Тип | Ограничения | Описание |
|---------|-----|-------------|----------|
| id | INTEGER | PRIMARY KEY | ID позиции |
| order_id | INTEGER | FOREIGN KEY | → orders_order.id |
| component_id | INTEGER | FOREIGN KEY NULL | → inventory_component.id |
| service_id | INTEGER | FOREIGN KEY NULL | → inventory_service.id |
| quantity | INTEGER | DEFAULT 1 | Количество |
| price | DECIMAL(10,2) | NOT NULL | Цена за единицу |

**Примечание:** Либо component_id, либо service_id (один из двух обязателен)

**Связи:**
- orders_order.id ← orders_orderitem.order_id
- inventory_component.id ← orders_orderitem.component_id
- inventory_service.id ← orders_orderitem.service_id

---

## 9. Таблица: orders_receipt (Чеки)

| Колонка | Тип | Ограничения | Описание |
|---------|-----|-------------|----------|
| id | INTEGER | PRIMARY KEY | ID чека |
| order_id | INTEGER | FOREIGN KEY UNIQUE | → orders_order.id (один чек на заявку) |
| receipt_number | VARCHAR(50) | UNIQUE | Номер чека (формат: YYYYMMDD-NNNN) |
| issue_date | TIMESTAMP | AUTO | Дата выдачи |
| total_amount | DECIMAL(10,2) | NOT NULL | Общая сумма |
| notes | TEXT | | Примечания |

**Связи:**
- orders_order.id ← orders_receipt.order_id (ONE-TO-ONE)

---

## 10. Django системные таблицы

### auth_group (Группы пользователей)
- id, name

### auth_permission (Разрешения)
- id, name, content_type_id, codename

### django_session (Сессии)
- session_key, session_data, expire_date

### django_content_type (Типы контента)
- id, app_label, model

### django_migrations (История миграций)
- id, app, name, applied

---

## Связи Many-to-Many

### users_user_groups (Пользователи ↔ Группы)
- id
- user_id → users_user.id
- group_id → auth_group.id

### users_user_user_permissions (Пользователи ↔ Разрешения)
- id
- user_id → users_user.id
- permission_id → auth_permission.id

### auth_group_permissions (Группы ↔ Разрешения)
- id
- group_id → auth_group.id
- permission_id → auth_permission.id

---

## Основные бизнес-процессы

### 1. Создание заявки на обслуживание
```
users_user (client) → orders_order → orders_orderitem (service) → inventory_service
```

### 2. Создание заявки на комплектующие
```
users_user (client) → orders_order → orders_orderitem (component) → inventory_component
```

### 3. Назначение заявки работнику
```
orders_order.assigned_to_id → users_user (worker)
```

### 4. Движение товаров
```
inventory_component ← inventory_stockmovement (user_id → users_user)
```

### 5. Генерация чека
```
orders_order (completed) → orders_receipt
```

---

## Индексы (автоматические)

- **PRIMARY KEY** на всех id колонках
- **UNIQUE** на:
  - users_user.username
  - inventory_component.article_number
  - orders_receipt.receipt_number
  - orders_receipt.order_id
- **FOREIGN KEY INDEX** на всех связях:
  - orders_order.client_id
  - orders_order.assigned_to_id
  - inventory_component.category_id
  - orders_orderitem.order_id
  - orders_orderitem.component_id
  - orders_orderitem.service_id
  - inventory_stockmovement.component_id
  - inventory_stockmovement.user_id
  - orders_receipt.order_id

---

## Для визуализации диаграммы:

**Вариант 1 - dbdiagram.io:**
1. Откройте https://dbdiagram.io
2. Скопируйте код ниже в редактор
3. Получите визуальную диаграмму

```dbml
Table users_user {
  id integer [pk]
  username varchar(150) [unique]
  role varchar(20)
  email varchar
  phone varchar
}

Table inventory_category {
  id integer [pk]
  name varchar(200)
}

Table inventory_component {
  id integer [pk]
  name varchar(200)
  category_id integer [ref: > inventory_category.id]
  article_number varchar(100) [unique]
  price decimal
  quantity integer
}

Table inventory_service {
  id integer [pk]
  name varchar(300)
  category varchar(20)
  price decimal
}

Table orders_order {
  id integer [pk]
  client_id integer [ref: > users_user.id]
  assigned_to_id integer [ref: > users_user.id]
  order_type varchar(20)
  status varchar(20)
  total_amount decimal
}

Table orders_orderitem {
  id integer [pk]
  order_id integer [ref: > orders_order.id]
  component_id integer [ref: > inventory_component.id]
  service_id integer [ref: > inventory_service.id]
  quantity integer
  price decimal
}

Table orders_receipt {
  id integer [pk]
  order_id integer [unique, ref: - orders_order.id]
  receipt_number varchar(50) [unique]
  total_amount decimal
}

Table inventory_stockmovement {
  id integer [pk]
  component_id integer [ref: > inventory_component.id]
  user_id integer [ref: > users_user.id]
  movement_type varchar(20)
  quantity integer
}
```

**Вариант 2 - SQL запрос в Railway:**
```sql
-- Все таблицы
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Колонки конкретной таблицы
SELECT column_name, data_type, character_maximum_length, is_nullable
FROM information_schema.columns
WHERE table_name = 'orders_order'
ORDER BY ordinal_position;

-- Все связи (Foreign Keys)
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';
```
