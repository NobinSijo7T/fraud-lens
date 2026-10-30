"""
URL Feature Extractor Service
Extracts 22 features from a raw URL for phishing detection.
"""
import re
import math
from urllib.parse import urlparse
from collections import Counter


TRUSTED_DOMAINS = {
    'github.com', 'gitlab.com', 'google.com', 'microsoft.com', 'apple.com',
    'amazon.com', 'wikipedia.org', 'linkedin.com', 'paypal.com', 'adobe.com',
    'openai.com', 'youtube.com', 'facebook.com', 'instagram.com', 'reddit.com',
    'stackoverflow.com', 'dropbox.com'
}


def is_trusted_domain(url: str) -> bool:
    """Return true only for an exact trusted domain or its subdomains."""
    hostname = (urlparse(url).hostname or '').lower().strip('.')
    return any(hostname == domain or hostname.endswith('.' + domain) for domain in TRUSTED_DOMAINS)


def extract_features(url: str) -> dict:
    """
    Extract all 22 features from a URL string.
    
    Args:
        url: Raw URL string (e.g., "https://www.example.com/path?query=1")
    
    Returns:
        Dictionary with all 22 features required by the phishing model
    """
    # Parse the URL
    parsed = urlparse(url)
    
    # Basic metrics
    url_len = len(url)
    
    # Domain analysis
    # Keep inference features consistent with the dataset's URL parser:
    # remove credentials/ports and ignore the conventional www subdomain.
    domain = (parsed.hostname or parsed.path.split('/')[0]).lower().strip('.')
    if domain.startswith('www.'):
        domain = domain[4:]
    dom_len = len(domain)
    
    # Check if domain is an IP address
    ip_pattern = re.compile(r'^(?:\d{1,3}\.){3}\d{1,3}$')
    is_ip = 1 if ip_pattern.match(domain) else 0
    
    # TLD analysis
    tld = ''
    if '.' in domain:
        parts = domain.split('.')
        # The training data treats common two-level public suffixes as the
        # TLD (for example edu.au and co.uk), otherwise it uses the final label.
        compound_suffixes = {
            'ac.uk', 'co.uk', 'gov.uk', 'org.uk',
            'com.au', 'edu.au', 'gov.au', 'org.au',
            'co.nz', 'com.br', 'co.in', 'com.cn'
        }
        candidate = '.'.join(parts[-2:])
        tld = candidate if candidate in compound_suffixes else parts[-1]
    tld_len = len(tld)
    
    # Subdomain count
    if not is_ip and '.' in domain:
        domain_parts = domain.split('.')
        subdom_cnt = max(0, len(domain_parts) - 2)  # Exclude domain and TLD
    else:
        subdom_cnt = 0
    
    # Character composition
    letter_cnt = sum(1 for c in url if c.isalpha())
    digit_cnt = sum(1 for c in url if c.isdigit())
    special_cnt = sum(1 for c in url if not c.isalnum())
    
    # Ratios
    letter_ratio = letter_cnt / url_len if url_len > 0 else 0
    digit_ratio = digit_cnt / url_len if url_len > 0 else 0
    spec_ratio = special_cnt / url_len if url_len > 0 else 0
    
    # Special character counts
    eq_cnt = url.count('=')
    qm_cnt = url.count('?')
    amp_cnt = url.count('&')
    dot_cnt = url.count('.')
    dash_cnt = url.count('-')
    under_cnt = url.count('_')
    slash_cnt = url.count('/')
    
    # Security indicators
    is_https = 1 if parsed.scheme == 'https' else 0
    
    # Shannon entropy (measure of randomness)
    def calculate_entropy(s: str) -> float:
        if not s:
            return 0.0
        counter = Counter(s)
        length = len(s)
        entropy = 0.0
        for count in counter.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
        return entropy
    
    entropy = calculate_entropy(url)
    
    # Path and query analysis
    path = parsed.path or ''
    path_len = len(path) if path != '/' else 1
    
    query = parsed.query or ''
    query_len = len(query)
    
    return {
        'url_len': url_len,
        'dom_len': dom_len,
        'is_ip': is_ip,
        'tld_len': tld_len,
        'subdom_cnt': subdom_cnt,
        'letter_cnt': letter_cnt,
        'digit_cnt': digit_cnt,
        'special_cnt': special_cnt,
        'eq_cnt': eq_cnt,
        'qm_cnt': qm_cnt,
        'amp_cnt': amp_cnt,
        'dot_cnt': dot_cnt,
        'dash_cnt': dash_cnt,
        'under_cnt': under_cnt,
        'letter_ratio': round(letter_ratio, 6),
        'digit_ratio': round(digit_ratio, 6),
        'spec_ratio': round(spec_ratio, 6),
        'is_https': is_https,
        'slash_cnt': slash_cnt,
        'entropy': round(entropy, 6),
        'path_len': path_len,
        'query_len': query_len
    }


def extract_and_predict(url: str):
    """
    Extract features from URL and prepare for prediction.
    
    Args:
        url: Raw URL string
    
    Returns:
        Dictionary with extracted features
    """
    return extract_features(url)
