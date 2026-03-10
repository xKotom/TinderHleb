from django.contrib import admin
from .models import Profile, Match, Feedback, Event, Purchase


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'card_number', 'gender', 'age', 'bonuses')
    search_fields = ('nickname', 'card_number')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'status', 'created_at')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'created_at')
    list_filter = ('feedback_type',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'max_participants')
    filter_horizontal = ('participants',)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_name', 'price', 'bonuses_earned', 'date')
