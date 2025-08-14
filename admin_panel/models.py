from django.db import models

class IPO(models.Model):
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    price_band = models.CharField(max_length=100, blank=True, null=True)
    open_date = models.DateField(blank=True, null=True)
    close_date = models.DateField(blank=True, null=True)
    issue_size = models.CharField(max_length=100, blank=True, null=True)
    issue_type = models.CharField(max_length=50, choices=[
        ('book_building', 'Book Building'),
        ('fixed_price', 'Fixed Price')
    ], blank=True, null=True)
    listing_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('upcoming', 'Upcoming')
    ], blank=True, null=True)

    ipo_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    listing_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    listing_gain = models.CharField(max_length=100, blank=True, null=True)
    current_return = models.CharField(max_length=100, blank=True, null=True)
    cmp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    final_listing_date = models.DateField(blank=True, null=True)
    rhp_link = models.URLField(blank=True, null=True)
    drhp_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name
