# --- general comment --------------------------------------------------------------------------------------------------
# В этом проекте я постарался, насколько это возможно, всю логику обработки данных сосредоточить в представлениях,
# чтобы в шаблонах использовать DTL только для заполнения карточек. Поэтому все действия, необходимые для вычисления
# минимальной и максимальной цены и т.д., и т.п., также реализованы в этом файле.
#
# Также, выходя за рамки задания, я реализовал в едином со всем сайтом стиле доп. странички для предупреждения об
# отсутствии туров из других городов и о невозможности совершить оплату.
#
# Также, использую морфологический анализатор из библиотеки `pymorphy2` для согласования окончаний существительных.
# ----------------------------------------------------------------------------------------------------------------------

from django.shortcuts import render
from pymorphy2 import MorphAnalyzer
from random import sample

# mock-data
from data.data import title, subtitle, description, tours

departures = {'msk':   'москва',
              'spb':   'петербург',
              'nsk':   'новосибирск',
              'ekb':   'екатеринбург',
              'kazan': 'казань'}


# --- what if data was real... -----------------------------------------------------------------------------------------
# В реальных проектах нам приходится обрабатывать реальные данные, которые, как правильно, редко бывают предназначены
# для решения какой-то одной узкой задачи и, т.о., хранятся в нормализованном виде, приведенные к одному регистру и т.д.
#
# В своем коде я пытаюсь имитировать реальную структуру данных и поэтому переопределяю словарь `departures`
# и привожу пример, как получить текст вида "Из Москвы" из нормализованных названий городов
# ----------------------------------------------------------------------------------------------------------------------

def __get_gent(word):
    morph = MorphAnalyzer()
    return morph.parse(word)[0].inflect({"gent"}).word


def __get_agreed_with_number(number, word):
    morph = MorphAnalyzer()
    agreed_word = morph.parse(word)[0].make_agree_with_number(number).word
    return f"{number} {agreed_word}"


def __add_tour_details(tour, short_lng=10):
    nights = __get_agreed_with_number(tour['nights'], 'ночь')
    departure = __get_gent(departures.get(tour['departure'])).title()

    oneliner1 = f"{tour['stars']}★ | " + ", ".join([tour['date'], f"{nights}", f"{tour['price']} ₽"])
    oneliner2 = f"""{tour['country']} | Из {departure} | {nights}"""

    add = {'description_short': " ".join(tour['description'].split(' ')[:short_lng]) + '...',
           'oneliner_index': oneliner1,
           'oneliner_tour': oneliner2}

    return dict(tour, **add)


dep_links = [{'link': f'/departure/{k}/', 'title': f'из {__get_gent(v)}'.title()} for k, v in departures.items()]

mutual_context = context = {'title':       title,
                            'subtitle':    subtitle,
                            'description': description,
                            'tours':       {id: __add_tour_details(tour) for id, tour in tours.items()},
                            'links':       dep_links}


def main_view(request):
    context_index = mutual_context.copy()
    context_index.update({'random_tours': sample(tours.keys(), k=6)})
    return render(request, 'index.html', context=context_index)


def departure_view(request, departure):
    if departure in departures.keys():
        tours_departure = dict()
        min_price_departure = int(1e+15)
        max_price_departure = -1
        min_nights_departure = int(1e+15)
        max_nights_departure = -1

        for id, tour in mutual_context['tours'].items():
            if tour['departure'] == departure:
                tours_departure.update({id: tour})

                if tour['price'] < min_price_departure:
                    min_price_departure = tour['price']

                if tour['price'] > max_price_departure:
                    max_price_departure = tour['price']

                if tour['nights'] < min_nights_departure:
                    min_nights_departure = tour['nights']

                if tour['nights'] > max_nights_departure:
                    max_nights_departure = tour['nights']

        context_departure = mutual_context.copy()
        context_departure.update({'departure_rus':        __get_gent(departures.get(departure)).title(),
                                  'tours':                tours_departure,
                                  'tours_count':          __get_agreed_with_number(len(tours_departure.keys()), 'тур'),
                                  'min_price_departure':  min_price_departure,
                                  'max_price_departure':  __get_agreed_with_number(max_price_departure, 'рубль'),
                                  'min_nights_departure': min_nights_departure,
                                  'max_nights_departure': __get_agreed_with_number(max_nights_departure, 'ночь')})

        response = render(request, 'departure.html', context=context_departure)
    else:
        response = render(request, 'departure404.html', context=mutual_context)

    return response


def tour_view(request, id):
    context_tour = mutual_context.copy()
    context_tour.update({'tour': context['tours'].get(id)})
    return render(request, 'tour.html', context=context_tour)


def tour_purchase(request):
    return render(request, 'purchase404.html', context=mutual_context)
