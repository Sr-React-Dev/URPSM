# -*- coding: utf-8 -*-
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from slugify import slugify

from smart_selects.db_fields import ChainedForeignKey
# from easy_thumbnails.fields import ThumbnailerImageField
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage
from mobilify.custom_storages import StaticStorage

from app.shop.models import Shop
from app.phone.models import Brand, Model
from app.search.index import Indexed, SearchField, FilterField, RelatedFields


class Type(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(editable=False, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Type, self).save(*args, **kwargs)


class Component(models.Model, Indexed):

    CURRENCY = (("AED", "United Arab Emirates Dirham"),
                ("AFN", "Afghan Afghani"),
                ("ALL", "Albanian Lek"),
                ("AMD", "Armenian Dram"),
                ("ANG", "Netherlands Antillean Guilder"),
                ("AOA", "Angolan Kwanza"),
                ("ARS", "Argentine Peso"),
                ("AUD", "Australian Dollar"),
                ("AWG", "Aruban Florin"),
                ("AZN", "Azerbaijani Manat"),
                ("BAM", "Bosnia-Herzegovina Convertible Mark"),
                ("BBD", "Barbadian Dollar"),
                ("BDT", "Bangladeshi Taka"),
                ("BGN", "Bulgarian Lev"),
                ("BHD", "Bahraini Dinar"),
                ("BIF", "Burundian Franc"),
                ("BMD", "Bermudan Dollar"),
                ("BND", "Brunei Dollar"),
                ("BOB", "Bolivian Boliviano"),
                ("BRL", "Brazilian Real"),
                ("BSD", "Bahamian Dollar"),
                ("BTC", "Bitcoin"),
                ("BTN", "Bhutanese Ngultrum"),
                ("BWP", "Botswanan Pula"),
                ("BYR", "Belarusian Ruble"),
                ("BZD", "Belize Dollar"),
                ("CAD", "Canadian Dollar"),
                ("CDF", "Congolese Franc"),
                ("CHF", "Swiss Franc"),
                ("CLF", "Chilean Unit of Account (UF)"),
                ("CLP", "Chilean Peso"),
                ("CNY", "Chinese Yuan"),
                ("COP", "Colombian Peso"),
                ("CRC", "Costa Rican Colón"),
                ("CUC", "Cuban Convertible Peso"),
                ("CUP", "Cuban Peso"),
                ("CVE", "Cape Verdean Escudo"),
                ("CZK", "Czech Republic Koruna"),
                ("DJF", "Djiboutian Franc"),
                ("DKK", "Danish Krone"),
                ("DOP", "Dominican Peso"),
                ("DZD", "Algerian Dinar"),
                ("EEK", "Estonian Kroon"),
                ("EGP", "Egyptian Pound"),
                ("ERN", "Eritrean Nakfa"),
                ("ETB", "Ethiopian Birr"),
                ("EUR", "Euro"),
                ("FJD", "Fijian Dollar"),
                ("FKP", "Falkland Islands Pound"),
                ("GBP", "British Pound Sterling"),
                ("GEL", "Georgian Lari"),
                ("GGP", "Guernsey Pound"),
                ("GHS", "Ghanaian Cedi"),
                ("GIP", "Gibraltar Pound"),
                ("GMD", "Gambian Dalasi"),
                ("GNF", "Guinean Franc"),
                ("GTQ", "Guatemalan Quetzal"),
                ("GYD", "Guyanaese Dollar"),
                ("HKD", "Hong Kong Dollar"),
                ("HNL", "Honduran Lempira"),
                ("HRK", "Croatian Kuna"),
                ("HTG", "Haitian Gourde"),
                ("HUF", "Hungarian Forint"),
                ("IDR", "Indonesian Rupiah"),
                ("ILS", "Israeli New Sheqel"),
                ("IMP", "Manx pound"),
                ("INR", "Indian Rupee"),
                ("IQD", "Iraqi Dinar"),
                ("IRR", "Iranian Rial"),
                ("ISK", "Icelandic Króna"),
                ("JEP", "Jersey Pound"),
                ("JMD", "Jamaican Dollar"),
                ("JOD", "Jordanian Dinar"),
                ("JPY", "Japanese Yen"),
                ("KES", "Kenyan Shilling"),
                ("KGS", "Kyrgystani Som"),
                ("KHR", "Cambodian Riel"),
                ("KMF", "Comorian Franc"),
                ("KPW", "North Korean Won"),
                ("KRW", "South Korean Won"),
                ("KWD", "Kuwaiti Dinar"),
                ("KYD", "Cayman Islands Dollar"),
                ("KZT", "Kazakhstani Tenge"),
                ("LAK", "Laotian Kip"),
                ("LBP", "Lebanese Pound"),
                ("LKR", "Sri Lankan Rupee"),
                ("LRD", "Liberian Dollar"),
                ("LSL", "Lesotho Loti"),
                ("LTL", "Lithuanian Litas"),
                ("LVL", "Latvian Lats"),
                ("LYD", "Libyan Dinar"),
                ("MAD", "Moroccan Dirham"),
                ("MDL", "Moldovan Leu"),
                ("MGA", "Malagasy Ariary"),
                ("MKD", "Macedonian Denar"),
                ("MMK", "Myanma Kyat"),
                ("MNT", "Mongolian Tugrik"),
                ("MOP", "Macanese Pataca"),
                ("MRO", "Mauritanian Ouguiya"),
                ("MTL", "Maltese Lira"),
                ("MUR", "Mauritian Rupee"),
                ("MVR", "Maldivian Rufiyaa"),
                ("MWK", "Malawian Kwacha"),
                ("MXN", "Mexican Peso"),
                ("MYR", "Malaysian Ringgit"),
                ("MZN", "Mozambican Metical"),
                ("NAD", "Namibian Dollar"),
                ("NGN", "Nigerian Naira"),
                ("NIO", "Nicaraguan Córdoba"),
                ("NOK", "Norwegian Krone"),
                ("NPR", "Nepalese Rupee"),
                ("NZD", "New Zealand Dollar"),
                ("OMR", "Omani Rial"),
                ("PAB", "Panamanian Balboa"),
                ("PEN", "Peruvian Nuevo Sol"),
                ("PGK", "Papua New Guinean Kina"),
                ("PHP", "Philippine Peso"),
                ("PKR", "Pakistani Rupee"),
                ("PLN", "Polish Zloty"),
                ("PYG", "Paraguayan Guarani"),
                ("QAR", "Qatari Rial"),
                ("RON", "Romanian Leu"),
                ("RSD", "Serbian Dinar"),
                ("RUB", "Russian Ruble"),
                ("RWF", "Rwandan Franc"),
                ("SAR", "Saudi Riyal"),
                ("SBD", "Solomon Islands Dollar"),
                ("SCR", "Seychellois Rupee"),
                ("SDG", "Sudanese Pound"),
                ("SEK", "Swedish Krona"),
                ("SGD", "Singapore Dollar"),
                ("SHP", "Saint Helena Pound"),
                ("SLL", "Sierra Leonean Leone"),
                ("SOS", "Somali Shilling"),
                ("SRD", "Surinamese Dollar"),
                ("STD", u"São Tomé and Príncipe Dobra"),
                ("SVC", u"Salvadoran Colón"),
                ("SYP", "Syrian Pound"),
                ("SZL", "Swazi Lilangeni"),
                ("THB", "Thai Baht"),
                ("TJS", "Tajikistani Somoni"),
                ("TMT", "Turkmenistani Manat"),
                ("TND", "Tunisian Dinar"),
                ("TOP", "Tongan Paʻanga"),
                ("TRY", "Turkish Lira"),
                ("TTD", "Trinidad and Tobago Dollar"),
                ("TWD", "New Taiwan Dollar"),
                ("TZS", "Tanzanian Shilling"),
                ("UAH", "Ukrainian Hryvnia"),
                ("UGX", "Ugandan Shilling"),
                ("USD", "United States Dollar"),
                ("UYU", "Uruguayan Peso"),
                ("UZS", "Uzbekistan Som"),
                ("VEF", "Venezuelan Bolívar Fuerte"),
                ("VND", "Vietnamese Dong"),
                ("VUV", "Vanuatu Vatu"),
                ("WST", "Samoan Tala"),
                ("XAF", "CFA Franc BEAC"),
                ("XAG", "Silver (troy ounce)"),
                ("XAU", "Gold (troy ounce)"),
                ("XCD", "East Caribbean Dollar"),
                ("XDR", "Special Drawing Rights"),
                ("XOF", "CFA Franc BCEAO"),
                ("XPD", "Palladium Ounce"),
                ("XPF", "CFP Franc"),
                ("XPT", "Platinum Ounce"),
                ("YER", "Yemeni Rial"),
                ("ZAR", "South African Rand"),
                ("ZMK", "Zambian Kwacha (pre-2013)"),
                ("ZMW", "Zambian Kwacha"),
                ("ZWL", "Zimbabwean Dollar"),
                )

    image = VersatileImageField(upload_to='components/%Y/%m/', blank=True,
        placeholder_image=OnStoragePlaceholderImage(
            path='v2/images/75-752.png',
            storage=StaticStorage()
            )
        
        )
    title = models.CharField(max_length=255)
    slug = models.SlugField(editable=False, db_index=True)
    brand = models.ForeignKey(Brand)
    model = ChainedForeignKey(Model,
                              chained_field='brand',
                              chained_model_field='brand',
                              show_all=False, auto_choose=True)
    type = models.ForeignKey(Type, related_name='component_type')

    description = models.TextField()
    currency = models.CharField(max_length=64, choices=CURRENCY, default='USD')
    price = models.DecimalField(
        max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=0)
    shop = models.ForeignKey(Shop, related_name='component_shop')
    sold = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    search_fields = [
        SearchField('title', partial_match=True, boost=10),
        SearchField('slug', partial_match=True, boost=10),
        SearchField('description', partial_match=True, boost=10),
        SearchField('currency'),
        FilterField('sold'),
        FilterField('deleted'),
        RelatedFields('type', [
            SearchField('name', partial_match=True, boost=8),
            SearchField('slug', partial_match=True, boost=8)
        ]),
        RelatedFields('brand', [
            SearchField('name', partial_match=True, boost=8),
            SearchField('slug', partial_match=True, boost=8),
            # SearchField('logo'),
        ]),
        RelatedFields('model', [
            SearchField('name', partial_match=True, boost=8),
            SearchField('slug', partial_match=True, boost=8),
            # SearchField('picture'),
        ]),
        FilterField('price')]

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return unicode(self.shop)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Component, self).save(*args, **kwargs)
