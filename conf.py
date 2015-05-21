{% load projects_tags %}

import sys
from six import string_types

from sphinx import version_info

from recommonmark.parser import CommonMarkParser

# Only Sphinx 1.3+
if version_info[0] == 1 and version_info[1] > 2:

    # Markdown Support
    if 'source_suffix' in globals():
        if isinstance(source_suffix, string_types) and source_suffix != '.md':
            source_suffix = [source_suffix, '.md']
        elif '.md' not in source_suffix:
            source_suffix.append('.md')
    else:
        source_suffix = ['.rst', '.md']

    if 'source_parsers' in globals():
        source_parsers['.md'] = CommonMarkParser
    else:
        source_parsers = {
            '.md': CommonMarkParser,
        }

if globals().get('source_suffix', False):
    if isinstance(source_suffix, string_types):
        SUFFIX = source_suffix
    else:
        SUFFIX = source_suffix[0]
else:
    SUFFIX = '.rst'



#Add RTD Template Path.
if 'templates_path' in globals():
    templates_path.insert(0, '{{ template_path }}')
else:
    templates_path = ['{{ template_path }}', 'templates', '_templates',
                      '.templates']

# Add RTD Static Path. Add to the end because it overwrites previous files.
if 'html_static_path' in globals():
    html_static_path.append('{{ static_path }}')
else:
    html_static_path = ['_static', '{{ static_path }}']

# Add RTD Theme Path. 
if 'html_theme_path' in globals():
    html_theme_path.append('{{ template_path }}')
else:
    html_theme_path = ['_themes', '{{ template_path }}']

# Add RTD Theme only if they aren't overriding it already
using_rtd_theme = False
if 'html_theme' in globals():
    if html_theme in ['default']:
        # Allow people to bail with a hack of having an html_style
        if not 'html_style' in globals():
            html_theme = 'sphinx_rtd_theme'
            html_style = None
            html_theme_options = {}
            using_rtd_theme = True
else:
    html_theme = 'sphinx_rtd_theme'
    html_style = None
    html_theme_options = {}
    using_rtd_theme = True

# Force theme on setting
if globals().get('RTD_NEW_THEME', False):
    html_theme = 'sphinx_rtd_theme'
    html_style = None
    html_theme_options = {}
    using_rtd_theme = True

if globals().get('RTD_OLD_THEME', False):
    html_style = 'rtd.css'
    html_theme = 'default'

if globals().get('websupport2_base_url', False):
    websupport2_base_url = '{{ api_host }}/websupport'
    if 'http' not in settings.MEDIA_URL:
        websupport2_static_url = '{{ settings.STATIC_URL }}'
    else:
        websupport2_static_url = '{{ settings.MEDIA_URL }}/static'


#Add project information to the template context.
context = {
    'using_theme': using_rtd_theme,
    'html_theme': html_theme,
    'current_version': "{{ current_version }}",
    'MEDIA_URL': "{{ settings.MEDIA_URL }}",
    'PRODUCTION_DOMAIN': "{{ settings.PRODUCTION_DOMAIN }}",
    'versions': [{% for version in versions %}
    ("{{ version.slug }}", "/{{ version.project.language }}/{{ version.slug}}/"),{% endfor %}
    ],
    'downloads': [ {% for key, val in downloads.items %}
    ("{{ key }}", "{{ val }}"),{% endfor %}
    ],
    'slug': '{{ project.slug }}',
    'name': u'{{ project.name }}',
    'rtd_language': u'{{ project.language }}',
    'canonical_url': '{{ project.clean_canonical_url }}',
    'analytics_code': '{{ project.analytics_code }}',
    'single_version': {{ project.single_version }},
    'conf_py_path': '{{ conf_py_path }}',
    'api_host': '{{ api_host }}',
    'github_user': '{{ github_user }}',
    'github_repo': '{{ github_repo }}',
    'github_version': '{{ github_version }}',
    'display_github': {{ display_github }},
    'bitbucket_user': '{{ bitbucket_user }}',
    'bitbucket_repo': '{{ bitbucket_repo }}',
    'bitbucket_version': '{{ bitbucket_version }}',
    'display_bitbucket': {{ display_bitbucket }},
    'READTHEDOCS': True,
    'using_theme': (html_theme == "alabaster"),
    'new_theme': (html_theme == "alabaster"),
    'source_suffix': SUFFIX,
    'user_analytics_code': '{{ project.analytics_code|default_if_none:'' }}',
    'global_analytics_code': '{{ settings.GLOBAL_ANALYTICS_CODE }}',
    'commit': '{{ commit }}',
}
if 'html_context' in globals():
    html_context.update(context)
else:
    html_context = context

# Add custom RTD extension
if 'extensions' in globals():
    extensions.append("readthedocs_ext.readthedocs")
else:
    extensions = ["readthedocs_ext.readthedocs"]