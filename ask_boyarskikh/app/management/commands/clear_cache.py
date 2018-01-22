#!/usr/bin/env python3
from django.core.cache import cache
from django.utils.translation import ugettext as _
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = _('Clear cache data')

    def handle(self, *args, **options):
        cache.clear()
