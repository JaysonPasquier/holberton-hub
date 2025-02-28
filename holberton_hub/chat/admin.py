from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from django.utils import timezone
from .models import ChatRoom, Message, GlobalChatBot

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('project_title', 'project_type', 'creator', 'created_at', 'message_count', 'participants_count', 'status')
    list_filter = (
        'project__type_projet',
        'created_at',
        'project__createur',
        'project__statut_projet',
    )
    search_fields = ('project__titre', 'project__createur__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def project_title(self, obj):
        return format_html('<a href="/admin/projects/project/{}">{}</a>', obj.project.id, obj.project.titre)
    project_title.short_description = 'Projet'
    project_title.admin_order_field = 'project__titre'

    def project_type(self, obj):
        return obj.project.get_type_projet_display()
    project_type.short_description = 'Type de projet'
    project_type.admin_order_field = 'project__type_projet'

    def creator(self, obj):
        return obj.project.createur.username
    creator.short_description = 'Créateur'
    creator.admin_order_field = 'project__createur__username'

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Nombre de messages'

    def participants_count(self, obj):
        return obj.project.participants.count()
    participants_count.short_description = 'Participants'

    def status(self, obj):
        status_colors = {
            'OUVERT': 'green',
            'EN_COURS': 'orange',
            'TERMINE': 'red'
        }
        color = status_colors.get(obj.project.statut_projet, 'gray')
        return format_html('<span style="color: {};">{}</span>',
                         color,
                         obj.project.get_statut_projet_display())
    status.short_description = 'Statut'

    # Ajouter des stats en haut de la page
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_chatrooms'] = ChatRoom.objects.count()
        extra_context['active_rooms'] = ChatRoom.objects.filter(project__statut_projet='EN_COURS').count()
        extra_context['total_messages'] = Message.objects.count()
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'sender_with_link', 'content_preview', 'created_at', 'is_bot_message')
    list_filter = (
        ('room__project', admin.RelatedOnlyFieldListFilter),
        'sender',
        'created_at',
        'sender__is_superuser',  # Pour filtrer les messages du bot
    )
    search_fields = (
        'content',
        'sender__username',
        'room__project__titre'
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 50

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Message'

    def project_name(self, obj):
        return obj.room.project.titre
    project_name.short_description = 'Projet'
    project_name.admin_order_field = 'room__project__titre'

    def sender_with_link(self, obj):
        return format_html('<a href="/admin/users/user/{}">{}</a>',
                         obj.sender.id,
                         obj.sender.username)
    sender_with_link.short_description = 'Expéditeur'

    def is_bot_message(self, obj):
        return obj.sender.username == 'HolbieBot'
    is_bot_message.short_description = 'Message Bot'
    is_bot_message.boolean = True

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'sender',
            'room',
            'room__project'
        ).prefetch_related('room__project__participants')

    # Ajouter des statistiques en haut de la page
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['messages_today'] = Message.objects.filter(
            created_at__date=timezone.now().date()
        ).count()
        extra_context['active_users'] = Message.objects.values('sender').distinct().count()
        extra_context['bot_messages'] = Message.objects.filter(
            sender__username='HolbieBot'
        ).count()
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(GlobalChatBot)
class GlobalChatBotAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'response_preview', 'created_at')
    search_fields = ('message', 'response', 'user__username')
    list_filter = ('created_at', 'user')

    def message_preview(self, obj):
        return obj.message[:30] + '...' if len(obj.message) > 30 else obj.message

    def response_preview(self, obj):
        return obj.response[:30] + '...' if len(obj.response) > 30 else obj.response

    message_preview.short_description = 'Message'
    response_preview.short_description = 'Réponse'
