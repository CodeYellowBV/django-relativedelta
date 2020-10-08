__version__ = '1.1.2'

from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS

from .fields import RelativeDeltaField # noqa
from .forms import RelativeDeltaFormField # noqa

FORMFIELD_FOR_DBFIELD_DEFAULTS[RelativeDeltaField] = {
    'form_class': RelativeDeltaFormField
}
