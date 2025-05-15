"""
    test_kroki
    ~~~~~~~~~~~~~~~~
    Test the kroki extension.
"""

import re
import pytest
import responses
import requests
from sphinx.application import Sphinx
from sphinx.testing.path import path


def get_content(app: Sphinx) -> str:
    app.builder.build_all()

    index = app.outdir / "index.html"
    return index.read_text() if "read_text" in path.__dict__ else index.text()


@pytest.mark.sphinx(
    "html", testroot="kroki", confoverrides={"master_doc": "index"}
)
def test_kroki_html(app, status, warning):
    content = get_content(app)
    html = (
        r'figure[^>]*?(?:kroki kroki-plantuml align-default)?" .*?>\s*'
        r'<img alt="bar -&gt; baz" class="kroki kroki-plantuml" .+?/>.*?'
        r'<span class="caption-text">caption of diagram</span>.*?</p>'
    )
    assert re.search(html, content, re.S)

    html = r'<p>Hello <img alt="bar -&gt; baz" class="kroki kroki-plantuml" .*?/> kroki world</p>'
    assert re.search(html, content, re.S)

    html = r'<img .+?class="kroki kroki-mermaid graph" .+?/>'
    assert re.search(html, content, re.S)

    html = r'<img .+?class="kroki kroki-graphviz" .*?/>'
    assert re.search(html, content, re.S)

    html = (
        r'figure[^>]*?kroki kroki-plantuml align-center" .*?>\s*?'
        r'<img alt="foo -&gt; bar ".*?/>.*?'
        r'<span class="caption-text">on <em>center</em></span>'
    )
    assert re.search(html, content, re.S)

    html = r'<img.*?class="kroki kroki-ditaa align-right".*?/>'
    assert re.search(html, content, re.S)


@pytest.mark.sphinx(
    "html", 
    testroot="kroki", 
    confoverrides={
        "master_doc": "index",
        "kroki_use_placeholder_on_request_error": True
    }
)
@responses.activate
def test_kroki_placeholder_on_error(app, status, warning):
    # Mock a request exception
    responses.add(
        responses.POST, 
        re.compile(r'https://kroki\.io.*'), 
        body=requests.RequestException("Connection error")
    )
    
    # Build should complete without raising an exception
    content = get_content(app)
    
    # All images should be rendered with the placeholder
    assert "kroki kroki-plantuml" in content
    assert "kroki kroki-mermaid" in content
    assert "kroki kroki-graphviz" in content
    
    # Verify warning messages are logged
    assert "Connection error" in warning.getvalue()
