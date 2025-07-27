from django.core.management.base import BaseCommand
from sentinel.models import Achievement

class Command(BaseCommand):
    help = 'Create initial achievements for the CosmoDex system'

    def handle(self, *args, **options):
        achievements = [
            {
                'key': 'first_contact',
                'name': 'First Contact',
                'description': 'Ask the Quackstronaut chatbot your first question',
                'icon': '🚀',
                'category': 'Communication',
                'requirement': 1,
                'requirement_type': 'chat_questions'
            },
            {
                'key': 'cosmic_chatterbox',
                'name': 'Cosmic Chatterbox',
                'description': 'Ask Quackstronaut 10 questions',
                'icon': '💬',
                'category': 'Communication',
                'requirement': 10,
                'requirement_type': 'chat_questions'
            },
            {
                'key': 'space_conversationalist',
                'name': 'Space Conversationalist',
                'description': 'Ask Quackstronaut 25 questions',
                'icon': '🗣️',
                'category': 'Communication',
                'requirement': 25,
                'requirement_type': 'chat_questions'
            },
            {
                'key': 'galactic_investigator',
                'name': 'Galactic Investigator',
                'description': 'Ask questions about three different NEOs',
                'icon': '🔍',
                'category': 'Exploration',
                'requirement': 3,
                'requirement_type': 'unique_neo_chats'
            },
            {
                'key': 'cosmic_detective',
                'name': 'Cosmic Detective',
                'description': 'Ask questions about 10 different NEOs',
                'icon': '🕵️',
                'category': 'Exploration',
                'requirement': 10,
                'requirement_type': 'unique_neo_chats'
            },
            {
                'key': 'wish_upon_star',
                'name': 'Wish Upon a Star',
                'description': 'Favorite your very first NEO',
                'icon': '⭐',
                'category': 'Collection',
                'requirement': 1,
                'requirement_type': 'favorites_count'
            },
            {
                'key': 'constellation_creator',
                'name': 'Constellation Creator',
                'description': 'Have 10 NEOs in your favorites list',
                'icon': '✨',
                'category': 'Collection',
                'requirement': 10,
                'requirement_type': 'favorites_count'
            },
            {
                'key': 'galaxy_curator',
                'name': 'Galaxy Curator',
                'description': 'Have 25 NEOs in your favorites list',
                'icon': '🌌',
                'category': 'Collection',
                'requirement': 25,
                'requirement_type': 'favorites_count'
            },
            {
                'key': 'asteroid_archivist',
                'name': 'Asteroid Archivist',
                'description': 'Have 50 NEOs in your favorites list',
                'icon': '📚',
                'category': 'Collection',
                'requirement': 50,
                'requirement_type': 'favorites_count'
            },
            {
                'key': 'space_explorer',
                'name': 'Space Explorer',
                'description': 'View details of 5 different NEOs',
                'icon': '🛸',
                'category': 'Discovery',
                'requirement': 5,
                'requirement_type': 'neos_viewed'
            },
            {
                'key': 'cosmic_voyager',
                'name': 'Cosmic Voyager',
                'description': 'View details of 20 different NEOs',
                'icon': '🌠',
                'category': 'Discovery',
                'requirement': 20,
                'requirement_type': 'neos_viewed'
            },
            {
                'key': 'daily_visitor',
                'name': 'Daily Visitor',
                'description': 'Check your daily briefing 5 times',
                'icon': '📅',
                'category': 'Engagement',
                'requirement': 5,
                'requirement_type': 'daily_briefings'
            },
            {
                'key': 'space_station_regular',
                'name': 'Space Station Regular',
                'description': 'Check your daily briefing 15 times',
                'icon': '🏠',
                'category': 'Engagement',
                'requirement': 15,
                'requirement_type': 'daily_briefings'
            }
        ]

        for achievement_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                key=achievement_data['key'],
                defaults=achievement_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created achievement: {achievement.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Achievement already exists: {achievement.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully initialized achievements!')
        )
