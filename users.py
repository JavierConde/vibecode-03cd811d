This code represents a basic user model and  CRUD (Create, Read, Update, Delete) operations using a dictionary as an in-memory database.  For a production application, you'd want to replace this with a proper database (like PostgreSQL, MySQL, or SQLite) and an ORM (like SQLAlchemy).

```python
import uuid

class User:
    def __init__(self, email, password, nombre):
        self.id = uuid.uuid4()  # Using UUID for a more robust ID
        self.email = email
        self.password = password  # In a real application, hash this!
        self.nombre = nombre

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, nombre={self.nombre})>"


class Users:
    def __init__(self):
        self.users = {} # In-memory database. Replace with a real database in production.


    def create_user(self, email, password, nombre):
        user = User(email, password, nombre)
        self.users[user.id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_user_by_email(self, email):
        for user_id, user in self.users.items():
            if user.email == email:
                return user
        return None

    def update_user(self, user_id, updates):
        user = self.users.get(user_id)
        if user:
            for key, value in updates.items():
                setattr(user, key, value)
            return user
        return None

    def delete_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

    def list_users(self):
        return list(self.users.values())


# Example usage
users_manager = Users()

# Create users
user1 = users_manager.create_user("john.doe@example.com", "password123", "John Doe")
user2 = users_manager.create_user("jane.doe@example.com", "securepass", "Jane Doe")

# Get user
retrieved_user = users_manager.get_user(user1.id)
print(f"Retrieved user: {retrieved_user}")

#Get user by email
retrieved_user_email = users_manager.get_user_by_email("jane.doe@example.com")
print(f"Retrieved user by email: {retrieved_user_email}")

#Update user
users_manager.update_user(user1.id, {"nombre": "John Smith"})
print(f"Updated user: {users_manager.get_user(user1.id)}")

#List users
print(f"All users: {users_manager.list_users()}")


# Delete user
users_manager.delete_user(user1.id)
print(f"User {user1.id} deleted: {users_manager.get_user(user1.id) is None}")


```

Remember to install any necessary libraries if you are using a database and ORM.  This example provides a functional foundation; security considerations (like password hashing) are crucial for a real-world application.