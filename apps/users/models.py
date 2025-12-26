from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Email must be set")
        if not password:
            raise ValueError("Password must be set")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        return self.create_user(email, password)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    reset_token = models.CharField(max_length=255, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # --------- MODEL LOGIC ----------

    # Fetch user by email
    @classmethod
    def fetch_by_email(cls, email):
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None

    # Check password
    def check_password_correct(self, raw_password):
        return self.check_password(raw_password)

    # Generate token and store in database
    def generate_token(self):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(self)
        self.reset_token = token
        self.save()
        return token

    # Check incoming token
    def check_token_valid(self, token):
        return self.reset_token == token

    # Reset password
    def reset_password(self, token, new_password):
        if self.check_token_valid(token):
            self.set_password(new_password)
            self.reset_token = None  # clear token after use
            self.save()
            return True
        return False
