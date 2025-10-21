from typing import List, Optional


def format_mdn_feature_title(path: List[str]) -> str:
    title: Optional[str] = None
    if path[0] == "api":
        if len(path) == 2:
            title = f"{path[1]} API"
    elif path[0] == "css":
        if len(path) == 3:
            if path[1] == "at-rules":
                title = f"CSS at-rule: {path[2]}"
            elif path[1] == "properties":
                title = f"CSS Property: {path[2]}"
            elif path[1] == "selectors":
                title = f"CSS Selector: {path[2]}"
            elif path[1] == "types":
                title = f"CSS Data Type: {path[2]}"
        elif len(path) == 4 and path[1] == "properties":
            title = f"CSS Property: {path[2]}:{path[3]}"
    elif path[0] == "html":
        if len(path) in [3, 4]:
            if path[1] == "manifest":
                title = f"Web App Manifest Property: {path[2]}"
            elif path[1] == "global_attributes":
                title = f"Global HTML Attribute: {path[2]}"
            elif path[1] == "elements":
                if path[2] != "input":
                    title = f"HTML Element: {path[2]}"
                else:
                    title = f"HTML Element: {path[3]}"
    elif path[0] == "http":
        if len(path) == 3:
            if path[1] == "methods":
                title = f"HTTP Method: {path[2]}"
            elif path[1] == "status":
                title = f"HTTP Status: {path[2]}"
            elif path[1] == "headers":
                title = f"HTTP Header: {path[2]}"
    elif path[0] == "javascript":
        title = f"Javascript {path[-1]}"
    elif path[0] == "manifests":
        if len(path) == 3:
            title = f"PWA Manifest: {path[2]}"
        elif len(path) == 4:
            title = f"PWA Manifest: {path[2]}:{path[3]}"
    elif path[0] == "mathml":
        if len(path) == 3:
            if path[1] == "elements":
                title = f"MathML Element: {path[2]}"
    elif path[0] == "svg":
        if len(path) in [3, 4]:
            if path[1] == "elements":
                if len(path) == 3:
                    title = f"SVG Element: {path[2]}"
                else:
                    title = f"SVG Element: {path[2]}:{path[3]}"
            elif path[1] == "global_attributes":
                if len(path) == 3:
                    title = f"SVG Attribute: {path[2]}"
                else:
                    title = f"SVG Attribute: {path[2]}:{path[3]}"
    elif path[0] == "webextensions":
        if len(path) in [3, 4]:
            if path[1] == "manifest":
                if len(path) == 3:
                    title = f"WebExtension Manifest Property: {path[2]}"
            elif path[1] == "api":
                if len(path) == 3:
                    title = f"WebExtensions API: {path[2]}"
                else:
                    title = f"WebExtensions API: {path[2]}.{path[3]}"
    if not title:
        title = " ".join(path)
    return title
