from django.db import models

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=20, verbose_name="Роль")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
        ordering = ['name']

class Users(models.Model):
    username = models.CharField(max_length=50, verbose_name="Имя пользователя")
    fullname = models.CharField(max_length=100, verbose_name="ФИО", blank=True)
    company = models.CharField(max_length=50, verbose_name="Компания")
    address = models.CharField(max_length=1000, verbose_name="Адрес")
    email = models.EmailField(blank=True, verbose_name="Электронная почта")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    password = models.CharField(max_length=100, verbose_name="Пароль")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name="Роль", default=1)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

class Product(models.Model):
    vendor = models.ForeignKey(Users,
                               on_delete=models.PROTECT,
                               null=True,
                               blank=True,
                               verbose_name="Продавец")
    product_name = models.CharField(max_length=100, verbose_name="Название продукта")
    specification = models.CharField(max_length=2000, verbose_name="Спецификация")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    cost = models.PositiveIntegerField(verbose_name="Стоимость")
    average_rating = models.FloatField(verbose_name="Средний рейтинг")
    number_of_ratings = models.PositiveIntegerField(verbose_name="Количество оценок")

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['product_name']

class PurchaseHistory(models.Model):
    client = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name="Клиент")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Продукт")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    paid = models.BooleanField(default=False, verbose_name="Оплачено")

    def __str__(self):
        return f"{self.client} - {self.product}"

    class Meta:
        verbose_name = 'История покупки'
        verbose_name_plural = 'Истории покупок'
        ordering = ['-created']


class PaymentsInfo(models.Model):
    card = models.CharField(max_length=20, verbose_name="Номер карты")
    owner_name = models.CharField(max_length=100, verbose_name="Имя владельца карты")

    def __str__(self):
        return f"{self.card} - {self.owner_name}"

    class Meta:
        verbose_name = 'Платежная информация'
        verbose_name_plural = 'Платежная информация'
        ordering = ["owner_name"]

class UsersPaymentInfo(models.Model):
    client = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name="Клиент")
    card = models.ForeignKey(PaymentsInfo, on_delete=models.PROTECT, verbose_name="Платежная информация")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")


    def __str__(self):
        return f"{self.client} - {self.card}"

    class Meta:
        verbose_name = 'Платежная информация пользователя'
        verbose_name_plural = 'Платежная информация пользователей'
        ordering = ['-created']



