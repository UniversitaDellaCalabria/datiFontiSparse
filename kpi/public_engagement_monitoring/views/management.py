import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, reverse
from django.utils.translation import gettext_lazy as _

from organizational_area.models import *

from template.utils import *

from .. forms import *
from .. models import *
from .. settings import *
from .. utils import *


def event_basic_info(request, structure_slug, event_id, by_manager=False, event=None):

    if by_manager:
        breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                       reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                       reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                       reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                       reverse('public_engagement_monitoring:manager_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                       '#': _('General informations')}
    else:
        breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                       reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                       reverse('public_engagement_monitoring:operator_dashboard'): _('Evaluation operator'),
                       reverse('public_engagement_monitoring:operator_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                       reverse('public_engagement_monitoring:operator_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                       '#': _('General informations')}

    template = 'pem/event_basic_info.html'
    form = PublicEngagementEventOperatorForm(request=request, instance=event)
    # post
    if request.method == 'POST':
        form = PublicEngagementEventOperatorForm(request=request,
                                         instance=event,
                                         data=request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.modified_by = request.user
            event.save()

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg='{}: {}'.format(structure_slug, _('modified general informations')))

            messages.add_message(request, messages.SUCCESS,
                                 _("Modified general informations successfully"))

            # invia email al referente/compilatore
            subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('data modified'))
            body = '{} {} {}'.format(request.user, _('has modified the data of the event'), '.')

            send_email_to_event_referents(event, subject, body)

            # invia email agli operatori dipartimentali
            if by_manager:
                send_email_to_operators(event.structure, subject, body)

            return True

        else:  # pragma: no cover
            messages.add_message(request, messages.ERROR,
                                 '<b>{}</b>: {}'.format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs, 'event': event, 'form': form})


def event_data(request, structure_slug, event_id, by_manager=False, event=None):
    if by_manager:
        breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                       reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                       reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                       reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                       reverse('public_engagement_monitoring:manager_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                       '#': _('Event data')}
    else:
        breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                       reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                       reverse('public_engagement_monitoring:operator_dashboard'): _('Evaluation operator'),
                       reverse('public_engagement_monitoring:operator_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                       reverse('public_engagement_monitoring:operator_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                       '#': _('Event data')}

    template = 'pem/event_data.html'
    form = PublicEngagementEventDataForm(instance=getattr(event, 'data', None))
    if request.method == 'POST':
        form = PublicEngagementEventDataForm(instance=getattr(event, 'data', None),
                                             data=request.POST,
                                             files=request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.event = event
            data.modified_by = request.user
            data.created_by = request.user
            data.save()
            form.save_m2m()
            event.modified_by = request.user
            event.save()

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg='{}: {}'.format(structure_slug, _('data modified')))

            messages.add_message(request, messages.SUCCESS,
                                 _("Data updated successfully"))

            # invia email al referente/compilatore
            subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('data modified'))
            body = '{} {} {}'.format(request.user, _('has modified the data of the event'), '.')

            send_email_to_event_referents(event, subject, body)

            # invia email agli operatori dipartimentali
            if by_manager:
                send_email_to_operators(event.structure, subject, body)

            return True
        else:
            messages.add_message(request, messages.ERROR,
                                 '<b>{}</b>: {}'.format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'event': event,
                                      'form': form,
                                      'structure_slug': structure_slug})


def event_people(request, structure_slug, event_id, by_manager=False, event=None):
    data = event.data
    template = 'pem/event_people.html'

    if by_manager:
        breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                       reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                       reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                       reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                       reverse('public_engagement_monitoring:manager_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                       '#': _('Involved personnel')}
    else:
        breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                       reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                       reverse('public_engagement_monitoring:operator_dashboard'): _('Evaluation operator'),
                       reverse('public_engagement_monitoring:operator_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                       reverse('public_engagement_monitoring:operator_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                       '#': _('Involved personnel')}

    if request.method == 'POST':
        # recupero dati completi del referente (in entrambi i casi)
        # es: genere
        person_id = request.POST.get('person_id')
        if not person_id:
            raise PermissionDenied()
        decrypted_id = requests.post('{}{}'.format(API_DECRYPTED_ID, '/'),
                                     data={'id': request.POST['person_id']},
                                     headers={'Authorization': 'Token {}'.format(settings.STORAGE_TOKEN)})
        response = requests.get('{}{}'.format(API_ADDRESSBOOK_FULL, decrypted_id.json()), headers={
                                'Authorization': 'Token {}'.format(settings.STORAGE_TOKEN)})
        if response.status_code != 200:
            raise PermissionDenied()
        person_data = response.json()['results']
        person = get_user_model().objects.filter(
            codice_fiscale=person_data['Taxpayer_ID']).first()
        # aggiorno il dato sul genere (potrebbe non essere presente localmente)
        if person and not person.gender:
            person.gender = person_data['Gender']
            person.save(update_fields=['gender'])
        # se non esiste localmente lo creo
        if not person:
            person = get_user_model().objects.create(username=person_data['Taxpayer_ID'],
                                                     matricola_dipendente=person_data['ID'],
                                                     first_name=person_data['Name'],
                                                     last_name=person_data['Surname'],
                                                     codice_fiscale=person_data['Taxpayer_ID'],
                                                     email=person_data['Email'][0],
                                                     gender=person_data['Gender'])
        if data.person.filter(pk=person.pk).exists():
            messages.add_message(request, messages.ERROR,
                                 '{} {}'.format(person, _('already exists')))
        else:
            data.person.add(person)
            data.modified_by = request.user
            data.save()
            event.modified_by = request.user
            event.save()

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg='{}: {} {} {} {}'.format(structure_slug, _('added'), person.first_name, person.last_name, _('in involved personnel')))

            messages.add_message(request, messages.SUCCESS,
                                 '{} {}'.format(person, _('added successfully')))

            # invia email al referente/compilatore
            subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('data modified'))
            body = '{} {} {}'.format(request.user, _('has modified the data of the event'), '.')
            send_email_to_event_referents(event, subject, body)

            # invia email agli operatori dipartimentali
            if by_manager:
                send_email_to_operators(event.structure, subject, body)

        return True
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'event': event,
                                      'structure_slug': structure_slug})


def event_people_delete(request, structure_slug, event_id, person_id, by_manager=False, event=None):
    if not person_id:
        raise PermissionDenied()
    person = event.data.person.filter(pk=person_id).first()
    if not person:
        messages.add_message(request, messages.ERROR, _('Personnel does not exist'))
    else:
        event.data.person.remove(person)
        event.data.modified_by = request.user
        event.data.save()
        event.modified_by = request.user
        event.save()

        log_action(user=request.user,
                   obj=event,
                   flag=CHANGE,
                   msg='{}: {} {} {}'.format(structure_slug, person.first_name, person.last_name, _('removed from involved personnel')))

        messages.add_message(request, messages.SUCCESS, _('Personnel removed successfully'))

        # invia email al referente/compilatore
        subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('data modified'))
        body = '{} {} {}'.format(request.user, _('has modified the data of the event'), '.')
        send_email_to_event_referents(event, subject, body)

        # invia email agli operatori dipartimentali
        if by_manager:
            send_email_to_operators(event.structure, subject, body)

    return redirect("public_engagement_monitoring:manager_event",
                    structure_slug=structure_slug,
                    event_id=event_id)
