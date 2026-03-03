"""
Management command to populate the database with sample data.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User
from inventory.models import Category, Component, Supplier, Service, Movement
from orders.models import Order, OrderItem
from decimal import Decimal
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        
        # Создаём группы
        self.create_groups()
        
        # Создаём пользователей
        self.create_users()
        
        # Создаём категории
        self.create_categories()
        
        # Создаём поставщиков
        self.create_suppliers()
        
        # Создаём комплектующие
        self.create_components()
        
        # Создаём услуги
        self.create_services()
        
        # Создаём движения товаров (поставки)
        self.create_movements()
        
        # Создаём заявки
        self.create_orders()
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Test users created:'))
        self.stdout.write(self.style.SUCCESS('  Worker: worker / worker123 (Полный доступ)'))
        self.stdout.write(self.style.SUCCESS('  Client: client / client123 (Минимальный доступ)'))
        self.stdout.write(self.style.SUCCESS('  + 5 дополнительных клиентов (client2-6 / client123)'))

    def create_groups(self):
        Group.objects.get_or_create(name='Клиенты')
        Group.objects.get_or_create(name='Работники')
        self.stdout.write('✓ Groups created')

    def create_users(self):
        # Работник (полный доступ к системе)
        worker, created = User.objects.get_or_create(
            username='worker',
            defaults={
                'email': 'worker@ronix-l.ru',
                'first_name': 'Петр',
                'last_name': 'Работников',
                'role': 'worker',
                'phone': '+7 (999) 222-33-44',
                'address': 'г. Москва, ул. Рабочая, д. 20',
                'is_superuser': True,
                'is_staff': True,
            }
        )
        if created:
            worker.set_password('worker123')
            worker.save()
        
        # Клиент (минимальный доступ)
        client, created = User.objects.get_or_create(
            username='client',
            defaults={
                'email': 'client@example.com',
                'first_name': 'Иван',
                'last_name': 'Клиентов',
                'role': 'client',
                'phone': '+7 (999) 111-22-33',
                'address': 'г. Москва, ул. Примерная, д. 10, кв. 5',
            }
        )
        if created:
            client.set_password('client123')
            client.save()
        
        # Дополнительные клиенты для реалистичности
        additional_clients = [
            ('client2', 'Анна', 'Смирнова', 'anna@techcorp.ru', '+7 (999) 333-44-55', 'г. Москва, ул. Ленина, д. 15'),
            ('client3', 'Сергей', 'Петров', 'sergey@innovate.ru', '+7 (999) 444-55-66', 'г. Санкт-Петербург, Невский пр., д. 100'),
            ('client4', 'Мария', 'Сидорова', 'maria@startup.com', '+7 (999) 555-66-77', 'г. Казань, ул. Баумана, д. 30'),
            ('client5', 'Александр', 'Козлов', 'alex@robotics.ru', '+7 (999) 666-77-88', 'г. Новосибирск, ул. Академическая, д. 5'),
            ('client6', 'Елена', 'Волкова', 'elena@iot-systems.ru', '+7 (999) 777-88-99', 'г. Екатеринбург, ул. Малышева, д. 50'),
        ]
        
        for username, first_name, last_name, email, phone, address in additional_clients:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'client',
                    'phone': phone,
                    'address': address,
                }
            )
            if created:
                user.set_password('client123')
                user.save()
        
        self.stdout.write('✓ Users created')

    def create_categories(self):
        categories = [
            ('Электронные компоненты', 'Резисторы, конденсаторы, транзисторы'),
            ('Микроконтроллеры', 'Arduino, Raspberry Pi, ESP32'),
            ('Датчики', 'Температурные, давления, движения'),
            ('Дисплеи', 'LCD, OLED, TFT дисплеи'),
            ('Механические детали', 'Винты, гайки, крепежи'),
        ]
        
        for name, desc in categories:
            Category.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
        
        self.stdout.write('✓ Categories created')

    def create_suppliers(self):
        suppliers = [
            ('ООО "ЭлектроКомпонент"', 'Иванов И.И.', 'info@elektro.ru', '+7 (495) 111-22-33'),
            ('ООО "ТехПоставка"', 'Петров П.П.', 'sales@techpost.ru', '+7 (495) 222-33-44'),
            ('ИП Сидоров С.С.', 'Сидоров С.С.', 'sidorov@mail.ru', '+7 (495) 333-44-55'),
        ]
        
        for name, contact, email, phone in suppliers:
            Supplier.objects.get_or_create(
                name=name,
                defaults={
                    'contact_person': contact,
                    'email': email,
                    'phone': phone,
                    'address': 'г. Москва, ул. Складская, д. 10'
                }
            )
        
        self.stdout.write('✓ Suppliers created')

    def create_components(self):
        categories = {cat.name: cat for cat in Category.objects.all()}
        
        components = [
            # Электронные компоненты
            ('Резистор 10 кОм', categories['Электронные компоненты'], 'RES-10K', 'Vishay', Decimal('2.50'), 1000, 50),
            ('Конденсатор 100 мкФ', categories['Электронные компоненты'], 'CAP-100uF', 'Panasonic', Decimal('5.00'), 500, 30),
            ('Резистор 1 кОм', categories['Электронные компоненты'], 'RES-1K', 'Yageo', Decimal('1.80'), 800, 40),
            ('Резистор 100 Ом', categories['Электронные компоненты'], 'RES-100', 'KOA', Decimal('1.50'), 1200, 60),
            ('Конденсатор 10 мкФ', categories['Электронные компоненты'], 'CAP-10uF', 'Nichicon', Decimal('3.50'), 600, 35),
            ('Транзистор BC547', categories['Электронные компоненты'], 'TRN-BC547', 'Fairchild', Decimal('8.00'), 350, 25),
            ('Светодиод красный 5мм', categories['Электронные компоненты'], 'LED-RED-5', 'Kingbright', Decimal('4.50'), 850, 50),
            ('Светодиод синий 5мм', categories['Электронные компоненты'], 'LED-BLUE-5', 'Kingbright', Decimal('5.00'), 750, 45),
            
            # Микроконтроллеры
            ('Arduino Uno R3', categories['Микроконтроллеры'], 'ARD-UNO-R3', 'Arduino', Decimal('1200.00'), 15, 5),
            ('Raspberry Pi 4 8GB', categories['Микроконтроллеры'], 'RPI4-8GB', 'Raspberry', Decimal('8500.00'), 8, 3),
            ('ESP32 DevKit', categories['Микроконтроллеры'], 'ESP32-DEV', 'Espressif', Decimal('450.00'), 25, 10),
            ('Arduino Nano', categories['Микроконтроллеры'], 'ARD-NANO', 'Arduino', Decimal('650.00'), 30, 8),
            ('ESP8266 NodeMCU', categories['Микроконтроллеры'], 'ESP8266-MCU', 'Espressif', Decimal('320.00'), 40, 12),
            ('STM32 Blue Pill', categories['Микроконтроллеры'], 'STM32-BLUE', 'STMicro', Decimal('280.00'), 35, 10),
            
            # Датчики
            ('Датчик температуры DHT22', categories['Датчики'], 'DHT22', 'Asong', Decimal('350.00'), 30, 10),
            ('Ультразвуковой датчик HC-SR04', categories['Датчики'], 'HC-SR04', 'Generic', Decimal('120.00'), 50, 20),
            ('Датчик движения PIR HC-SR501', categories['Датчики'], 'PIR-SR501', 'Generic', Decimal('90.00'), 45, 15),
            ('Датчик влажности почвы', categories['Датчики'], 'SOIL-MOIST', 'Generic', Decimal('75.00'), 60, 20),
            ('Датчик света BH1750', categories['Датчики'], 'BH1750', 'Rohm', Decimal('180.00'), 28, 8),
            ('Акселерометр MPU6050', categories['Датчики'], 'MPU6050', 'InvenSense', Decimal('220.00'), 22, 7),
            
            # Дисплеи
            ('LCD дисплей 16x2', categories['Дисплеи'], 'LCD-16x2', 'Hitachi', Decimal('250.00'), 20, 5),
            ('OLED дисплей 0.96"', categories['Дисплеи'], 'OLED-096', 'SSD1306', Decimal('450.00'), 12, 5),
            ('TFT дисплей 2.4"', categories['Дисплеи'], 'TFT-24', 'ILI9341', Decimal('680.00'), 15, 4),
            ('LCD дисплей 20x4', categories['Дисплеи'], 'LCD-20x4', 'Hitachi', Decimal('420.00'), 10, 3),
            ('OLED дисплей 1.3"', categories['Дисплеи'], 'OLED-13', 'SH1106', Decimal('550.00'), 8, 3),
            
            # Механические детали
            ('Винт M3x10мм (100шт)', categories['Механические детали'], 'SCR-M3-10', 'DIN', Decimal('150.00'), 100, 20),
            ('Гайка M3 (100шт)', categories['Механические детали'], 'NUT-M3', 'DIN', Decimal('80.00'), 120, 25),
            ('Винт M2.5x8мм (100шт)', categories['Механические детали'], 'SCR-M25-8', 'DIN', Decimal('130.00'), 90, 18),
            ('Стойка M3x20мм (50шт)', categories['Механические детали'], 'STANDOFF-M3-20', 'Generic', Decimal('200.00'), 70, 15),
            ('Кабель Dupont М-М 20см (40шт)', categories['Механические детали'], 'WIRE-MM-20', 'Generic', Decimal('180.00'), 50, 10),
        ]
        
        for name, category, article, manufacturer, price, quantity, min_qty in components:
            Component.objects.get_or_create(
                article_number=article,
                defaults={
                    'name': name,
                    'category': category,
                    'manufacturer': manufacturer,
                    'price': price,
                    'quantity': quantity,
                    'min_quantity': min_qty,
                    'description': f'Описание для {name}'
                }
            )
        
        self.stdout.write('✓ Components created')

    def create_services(self):
        services = [
            # Замена деталей
            ('Замена батареи iPhone', 'replacement', 'Замена аккумулятора на оригинальную или совместимую батарею для iPhone всех моделей', Decimal('1500.00'), 30),
            ('Замена батареи Android', 'replacement', 'Замена аккумулятора для смартфонов на базе Android (Samsung, Xiaomi, Huawei и др.)', Decimal('1200.00'), 30),
            ('Замена экрана iPhone', 'replacement', 'Замена дисплейного модуля iPhone с оригинальной или совместимой матрицей', Decimal('3500.00'), 60),
            ('Замена экрана Samsung', 'replacement', 'Замена дисплея для смартфонов Samsung Galaxy', Decimal('2800.00'), 60),
            ('Замена стекла камеры', 'replacement', 'Замена защитного стекла основной или фронтальной камеры', Decimal('500.00'), 20),
            ('Замена динамика/микрофона', 'replacement', 'Замена разговорного динамика или микрофона в смартфоне', Decimal('800.00'), 40),
            ('Замена разъёма зарядки', 'replacement', 'Замена USB/Lightning разъёма зарядки', Decimal('1000.00'), 45),
            
            # Ремонт
            ('Ремонт материнской платы', 'repair', 'Диагностика и ремонт материнской платы смартфона/планшета (пайка, замена чипов)', Decimal('2500.00'), 120),
            ('Ремонт после попадания влаги', 'repair', 'Чистка, сушка и восстановление устройства после попадания жидкости', Decimal('1800.00'), 90),
            ('Ремонт кнопок управления', 'repair', 'Ремонт или замена физических кнопок (громкость, питание, Home)', Decimal('700.00'), 30),
            ('Ремонт Face ID/Touch ID', 'repair', 'Восстановление работы биометрических датчиков', Decimal('2000.00'), 60),
            ('Ремонт камеры', 'repair', 'Ремонт основной или фронтальной камеры', Decimal('1500.00'), 45),
            
            # Диагностика
            ('Диагностика смартфона', 'diagnostics', 'Полная диагностика смартфона с выявлением всех неисправностей', Decimal('300.00'), 30),
            ('Диагностика планшета', 'diagnostics', 'Комплексная диагностика планшета', Decimal('350.00'), 30),
            ('Диагностика ноутбука', 'diagnostics', 'Полная диагностика ноутбука (железо и ПО)', Decimal('500.00'), 45),
            ('Экспресс-диагностика', 'diagnostics', 'Быстрая проверка основных функций устройства', Decimal('0.00'), 15),
            
            # Обслуживание
            ('Чистка от пыли', 'maintenance', 'Профилактическая чистка устройства от пыли и грязи', Decimal('600.00'), 30),
            ('Замена термопасты', 'maintenance', 'Замена термопасты в ноутбуке/компьютере', Decimal('800.00'), 40),
            ('Профилактика системы охлаждения', 'maintenance', 'Чистка и обслуживание системы охлаждения (вентиляторы, радиаторы)', Decimal('1000.00'), 50),
            
            # Установка
            ('Установка защитного стекла', 'installation', 'Установка защитного стекла на экран (стекло не входит в стоимость)', Decimal('200.00'), 10),
            ('Установка чехла/бампера', 'installation', 'Подбор и установка защитного чехла', Decimal('100.00'), 5),
            ('Прошивка устройства', 'installation', 'Установка или переустановка операционной системы', Decimal('1200.00'), 60),
            ('Разблокировка устройства', 'installation', 'Разблокировка смартфона от оператора или iCloud (при наличии документов)', Decimal('1500.00'), 90),
            
            # Прочее
            ('Восстановление данных', 'other', 'Восстановление удалённых файлов, фото, контактов', Decimal('2000.00'), 120),
            ('Перенос данных', 'other', 'Перенос всех данных со старого устройства на новое', Decimal('500.00'), 30),
            ('Настройка устройства', 'other', 'Первичная настройка нового устройства, установка приложений', Decimal('400.00'), 40),
            ('Прочее', 'other', 'Прочие работы (цена указана за 1 час работы)', Decimal('1000.00'), 60),
        ]
        
        for name, category, description, price, duration in services:
            Service.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'description': description,
                    'price': price,
                    'duration': duration,
                    'is_active': True,
                }
            )
        
        self.stdout.write('✓ Services created')

    def create_movements(self):
        """Создаём движения товаров (поставки) за 2026 год"""
        worker = User.objects.get(username='worker')
        suppliers = list(Supplier.objects.all())
        components = list(Component.objects.all())
        
        # Создаём по 3-5 поставок для разных компонентов в течение года
        start_date = datetime(2026, 1, 1)
        
        for i in range(20):  # Создаём 20 поставок
            # Случайная дата в 2026 году
            days_offset = random.randint(0, 90)  # Первые 3 месяца года
            movement_date = start_date + timedelta(days=days_offset)
            
            # Выбираем случайный компонент и поставщика
            component = random.choice(components)
            supplier = random.choice(suppliers)
            
            # Количество от 50 до 500
            quantity = random.randint(50, 500)
            
            Movement.objects.get_or_create(
                component=component,
                date=movement_date,
                movement_type='in',
                defaults={
                    'quantity': quantity,
                    'supplier': supplier,
                    'user': worker,
                    'notes': f'Поставка от {supplier.name}',
                }
            )
        
        self.stdout.write('✓ Movements created (20 поставок)')

    def create_orders(self):
        """Создаём заявки за 2026 год с разными статусами"""
        worker = User.objects.get(username='worker')
        clients = list(User.objects.filter(role='client'))
        components_list = list(Component.objects.all())
        services_list = list(Service.objects.all())
        
        # Описания для заявок на ремонт
        service_descriptions = [
            'Требуется замена батареи на iPhone 12. Быстрая разрядка.',
            'Ремонт материнской платы после попадания влаги.',
            'Не работает экран, требуется замена дисплея Samsung Galaxy S21.',
            'Диагностика планшета - не включается.',
            'Замена разъёма зарядки на Xiaomi Redmi Note 10.',
            'Ремонт кнопки громкости на iPhone 13 Pro.',
            'Восстановление данных после сброса настроек.',
            'Профилактическая чистка ноутбука от пыли.',
            'Замена термопасты в игровом ноутбуке.',
            'Установка защитного стекла на новый телефон.',
        ]
        
        # Описания для заявок на комплектующие
        component_descriptions = [
            'Необходимы комплектующие для проекта умного дома',
            'Требуются датчики и контроллеры для системы автоматизации',
            'Заказ электронных компонентов для прототипа устройства',
            'Закупка резисторов и конденсаторов для ремонтной мастерской',
            'Нужны микроконтроллеры для учебного проекта',
            'Заказ дисплеев и датчиков для IoT-решения',
            'Комплектующие для разработки робототехнического комплекса',
            'Электронные компоненты для системы мониторинга',
        ]
        
        statuses = ['new', 'in_progress', 'completed', 'cancelled']
        status_weights = [0.2, 0.3, 0.4, 0.1]  # Больше выполненных заявок
        
        start_date = datetime(2026, 1, 1)
        created_orders = 0
        
        # Создаём 30-40 заявок за первые 3 месяца 2026 года
        for i in range(35):
            # Случайная дата
            days_offset = random.randint(0, 90)
            order_date = start_date + timedelta(days=days_offset)
            
            # Случайный клиент
            client = random.choice(clients)
            
            # Случайный тип заявки
            order_type = random.choice(['service', 'components'])
            
            # Статус заявки (выполненных больше)
            status = random.choices(statuses, weights=status_weights)[0]
            
            # Назначен ли работник (если заявка не новая)
            assigned_to = worker if status != 'new' else None
            
            if order_type == 'service':
                description = random.choice(service_descriptions)
            else:
                description = random.choice(component_descriptions)
            
            # Создаём заявку
            order = Order.objects.create(
                client=client,
                order_type=order_type,
                status=status,
                description=description,
                assigned_to=assigned_to,
                created_at=order_date,
            )
            
            # Если заявка на комплектующие, добавляем позиции
            if order_type == 'components':
                # Добавляем 2-5 позиций
                num_items = random.randint(2, 5)
                selected_components = random.sample(components_list, min(num_items, len(components_list)))
                
                for component in selected_components:
                    quantity = random.randint(1, 10)
                    OrderItem.objects.create(
                        order=order,
                        component=component,
                        quantity=quantity,
                        price=component.price
                    )
                
                order.calculate_total()
            
            # Если заявка на услугу, добавляем услуги
            elif order_type == 'service':
                # Добавляем 1-3 услуги
                num_services = random.randint(1, 3)
                selected_services = random.sample(services_list, min(num_services, len(services_list)))
                
                for service in selected_services:
                    OrderItem.objects.create(
                        order=order,
                        service=service,
                        quantity=1,
                        price=service.price
                    )
                
                order.calculate_total()
            
            created_orders += 1
        
        self.stdout.write(f'✓ Orders created ({created_orders} заявок за 2026 год)')
