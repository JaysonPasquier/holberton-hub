from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages as django_messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from projects.models import Project
from .models import ChatRoom, Message, GlobalChatBot  # Ajout de GlobalChatBot

from .serializers import ChatRoomSerializer, MessageSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Message.objects.all()
        room_id = self.request.query_params.get('room', None)
        last_id = self.request.query_params.get('after', None)

        if room_id is not None:
            queryset = queryset.filter(room_id=room_id)
            if last_id:
                queryset = queryset.filter(id__gt=last_id)

        return queryset.order_by('-created_at')

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            room_id = data.get('room')
            content = data.get('content')
            is_command = data.get('is_command', False)

            if not request.user.is_authenticated:
                return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

            chat_room = ChatRoom.objects.get(id=room_id)

            # Gérer les commandes bot
            if content.startswith('/'):
                handle_bot_command(chat_room, content)
                return Response({"status": "command executed"}, status=status.HTTP_200_OK)

            # Créer le message normal
            message = Message.objects.create(
                room=chat_room,
                sender=request.user,
                content=content
            )
            serializer = self.get_serializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        room_id = self.request.data.get('room')
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        serializer.save(sender=self.request.user, room=chat_room)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class ChatBotViewSet(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]  # Changed from [IsAuthenticated]

    def create(self, request):
        try:
            command = request.data.get('message', '')
            if not command:
                return Response({
                    'response': "Je n'ai pas compris votre message. Tapez 'help' pour voir les commandes disponibles.",
                    'quickReplies': self.get_default_buttons()
                })

            response_data = self.get_bot_response(command.strip().lower())
            return Response(response_data, status=200)
        except Exception as e:
            print(f"ChatBot Error: {str(e)}")
            return Response({
                'response': "Une erreur s'est produite. Veuillez réessayer.",
                'quickReplies': self.get_default_buttons()
            }, status=200)

    def get_bot_response(self, command):
        responses = {
            'about_site': {
                'response': (
                    "<h4>🌟 À propos de Holberton Hub</h4>"
                    "<p>Holberton Hub est une plateforme collaborative permettant aux étudiants de:</p>"
                    "<ol>"
                    "<li>Créer et rejoindre des projets innovants</li>"
                    "<li>Partager leurs compétences</li>"
                    "<li>Développer leur réseau professionnel</li>"
                    "<li>Travailler en équipe sur des projets concrets</li>"
                    "</ol>"
                    "<p>C'est l'endroit idéal pour concrétiser vos idées et développer votre portfolio !</p>"
                ),
                'quickReplies': self.get_default_buttons()
            },
            'create_project': {
                'response': (
                    "<h4>📝 Création de projet</h4>"
                    "<p>Pour créer un projet, suivez ces étapes:</p>"
                    "<ol>"
                    "<li>Cliquez sur <strong>'Créer un projet'</strong> dans le menu</li>"
                    "<li>Remplissez le titre et la description</li>"
                    "<li>Choisissez le type de projet donc si cest une spé ou pas</li>"
                    "<li>Indiquez la taille de l'équipe et le statut du projet</li>"
                    "<li>Choisissez si le projet est rémunerer ou pas</li>"
                    "<li>Donnez un lien de repository github si vous le voulez</li>"
                    "<li>Ajoutez les technologies requises</li>"
                    "<li>Enregistrez les modifications</li>"
                    "</ol>"
                ),
                'quickReplies': self.get_default_buttons()
            },
            'search_project': {
                'response': (
                    "<h4>🔍 trouver un projet </h4>"
                    "<p>Voici comment trouver un projet:</p>"
                    "<ol>"
                    "<li>Allez sur la page 'Projets'</li>"
                    "<li>Utilisez les filtres par type</li>"
                    "<li>Consultez les descriptions</li>"
                    "<li>Postulez aux projets qui vous intéressent</li>"
                    "</ol>"
                ),
                'quickReplies': self.get_default_buttons()
            },
            'profile': {
                'response': (
                    "<h4>👤 Gérer votre profil</h4>"
                    "<p>Voici comment gérer votre profil:</p>"
                    "<ol>"
                    "<li>Cliquez sur 'Profil' dans le menu</li>"
                    "<li>Mettez à jour vos informations</li>"
                    "<li>Consultez vos projets</li>"
                    "<li>Suivez vos candidatures</li>"
                    "</ol>"
                    "<p>Vous pouvez également consulter le profil des autres utilisateurs.</p>"
                ),
                'quickReplies': self.get_default_buttons()
            },
            'help': {
                'response': (
                    "<h4>🤖 Bienvenue sur Holberton Hub!</h4>"
                    "<p>Je suis HolbieBot, votre assistant virtuel. Je suis là pour vous guider "
                    "dans l'utilisation de notre plateforme de collaboration entre étudiants.</p>"
                    "<p>Comment puis-je vous aider?</p>"
                ),
                'quickReplies': self.get_extended_buttons()
            }
        }
        return responses.get(command, responses['help'])

    def get_default_buttons(self):
        return [
            {"text": "💡 Créer un projet", "value": "create_project"},
            {"text": "🔍 Chercher un projet", "value": "search_project"},
            {"text": "👤 Mon profil", "value": "profile"},
            {"text": "ℹ️ À propos", "value": "about_site"},
            {"text": "❓ Aide", "value": "help"}
        ]

    def get_extended_buttons(self):
        return self.get_default_buttons()

@login_required
def project_chat(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.createur and request.user not in project.participants.all():
        django_messages.error(request, "Vous n'avez pas accès à ce chat.")
        return redirect('project_detail', pk=project_id)

    chat_room, created = ChatRoom.objects.get_or_create(project=project)

    # Envoyer le message de bienvenue si c'est une nouvelle room
    if created:
        chat_room.send_welcome_message()

    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        if content:
            # Vérifier les commandes du bot
            if content.startswith('/'):
                handle_bot_command(chat_room, content)
            else:
                try:
                    Message.objects.create(
                        room=chat_room,
                        sender=request.user,
                        content=content
                    )
                except IntegrityError:
                    pass
            return redirect('project_chat', project_id=project_id)

    chat_messages = Message.objects.filter(room=chat_room).select_related('sender').order_by('-created_at')
    return render(request, 'chat/project_chat.html', {
        'project': project,
        'chat_messages': chat_messages,
        'chat_room': chat_room,
        'oldest_id': chat_messages.last().id if chat_messages.exists() else 0
    })

def handle_bot_command(chat_room, command):
    if command == '/help':
        help_message = (
            "📚 Commandes disponibles:\n"
            "/help - Affiche cette aide\n"
            "/project - Informations sur le projet\n"
            "/members - Liste des participants\n"
            "/status - État du projet"
        )
        chat_room.send_bot_message(help_message)
    elif command == '/project':
        project_info = (
            f"ℹ️ Projet: {chat_room.project.title}\n"
            f"Description: {chat_room.project.description[:100]}...\n"
            f"Type: {chat_room.project.project_type}\n"
            f"Statut: {chat_room.project.status}"
        )
        chat_room.send_bot_message(project_info)
    # Ajoutez d'autres commandes selon vos besoins
