from typing import List, Optional


def format_mdn_feature_title(path: List[str]) -> str:
    title: Optional[str] = None
    if path[0] == "api":
        if len(path) == 2:
            title = f"{path[1]} API"
        else:
            title = f"{path[1]} API: {' '.join(path[2:])}"
    elif path[0] == "css":
        if len(path) == 3:
            if path[1] == "at-rules":
                title = f"CSS at-rule: @{path[2]}"
            elif path[1] == "properties":
                title = f"CSS Property: {path[2]}"
            elif path[1] == "selectors":
                title = f"CSS Selector: :{path[2]}"
            elif path[1] == "types":
                title = f"CSS Data Type: {path[2]}"
        else:
            if path[1] == "at-rules":
                title = f"CSS at-rule: @{' '.join(path[2:])}"
            if path[1] == "properties":
                title = f"CSS Property: {path[2]}:{' '.join(path[3:])}"
            elif path[1] == "selectors":
                title = f"CSS Selector: :{' '.join(path[2:])}"
            elif path[1] == "types":
                title = f"CSS Data Type: {' '.join(path[2:])}"
    elif path[0] == "html":
        if path[1] == "manifest":
            title = f"Web App Manifest Property: {path[2]}"
        elif path[1] == "global_attributes":
            title = f"Global HTML Attribute: {path[2]}"
        elif path[1] == "elements":
            if len(path) == 3:
                title = f"HTML Element: {path[2]}"
            elif len(path) > 3:
                title = f"HTML Element: {path[2]}:{' '.join(path[3:])}"
    elif path[0] == "http":
        if path[1] == "methods":
            title = f"HTTP Method: {' '.join(path[2:])}"
        elif path[1] == "status":
            title = f"HTTP Status: {' '.join(path[2:])}"
        elif path[1] == "headers":
            title = f"HTTP Header: {' '.join(path[2:])}"
    elif path[0] == "javascript":
        title = f"Javascript {path[1]}: {' '.join(path[2:])}"
    elif path[0] == "manifests":
        if len(path) == 3:
            title = f"PWA Manifest: {path[2]}"
        elif len(path) == 4:
            title = f"PWA Manifest: {path[2]}:{path[3]}"
    elif path[0] == "mathml":
        if path[1] == "elements":
            title = f"MathML Element: {' '.join(path[2:])}"
    elif path[0] == "svg":
        if path[1] == "elements":
            if len(path) == 3:
                title = f"SVG Element: {path[2]}"
            else:
                title = f"SVG Element: {path[2]}:{' '.join(path[3:])}"
        elif path[1] == "global_attributes":
            if len(path) == 3:
                title = f"SVG Attribute: {path[2]}"
            else:
                title = f"SVG Attribute: {path[2]}:{' '.join(path[3:])}"
    elif path[0] == "webextensions":
        if path[1] == "manifest":
            title = f"WebExtension Manifest Property: {' '.join(path[2:])}"
        elif path[1] == "api":
            if len(path) == 3:
                title = f"WebExtensions API: {path[2]}"
            else:
                title = f"WebExtensions API: {path[2]}.{' '.join(path[3:])}"
        elif path[1] == "match_patterns":
            title = f"WebExtensions Match patterns: {' '.join(path[2:])}"
    if not title:
        title = " ".join(path)
    return title
