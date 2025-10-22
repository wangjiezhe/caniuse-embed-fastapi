from typing import List


def format_mdn_feature_title(path: List[str]) -> str:
    match path:
        case ["api"]:
            title = "API"
        case ["api", name]:
            title = f"{name} API"
        case ["api", name, *rest]:
            title = f"{name} API: {' '.join(rest)}"

        case ["css", category, name]:
            match category:
                case "at-rules":
                    title = f"CSS at-rule: @{name}"
                case "properties":
                    title = f"CSS Property: {name}"
                case "selectors":
                    title = f"CSS Selector: :{name}"
                case "types":
                    title = f"CSS Data Type: {name}"
        case ["css", category, *rest]:
            match category:
                case "at-rules":
                    title = f"CSS at-rule: @{' '.join(rest)}"
                case "properties" if rest:
                    title = f"CSS Property: {rest[0]}:{' '.join(rest[1:])}"
                case "selectors":
                    title = f"CSS Selector: :{' '.join(rest)}"
                case "types":
                    title = f"CSS Data Type: {' '.join(rest)}"

        case ["html", "global_attributes", name]:
            title = f"Global HTML Attribute: {name}"
        case ["html", "global_attributes", name, *rest]:
            title = f"Global HTML Attribute: {name}:{' '.join(rest)}"
        case ["html", "elements", name]:
            title = f"HTML Element: {name}"
        case ["html", "elements", name, *rest]:
            title = f"HTML Element: {name}:{' '.join(rest)}"

        case ["http", category, *rest]:
            match category:
                case "methods":
                    title = f"HTTP Method: {' '.join(rest)}"
                case "status":
                    title = f"HTTP Status: {' '.join(rest)}"
                case "headers":
                    title = f"HTTP Header: {' '.join(rest)}"

        case ["javascript", category, *rest]:
            title = f"Javascript {category}: {' '.join(rest)}"

        case ["manifests", "webapp", name]:
            title = f"Web App Manifest: {name}"
        case ["manifests", "webapp", name, *rest]:
            title = f"Web App Manifest: {name}:{' '.join(rest)}"

        case ["mathml", "elements", *rest]:
            title = f"MathML Element: {' '.join(rest)}"

        case ["svg", "elements", name]:
            title = f"SVG Element: {name}"
        case ["svg", "elements", name, *rest]:
            title = f"SVG Element: {name}:{' '.join(rest)}"
        case ["svg", "global_attributes", name]:
            title = f"SVG Attribute: {name}"
        case ["svg", "global_attributes", name, *rest]:
            title = f"SVG Attribute: {name}:{' '.join(rest)}"

        case ["webextensions", category, *rest]:
            match category:
                case "manifest":
                    title = f"WebExtension Manifest Property: {' '.join(rest)}"
                case "api" if not rest:
                    title = "WebExtensions API"
                case "api" if len(rest) == 1:
                    title = f"WebExtensions API: {rest[0]}"
                case "api" if len(rest) > 1:
                    title = f"WebExtensions API: {rest[0]}.{' '.join(rest[1:])}"
                case "match_patterns":
                    title = f"WebExtensions Match patterns: {' '.join(rest)}"

        case _:
            title = " ".join(path)
    return title
