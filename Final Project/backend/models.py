import uuid
from datetime import datetime
from enum import Enum
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

class Role(str, Enum):
    user = "user"
    admin = "admin"

class User(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    email = fields.CharField(max_length=255, unique=True, index=True)
    username = fields.CharField(max_length=50, unique=True, index=True, null=False)
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    role = fields.CharEnumField(Role, default=Role.user)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def to_public(self):
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "role": self.role.value,
            "created_at": self.created_at.isoformat(),
        }

class Product(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    name = fields.CharField(max_length=200)
    description = fields.TextField(null=True)
    price_cents = fields.IntField()
    stock = fields.IntField(default=0)
    image_url = fields.CharField(max_length=1024, null=True)
    owner = fields.ForeignKeyField("models.User", related_name="products", on_delete=fields.CASCADE, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class Order(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    user = fields.ForeignKeyField("models.User", related_name="orders", on_delete=fields.CASCADE)
    total_cents = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)

class OrderItem(Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField("models.Order", related_name="items", on_delete=fields.CASCADE)
    product = fields.ForeignKeyField("models.Product", related_name="order_items", on_delete=fields.SET_NULL, null=True)  # Updated here
    quantity = fields.IntField()
    price_cents = fields.IntField()

# Pydantic models for serialization
User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True, exclude=("hashed_password", "created_at", "updated_at"))
UserOut_Pydantic = pydantic_model_creator(User, name="UserOut", exclude=("hashed_password",))

Product_Pydantic = pydantic_model_creator(Product, name="Product")
ProductIn_Pydantic = pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)

Order_Pydantic = pydantic_model_creator(Order, name="Order")
OrderItem_Pydantic = pydantic_model_creator(OrderItem, name="OrderItem")