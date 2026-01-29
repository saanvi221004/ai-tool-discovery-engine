from app import app, db, AITool
import json

def init_database():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if data already exists
        if AITool.query.first():
            print("Database already contains data. Skipping initialization.")
            return
        
        # Sample AI tools data
        tools_data = [
            {
                'name': 'ChatGPT',
                'description': 'A powerful AI language model for text generation, coding assistance, and problem-solving.',
                'category': 'Text Generation',
                'target_roles': ['Developer', 'Writer', 'Marketer', 'Student', 'Researcher'],
                'skill_level': 'beginner',
                'use_cases': ['Content creation', 'Code generation', 'Research assistance', 'Learning'],
                'pain_points': ['Writer\'s block', 'Complex coding problems', 'Research time', 'Content ideas'],
                'pricing_model': 'Freemium',
                'official_url': 'https://chat.openai.com',
                'features': ['Text generation', 'Code assistance', 'Multiple languages', 'Conversation memory'],
                'rating': 4.8
            },
            {
                'name': 'GitHub Copilot',
                'description': 'AI-powered code completion tool that helps developers write code faster and more accurately.',
                'category': 'Code Assistance',
                'target_roles': ['Developer', 'Software Engineer', 'Full Stack Developer'],
                'skill_level': 'intermediate',
                'use_cases': ['Code completion', 'Function generation', 'Bug fixing', 'Code refactoring'],
                'pain_points': ['Slow coding', 'Syntax errors', 'Code duplication', 'Learning new APIs'],
                'pricing_model': 'Subscription',
                'official_url': 'https://github.com/features/copilot',
                'features': ['Real-time suggestions', 'Multi-language support', 'IDE integration', 'Context awareness'],
                'rating': 4.6
            },
            {
                'name': 'Midjourney',
                'description': 'AI image generation tool that creates stunning visuals from text descriptions.',
                'category': 'Image Generation',
                'target_roles': ['Designer', 'Artist', 'Marketer', 'Content Creator'],
                'skill_level': 'beginner',
                'use_cases': ['Art creation', 'Marketing visuals', 'Concept design', 'Social media content'],
                'pain_points': ['Design skills gap', 'Stock photo costs', 'Creative blocks', 'Time-consuming design'],
                'pricing_model': 'Subscription',
                'official_url': 'https://www.midjourney.com',
                'features': ['High-quality images', 'Various art styles', 'Image editing', 'Batch generation'],
                'rating': 4.7
            },
            {
                'name': 'Notion AI',
                'description': 'AI-powered workspace assistant for writing, planning, and organizing information.',
                'category': 'Productivity',
                'target_roles': ['Project Manager', 'Writer', 'Student', 'Business Analyst'],
                'skill_level': 'beginner',
                'use_cases': ['Document creation', 'Project planning', 'Note-taking', 'Task management'],
                'pain_points': ['Disorganized information', 'Writer\'s block', 'Poor planning', 'Information overload'],
                'pricing_model': 'Freemium',
                'official_url': 'https://www.notion.so/product/ai',
                'features': ['Text generation', 'Summarization', 'Task automation', 'Template creation'],
                'rating': 4.5
            },
            {
                'name': 'Jasper AI',
                'description': 'AI content platform for marketing copy, blog posts, and creative writing.',
                'category': 'Content Marketing',
                'target_roles': ['Marketer', 'Content Creator', 'Copywriter', 'SEO Specialist'],
                'skill_level': 'intermediate',
                'use_cases': ['Marketing copy', 'Blog writing', 'Social media posts', 'Email campaigns'],
                'pain_points': ['Content creation time', 'Writer\'s block', 'SEO optimization', 'Brand consistency'],
                'pricing_model': 'Subscription',
                'official_url': 'https://www.jasper.ai',
                'features': ['Brand voice', 'SEO optimization', 'Multiple templates', 'Plagiarism checker'],
                'rating': 4.4
            },
            {
                'name': 'Replit AI',
                'description': 'AI-powered coding assistant integrated into an online development environment.',
                'category': 'Code Assistance',
                'target_roles': ['Developer', 'Student', 'Beginner Programmer'],
                'skill_level': 'beginner',
                'use_cases': ['Code completion', 'Debugging', 'Learning to code', 'Project collaboration'],
                'pain_points': ['Setup complexity', 'Learning curve', 'Debugging time', 'Environment issues'],
                'pricing_model': 'Freemium',
                'official_url': 'https://replit.com/site/ai',
                'features': ['Online IDE', 'AI code completion', 'Collaboration', 'Multiple languages'],
                'rating': 4.3
            },
            {
                'name': 'Canva Magic Design',
                'description': 'AI-powered design tool that creates professional graphics and templates.',
                'category': 'Design',
                'target_roles': ['Designer', 'Marketer', 'Social Media Manager', 'Small Business Owner'],
                'skill_level': 'beginner',
                'use_cases': ['Social media graphics', 'Presentations', 'Marketing materials', 'Brand design'],
                'pain_points': ['Design complexity', 'Time consumption', 'Brand consistency', 'Professional look'],
                'pricing_model': 'Freemium',
                'official_url': 'https://www.canva.com/magic-design/',
                'features': ['Template generation', 'Brand kit', 'Image editing', 'Collaboration'],
                'rating': 4.6
            },
            {
                'name': 'Grammarly',
                'description': 'AI writing assistant for grammar checking, style improvement, and clarity.',
                'category': 'Writing Assistant',
                'target_roles': ['Writer', 'Student', 'Professional', 'Content Creator'],
                'skill_level': 'beginner',
                'use_cases': ['Grammar checking', 'Style improvement', 'Clarity enhancement', 'Plagiarism detection'],
                'pain_points': ['Grammar errors', 'Writing clarity', 'Professional tone', 'Proofreading time'],
                'pricing_model': 'Freemium',
                'official_url': 'https://www.grammarly.com',
                'features': ['Real-time checking', 'Style suggestions', 'Tone detection', 'Plagiarism checker'],
                'rating': 4.5
            },
            {
                'name': 'Perplexity AI',
                'description': 'AI-powered search engine that provides accurate, cited answers to questions.',
                'category': 'Research',
                'target_roles': ['Researcher', 'Student', 'Analyst', 'Journalist'],
                'skill_level': 'intermediate',
                'use_cases': ['Research queries', 'Fact-checking', 'Information synthesis', 'Source verification'],
                'pain_points': ['Information overload', 'Source reliability', 'Research time', 'Fact verification'],
                'pricing_model': 'Freemium',
                'official_url': 'https://www.perplexity.ai',
                'features': ['Cited sources', 'Real-time information', 'Conversation mode', 'File analysis'],
                'rating': 4.4
            },
            {
                'name': 'Runway ML',
                'description': 'AI platform for video editing, generation, and creative media production.',
                'category': 'Video Generation',
                'target_roles': ['Video Creator', 'Filmmaker', 'Marketer', 'Content Creator'],
                'skill_level': 'advanced',
                'use_cases': ['Video generation', 'Video editing', 'Special effects', 'Motion graphics'],
                'pain_points': ['Video editing complexity', 'High production costs', 'Time-consuming editing', 'Technical skills'],
                'pricing_model': 'Subscription',
                'official_url': 'https://runwayml.com',
                'features': ['Text-to-video', 'Video editing', 'AI effects', 'Green screen removal'],
                'rating': 4.2
            }
        ]
        
        # Add tools to database
        for tool_data in tools_data:
            tool = AITool(
                name=tool_data['name'],
                description=tool_data['description'],
                category=tool_data['category'],
                target_roles=json.dumps(tool_data['target_roles']),
                skill_level=tool_data['skill_level'],
                use_cases=json.dumps(tool_data['use_cases']),
                pain_points=json.dumps(tool_data['pain_points']),
                pricing_model=tool_data['pricing_model'],
                official_url=tool_data['official_url'],
                features=json.dumps(tool_data['features']),
                rating=tool_data['rating']
            )
            db.session.add(tool)
        
        db.session.commit()
        print(f"Database initialized with {len(tools_data)} AI tools.")

if __name__ == '__main__':
    init_database()
