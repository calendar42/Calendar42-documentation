import sys, os

sys.path.append(os.path.abspath('_themes'))


extensions = [
    'sphinx.ext.ifconfig',
    'sphinx.ext.todo',
    'sphinx.ext.intersphinx',
    'sphinx.ext.doctest',
]

templates_path = ['_templates']

source_suffix = '.md'

master_doc = 'index'

exclude_patterns = ['_build']

pygments_style = 'flask_theme_support.FlaskyStyle'


html_theme = 'kr'

html_theme_path = ['_themes']

html_title = 'Calendar42 Documentation'

html_static_path = ['_static']

html_sidebars = {
    'index':    ['sidebarintro.html', 'sourcelink.html', 'searchbox.html'],
    '**':       ['sidebarlogo.html', 'localtoc.html', 'relations.html',
                 'sourcelink.html', 'searchbox.html']
}

html_show_sourcelink = True

html_show_sphinx = False

htmlhelp_basename = 'c42docs'



todo_include_todos = True

