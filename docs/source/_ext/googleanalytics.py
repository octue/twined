from sphinx.errors import ExtensionError


def add_ga_javascript(app, pagename, templatename, context, doctree):
    if app.config.googleanalytics_enabled:
        id = app.config.googleanalytics_id
        metatags = context.get('metatags', '')
        metatags += "<!-- Global site tag (gtag.js) - Google Analytics -->\n"
        metatags += f'<script async src="https://www.googletagmanager.com/gtag/js?id={id}"></script>\n'
        metatags += "<script>\n"
        metatags += "  window.dataLayer = window.dataLayer || [];\n"
        metatags += "  function gtag(){dataLayer.push(arguments);}\n"
        metatags += "  gtag('js', new Date());\n"
        metatags += f"  gtag('config', '{id}');\n"
        metatags += "</script>\n"
        context['metatags'] = metatags


def check_config(app):
    if not app.config.googleanalytics_id:
        raise ExtensionError("'googleanalytics_id' config value must be set for ga statistics to function properly.")


def setup(app):
    app.add_config_value('googleanalytics_id', '', 'html')
    app.add_config_value('googleanalytics_enabled', True, 'html')
    app.connect('html-page-context', add_ga_javascript)
    app.connect('builder-inited', check_config)
    return {'version': '0.1'}
