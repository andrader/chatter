from xml.etree import ElementTree

import requests

from chatter.utils import TreeNode


class Sitemap(TreeNode):
    pass


def get_sitemap(url) -> Sitemap:
    """Get the sitemap from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Parse the XML
        root = ElementTree.fromstring(response.content)

        # Extract all URLs from the sitemap
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [loc.text for loc in root.findall(".//ns:loc", namespace)]

        # Create a Sitemap object
        sitemap = Sitemap(url)

        for loc in urls:
            # Add each URL to the sitemap
            sitemap.add_child(loc, TreeNode(loc))

        return sitemap

    except Exception as e:
        raise e
