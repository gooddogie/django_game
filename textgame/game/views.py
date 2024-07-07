from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Character, Item, Monster
from .forms import CharacterForm, ItemForm, Character
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib import messages 
import random
from .models import Character, Monster, Item


def index(request):
    return render(request, 'game/home.html')

@login_required
def create_character(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.save()
            return redirect('profile')
    else:
        form = CharacterForm()
    return render(request, 'game/create_character.html', {'form': form})

@login_required
def profile(request):
    character = request.user.character
    items = character.items.all()
    item_with_half_price = []
    for item in items:
        item_with_half_price.append({
            'item': item,
            'half_price': item.price // 2
        })
    context = {
        'character': character,
        'items_with_half_price': item_with_half_price,
        'total_item_hp': sum(item.hp for item in items),
        'total_item_armor': sum(item.armor for item in items),
        'total_item_power': sum(item.power for item in items),
    }
    return render(request, 'game/profile.html', context)

@login_required
def shop(request):
    items = Item.objects.all()  
    character = Character.objects.get(user=request.user)

    context = {
        'items': items,
        'character': character,
    }
    return render(request, 'game/shop.html', context)

@login_required
def buy_item(request, item_id):
    character = Character.objects.get(user=request.user)
    item = Item.objects.get(id=item_id)

    #Check if character already has 5 items (which doesn't work and message system too!)
    if character.items.count() >= 5:
        messages.error(request, "You can't have more than 5 items.")
        return redirect('shop')

    #Check if character already owns this item
    elif item in character.items.all():
        messages.error(request, "You already own this item.")
        return redirect('shop')

    #Proceed to buy item if character has enough money
    elif character.money >= item.price:
        character.money -= item.price
        character.items.add(item) 
        character.save()
        messages.success(request, "Item purchased successfully!")
        return redirect('profile')
    else:
        messages.error(request, "You don't have enough money to buy this item.")
        return redirect('shop')
    
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.character = Character.objects.filter(user=request.user).first()
            item.save()
            return redirect('profile')
    else:
        form = ItemForm()
    return render(request, 'game/add_item.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_character')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('index')
    return render(request, 'registration/logout.html')

@login_required
def shop(request):
    items = Item.objects.all()
    return render(request, 'game/shop.html', {'items': items})

@login_required
def buy_item(request, item_id):
    character = Character.objects.get(user=request.user)
    item = Item.objects.get(id=item_id)

    if character.money >= item.price:
        character.money -= item.price
        character.items.add(item) 
        character.save()
        return redirect('profile')
    else:
        return redirect('shop') 
    
@login_required
def sell_item(request, item_id):
    character = request.user.character
    item = get_object_or_404(Item, id=item_id)
    character.sell_item(item)
    return redirect('profile')

def battle(request):
    character = Character.objects.get(user=request.user)

    #Base stats
    base_hp = 8 + character.level * 2
    base_armor = character.level
    base_power = 4 + character.level
    base_stamina = 8 + character.level * 2

    #Item stats
    total_item_hp = sum(item.hp for item in character.items.all())
    total_item_armor = sum(item.armor for item in character.items.all())
    total_item_power = sum(item.power for item in character.items.all())
    total_item_stamina = sum(item.stamina for item in character.items.all()) 

    #Combine base stats with item stats
    character.hp = base_hp + total_item_hp
    character.armor = base_armor + total_item_armor
    character.power = base_power + total_item_power
    character.stamina = base_stamina + total_item_stamina

    character.save()
    
    #Get random monster
    monster = Monster.objects.order_by('?').first()
    
    #Monster ID in session
    request.session['monster_id'] = monster.id
    
    context = {
        'character': character,
        'monster': monster,
    }
    return render(request, 'game/battle.html', context)


@login_required
def battle_action(request):
    character = Character.objects.get(user=request.user)
    monster_id = request.session.get('monster_id')

    if monster_id is None:
        return HttpResponse("No monster ID found in session.")

    monster = Monster.objects.get(pk=monster_id)

    action = request.POST.get('action')
    if action == 'attack' and character.stamina > 0:
        #Calculate damage for character
        base_damage = character.power - monster.armor
        base_damage = max(1, base_damage)
        damage_range = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
        actual_damage = max(1, damage_range)  #Damage is at least 1

        #Apply damage to monster
        monster.hp -= actual_damage
        character.stamina -= 1 

        #Calculate damage for monster
        base_damage = monster.power - character.armor
        base_damage = max(1, base_damage)
        damage_range = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
        actual_damage = max(1, damage_range)  #Damage is at least 1

        if monster.hp <= 0:
            #Handle monster defeat logic
            character.experience += monster.experience_worth
            money_gained = monster.level * random.randint(15, 20)  #Random money gain
            character.money += money_gained
            monster.hp = monster.default_hp  #Reset monster HP for next battle
            request.session['monster_id'] = None  #Reset monster in session
            monster.save()
            character.save()

            query_string = urlencode({'monster_id': monster.id, 'money_gained': money_gained})
            url = reverse('battle_result')
            return HttpResponseRedirect(f'{url}?{query_string}')
        
        else:
            #Apply damage to character
            if monster.stamina > 0:
                character.hp -= actual_damage
                monster.stamina -= 1
                if character.hp <= 0:
                    return redirect('profile')
            else:
                monster.stamina += 2

        character.save()
        monster.save()

    elif action == 'defend':
        character.stamina += 2

        #Calculate damage for monster
        base_damage = monster.power - character.armor
        base_damage = max(1, base_damage)
        damage_range = random.randint(int(base_damage * 0.8), int(base_damage * 1.2))
        actual_damage = max(1, damage_range)  #Damage is at least 1

        #Apply damage to character
        if monster.stamina > 0:
            character.hp -= actual_damage
            monster.stamina -= 1
            if character.hp <= 0:
                return redirect('profile')
        else:
            monster.stamina += 2

        character.save()

    context = {
        'character': character,
        'monster': monster,
    }
    return render(request, 'game/battle.html', context)


def battle_result(request):
    monster_id = request.GET.get('monster_id')
    money_gained = request.GET.get('money_gained')
    
    monster = Monster.objects.get(id=monster_id)
    
    context = {
        'monster': monster,
        'money_gained': money_gained,
        'experience_gained': monster.experience_worth,
    }
    return render(request, 'game/battle_result.html', context)