from django.forms.widgets import *


class BootstrapItaliaAPISelectEventWidget(Select):
    template_name = 'pem/widgets/api_select_event.html'

    def __init__(self,  *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)
