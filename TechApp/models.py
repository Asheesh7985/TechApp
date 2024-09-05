from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from froala_editor.fields import FroalaField
from django.utils.timezone import now



class MyUserManager(BaseUserManager):
    def create_user(self, email,   password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
           
           
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    otp = models.IntegerField(default=0,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    profile = models.ImageField(upload_to='profile/',null=True,blank=True)

    def __str__(self):
        return self.first_name+" "+self.last_name

   

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=70,unique=True)

    def __str__(self):
        return  str(self.id) +"  "+self.cname

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = FroalaField()
    slug = models.CharField(max_length=100,unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/',null=True,blank=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    message = models.CharField(max_length=1000)

class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    comment_data = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    post = models.ForeignKey(Post, models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    datetime = models.DateTimeField(default=now)


    def __str__(self):
        return self.comment_data[0:13] + "..." + "by " + self.author.user


