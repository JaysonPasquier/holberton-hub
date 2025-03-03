# Define skill categories and their display names
SKILL_CATEGORIES = [
    {
        'id': 'programming_languages',
        'name': 'Programming Languages',
        'icon': 'fas fa-code',
        'start': 'ABAP',
        'end': 'ZIG'
    },
    {
        'id': 'web_frameworks',
        'name': 'Web Frameworks & Libraries',
        'icon': 'fas fa-server',
        'start': 'ASPNET',
        'end': 'ZEND'
    },
    {
        'id': 'frontend',
        'name': 'Frontend Frameworks & Libraries',
        'icon': 'fas fa-desktop',
        'start': 'ALPINE',
        'end': 'ZUSTAND'
    },
    {
        'id': 'backend',
        'name': 'Backend & Infrastructure',
        'icon': 'fas fa-cogs',
        'start': 'ANSIBLE',
        'end': 'TRAEFIK'
    },
    {
        'id': 'cloud',
        'name': 'Cloud Platforms & Services',
        'icon': 'fas fa-cloud',
        'start': 'APP_ENGINE',
        'end': 'VERCEL'
    },
    {
        'id': 'databases',
        'name': 'Databases',
        'icon': 'fas fa-database',
        'start': 'APPWRITE',
        'end': 'TIMESCALE'
    },
    {
        'id': 'vcs',
        'name': 'Version Control',
        'icon': 'fab fa-git-alt',
        'start': 'BITBUCKET',
        'end': 'TFS'
    },
    {
        'id': 'testing',
        'name': 'Testing',
        'icon': 'fas fa-vial',
        'start': 'CHAI',
        'end': 'WEBDRIVERIO'
    },
    {
        'id': 'mobile',
        'name': 'Mobile Development',
        'icon': 'fas fa-mobile-alt',
        'start': 'ANDROID',
        'end': 'XAMARIN'
    },
    {
        'id': 'cms',
        'name': 'CMS & eCommerce',
        'icon': 'fas fa-shopping-cart',
        'start': 'BIGCOMMERCE',
        'end': 'WORDPRESS'
    },
    {
        'id': 'design',
        'name': 'Design & UI/UX',
        'icon': 'fas fa-paint-brush',
        'start': 'ADOBE',
        'end': 'ZEPLIN'
    },
    {
        'id': 'devops',
        'name': 'DevOps & Tools',
        'icon': 'fas fa-tools',
        'start': 'ASANA',
        'end': 'YARN'
    },
    {
        'id': 'data_science',
        'name': 'Data Science & AI',
        'icon': 'fas fa-brain',
        'start': 'APACHE_AIRFLOW',
        'end': 'TENSORFLOW'
    },
    {
        'id': 'api',
        'name': 'API & Communication',
        'icon': 'fas fa-exchange-alt',
        'start': 'AMQP',
        'end': 'ZEROMQ'
    },
    {
        'id': 'other',
        'name': 'Other',
        'icon': 'fas fa-layer-group',
        'start': 'AGILE',
        'end': 'WEBGL'
    },
]

def get_skill_category(skill_code):
    """Get the category information for a given skill code"""
    current_category = None

    for category in SKILL_CATEGORIES:
        # Check if this skill is in this category's range
        if skill_code >= category['start'] and skill_code <= category['end']:
            return category

    return {
        'id': 'uncategorized',
        'name': 'Uncategorized',
        'icon': 'fas fa-question'
    }

def get_skills_by_category():
    """Group skills by their categories"""
    from users.skills_constants import SKILL_CHOICES

    result = {}
    current_category = None

    for skill_code, skill_name in SKILL_CHOICES:
        category = get_skill_category(skill_code)
        category_id = category['id']

        if category_id not in result:
            result[category_id] = {
                'name': category['name'],
                'icon': category['icon'],
                'skills': []
            }

        result[category_id]['skills'].append((skill_code, skill_name))

    return result
