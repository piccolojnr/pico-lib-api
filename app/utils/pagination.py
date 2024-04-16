from flask import url_for


# Function to generate pagination navigation links
def _pagination_nav_links(pagination, endpoint, **kwargs):
    # Initialize a dictionary to store navigation links
    nav_links = {}

    # Extract pagination information
    per_page = pagination["items_per_page"]
    this_page = pagination["page"]
    last_page = pagination["total_pages"]

    # Generate links for self, first, previous, next, and last pages
    nav_links["self"] = url_for(
        f"api.{endpoint}", **kwargs, page=this_page, per_page=per_page
    )
    nav_links["first"] = url_for(f"api.{endpoint}", **kwargs, page=1, per_page=per_page)
    if pagination["has_prev"]:
        nav_links["prev"] = url_for(
            f"api.{endpoint}", **kwargs, page=this_page - 1, per_page=per_page
        )
    if pagination["has_next"]:
        nav_links["next"] = url_for(
            f"api.{endpoint}", **kwargs, page=this_page + 1, per_page=per_page
        )
    nav_links["last"] = url_for(
        f"api.{endpoint}", **kwargs, page=last_page, per_page=per_page
    )
    return nav_links


# Function to generate pagination navigation links for HTTP header
def _pagination_nav_header_links(pagination, endpoint, **kwargs):
    # Get navigation links dictionary
    url_dict = _pagination_nav_links(pagination, endpoint, **kwargs)

    # Initialize a string to store HTTP header links
    link_header = ""

    # Construct link header from navigation links
    for rel, url in url_dict.items():
        link_header += f"<{url}>; rel={rel}"

    # Strip extra spaces and commas from the link header and return
    return link_header.strip().strip(",")
