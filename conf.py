# -*- coding: utf-8 -*-
#
# -- General configuration -----------------------------------------------------

source_suffix = '.rst'
master_doc = 'index'

project = u'sphinx theme for basicstrap style'
copyright = u'2014, tell-k'

version = '0.4.1'

# -- Options for HTML output ---------------------------------------------------

extensions = ['sphinxjp.themes.basicstrap']
html_theme = 'basicstrap'

# -- HTML theme options for `basicstrap` style -------------------------------------

html_theme_options = {
    'lang': 'en',
    'nosidebar': False,
    'rightsidebar': False,
    'sidebar_span': 3,
    'nav_fixed_top': True,

    'nav_fixed': False,
    'nav_width': '900px',

    'content_fixed': False,
    'content_width': '900px',

    'row_fixed': False,
    'noresponsive': False,
    'noflatdesign': False,

    'googlewebfont': False,
    'googlewebfont_url': 'http://fonts.googleapis.com/css?family=Lily+Script+One',
    'googlewebfont_style': u"font-family: 'Lily Script One' cursive;",

    'header_inverse': False,
    'relbar_inverse': False,

    'inner_theme': False,
    'inner_theme_name': 'bootswatch-flatly',

    'bootstrap_version': '3',
    'quick_preview': True,

    # 'h1_size': '3.0em',
    # 'h2_size': '2.6em',
    # 'h3_size': '2.2em',
    # 'h4_size': '1.8em',
    # 'h5_size': '1.4em',
    # 'h6_size': '1.1em',
}


#Add RTD Template Path.
if 'templates_path' in globals():
    templates_path.insert(0, '/home/docs/checkouts/readthedocs.org/readthedocs/templates/sphinx')
else:
    templates_path = ['/home/docs/checkouts/readthedocs.org/readthedocs/templates/sphinx', 'templates', '_templates',
                      '.templates']

# Add RTD Static Path. Add to the end because it overwrites previous files.
if 'html_static_path' in globals():
    html_static_path.append('/home/docs/checkouts/readthedocs.org/readthedocs/templates/sphinx/_static')
else:
    html_static_path = ['_static', '/home/docs/checkouts/readthedocs.org/readthedocs/templates/sphinx/_static']

# Add RTD Theme Path. 
if 'html_theme_path' in globals():
    html_theme_path.append('/home/docs/checkouts/readthedocs.org/readthedocs/templates/sphinx')
else:
    html_theme_path = ['_themes', '/home/docs/checkouts/readthedocs.org/readthedocs/templates/sphinx']

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

if globals().get('source_suffix', False):
    SUFFIX = source_suffix
else:
    SUFFIX = '.rst'

#Add project information to the template context.
context = {
    'using_theme': using_rtd_theme,
    'html_theme': html_theme,
    'current_version': "latest",
    'MEDIA_URL': "https://media.readthedocs.org/",
    'PRODUCTION_DOMAIN': "readthedocs.org",
    'versions': [
    ("latest", "/en/latest/"),
    ],
    'downloads': [ 
    ("PDF", "https://readthedocs.org/projects/sphinxjpthemesbasicstrap/downloads/pdf/latest/"),
    ("HTML", "https://readthedocs.org/projects/sphinxjpthemesbasicstrap/downloads/htmlzip/latest/"),
    ("Epub", "https://readthedocs.org/projects/sphinxjpthemesbasicstrap/downloads/epub/latest/"),
    ],
    'slug': 'sphinxjpthemesbasicstrap',
    'name': u'sphinxjp.themes.basicstrap',
    'rtd_language': u'en',
    'canonical_url': '',
    'analytics_code': '',
    'single_version': False,
    'conf_py_path': '/docs/',
    'api_host': 'https://readthedocs.org',
    'github_user': 'tell-k',
    'github_repo': 'sphinxjp.themes.basicstrap',
    'github_version': 'master',
    'display_github': True,
    'bitbucket_user': 'None',
    'bitbucket_repo': 'None',
    'bitbucket_version': 'master',
    'display_bitbucket': False,
    'READTHEDOCS': True,
    'using_theme': (html_theme == "default"),
    'new_theme': (html_theme == "sphinx_rtd_theme"),
    'source_suffix': SUFFIX,
    'user_analytics_code': '',
    'global_analytics_code': 'UA-17997319-1',
    'commit': 'ae900262762f9935398648f290c1e7d386ad3edc',
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