"""Forms for the App."""

from django.core.validators import URLValidator
from django.forms import ModelForm, ValidationError

from ezscrape.scraping.scraper import check_url

from .models import Store


class StoreCreateForm(ModelForm):
    """Create form for the Store Model."""

    class Meta:
        """Define the Form meta data."""

        model = Store
        fields = ('name', 'prod_base_url', 'currency', 'dynamic_page')

    def clean_prod_base_url(self):
        """Validate the Store base url."""
        base_url = self.cleaned_data['prod_base_url']

        # Validate the Url is in the correct Form
        url_validator = URLValidator(schemes=['http', 'https'])
        try:
            url_validator(base_url)
        except ValidationError as error:
            raise ValidationError(F'Invalid Url: {error} - Dont forget to include the schema like http or https')

        # Check if we can reach the url
        if not check_url(base_url, local_only=False):
            raise ValidationError(F'Cannot Reach URL')

        return base_url
