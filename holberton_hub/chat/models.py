from django.db import models
from users.models import User
from projects.models import Project

class ChatRoom(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def send_welcome_message(self):
        try:
            bot_user = User.objects.get(username='HolbieBot')
            welcome_message = (
                "👋 Bienvenue dans le chat du projet!\n\n"
                "🤖 Je suis HolbieBot, voici quelques informations utiles:\n"
                "- Les participants peuvent échanger des messages en temps réel\n"
                "- Les messages sont chargés automatiquement toutes les 3 secondes\n"
                "- Vous pouvez faire défiler vers le bas pour voir les anciens messages\n\n"
                "Pour plus d'aide, tapez /help 🎯"
            )
            Message.objects.create(
                room=self,
                sender=bot_user,
                content=welcome_message
            )
        except User.DoesNotExist:
            pass

    def send_bot_message(self, content):
        try:
            bot_user = User.objects.get(username='HolbieBot')
            Message.objects.create(
                room=self,
                sender=bot_user,
                content=content
            )
        except User.DoesNotExist:
            pass

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"

    class Meta:
        ordering = ['-created_at']  # Inverser l'ordre pour avoir les plus récents en premier
        constraints = [
            models.UniqueConstraint(
                fields=['room', 'sender', 'content', 'created_at'],
                name='unique_message'
            )
        ]

class GlobalChatBot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
