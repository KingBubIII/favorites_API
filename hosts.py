from django.conf import settings
from django_hosts import patterns, host
from django.urls import path, include

host_patterns = patterns('',
    host(r'api', 'api_urls', name='api'),
    host(r'docs', 'doc_urls', name='doc'),
)