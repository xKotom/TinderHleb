from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from .models import Profile, Match, Feedback, Event, Purchase
from .forms import RegisterForm, LoginForm, ProfileForm, FeedbackForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            card_number = form.cleaned_data['card_number']
            password = form.cleaned_data['password']
            if Profile.objects.filter(card_number=card_number).exists():
                form.add_error('card_number', 'Эта карта уже зарегистрирована')
            else:
                username = f"card_{card_number}"
                email = form.cleaned_data['email']
                user = User.objects.create_user(username=username, password=password, email=email)
                Profile.objects.create(user=user, nickname=nickname, card_number=card_number)
                login(request, user)
                return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            password = form.cleaned_data['password']
            try:
                profile = Profile.objects.get(card_number=card_number)
                user = authenticate(request, username=profile.user.username, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, 'Неверный пароль')
            except Profile.DoesNotExist:
                form.add_error('card_number', 'Карта не найдена')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    return render(request, 'core/home.html')


@login_required
def profile_view(request):
    profile = request.user.profile
    events = Event.objects.all().order_by('date')
    joined_events = request.user.events_joined.all()
    purchases = Purchase.objects.filter(user=request.user).order_by('-date')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/profile.html', {
        'form': form,
        'profile': profile,
        'events': events,
        'joined_events': joined_events,
        'purchases': purchases,
    })


@login_required
def tinder_view(request):
    profile = request.user.profile
    already_acted = Match.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)

    candidates = Profile.objects.exclude(user=request.user).exclude(user_id__in=already_acted)

    if profile.looking_for_gender:
        candidates = candidates.filter(gender=profile.looking_for_gender)

    candidate = None
    match_score = 0
    shared_keywords = []
    shared_items = []

    for c in candidates:
        score = 0
        sk = set(profile.get_keywords_list()) & set(c.get_keywords_list())
        si = set(profile.get_favorite_items_list()) & set(c.get_favorite_items_list())
        score = len(sk) * 2 + len(si) * 3
        if candidate is None or score > match_score:
            candidate = c
            match_score = score
            shared_keywords = list(sk)
            shared_items = list(si)

    mutual_matches = Match.objects.filter(
        from_user=request.user, status='liked',
        to_user__in=Match.objects.filter(to_user=request.user, status='liked').values_list('from_user', flat=True)
    ).select_related('to_user__profile')

    return render(request, 'core/tinder.html', {
        'candidate': candidate,
        'match_score': match_score,
        'shared_keywords': shared_keywords,
        'shared_items': shared_items,
        'mutual_matches': mutual_matches,
        'profile': profile,
    })


@login_required
def swipe_view(request):
    if request.method == 'POST':
        to_user_id = request.POST.get('to_user_id')
        action = request.POST.get('action')
        to_user = get_object_or_404(User, id=to_user_id)

        Match.objects.update_or_create(
            from_user=request.user,
            to_user=to_user,
            defaults={'status': action}
        )

        is_mutual = False
        if action == 'liked':
            is_mutual = Match.objects.filter(
                from_user=to_user, to_user=request.user, status='liked'
            ).exists()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'mutual': is_mutual, 'name': to_user.profile.nickname})

    return redirect('tinder')


@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        feedback_type = request.POST.get('feedback_type', 'praise')
        if form.is_valid():
            fb = form.save(commit=False)
            fb.user = request.user
            fb.feedback_type = feedback_type
            fb.save()
            return redirect('feedback')
    else:
        form = FeedbackForm()

    user_feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'core/feedback.html', {'form': form, 'feedbacks': user_feedbacks})


@login_required
def chat_view(request):
    return render(request, 'core/chat.html')


@login_required
def set_search_mode(request):
    if request.method == 'POST':
        mode = request.POST.get('mode', '')
        if mode in ('friends', 'love'):
            request.user.profile.search_mode = mode
            request.user.profile.save(update_fields=['search_mode'])
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'mode': mode})
    return redirect('tinder')


@login_required
def event_join(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user not in event.participants.all() and event.spots_left() > 0:
        event.participants.add(request.user)
    return redirect('profile')


@login_required
def event_leave(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.participants.remove(request.user)
    return redirect('profile')
