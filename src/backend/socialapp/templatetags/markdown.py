from django import template
import markdown
import bleach
from bs4 import BeautifulSoup

register = template.Library()

allowed = bleach.sanitizer.ALLOWED_TAGS + ["p", "h1", "h2", "h3", "img"]
attrs = {**bleach.sanitizer.ALLOWED_ATTRIBUTES, "img": ["src", "alt"]}

@register.filter(name='markdown')
def md(value):
    text = markdown.markdown(value)
    print(text)
    html = bleach.clean(text, tags=allowed, attributes=attrs)
    
    soup = BeautifulSoup(html, "html.parser")

    images = soup.find_all("img")
    print(images)
    return html
    