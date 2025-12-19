import os
from bs4 import BeautifulSoup
import requests
import time

# --- CONFIGURATION ---
# We check the local website folder directly
SITE_FOLDER = "../website"
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; CyberSentinel_Bot/1.0)'
}

def check_external_link(url):
    """Pings an external URL to see if it's alive."""
    try:
        r = requests.head(url, headers=headers, timeout=5)
        return r.status_code
    except requests.RequestException:
        return 0 # Connection failed

def audit_file(file_path):
    print(f"\n Auditing: {os.path.basename(file_path)}")
    issues = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        
        # 1. Check Title Tag
        title = soup.find("title")
        if not title:
            issues.append(" Missing <title> tag")
        elif len(title.get_text()) > 60:
            issues.append("⚠️ Title tag too long (>60 chars)")
            
        # 2. Check Meta Description
        desc = soup.find("meta", attrs={"name": "description"})
        if not desc:
            # Note: We intentionally didn't add one to index.html yet to test this!
            issues.append("Missing Meta Description (Critical for Click-Through Rate)")
        
        # 3. Check Links
        links = soup.find_all("a")
        print(f"   Found {len(links)} links. Checking validity...")
        
        for link in links:
            href = link.get("href")
            if not href or href.startswith("#"):
                continue
            
            if href.startswith("http"):
                # External Link
                status = check_external_link(href)
                if status == 200:
                    print(f"   [OK] {href}")
                elif status == 404:
                    issues.append(f"🔴 Broken External Link (404): {href}")
                else:
                    issues.append(f"🟠 Suspicious Link Status ({status}): {href}")
            else:
                # Internal Link - check if file exists
                # simple logic: assume relative path
                target_path = os.path.join(os.path.dirname(file_path), href)
                if not os.path.exists(target_path):
                     issues.append(f"🔴 Broken Internal Link: {href}")

    return issues

def run_audit():
    print("--- 🩺 Auto-Growth SEO Doctor Started ---")
    
    report_card = {}
    
    # Walk through the website folder finding HTML files
    for root, dirs, files in os.walk(SITE_FOLDER):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                issues = audit_file(full_path)
                if issues:
                    report_card[file] = issues
                else:
                    print("   ✅ No issues found!")

    print("\n" + "="*40)
    print(" FINAL AUDIT REPORT")
    print("="*40)
    
    if not report_card:
        print(" Perfect Score! No SEO issues detected.")
    else:
        for file, errors in report_card.items():
            print(f"\n {file}:")
            for err in errors:
                print(f"   {err}")
    
    print("\n" + "="*40)

if __name__ == "__main__":
    run_audit()