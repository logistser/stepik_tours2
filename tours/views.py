from django.shortcuts import render
from django.http import HttpResponseNotFound


departures = {'moscow': 'из Москвы',
              'stpetersburg': 'из Петербурга',
              'novosibirsk': 'из Новосибирска',
              'ekaterinburg': 'из Екатеринбурга',
              'kazan': 'из Казани'}


def main_view(request):
    return render(request, 'index.html')


def departure_view(request, departure):
    context = {'departure': departures.get(departure)}

    if departure in departures.keys():
        response = render(request, 'departure.html', context=context)
    else:
        response = HttpResponseNotFound('Простите, из вашего города мы пока не летаем.')

    return response


def tour_view(request, id):
    return render(request, 'tour.html')
