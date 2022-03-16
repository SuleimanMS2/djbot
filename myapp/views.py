import json
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from telegram import Update

from .block_bot.bot import bot, dispatcher


@method_decorator(csrf_exempt, 'dispatch')
class Master(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        try:
            body = request.body
            data = json.loads(body)
            update: Update = Update.de_json(data, bot)
            dispatcher.process_update(update)
        except Exception as e:
            pass
        return HttpResponse('ok', status=200)


def home(request):
    return render(request, 'home.html')
