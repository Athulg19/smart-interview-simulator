
# from django.db import models
# from django.contrib.auth.hashers import make_password, check_password

# class User(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=255)  # Store hashed passwords

#     def set_password(self, raw_password):
#         """Hash and set the password."""
#         self.password = make_password(raw_password)

#     def check_password(self, raw_password):
#         """Check if the raw password matches the hashed password."""
#         return check_password(raw_password, self.password)

#     def __str__(self):
#         return self.username
