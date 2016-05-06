from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext

from news.apps.person.forms import PersonImageForm
from news.apps.person.models import Person, PersonImage


# TODO(Kk): change name for profile_show or something more descriptive
def settings(request):
    user = request.user
    image_form = PersonImageForm()
    try:
        person = Person.objects.get(user=user)
    except Person.DoesNotExist:
        return render_to_response(template_name='global/auth/login.html')
    context = {
        'person': person,
        'image_form': image_form
    }
    return render(request=request, template_name='person/profile.html', context=context)


def add_image(request):
    if request.method == "POST":
        user = request.user
        person = Person.objects.get(user=user)
        image_form = PersonImageForm(request.POST, request.FILES)

        if image_form.is_valid():
            name = image_form.cleaned_data['name']
            image = request.FILES['image']
            person_image = PersonImage(name=name, image=image, person=person)
            person_image.crop_thumbnail()
            person_image.save()

            return redirect('person:profile:show')
    return HttpResponse('not ok')
