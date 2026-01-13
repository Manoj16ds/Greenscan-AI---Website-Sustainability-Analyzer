# main.py

import os
import requests
from accessibility import is_website_accessible
from crawler import extract_internal_links, extract_image_urls
from carbon_calculator import estimate_carbon
from classifier import classify_images
from suggestions import generate_suggestions
from utils.downloader import download_images
from report_generator import generate_pdf_report
from visualizer import plot_image_classification, plot_carbon_vs_size, plot_emission_comparison
from optimizer import simulate_optimization


def get_page_size(image_paths):
    return round(sum(os.path.getsize(p) for p in image_paths) / 1024, 2)  # KB


def print_report(url, pages_scanned, total_images, page_size, carbon,
                 classification, suggestions_by_page, optimized_size, optimized_carbon):
    print("\n" + "=" * 60)
    print("🌐 GREENSCAN AI - WEBSITE SUSTAINABILITY REPORT")
    print("=" * 60)
    print(f"🔗 Website URL             : {url}")
    print(f"📄 Pages Scanned           : {pages_scanned}")
    print(f"🖼  Images Found            : {total_images}")
    print(f"💾 Page Size (Original)    : {page_size} KB")
    print(f"♻  CO2 Emissions (Original): {carbon} kg/month")
    print(f"✅ Page Size (Optimized)   : {optimized_size} KB")
    print(f"✅ CO2 Emissions (Optimized): {optimized_carbon} kg/month")
    print(f"🧠 Image Classification    : {len(classification['essential'])} essential, "
          f"{len(classification['decorative'])} decorative\n")

    print("🛠  Page-wise Suggested Improvements:\n")
    for page_url, suggestions in suggestions_by_page.items():
        print(f"📄 {page_url}")
        for s in suggestions:
            print(f"   🔹 {s}")
        print()
    print("=" * 60)


# ✅ Function version for Streamlit
def run_greenscan(base_url):
    """
    Executes full GreenScan pipeline for a given URL and returns summary results.
    """

    results_summary = {}

    print("\n🔍 GreenScan AI - Multi-page Eco Analyzer\n")
    print(f"[+] Checking accessibility for {base_url}...")

    if not is_website_accessible(base_url):
        print("[-] Website is not accessible. Exiting.")
        results_summary["error"] = "Website is not accessible."
        return results_summary

    # Crawl internal links
    print("[+] Crawling internal pages...")
    internal_links = extract_internal_links(base_url, max_links=4)
    if base_url not in internal_links:
        internal_links.insert(0, base_url)
    print(f"[✓] Found {len(internal_links)} pages to scan.")

    total_images = 0
    total_size_kb = 0
    total_carbon = 0
    classification_all = {"essential": [], "decorative": []}
    suggestions_by_page = {}

    for i, url in enumerate(internal_links):
        print(f"\n🔄 Scanning page {i + 1}/{len(internal_links)}: {url}")
        image_urls = extract_image_urls(url)
        image_paths = download_images(image_urls)

        if not image_paths:
            print("[-] No images downloaded. Skipping this page.")
            continue

        page_size_kb = get_page_size(image_paths)
        carbon = estimate_carbon(page_size_kb)
        classification = classify_images(image_paths)

        try:
            html_text = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).text
        except Exception:
            html_text = ""

        suggestions = generate_suggestions(
            classification,
            html_text=html_text,
            page_size_kb=page_size_kb,
            image_urls=image_urls
        )

        optimized_size_kb = simulate_optimization(page_size_kb, len(image_paths))
        optimized_carbon = estimate_carbon(optimized_size_kb)

        # Aggregate totals
        total_images += len(image_paths)
        total_size_kb += page_size_kb
        total_carbon += carbon
        classification_all["essential"].extend(classification["essential"])
        classification_all["decorative"].extend(classification["decorative"])
        suggestions_by_page[url] = suggestions

    if total_images == 0:
        print("\n🚫 No downloadable images found across pages.")
        results_summary["error"] = "No downloadable images found."
        return results_summary

    optimized_total_size = simulate_optimization(total_size_kb, total_images)
    optimized_total_carbon = estimate_carbon(optimized_total_size)

    # Print and generate report
    print_report(
        base_url,
        len(internal_links),
        total_images,
        total_size_kb,
        total_carbon,
        classification_all,
        suggestions_by_page,
        optimized_total_size,
        optimized_total_carbon
    )

    try:
        generate_pdf_report(
            "greenscan_report.pdf",
            base_url,
            total_images,
            total_size_kb,
            total_carbon,
            classification_all,
            suggestions_by_page,
            optimized_total_size,
            optimized_total_carbon,
            len(internal_links)
        )
        print("\n📄 PDF report generated: greenscan_report.pdf")
    except Exception as e:
        print(f"[!] PDF report generation failed: {e}")

    try:
        if classification_all["essential"] or classification_all["decorative"]:
            plot_image_classification(classification_all)
        plot_carbon_vs_size(total_size_kb, total_carbon)
        plot_emission_comparison(total_carbon, optimized_total_carbon)
        print("📊 Charts saved successfully.")
    except Exception as e:
        print(f"[!] Chart generation failed: {e}")

    # ✅ Return results for Streamlit interface
    results_summary = {
        "url": base_url,
        "pages_scanned": len(internal_links),
        "images_found": total_images,
        "page_size_original": round(total_size_kb, 2),
        "carbon_original": round(total_carbon, 2),
        "page_size_optimized": round(optimized_total_size, 2),
        "carbon_optimized": round(optimized_total_carbon, 2),
        "essential_images": len(classification_all["essential"]),
        "decorative_images": len(classification_all["decorative"]),
        "report_file": "greenscan_report.pdf"
    }

    return results_summary


# Keep terminal mode functional
if __name__ == "__main__":
    base_url = input("Enter website URL: ").strip()
    run_greenscan(base_url)
