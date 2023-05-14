from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from captcha.fields import CaptchaField
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import shortened_url
from .forms import ShortcodeForm
import string
import random


def index(request):
    all_shortened_urls = shortened_url.objects.order_by('-id')
    paginator = Paginator(all_shortened_urls, 10)
    page_number = request.GET.get('page')
    shortened_urls = paginator.get_page(page_number)
    captcha = CaptchaField()
    form = ShortcodeForm()
    context = {'shortened_urls': shortened_urls, 'captcha': captcha, 'form': form}
    return render(request, 'url_shortener/index.html', context)

@login_required
def saveurl(request):
    # get the characters to choose from from string()
    letters = string.ascii_letters      # UPPER and lower case letters, a-Z
    digits = str(string.digits)         # integers, 0-9
    letters_digits = letters + digits   # combine letters & digits into one string
    if request.method == 'POST':
        form = ShortcodeForm(request.POST)
        long_url = request.POST['long_url']
        if form.is_valid():
            while True:
                shorturl_code = ''
                for i in range(5):
                    shorturl_code += random.choice(letters_digits)
                exist_count = shortened_url.objects.filter(code=shorturl_code).count()
                if exist_count > 0:
                    print("shorturl_code already exists")
                else:
                    short_url = shortened_url(code=shorturl_code, long_url=long_url)
                    short_url.save()
                    break
            return HttpResponseRedirect(reverse('url_shortener:index'))

    return HttpResponseRedirect(reverse('url_shortener:index'))

def redir_to_long_url(request, code):
    y = request.GET.get('y', '') # y=year
    try:
        url_object = shortened_url.objects.get(code=code)
        if code == 'h':
            if y:
                return redirect(url_object.long_url + "?" + y + "&" + "full")
        return redirect(url_object.long_url)
    except ObjectDoesNotExist:
        return HttpResponse("The code does not exist!")
