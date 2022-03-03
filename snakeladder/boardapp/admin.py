from django.contrib import admin
from .models import GameMaster, Player, ScoreHistory
from django.contrib import admin
# Register your models here.
class GameMasterAdmin(admin.ModelAdmin):
    list_display  = [field.name for field in GameMaster._meta.fields if field.name != "id"]

class PlayerAdmin(admin.ModelAdmin):
    list_display  = [field.name for field in Player._meta.fields if field.name != "id"]

class ScoreHistoryAdmin(admin.ModelAdmin):
    list_display  = [field.name for field in ScoreHistory._meta.fields if field.name != "id"]

admin.site.register(GameMaster, GameMasterAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(ScoreHistory)
