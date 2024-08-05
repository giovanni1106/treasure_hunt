from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import ConfigHome, Challenge, UserChallengeCompletion
from .forms import ConfigHomeForm, ChallengeForm
from django.contrib.auth.models import User
from django.contrib import messages  # Para mensagens de feedback


def home(request):
    config_home = ConfigHome.objects.first()
    challenges = Challenge.objects.all().order_by("index")
    user = request.user

    return render(
        request,
        "home.html",
        {
            "config_home": config_home,
            "challenges": challenges,
            "user": user,
        },
    )


@staff_member_required
def update_config_home(request):
    config_home = ConfigHome.objects.first() or ConfigHome()

    if request.method == "POST":
        form = ConfigHomeForm(request.POST, request.FILES, instance=config_home)

        if "delete_banner" in request.POST:
            # Remove o banner atual
            config_home.banner.delete(save=False)
            config_home.banner = None
            config_home.save()
            messages.success(request, "Banner apagado com sucesso.")
            return redirect("update_config_home")

        if form.is_valid():
            form.save()
            messages.success(request, "Configurações salvas com sucesso.")
            return redirect("/")

    else:
        form = ConfigHomeForm(instance=config_home)

    return render(
        request, "update_config_home.html", {"form": form, "config_home": config_home}
    )


@staff_member_required
def create_or_edit_challenge(request, challenge_id=None):
    if challenge_id:
        challenge = get_object_or_404(Challenge, id=challenge_id)
    else:
        challenge = Challenge()

    if request.method == "POST" and "delete" in request.POST:
        challenge.delete()
        return redirect("/")

    if request.method == "POST":
        form = ChallengeForm(request.POST, instance=challenge)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = ChallengeForm(instance=challenge)

    return render(
        request, "update_challenges.html", {"form": form, "challenge_id": challenge_id}
    )


@login_required
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    user = request.user

    # Check if the user has already completed the challenge
    if not user.is_staff and user not in challenge.users_completed.all():
        secret_code = request.GET.get("secret_code")

        # Check if the challenge requires a secret code
        if not challenge.is_free and (
            not secret_code or secret_code != challenge.secret_code
        ):
            messages.error(request, "Código secreto inválido ou desafio não liberado.")
            return redirect("/")

        # Check if the user has completed past challenges
        if challenge.index > 1:
            previous_challenge = Challenge.objects.get(index=challenge.index - 1)
            if (
                user not in previous_challenge.users_completed.all()
                and not challenge.is_free
            ):
                messages.error(request, "Desafio anterior não completado.")
                return redirect("/")

        # Mark challenge as completed
        completion, created = UserChallengeCompletion.objects.get_or_create(
            user=user, challenge=challenge
        )
        if created:
            challenge.users_completed.add(user)
            messages.success(request, "Desafio completado com sucesso!")

    # Retrieve completions
    completions = []
    if challenge.is_free:
        # return all users to board
        completions = User.objects.all()
    else:
        completions = (
            UserChallengeCompletion.objects.filter(challenge=challenge)
            .select_related("user")
            .order_by("-completed_at")
        )

    return render(
        request,
        "challenge_detail.html",
        {
            "challenge": challenge,
            "completions": completions,
        },
    )
