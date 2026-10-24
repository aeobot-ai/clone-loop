from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def with_utm(url: str, medium: str, campaign: str, content: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query))
    query.update(utm_source="iboss", utm_medium=medium, utm_campaign=campaign, utm_content=content)
    return urlunsplit(parts._replace(query=urlencode(query)))
