""" Accordion dropdown for Sphinx, with HTML builder """

import json
import posixpath
import os
from docutils import nodes
from docutils.parsers.rst import Directive
from pkg_resources import resource_filename
from pygments.lexers import get_all_lexers
from sphinx.util.osutil import copyfile
from sphinx.util import logging


FILES = [
    'semantic-ui-2.4.2/accordion.css',
    'semantic-ui-2.4.2/accordion.js',
    'accordion.css',
    'accordion.js',
]


LEXER_MAP = {}
for lexer in get_all_lexers():
    for short_name in lexer[1]:
        LEXER_MAP[short_name] = lexer[0]


def get_compatible_builders(app):
    builders = [
        'html',
        'singlehtml',
        'dirhtml',
        'readthedocs',
        'readthedocsdirhtml',
        'readthedocssinglehtml',
        'readthedocssinglehtmllocalmedia',
        'spelling'
    ]
    builders.extend(app.config['sphinx_tabs_valid_builders'])
    return builders


class AccordionDirective(Directive):
    """ Top-level accordion directive """

    has_content = True

    def run(self):
        """ Parse an accordion directive """
        self.assert_has_content()
        env = self.state.document.settings.env

        node = nodes.container()
        node['classes'] = ['sphinx-accordion', 'ui', 'styled', 'fluid', 'accordion']

        if 'next_accordion_id' not in env.temp_data:
            env.temp_data['next_accordion_id'] = 0
        if 'accordion_stack' not in env.temp_data:
            env.temp_data['accordion_stack'] = []

        accordion_id = env.temp_data['next_accordion_id']
        accordion_key = 'accordion_%d' % accordion_id
        env.temp_data['next_accordion_id'] += 1
        env.temp_data['accordion_stack'].append(accordion_id)

        env.temp_data[accordion_key] = {}
        env.temp_data[accordion_key]['row_ids'] = []
        env.temp_data[accordion_key]['row_titles'] = []
        env.temp_data[accordion_key]['is_first_row'] = True

        self.state.nested_parse(self.content, self.content_offset, node)

        if env.app.builder.name in get_compatible_builders(env.app):
            title_nodes = []
            row_ids = env.temp_data[accordion_key]['row_ids']
            row_titles = env.temp_data[accordion_key]['row_titles']
            for idx, [data_row, row_name] in enumerate(row_titles):
                title_node = nodes.container()
                title_node.tagname = 'div'
                title_node['classes'] = ['sphinx-accordion', 'title']
                title_node['classes'].append(f'sphinx-accordion-title-{accordion_id}-{row_ids[idx]}')
                title_node += row_name.children
                icon_node = nodes.inline()
                icon_node.tagname = 'i'
                icon_node['classes'] = ['dropdown', 'icon']
                # Access the first child, we don't want the container that somehow gets generated
                title_node.children.insert(0, icon_node)
                title_nodes.append(title_node)

            node.children = [child for pair in zip(title_nodes, node.children) for child in pair]

        env.temp_data['accordion_stack'].pop()
        return [node]


class AccordionRowDirective(Directive):
    """ AccordionRow directive, for adding a row to an accordion """

    has_content = True

    def run(self):
        """ Parse a row directive """
        self.assert_has_content()
        env = self.state.document.settings.env

        accordion_id = env.temp_data['accordion_stack'][-1]
        accordion_key = 'accordion_%d' % accordion_id

        args = self.content[0].strip()
        if args.startswith('{'):
            try:
                args = json.loads(args)
                self.content.trim_start(1)
            except ValueError:
                args = {}
        else:
            args = {}

        row_name = nodes.container()
        self.state.nested_parse(self.content[:1], self.content_offset, row_name)
        args['row_name'] = row_name

        include_accordion_id_in_data_row = False
        if 'row_id' not in args:
            args['row_id'] = env.new_serialno(accordion_key)
            include_accordion_id_in_data_row = True
        i = 1
        while args['row_id'] in env.temp_data[accordion_key]['row_ids']:
            args['row_id'] = '%s-%d' % (args['row_id'], i)
            i += 1
        env.temp_data[accordion_key]['row_ids'].append(args['row_id'])

        data_row = str(args['row_id'])
        if include_accordion_id_in_data_row:
            data_row = '%d-%s' % (accordion_id, data_row)
        data_row = "sphinx-accordion-content-{}".format(data_row)

        env.temp_data[accordion_key]['row_titles'].append(
            (data_row, args['row_name'])
        )

        text = '\n'.join(self.content)
        node = nodes.container(text)
        classes = 'sphinx-accordion content'
        node['classes'] = classes.split(' ')
        node['classes'].extend(args.get('classes', []))
        node['classes'].append(data_row)

        self.state.nested_parse(self.content[2:], self.content_offset, node)

        if env.app.builder.name not in get_compatible_builders(env.app):
            outer_node = nodes.container()
            row = nodes.container()
            row.tagname = 'a'
            row['classes'] = ['item']
            row += row_name
            outer_node.append(row)
            outer_node.append(node)
            return [outer_node]

        return [node]


class _FindAccordionDirectiveVisitor(nodes.NodeVisitor):
    """ Visitor pattern than looks for a sphinx accordion directive in a document """
    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self._found = False

    def unknown_visit(self, node):
        if not self._found and isinstance(node, nodes.container) and 'classes' in node and isinstance(node['classes'], list):
            self._found = 'sphinx-accordion' in node['classes']

    @property
    def found_accordion_directive(self):
        """ Return whether a sphinx accordion directive was found """
        return self._found


def update_context(app, pagename, templatename, context, doctree):
    """ Remove sphinx-accordion CSS and JS asset files if not used in a page """
    if doctree is None:
        return
    visitor = _FindAccordionDirectiveVisitor(doctree)
    doctree.walk(visitor)
    if not visitor.found_accordion_directive:
        paths = [posixpath.join('_static', 'sphinx_accordion/' + f) for f in FILES]
        if 'css_files' in context:
            context['css_files'] = context['css_files'][:]
            for path in paths:
                if path.endswith('.css') and path in context['css_files']:
                    context['css_files'].remove(path)
        if 'script_files' in context:
            context['script_files'] = context['script_files'][:]
            for path in paths:
                if path.endswith('.js') and path in context['script_files']:
                    context['script_files'].remove(path)


def copy_assets(app, exception):
    """ Copy asset files to the output """
    if 'getLogger' in dir(logging):
        log = logging.getLogger(__name__).info
        warn = logging.getLogger(__name__).warning
    else:
        log = app.info
        warn = app.warning
    builders = get_compatible_builders(app)
    if exception:
        return
    if app.builder.name not in builders:
        if not app.config['sphinx_accordion_nowarn']:
            warn(
                'Not copying accordion assets! Not compatible with %s builder' %
                app.builder.name)
        return

    log('Copying accordion assets')

    installdir = os.path.join(app.builder.outdir, '_static', 'sphinx_accordion')

    for path in FILES:
        source = resource_filename('sphinx_accordion', path)
        dest = os.path.join(installdir, path)
        destdir = os.path.dirname(dest)
        if not os.path.exists(destdir):
            os.makedirs(destdir)

        copyfile(source, dest)


def setup(app):
    """ Set up the plugin """
    app.add_config_value('sphinx_accordion_nowarn', False, '')
    app.add_config_value('sphinx_accordion_valid_builders', [], '')
    app.add_directive('accordion', AccordionDirective)
    app.add_directive('accordion-row', AccordionRowDirective)

    for path in ['sphinx_accordion/' + f for f in FILES]:
        if path.endswith('.css'):
            if 'add_css_file' in dir(app):
                app.add_css_file(path)
            else:
                app.add_stylesheet(path)
        if path.endswith('.js'):
            if 'add_script_file' in dir(app):
                app.add_script_file(path)
            else:
                app.add_javascript(path)

    app.connect('html-page-context', update_context)
    app.connect('build-finished', copy_assets)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
