import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def render_template(template_name, context):
    """Renders an email template with the provided context."""
    # Path to the templates directory (e.g., data/templates)
    template_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'templates')
    template_dir = os.path.abspath(template_dir)

    env = Environment(loader=FileSystemLoader(template_dir))

    try:
        template = env.get_template(template_name)
    except TemplateNotFound:
        raise FileNotFoundError(f"Template '{template_name}' not found in {template_dir}")
    
    return template.render(context)

if __name__ == "__main__":
    # Example usage for testing
    context = {"name": "Facu"}
    try:
        rendered_email = render_template("welcome_email.html", context)
        print("✅ Rendered template:\n")
        print(rendered_email)
    except Exception as e:
        print(f"❌ Error rendering template: {str(e)}")