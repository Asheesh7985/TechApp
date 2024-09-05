from django.contrib import admin
from .models import User,Category, Post,Author,Contact,Comment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserModelAdmin(BaseUserAdmin):
    # The forms to add and change user instances
   

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email',  'is_admin','password')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()


# Now register the new UserModelAdmin..
admin.site.register(User, UserModelAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id','user','first_name','last_name','phone','profile']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','cname']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','content','slug','category','author','date','image']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','message']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['cid','comment_data', 'user','post','parent','datetime']
