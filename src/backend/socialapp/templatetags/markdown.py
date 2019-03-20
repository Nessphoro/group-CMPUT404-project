from django import template
import markdown
import bleach
from bs4 import BeautifulSoup
from ..models import Post
from django.conf import settings

localsite = settings.SITE_URL + "/Post/"

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
    for image in images:
        image["class"] = "ui fluid round image"
        try:
            if image["src"].startswith(localsite):
                # Reference to a local image
                preId = image["src"][len(localsite):]
                if preId[-1] == "/":
                    preId = preId[0:-1]
                
                
                postReference = Post.objects.filter(id=preId)
                if not postReference:
                    continue
                
                post = postReference[0]

                
                if post.contentType.startswith("image"):
                    image["src"] = f"data:{post.contentType},{post.content}"
        except Exception as e:
            print(e)

    return soup.prettify()
    