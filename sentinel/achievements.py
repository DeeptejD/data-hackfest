from django.db.models import Count
from .models import UserInteraction, Achievement, UserAchievement, FavoriteNEO


def track_user_interaction(user_email, interaction_type, neo_name=None):
    """Track a user interaction and check for new achievements"""
    # Record the interaction
    UserInteraction.objects.create(
        user_email=user_email,
        interaction_type=interaction_type,
        neo_name=neo_name
    )
    
    # Check for new achievements
    check_achievements(user_email)


def check_achievements(user_email):
    """Check if user has unlocked any new achievements"""
    # Get all achievements not yet unlocked by this user
    unlocked_achievement_ids = UserAchievement.objects.filter(
        user_email=user_email
    ).values_list('achievement_id', flat=True)
    
    available_achievements = Achievement.objects.exclude(
        id__in=unlocked_achievement_ids
    )
    
    newly_unlocked = []
    
    for achievement in available_achievements:
        if check_single_achievement(user_email, achievement):
            UserAchievement.objects.create(
                user_email=user_email,
                achievement=achievement
            )
            newly_unlocked.append(achievement)
    
    return newly_unlocked


def check_single_achievement(user_email, achievement):
    """Check if a specific achievement should be unlocked"""
    if achievement.requirement_type == 'chat_questions':
        count = UserInteraction.objects.filter(
            user_email=user_email,
            interaction_type='chat_question'
        ).count()
        return count >= achievement.requirement
    
    elif achievement.requirement_type == 'unique_neo_chats':
        count = UserInteraction.objects.filter(
            user_email=user_email,
            interaction_type='chat_question'
        ).values('neo_name').distinct().count()
        return count >= achievement.requirement
    
    elif achievement.requirement_type == 'favorites_count':
        count = FavoriteNEO.objects.filter(user_email=user_email).count()
        return count >= achievement.requirement
    
    elif achievement.requirement_type == 'neos_viewed':
        count = UserInteraction.objects.filter(
            user_email=user_email,
            interaction_type='neo_viewed'
        ).values('neo_name').distinct().count()
        return count >= achievement.requirement
    
    elif achievement.requirement_type == 'daily_briefings':
        count = UserInteraction.objects.filter(
            user_email=user_email,
            interaction_type='daily_briefing'
        ).count()
        return count >= achievement.requirement
    
    return False


def get_user_stats(user_email):
    """Get comprehensive user statistics"""
    stats = {
        'total_questions': UserInteraction.objects.filter(
            user_email=user_email,
            interaction_type='chat_question'
        ).count(),
        'unique_neos_chatted': UserInteraction.objects.filter(
            user_email=user_email,
            interaction_type='chat_question'
        ).values('neo_name').distinct().count(),
        'favorites_count': FavoriteNEO.objects.filter(user_email=user_email).count(),
        'neos_viewed': UserInteraction.objects.filter(
            user_email=user_email,
            interaction_type='neo_viewed'
        ).values('neo_name').distinct().count(),
        'daily_briefings': UserInteraction.objects.filter(
            user_email=user_email,
            interaction_type='daily_briefing'
        ).count(),
        'achievements_count': UserAchievement.objects.filter(user_email=user_email).count(),
        'total_achievements': Achievement.objects.count()
    }
    return stats


def get_user_achievements(user_email):
    """Get all achievements for a user, both unlocked and locked"""
    unlocked = UserAchievement.objects.filter(
        user_email=user_email
    ).select_related('achievement').order_by('-unlocked_at')
    
    unlocked_ids = [ua.achievement.id for ua in unlocked]
    
    locked = Achievement.objects.exclude(id__in=unlocked_ids).order_by('category', 'requirement')
    
    return {
        'unlocked': unlocked,
        'locked': locked
    }
