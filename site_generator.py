import json
import os
import markdown

from jinja2 import Environment
from jinja2 import FileSystemLoader
from os.path import join
from os.path import normpath


def ensure_folder_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_articles_config_json(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding="UTF-8") as file_handler:
        return json.load(file_handler)


def get_site_templates():
    templates_folder = "templates"
    index_page_template_name = "index_page_template.html"
    article_page_template_name = "article_page_template.html"
    environment = Environment(loader=FileSystemLoader(templates_folder), autoescape=True)
    index_page_template = environment.get_template(index_page_template_name)
    article_page_template = environment.get_template(article_page_template_name)
    return index_page_template, article_page_template


def save_rendered_html(html_output_filepath, html):
    with open(html_output_filepath, "w", encoding="utf8") as file_handler:
        file_handler.write(html)


def form_path_to_html_file(markdown_path):
    articles_folder = "articles/"
    return normpath(join(articles_folder, markdown_path.replace('.md', '.html')))


def create_index_page_from_html_template(index_page_template, config):
    rendered_index_page_filepath = "site/index.html"
    index_page_template.globals['form_article_path'] = form_path_to_html_file
    rendered_index_page = index_page_template.render(config)
    save_rendered_html(rendered_index_page_filepath, rendered_index_page)


def get_article_markdown(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding="UTF-8") as file_handler:
        return file_handler.read()


def render_article_markdown_to_html_template(template, article_markdown, article_info):
    link_to_index_page = "../../index.html"
    article_info_data = article_info
    article_html = markdown.markdown(article_markdown, extensions=['codehilite', 'fenced_code'])
    article_info_data.update({'html': article_html, 'link': link_to_index_page})
    return template.render(article_info_data)


def create_articles_from_html_template(article_page_template, config):
    articles_info_from_config = config["articles"]
    markdown_articles_folder = "./articles/"
    html_articles_folder = "./site/articles/"
    ensure_folder_exists(html_articles_folder)
    for article_info in articles_info_from_config:
        article_source = article_info["source"]
        article_source_html = article_source.replace("md", "html")
        html_output_filepath = normpath(join(html_articles_folder, article_source_html))
        article_topic_folder = os.path.split(html_output_filepath)[0]
        ensure_folder_exists(article_topic_folder)
        article_markdown_filepath = normpath(join(markdown_articles_folder, article_source))
        article_markdown = get_article_markdown(article_markdown_filepath)
        article_html = render_article_markdown_to_html_template(article_page_template,
                                                                article_markdown, article_info)
        save_rendered_html(html_output_filepath, article_html)


if __name__ == "__main__":
    site_folder = "site"
    ensure_folder_exists(site_folder)
    articles_config_json_filepath = "config.json"
    config = get_articles_config_json(articles_config_json_filepath)
    index_page_template, article_page_template = get_site_templates()
    create_index_page_from_html_template(index_page_template, config)
    create_articles_from_html_template(article_page_template, config)
    print("Site was successfully generated in \"{}\" folder.".format(site_folder))
