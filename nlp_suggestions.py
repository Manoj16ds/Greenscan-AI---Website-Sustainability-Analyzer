from bs4 import BeautifulSoup

def nlp_based_suggestions(html_text):
    suggestions = []
    if not html_text:
        return suggestions

    soup = BeautifulSoup(html_text, "html.parser")
    body_text = soup.get_text().lower()

    if "news" in body_text or "article" in body_text:
        suggestions.append("Enable caching for recurring visitors to news content.")
    if "actor" in body_text or "filmography" in body_text or "biography" in body_text:
        suggestions.append("Optimize photo galleries and media-heavy sections.")
    if "religion" in body_text or "temple" in body_text or "culture" in body_text:
        suggestions.append("Use semantic headings for better readability in long text-heavy sections.")
    if ".gov" in str(soup) or "government" in body_text:
        suggestions.append("Ensure compliance with WCAG accessibility guidelines.")
    if "shop" in body_text or "product" in body_text or "cart" in body_text:
        suggestions.append("Compress product images and use CDN for faster e-commerce delivery.")

    return suggestions
