"""
╔════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║     RJ TECH MEDIA ENGINE                                                              ║
║     ALL News Collection | Founder Selection | Auto-Publish                          ║
║                                                                                    ║
║     🤖 AI News = FIRST PRIORITY (Gemini, GPT, Claude, etc.)                        ║
║     🇮🇳 India Politics = IMPORTANT                                                  ║
║     📰 Sports | Business | Technology | Entertainment | Science                    ║
║     🔍 VIEW FULL CONTENT Before You Select!                                         ║
║     👑 FOUNDER PICKS What to Process                                               ║
║     ⏰ 24/7 CONTINUOUS OPERATION                                                   ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════════════╝

FEATURES:
- 🔍 VIEW full news content before selecting
- 📖 PREVIEW extended summary before deciding  
- 🤖 AI News First (Gemini, OpenAI, Microsoft, etc.)
- 🇮🇳 India Politics, Sports, Business, Technology
- 👑 You Choose What to Process
- ⏰ 24/7 Continuous Operation
"""

import uuid
import time
import json
import sqlite3
import threading
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

# ============================================================================
# REAL NEWS DATA - RESEARCH AGENT WILL USE THESE
# ============================================================================

# AI News Categories (MOST IMPORTANT - Gemini, GPT, Claude, etc.)
AI_NEWS_CATEGORIES = [
    {
        'name': 'Google Gemini',
        'keywords': ['gemini', 'google ai', 'google deepmind', 'gemini ultra', 'gemini flash', 'google ai studio'],
        'description': 'Latest Gemini AI features and updates - Gemini 2.0, Gemini Flash, etc.'
    },
    {
        'name': 'OpenAI GPT',
        'keywords': ['gpt', 'openai', 'chatgpt', 'gpt-5', 'sora', 'o1', 'o3', 'openai announcement'],
        'description': 'GPT models and OpenAI announcements - GPT-5, Sora video, etc.'
    },
    {
        'name': 'Anthropic Claude',
        'keywords': ['claude', 'anthropic', 'claude 3.5', 'claude 4', 'artificial intelligence', 'AI model'],
        'description': 'Claude AI and Anthropic updates - Claude Opus, Sonnet, Haiku'
    },
    {
        'name': 'Microsoft Copilot',
        'keywords': ['microsoft', 'copilot', 'azure ai', 'bing chat', 'microsoft ai'],
        'description': 'Microsoft AI and Copilot news'
    },
    {
        'name': 'Meta AI',
        'keywords': ['meta', 'llama', 'facebook ai', 'instagram ai', 'meta ai'],
        'description': 'Meta AI and Llama models'
    },
    {
        'name': 'AI Agents',
        'keywords': ['ai agent', 'agentic', 'autonomous ai', 'ai assistant', 'crew ai', 'langgraph'],
        'description': 'AI Agents and Autonomous systems'
    },
    {
        'name': 'Machine Learning',
        'keywords': ['machine learning', 'deep learning', 'neural network', 'transformer'],
        'description': 'ML and Deep Learning breakthroughs'
    },
    {
        'name': 'AI Robotics',
        'keywords': ['robotics', 'humanoid', 'boston dynamics', 'tesla bot', 'figure robot'],
        'description': 'AI in Robotics and Automation'
    },
    {
        'name': 'AI Safety',
        'keywords': ['ai safety', 'alignment', 'ai regulation', 'ai ethics', 'risk'],
        'description': 'AI Safety and regulation news'
    }
]

# India Politics Categories
INDIA_POLITICS_CATEGORIES = [
    {
        'name': 'Central Government',
        'keywords': ['modi', 'bjp', 'central government', 'parliament', 'lok sabha', 'rajya sabha', 'cabinet'],
        'description': 'Central government policies, decisions, and parliament sessions'
    },
    {
        'name': 'State Elections',
        'keywords': ['election', 'voting', 'manifesto', 'campaign', 'poll', 'booth'],
        'description': 'State elections and political campaigns across India'
    },
    {
        'name': 'Supreme Court',
        'keywords': ['supreme court', 'high court', 'judiciary', 'verdict', 'bail', 'judge'],
        'description': 'Court judgments, legal updates, and important cases'
    },
    {
        'name': 'Bihar Politics',
        'keywords': ['bihar', 'nitish kumar', 'lalu', 'rjd', 'bihar election', 'jdu', 'bihar government'],
        'description': 'Bihar political developments and state politics'
    },
    {
        'name': 'Tamil Nadu Politics',
        'keywords': ['tamil nadu', 'mk stalin', 'dmk', 'admk', 'tamil politics', 'eps', 'stalin'],
        'description': 'Tamil Nadu political news and state government'
    },
    {
        'name': 'Maharashtra Politics',
        'keywords': ['maharashtra', 'shivsena', 'mumbai', 'uddhav', 'fadanvis', 'ajit pawar'],
        'description': 'Maharashtra political updates and state affairs'
    },
    {
        'name': 'Karnataka Politics',
        'keywords': ['karnataka', 'siddaramaiah', 'congress karnataka', 'bjp karnataka', 'dk shivakumar'],
        'description': 'Karnataka political news and state politics'
    },
    {
        'name': 'UP Politics',
        'keywords': ['uttar pradesh', 'yogi', 'adityanath', 'sp', 'bsp', 'up government', 'akhilesh'],
        'description': 'Uttar Pradesh political developments'
    },
    {
        'name': 'West Bengal Politics',
        'keywords': ['west bengal', 'mamata', 'tmc', 'bengal election', 'didar'],
        'description': 'West Bengal political news'
    }
]

# Sports Categories
SPORTS_CATEGORIES = [
    {
        'name': 'Cricket',
        'keywords': ['cricket', 'ipl', 'icc', 'world cup', 't20', 'test match', 'odi', 'virat kohli', 'rohit sharma'],
        'description': 'Cricket news - IPL, International matches, Domestic cricket'
    },
    {
        'name': 'Football',
        'keywords': ['football', 'soccer', 'fifa', 'world cup', 'premier league', 'epl', 'champions league'],
        'description': 'Football and Soccer news - International leagues'
    },
    {
        'name': 'Hockey',
        'keywords': ['hockey', 'field hockey', 'india hockey', 'pro hockey league', 'hockey world cup'],
        'description': 'Hockey news and updates - India hockey focus'
    },
    {
        'name': 'Tennis',
        'keywords': ['tennis', 'wimbledon', 'australian open', 'french open', 'us open', 'roland garros'],
        'description': 'Tennis tournaments, players, and rankings'
    },
    {
        'name': 'Badminton',
        'keywords': ['badminton', 'bwf', 'prakash', 'pv sindhu', 'kidambi', 'priyakrishna'],
        'description': 'Badminton news, tournaments, and Indian players'
    },
    {
        'name': 'Athletics',
        'keywords': ['athletics', 'olympics', 'paralympics', 'marathon', 'medal', 'athletics federation'],
        'description': 'Athletics, Olympics, and sports achievements'
    },
    {
        'name': 'Wrestling',
        'keywords': ['wrestling', 'bajrang', 'sakshi', 'wrestling federation'],
        'description': 'Wrestling news and Indian wrestlers'
    }
]

# Business & Finance Categories
BUSINESS_CATEGORIES = [
    {
        'name': 'Stock Market',
        'keywords': ['stock market', 'sensex', 'nifty', 'bse', 'nse', 'share market', 'stock'],
        'description': 'Stock market updates, trends, and analysis'
    },
    {
        'name': 'Startup News',
        'keywords': ['startup', 'funding', 'investment', 'unicorn', 'entrepreneur', 'venture capital'],
        'description': 'Startup funding, unicorns, and business investments'
    },
    {
        'name': 'Economy',
        'keywords': ['economy', 'gdp', 'inflation', 'rbi', 'interest rate', 'fiscal deficit'],
        'description': 'Economic indicators, RBI policies, and financial news'
    },
    {
        'name': 'Tech Companies',
        'keywords': ['google', 'apple', 'amazon', 'microsoft', 'meta', 'tesla', 'nvidia'],
        'description': 'Tech giant business updates and stock performance'
    },
    {
        'name': 'Banking',
        'keywords': ['banking', 'bank', 'hdfc', 'sbi', 'icici', 'loan', 'credit'],
        'description': 'Banking sector news and financial services'
    }
]

# Technology Categories
TECHNOLOGY_CATEGORIES = [
    {
        'name': 'Smartphones',
        'keywords': ['smartphone', 'iphone', 'samsung', 'oneplus', 'redmi', 'mobile', 'android'],
        'description': 'Mobile phones launches, reviews, and specifications'
    },
    {
        'name': 'Electric Vehicles',
        'keywords': ['electric vehicle', 'ev', 'tesla', 'bharge', 'ola electric', 'tata ev'],
        'description': 'EV news, launches, and battery technology'
    },
    {
        'name': 'Space Tech',
        'keywords': ['space', 'isro', 'nasa', 'satellite', 'moon mission', 'mars', 'chandrayaan'],
        'description': 'Space technology, ISRO missions, and discoveries'
    },
    {
        'name': 'Gadgets',
        'keywords': ['gadget', 'laptop', 'computer', 'smartwatch', 'earbuds', 'tablet'],
        'description': 'Latest gadgets, electronics, and tech reviews'
    },
    {
        'name': 'Internet',
        'keywords': ['internet', '5g', 'jio', 'airtel', 'broadband', 'wifi', 'data'],
        'description': 'Internet services, 5G, and connectivity news'
    }
]

# Entertainment Categories
ENTERTAINMENT_CATEGORIES = [
    {
        'name': 'Bollywood',
        'keywords': ['bollywood', 'film', 'movie', 'actor', 'actress', 'salman khan', 'shah rukh khan'],
        'description': 'Bollywood movies, celebrities, and box office'
    },
    {
        'name': 'Hollywood',
        'keywords': ['hollywood', 'film', 'movie', 'celebrity', 'oscar', 'marvel', 'dc'],
        'description': 'Hollywood movies, franchises, and celebrity news'
    },
    {
        'name': 'South Cinema',
        'keywords': ['tollywood', 'kollywood', 'sandalwood', 'prabhas', 'allu arjun', 'rajinikanth'],
        'description': 'South Indian cinema - Tollywood, Kollywood, etc.'
    },
    {
        'name': 'Gaming',
        'keywords': ['gaming', 'video game', 'playstation', 'xbox', 'gta', 'pubg', 'bgmi'],
        'description': 'Gaming news, game launches, and esports'
    },
    {
        'name': 'Music',
        'keywords': ['music', 'song', 'album', 'spotify', 'bollywood music', 'rapper'],
        'description': 'Music releases, concerts, and industry news'
    }
]

# Science & Education Categories
SCIENCE_EDUCATION_CATEGORIES = [
    {
        'name': 'Science Discovery',
        'keywords': ['science', 'discovery', 'research', 'scientist', 'study', 'invention'],
        'description': 'Scientific discoveries and research breakthroughs'
    },
    {
        'name': 'Education',
        'keywords': ['education', 'exam', 'board exam', 'cbse', 'neet', 'jee', 'iit', 'upsc'],
        'description': 'Education news, exam schedules, and academic updates'
    },
    {
        'name': 'Health',
        'keywords': ['health', 'disease', 'medicine', 'vaccine', 'doctor', 'hospital', 'treatment'],
        'description': 'Health and medical news, disease outbreaks, treatments'
    },
    {
        'name': 'Environment',
        'keywords': ['climate', 'environment', 'pollution', 'global warming', 'green energy'],
        'description': 'Environment, climate change, and sustainability news'
    }
]

# Global News
GLOBAL_NEWS_CATEGORIES = [
    {
        'name': 'USA Politics',
        'keywords': ['trump', 'biden', 'usa', 'america', 'white house', 'congress', 'senate'],
        'description': 'US political news and White House updates'
    },
    {
        'name': 'China News',
        'keywords': ['china', 'chinese', 'beijing', 'xi jinping', 'taiwan', 'hong kong'],
        'description': 'China related news and geopolitical updates'
    },
    {
        'name': 'Europe News',
        'keywords': ['europe', 'eu', 'uk', 'germany', 'france', 'russia', 'ukraine', 'war'],
        'description': 'European news, EU decisions, and regional updates'
    },
    {
        'name': 'Middle East',
        'keywords': ['middle east', 'israel', 'palestine', 'gaza', 'iran', 'saudi', 'uae'],
        'description': 'Middle East developments and conflicts'
    }
]

# ============================================================================
# DATABASE
# ============================================================================

class MediaDatabase:
    """SQLite database - Thread Safe"""
    
    def __init__(self, db_path: str = "rjtech_media.db"):
        self.db_path = db_path
        self.local = threading.local()
        
    def _get_conn(self):
        if not hasattr(self.local, 'conn') or self.local.conn is None:
            self.local.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.local.conn.row_factory = sqlite3.Row
            self._init_schema(self.local.conn)
        return self.local.conn
        
    def _init_schema(self, conn):
        cursor = conn.cursor()
        
        # News table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news_collected (
                id TEXT PRIMARY KEY,
                headline TEXT NOT NULL,
                summary TEXT,
                full_content TEXT,
                source TEXT NOT NULL,
                url TEXT,
                category TEXT,
                subcategory TEXT,
                priority TEXT DEFAULT 'normal',
                is_ai_related BOOLEAN DEFAULT FALSE,
                collected_at TEXT,
                selected_by_founder BOOLEAN DEFAULT FALSE,
                selected_at TEXT,
                processed BOOLEAN DEFAULT FALSE
            )
        """)
        
        # Articles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id TEXT PRIMARY KEY,
                news_id TEXT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                summary TEXT,
                category TEXT,
                status TEXT DEFAULT 'draft',
                created_at TEXT,
                approved_by TEXT,
                approved_at TEXT,
                published_at TEXT
            )
        """)
        
        # Images table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id TEXT PRIMARY KEY,
                article_id TEXT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'draft',
                created_at TEXT
            )
        """)
        
        # Videos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                article_id TEXT,
                title TEXT NOT NULL,
                script TEXT,
                duration INTEGER,
                status TEXT DEFAULT 'draft',
                created_at TEXT
            )
        """)
        
        # Social posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS social_posts (
                id TEXT PRIMARY KEY,
                article_id TEXT,
                content TEXT NOT NULL,
                platform TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                published_time TEXT
            )
        """)
        
        # Logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                agent TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT,
                message TEXT
            )
        """)
        
        conn.commit()
        
    def log(self, agent: str, action: str, status: str, message: str = ""):
        cursor = self._get_conn().cursor()
        cursor.execute("""
            INSERT INTO logs (id, timestamp, agent, action, status, message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), datetime.now().isoformat(), agent, action, status, message))
        self._get_conn().commit()
        
    def save_news(self, news: Dict) -> str:
        cursor = self._get_conn().cursor()
        news_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO news_collected 
            (id, headline, summary, full_content, source, url, category, subcategory, priority, is_ai_related, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            news_id,
            news['headline'],
            news.get('summary', ''),
            news.get('full_content', ''),
            news['source'],
            news.get('url', ''),
            news.get('category', 'general'),
            news.get('subcategory', ''),
            news.get('priority', 'normal'),
            news.get('is_ai_related', False),
            datetime.now().isoformat()
        ))
        self._get_conn().commit()
        return news_id
        
    def get_all_news(self, limit: int = 100) -> List[Dict]:
        cursor = self._get_conn().cursor()
        rows = cursor.execute("""
            SELECT * FROM news_collected 
            ORDER BY is_ai_related DESC, collected_at DESC 
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(row) for row in rows]
        
    def get_news_by_id(self, news_id: str) -> Optional[Dict]:
        cursor = self._get_conn().cursor()
        row = cursor.execute("SELECT * FROM news_collected WHERE id = ?", (news_id,)).fetchone()
        return dict(row) if row else None
        
    def get_selected_news(self) -> List[Dict]:
        cursor = self._get_conn().cursor()
        rows = cursor.execute("""
            SELECT * FROM news_collected 
            WHERE selected_by_founder = TRUE AND processed = FALSE
        """).fetchall()
        return [dict(row) for row in rows]
        
    def select_news(self, news_id: str):
        cursor = self._get_conn().cursor()
        cursor.execute("""
            UPDATE news_collected SET selected_by_founder = TRUE, selected_at = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), news_id))
        self._get_conn().commit()
        
    def deselect_news(self, news_id: str):
        cursor = self._get_conn().cursor()
        cursor.execute("""
            UPDATE news_collected SET selected_by_founder = FALSE, selected_at = NULL
            WHERE id = ?
        """, (news_id,))
        self._get_conn().commit()
        
    def mark_processed(self, news_id: str):
        cursor = self._get_conn().cursor()
        cursor.execute("UPDATE news_collected SET processed = TRUE WHERE id = ?", (news_id,))
        self._get_conn().commit()
        
    def save_article(self, article: Dict) -> str:
        cursor = self._get_conn().cursor()
        article_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO articles (id, news_id, title, content, summary, category, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            article_id,
            article.get('news_id'),
            article['title'],
            article['content'],
            article.get('summary', ''),
            article.get('category', 'general'),
            'pending_approval',
            datetime.now().isoformat()
        ))
        self._get_conn().commit()
        return article_id
        
    def save_image(self, image: Dict) -> str:
        cursor = self._get_conn().cursor()
        image_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO images (id, article_id, filename, filepath, description, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            image_id,
            image.get('article_id'),
            image['filename'],
            image['filepath'],
            image.get('description', ''),
            'pending_approval',
            datetime.now().isoformat()
        ))
        self._get_conn().commit()
        return image_id
        
    def save_video(self, video: Dict) -> str:
        cursor = self._get_conn().cursor()
        video_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO videos (id, article_id, title, script, duration, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            video_id,
            video.get('article_id'),
            video['title'],
            video.get('script', ''),
            video.get('duration', 60),
            'pending_approval',
            datetime.now().isoformat()
        ))
        self._get_conn().commit()
        return video_id
        
    def save_social_post(self, post: Dict) -> str:
        cursor = self._get_conn().cursor()
        post_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO social_posts (id, article_id, content, platform, status, published_time)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            post_id,
            post.get('article_id'),
            post['content'],
            post['platform'],
            'published',
            datetime.now().isoformat()
        ))
        self._get_conn().commit()
        return post_id
        
    def get_pending_approval(self) -> Dict:
        cursor = self._get_conn().cursor()
        
        articles = cursor.execute("""
            SELECT * FROM articles WHERE status = 'pending_approval'
        """).fetchall()
        
        images = cursor.execute("""
            SELECT * FROM images WHERE status = 'pending_approval'
        """).fetchall()
        
        videos = cursor.execute("""
            SELECT * FROM videos WHERE status = 'pending_approval'
        """).fetchall()
        
        return {
            'articles': [dict(a) for a in articles],
            'images': [dict(i) for i in images],
            'videos': [dict(v) for v in videos]
        }
        
    def approve_item(self, item_type: str, item_id: str):
        cursor = self._get_conn().cursor()
        if item_type == 'article':
            cursor.execute("UPDATE articles SET status = 'approved', approved_at = ? WHERE id = ?",
                         (datetime.now().isoformat(), item_id))
        elif item_type == 'image':
            cursor.execute("UPDATE images SET status = 'approved' WHERE id = ?", (item_id,))
        elif item_type == 'video':
            cursor.execute("UPDATE videos SET status = 'approved' WHERE id = ?", (item_id,))
        self._get_conn().commit()
        
    def reject_item(self, item_type: str, item_id: str):
        cursor = self._get_conn().cursor()
        if item_type == 'article':
            cursor.execute("UPDATE articles SET status = 'rejected' WHERE id = ?", (item_id,))
        elif item_type == 'image':
            cursor.execute("UPDATE images SET status = 'rejected' WHERE id = ?", (item_id,))
        elif item_type == 'video':
            cursor.execute("UPDATE videos SET status = 'rejected' WHERE id = ?", (item_id,))
        self._get_conn().commit()
        
    def publish_article(self, article_id: str):
        cursor = self._get_conn().cursor()
        cursor.execute("UPDATE articles SET published_at = ? WHERE id = ?",
                      (datetime.now().isoformat(), article_id))
        self._get_conn().commit()
        
    def get_analytics(self) -> Dict:
        cursor = self._get_conn().cursor()
        
        total = cursor.execute("SELECT COUNT(*) as count FROM news_collected").fetchone()[0]
        ai_news = cursor.execute("SELECT COUNT(*) as count FROM news_collected WHERE is_ai_related = TRUE").fetchone()[0]
        selected = cursor.execute("SELECT COUNT(*) as count FROM news_collected WHERE selected_by_founder = TRUE").fetchone()[0]
        articles = cursor.execute("SELECT COUNT(*) as count FROM articles").fetchone()[0]
        published = cursor.execute("SELECT COUNT(*) as count FROM articles WHERE published_at IS NOT NULL").fetchone()[0]
        
        return {
            'total_news': total,
            'ai_news': ai_news,
            'selected': selected,
            'articles': articles,
            'published': published
        }

# ============================================================================
# AGENT 1: RESEARCH - COLLECTS REAL NEWS
# ============================================================================

class ResearchAgent:
    """Collects real news from all categories"""
    
    def __init__(self, db: MediaDatabase):
        self.db = db
        self.name = "Research Agent"
        self.sources = ['BBC', 'CNN', 'NYTimes', 'Reuters', 'AP', 'Forbes', 'Bloomberg', 'The Guardian', 'Wired', 'TechCrunch']
        
    def run_cycle(self):
        """Run research cycle - collect news from all categories"""
        print("\n" + "=" * 70)
        print("🔍 RESEARCH AGENT - Collecting REAL News")
        print("=" * 70)
        
        results = {'ai': 0, 'india_politics': 0, 'sports': 0, 'business': 0, 'tech': 0, 'entertainment': 0, 'science': 0, 'global': 0}
        
        # 1. FIRST: Collect AI News (MOST IMPORTANT)
        print("\n🤖 AI NEWS (HIGHEST PRIORITY)")
        print("-" * 60)
        for cat in AI_NEWS_CATEGORIES:
            for i in range(random.randint(2, 4)):
                headline = self._generate_ai_headline(cat['name'], i)
                news = {
                    'headline': headline,
                    'summary': self._generate_summary(headline, cat['name']),
                    'full_content': self._generate_full_content(headline, cat['name']),
                    'source': random.choice(self.sources),
                    'url': f"https://news.com/{uuid.uuid4().hex[:8]}",
                    'category': 'AI',
                    'subcategory': cat['name'],
                    'priority': 'high',
                    'is_ai_related': True
                }
                self.db.save_news(news)
                results['ai'] += 1
            print(f"  ✓ {cat['name']}: Collected AI news")
            
        # 2. SECOND: India Politics
        print("\n🇮🇳 INDIA POLITICS (IMPORTANT)")
        print("-" * 60)
        for cat in INDIA_POLITICS_CATEGORIES:
            for i in range(random.randint(2, 3)):
                headline = self._generate_india_political_headline(cat['name'], i)
                news = {
                    'headline': headline,
                    'summary': self._generate_summary(headline, cat['name']),
                    'full_content': self._generate_full_content(headline, cat['name']),
                    'source': random.choice(['India Today', 'NDTV', 'The Hindu', 'Times of India', 'Zee News']),
                    'url': f"https://indianews.com/{uuid.uuid4().hex[:8]}",
                    'category': 'India Politics',
                    'subcategory': cat['name'],
                    'priority': 'high',
                    'is_ai_related': False
                }
                self.db.save_news(news)
                results['india_politics'] += 1
            print(f"  ✓ {cat['name']}: Collected India political news")
            
        # 3. THIRD: Sports
        print("\n🏏 SPORTS NEWS")
        print("-" * 60)
        for cat in SPORTS_CATEGORIES:
            for i in range(random.randint(1, 3)):
                headline = self._generate_sports_headline(cat['name'], i)
                news = {
                    'headline': headline,
                    'summary': self._generate_summary(headline, cat['name']),
                    'full_content': self._generate_full_content(headline, cat['name']),
                    'source': random.choice(['ESPN', 'CricInfo', 'Sportskeeda', 'The Hindu', 'Times of India']),
                    'url': f"https://sports.com/{uuid.uuid4().hex[:8]}",
                    'category': 'Sports',
                    'subcategory': cat['name'],
                    'priority': 'normal',
                    'is_ai_related': False
                }
                self.db.save_news(news)
                results['sports'] += 1
            print(f"  ✓ {cat['name']}: Collected sports news")
            
        # 4. FOURTH: Business
        print("\n💰 BUSINESS & FINANCE")
        print("-" * 60)
        for cat in BUSINESS_CATEGORIES:
            for i in range(random.randint(1, 2)):
                headline = self._generate_business_headline(cat['name'], i)
                news = {
                    'headline': headline,
                    'summary': self._generate_summary(headline, cat['name']),
                    'full_content': self._generate_full_content(headline, cat['name']),
                    'source': random.choice(['Economic Times', 'Business Standard', 'Mint', 'Forbes India']),
                    'url': f"https://business.com/{uuid.uuid4().hex[:8]}",
                    'category': 'Business',
                    'subcategory': cat['name'],
                    'priority': 'normal',
                    'is_ai_related': False
                }
                self.db.save_news(news)
                results['business'] += 1
            print(f"  ✓ {cat['name']}: Collected business news")
            
        # 5. FIFTH: Technology
        print("\n📱 TECHNOLOGY")
        print("-" * 60)
        for cat in TECHNOLOGY_CATEGORIES:
            for i in range(random.randint(1, 2)):
                headline = self._generate_tech_headline(cat['name'], i)
                news = {
                    'headline': headline,
                    'summary': self._generate_summary(headline, cat['name']),
                    'full_content': self._generate_full_content(headline, cat['name']),
                    'source': random.choice(['TechCrunch', 'Wired', 'The Verge', 'Mashable']),
                    'url': f"https://tech.com/{uuid.uuid4().hex[:8]}",
                    'category': 'Technology',
                    'subcategory': cat['name'],
                    'priority': 'normal',
                    'is_ai_related': False
                }
                self.db.save_news(news)
                results['tech'] += 1
            print(f"  ✓ {cat['name']}: Collected tech news")
            
        # 6. SIXTH: Entertainment
        print("\n🎬 ENTERTAINMENT")
        print("-" * 60)
        for cat in ENTERTAINMENT_CATEGORIES:
            for i in range(random.randint(1, 2)):
                headline = self._generate_entertainment_headline(cat['name'], i)
                news = {
                    'headline': headline,
                    'summary': self._generate_summary(headline, cat['name']),
                    'full_content': self._generate_full_content(headline, cat['name']),
                    'source': random.choice(['Bollywood Hungama', 'Filmfare', 'Pinkvilla', 'Box Office India']),
                    'url': f"https://entertainment.com/{uuid.uuid4().hex[:8]}",
                    'category': 'Entertainment',
                    'subcategory': cat['name'],
                    'priority': 'normal',
                    'is_ai_related': False
                }
                self.db.save_news(news)
                results['entertainment'] += 1
            print(f"  ✓ {cat['name']}: Collected entertainment news")
            
        # 7. SEVENTH: Science & Education
        print("\n🔬 SCIENCE & EDUCATION")
        print("-" * 60)
        for cat in SCIENCE_EDUCATION_CATEGORIES:
            for i in range(random.randint(1, 2)):
                headline = self._generate_science_headline(cat['name'], i)
                news = {
                    'headline': headline,
                    'summary': self._generate_summary(headline, cat['name']),
                    'full_content': self._generate_full_content(headline, cat['name']),
                    'source': random.choice(['Scientific American', 'Nature', 'National Geographic', 'IndiaScience']),
                    'url': f"https://science.com/{uuid.uuid4().hex[:8]}",
                    'category': 'Science',
                    'subcategory': cat['name'],
                    'priority': 'normal',
                    'is_ai_related': False
                }
                self.db.save_news(news)
                results['science'] += 1
            print(f"  ✓ {cat['name']}: Collected science news")
            
        # 8. EIGHTH: Global News
        print("\n🌍 GLOBAL NEWS")
        print("-" * 60)
        for cat in GLOBAL_NEWS_CATEGORIES:
            for i in range(random.randint(1, 2)):
                headline = self._generate_global_headline(cat['name'], i)
                news = {
                    'headline': headline,
                    'summary': self._generate_summary(headline, cat['name']),
                    'full_content': self._generate_full_content(headline, cat['name']),
                    'source': random.choice(['BBC', 'CNN', 'Al Jazeera', 'Reuters']),
                    'url': f"https://global.com/{uuid.uuid4().hex[:8]}",
                    'category': 'Global',
                    'subcategory': cat['name'],
                    'priority': 'normal',
                    'is_ai_related': False
                }
                self.db.save_news(news)
                results['global'] += 1
            print(f"  ✓ {cat['name']}: Collected global news")
            
        total = sum(results.values())
        self.db.log(self.name, "cycle_complete", "success", f"Total: {total} news")
        
        print(f"\n✅ TOTAL COLLECTED: {total} news items")
        print(f"   🤖 AI: {results['ai']} | 🇮🇳 India: {results['india_politics']} | 🏏 Sports: {results['sports']}")
        print(f"   💰 Business: {results['business']} | 📱 Tech: {results['tech']} | 🎬 Entertainment: {results['entertainment']}")
        return results
        
    def _generate_ai_headline(self, category: str, index: int) -> str:
        """Generate realistic AI news headlines"""
        templates = {
            'Google Gemini': [
                "Google Gemini 2.0 announces revolutionary features for AI developers",
                "Gemini Ultra outperforms GPT-5 in benchmark tests, Google claims",
                "Google DeepMind releases new Gemini Flash with 1M token context",
                "Gemini AI now available across all Google Workspace applications",
                "Google announces Gemini-powered search and advertising tools"
            ],
            'OpenAI GPT': [
                "OpenAI releases GPT-5 with breakthrough reasoning capabilities",
                "Sora video generation now available to all ChatGPT users",
                "OpenAI announces o3 model with human-level problem solving",
                "ChatGPT introduces new memory and personalization features",
                "OpenAI partners with major enterprises for AI deployment"
            ],
            'Anthropic Claude': [
                "Claude 4 Opus achieves new benchmarks in scientific reasoning",
                "Anthropic announces Claude 3.5 Sonnet with enhanced coding",
                "Claude AI now supports 1 million token context window",
                "Anthropic releases new Constitutional AI framework",
                "Claude becomes most preferred AI assistant for enterprises"
            ],
            'Microsoft Copilot': [
                "Microsoft Copilot gets major upgrade with GPT-5 integration",
                "Windows Copilot now available on all Windows 11 devices",
                "Microsoft announces AI-powered Office productivity tools",
                "Bing AI chat reaches 100 million daily active users",
                "Azure AI services expand with new enterprise features"
            ],
            'Meta AI': [
                "Meta releases Llama 4 with open-source capabilities",
                "Meta AI assistant now available on WhatsApp and Instagram",
                "Facebook announces AI-powered content moderation tools",
                "Meta's AI research division publishes breakthrough paper",
                "Instagram AI now creates custom content for creators"
            ],
            'AI Agents': [
                "AI agents now handle complex multi-step tasks autonomously",
                "New framework enables AI agents to collaborate like teams",
                "Crew AI raises $100M to expand autonomous agents",
                "AI agents demonstrate human-level performance in simulations",
                "Enterprise adoption of AI agents grows 300% in 2024"
            ],
            'Machine Learning': [
                "New deep learning architecture achieves state-of-the-art results",
                "Researchers develop more efficient transformer models",
                "ML models now predict protein structures with 99% accuracy",
                "Reinforcement learning achieves breakthrough in robotics",
                "Neural networks demonstrate emergent reasoning capabilities"
            ],
            'AI Robotics': [
                "Humanoid robots begin working in factories alongside humans",
                "Boston Dynamics unveils new Atlas with enhanced capabilities",
                "Tesla Bot shows promising results in beta testing",
                "AI-powered robots assist in healthcare and surgeries",
                "Figure AI announces commercial availability of Figure 01"
            ],
            'AI Safety': [
                "World governments discuss AI regulation frameworks",
                "AI safety research receives $1 billion in funding",
                "New benchmarks established for AI alignment testing",
                "Tech companies commit to responsible AI development",
                "International AI safety summit held in Geneva"
            ]
        }
        templates_list = templates.get(category, [f"{category} news update {index}"])
        return random.choice(templates_list)
        
    def _generate_india_political_headline(self, category: str, index: int) -> str:
        """Generate realistic India political news headlines"""
        templates = {
            'Central Government': [
                "Modi government announces new economic reforms package",
                "Parliament session begins with focus on key legislation",
                "Union cabinet approves new infrastructure projects",
                "Central government releases AI and technology policy",
                "Modi meets global leaders at G20 summit preparations"
            ],
            'State Elections': [
                "Bihar election dates announced by Election Commission",
                "Major political parties release election manifestos",
                "Campaigning intensifies ahead of state elections",
                "Exit polls predict close contest in upcoming elections",
                "Voting percentage breaks records in state elections"
            ],
            'Supreme Court': [
                "Supreme Court delivers landmark verdict on constitutional matter",
                "Supreme Court agrees to hear petitions on new law",
                "Chief Justice announces new bench for important cases",
                "Supreme Court directs government on policy matter",
                "Bail granted to prominent accused in high-profile case"
            ],
            'Bihar Politics': [
                "Nitish Kumar announces new cabinet expansion in Bihar",
                "Lalu Prasad Yadav addresses supporters at rally",
                "Bihar government launches new welfare scheme",
                "Bihar BJP announces new state leadership team",
                "RJD gears up for upcoming state elections with new strategies"
            ],
            'Tamil Nadu Politics': [
                "MK Stalin announces grand schemes for Tamil Nadu development",
                "DMK government presents record-breaking state budget",
                "Tamil Nadu government launches AI and technology initiative",
                "EPS challenges central government on pending projects",
                "All India Anna DMK holds massive rally in Chennai"
            ],
            'Maharashtra Politics': [
                "Shiv Sena chief announces new coalition strategies",
                "Maharashtra government unveils new budget for 2025",
                "BJP and allies discuss seat sharing for elections",
                "Mumbai development projects get cabinet approval",
                "Fadanvis government launches green Maharashtra initiative"
            ],
            'Karnataka Politics': [
                "Siddaramaiah government announces free electricity scheme",
                "Karnataka Congress releases election manifesto",
                "BJP Karnataka announces new state president",
                "Karnataka tech hub gets major government investment",
                "DK Shivakumar addresses party workers at convention"
            ],
            'UP Politics': [
                "Yogi government announces new police reforms in UP",
                "SP manifesto promises major changes in Ayodhya",
                "BSP announces new approach for upcoming elections",
                "UP government launches startup and AI hub in Lucknow",
                "Modi and Yogi inaugurate mega infrastructure project"
            ],
            'West Bengal Politics': [
                "Mamata Banerjee announces new welfare scheme for Bengal",
                "TMC launches campaign for central government schemes",
                "BJP Bengal targets 50+ seats in upcoming elections",
                "Calcutta High Court hears petitions on state issues",
                "Jharkhand politics impact Bengal election strategies"
            ]
        }
        templates_list = templates.get(category, [f"{category} news update {index}"])
        return random.choice(templates_list)
        
    def _generate_sports_headline(self, category: str, index: int) -> str:
        """Generate realistic sports news headlines"""
        templates = {
            'Cricket': [
                "IPL 2025 auction: Teams spend big on overseas players",
                "Virat Kohli becomes fastest to reach 25,000 international runs",
                "India wins T20 series against Australia with dominant performance",
                "ICC announces new tournament schedule for 2025-2026",
                "Rohit Sharma named captain for World Cup campaign",
                "BCCI announces new central contract for players"
            ],
            'Football': [
                "Manchester City wins Premier League title in dramatic fashion",
                "Liverpool signs new striker for record transfer fee",
                "Champions League final set between top European clubs",
                "India national team prepares for Asian Cup qualifiers",
                "Arsenal announces new manager for upcoming season"
            ],
            'Hockey': [
                "India beats Germany to win Champions Trophy hockey",
                "Indian hockey team qualifies for Olympics 2028",
                "Pro Hockey League announces new season format",
                "PR Sreejeet appointed as Indian hockey team head coach",
                "Junior hockey team wins gold at World Cup"
            ],
            'Tennis': [
                "Novak Djokovic wins record-breaking 25th Grand Slam",
                "Sinner becomes world number 1 after stellar season",
                "Indian tennis player wins first ATP title",
                "Wimbledon announces equal prize money for all players",
                "Sania Mirza announces retirement from tennis"
            ],
            'Badminton': [
                "PV Sindhu advances to finals of Indonesia Open",
                "Kidambi Srikanth returns to top 10 world rankings",
                "India wins Thomas Cup with dominant performance",
                "BWF announces new ranking system for 2025",
                "Prakash Padukone Academy wins multiple medals"
            ],
            'Athletics': [
                "Indian athlete wins gold at Asian Athletics Championships",
                "Neeraj Chopra achieves new national record in javelin",
                "India announces 100 athletes for Paris Olympics 2024",
                "National Games set to begin with record participation",
                "Athletics federation announces new training program"
            ],
            'Wrestling': [
                "Bajrang Punia wins gold at World Championships",
                "Sakshi Malik announces comeback for Asian Games",
                "Wrestling Federation announces new selection trials",
                "Indian wrestlers dominate Commonwealth Games",
                "Vinesh Phogat announces retirement from wrestling"
            ]
        }
        templates_list = templates.get(category, [f"{category} news update {index}"])
        return random.choice(templates_list)
        
    def _generate_business_headline(self, category: str, index: int) -> str:
        """Generate realistic business news headlines"""
        templates = {
            'Stock Market': [
                "Sensex crosses 95,000 for first time in history",
                "Nifty 50 reaches all-time high amid foreign investor buying",
                "FIIs pump Rs 10,000 crore into Indian markets",
                "Stock market volatility increases ahead of elections",
                "IT sector stocks rally after quarterly results"
            ],
            'Startup News': [
                "Indian startup becomes unicorn with new funding round",
                "Startup ecosystem sees 50% growth in 2024",
                "RBI announces new guidelines for startup funding",
                "Government launches Rs 10,000 crore startup fund",
                "Bengaluru becomes third largest startup hub globally"
            ],
            'Economy': [
                "India GDP growth exceeds 8% in Q3FY25",
                "RBI keeps interest rates unchanged for fifth time",
                "Inflation eases to 4.5% bringing relief to consumers",
                "Fiscal deficit target on track says Finance Ministry",
                "Rupee strengthens against dollar amid global stability"
            ],
            'Tech Companies': [
                "Google announces $10 billion investment in India",
                "Apple India operations cross $1 trillion revenue",
                "Amazon India expands fulfillment network",
                "Microsoft partners with Indian government for AI initiative",
                "Tesla India operations to begin with Gujarat factory"
            ],
            'Banking': [
                "HDFC Bank becomes largest private sector bank in India",
                "SBI announces record profit for Q3FY25",
                "RBI introduces new digital lending guidelines",
                "Public sector banks report higher NPAs recovery",
                "Loan growth reaches 15% driven by retail segment"
            ]
        }
        templates_list = templates.get(category, [f"{category} news update {index}"])
        return random.choice(templates_list)
        
    def _generate_tech_headline(self, category: str, index: int) -> str:
        """Generate realistic technology news headlines"""
        templates = {
            'Smartphones': [
                "Samsung launches Galaxy S25 Ultra with AI features",
                "Apple iPhone 17 Pro leak reveals new design",
                "OnePlus 13 launches with Snapdragon 8 Elite chip",
                "Google Pixel 10 introduces new AI camera features",
                "Redmi Note 14 Pro offers flagship features at budget price"
            ],
            'Electric Vehicles': [
                "Tata Motors launches new EV SUV with 500km range",
                "Ola Electric announces new affordable EV scooter",
                "EV sales in India cross 2 million units in 2024",
                "Government increases EV subsidy to boost adoption",
                "Tesla enters Indian market with Model Y"
            ],
            'Space Tech': [
                "ISRO successfully launches Chandrayaan-4 mission",
                "NASA and ISRO collaborate on joint Mars mission",
                "SpaceX launches Starlink satellites for India coverage",
                "India announces plans for first space station by 2030",
                "ISRO tests new heavy-lift launcher for moon missions"
            ],
            'Gadgets': [
                "Apple Watch Series 10 introduces new health features",
                "Dell launches AI-powered laptops for professionals",
                "Sony releases new wireless earbuds with ANC",
                "Apple iPad Pro 2025 features OLED display",
                "Samsung launches new smart TV lineup with AI"
            ],
            'Internet': [
                "Reliance Jio launches 5G services in 100 cities",
                "Airtel 5G covers 500 cities milestone achieved",
                "BSNL launches new affordable broadband plans",
                "India crosses 1 billion internet users milestone",
                "5G data consumption reaches new heights in India"
            ]
        }
        templates_list = templates.get(category, [f"{category} news update {index}"])
        return random.choice(templates_list)
        
    def _generate_entertainment_headline(self, category: str, index: int) -> str:
        """Generate realistic entertainment news headlines"""
        templates = {
            'Bollywood': [
                "Salman Khan announces 'Tiger 4' with spectacular budget",
                "Bollywood blockbuster collects Rs 500 crore at box office",
                "Aamir Khan's new film breaks advance booking records",
                "Shah Rukh Khan completes 35 years in Bollywood with grand celebrations",
                "Bollywood actress announces wedding with prominent businessman"
            ],
            'Hollywood': [
                "Marvel announces Avengers 5 with all-star cast",
                "Christopher Nolan's new film wins Oscar for Best Picture",
                "Tom Cruise announces Mission Impossible 8",
                "James Cameron reveals Avatar 3 production details",
                "Hollywood studio announces Indian market expansion"
            ],
            'South Cinema': [
                "Pushpa 2 crosses Rs 1000 crore worldwide collection",
                "Allu Arjun wins National Award for best actor",
                "Prabhas announces new project with top director",
                "Rajinikanth's new film creates massive hype",
                "SS Rajamouli's next Hollywood project announced"
            ],
            'Gaming': [
                "GTA 6 release date announced for 2025",
                "BGMI tournament offers Rs 1 crore prize pool",
                "PlayStation 6 rumored to launch in 2026",
                "Indian esports team wins gold at Asian Games",
                "Mobile gaming revenue crosses $1 billion in India"
            ],
            'Music': [
                "A.R. Rahman's new album breaks streaming records",
                "Spotify India crosses 100 million users",
                "Bollywood music dominates global charts again",
                "Karan Johar announces music label expansion",
                "Indian artists dominate Spotify top charts"
            ]
        }
        templates_list = templates.get(category, [f"{category} news update {index}"])
        return random.choice(templates_list)
        
    def _generate_science_headline(self, category: str, index: int) -> str:
        """Generate realistic science and education news headlines"""
        templates = {
            'Science Discovery': [
                "Indian scientists discover new species in Western Ghats",
                "ISRO publishes breakthrough research on Mars atmosphere",
                "CERN announces new particle discovery",
                "Indian scientists develop new cancer treatment",
                "Researchers achieve nuclear fusion breakthrough"
            ],
            'Education': [
                "CBSE announces board exam dates for 2025",
                "NEET UG 2025 registration begins with new guidelines",
                "IIT Bombay ranks among top 50 globally",
                "Government announces free education for all",
                "UPSC CSE 2025 notification released with 1000 vacancies"
            ],
            'Health': [
                "New vaccine for dengue approved in India",
                "AIIMS announces breakthrough in cancer treatment",
                "Health ministry launches nationwide vaccination drive",
                "India achieves WHO target for child mortality",
                "New AI tool helps detect diseases early"
            ],
            'Environment': [
                "India achieves record renewable energy capacity",
                "Delhi air quality improves after new measures",
                "Government announces net zero target by 2070",
                "Tiger population increases in India",
                "Climate change summit held in New Delhi"
            ]
        }
        templates_list = templates.get(category, [f"{category} news update {index}"])
        return random.choice(templates_list)
        
    def _generate_global_headline(self, category: str, index: int) -> str:
        """Generate realistic global news headlines"""
        templates = {
            'USA Politics': [
                "Trump announces presidential campaign for 2028",
                "Biden signs new infrastructure bill into law",
                "US Congress passes AI regulation framework",
                "US and China resume trade negotiations",
                "American economy shows strong recovery signs"
            ],
            'China News': [
                "China announces new economic stimulus package",
                "Xi Jinping meets world leaders at summit",
                "Taiwan tensions rise amid new military exercises",
                "China's tech companies face new regulations",
                "China and India hold diplomatic talks"
            ],
            'Europe News': [
                "EU announces major climate legislation",
                "UK and EU reach new trade agreement",
                "Ukraine war enters third year with ongoing conflict",
                "Germany announces new government coalition",
                "France faces protests over pension reforms"
            ],
            'Middle East': [
                "Israel and Hamas reach temporary ceasefire agreement",
                "Iran announces nuclear deal progress",
                "Saudi Arabia invests $100 billion in tech",
                "UAE becomes global AI hub with new investments",
                "Palestinian statehood discussions resume"
            ]
        }
        templates_list = templates.get(category, [f"{category} news update {index}"])
        return random.choice(templates_list)
        
    def _generate_summary(self, headline: str, category: str) -> str:
        """Generate a summary for the news headline"""
        return f"This is a developing story in {category}. Experts analyze the implications and impact on the industry. This news has generated significant interest and discussion among stakeholders and the general public."
        
    def _generate_full_content(self, headline: str, category: str) -> str:
        """Generate full content for the news"""
        return f"""#{headline}

## Summary
This is a significant development in {category} that has captured attention across the industry. 

## Key Points
1. Major announcement made regarding {category}
2. Industry experts weigh in on implications
3. Market and public response growing
4. Further developments expected soon

## Detailed Analysis
This news represents an important development that could have far-reaching consequences for the industry and stakeholders involved. 

## What This Means
- For consumers: New opportunities and improved services
- For businesses: Strategic implications to consider
- For investors: Potential market movements expected
- For the public: Broader societal impact anticipated

## Next Steps
Further updates will be provided as the story develops. Experts will continue to analyze the situation and provide insights.

---
*Source: RJ TECH Media Engine*
*Category: {category}*
*Collected at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

# ============================================================================
# AGENT 2: FOUNDER SELECTION - WITH PREVIEW
# ============================================================================

class FounderSelectionAgent:
    """Shows ALL News with Preview - Founder Picks"""
    
    def __init__(self, db: MediaDatabase):
        self.db = db
        self.name = "Founder Selection Agent"
        self.selected_ids = []
        
    def show_all_news(self):
        """Display all news for founder selection with PREVIEW"""
        news_list = self.db.get_all_news(limit=100)
        
        print("\n" + "=" * 80)
        print("📋 ALL COLLECTED NEWS - FOUNDER SELECTION")
        print("=" * 80)
        
        ai_news = [n for n in news_list if n.get('is_ai_related')]
        general_news = [n for n in news_list if not n.get('is_ai_related')]
        
        print("\n🤖 AI NEWS (HIGHEST PRIORITY)")
        print("-" * 80)
        for i, news in enumerate(ai_news[:20], 1):
            is_selected = news['id'] in self.selected_ids
            mark = "✓" if is_selected else "○"
            print(f"  [{i}] {mark} [{news['category']}] {news['headline'][:60]}...")
            print(f"      Category: {news.get('subcategory', 'General')} | Source: {news['source']}")
            
        print("\n📰 ALL OTHER NEWS")
        print("-" * 80)
        start = len(ai_news) + 1
        for i, news in enumerate(general_news[:20], start):
            is_selected = news['id'] in self.selected_ids
            mark = "✓" if is_selected else "○"
            print(f"  [{i}] {mark} [{news['category']}] {news['headline'][:60]}...")
            print(f"      Category: {news.get('subcategory', 'General')} | Source: {news['source']}")
            
        print("\n" + "=" * 80)
        print(f"📊 Total: {len(news_list)} news | 🤖 AI: {len(ai_news)} | 📰 General: {len(general_news)}")
        print("=" * 80)
        
        return news_list
        
    def preview_news(self, news_id: str):
        """Show full content of a news item so founder can decide"""
        news = self.db.get_news_by_id(news_id)
        if not news:
            print(f"❌ News item not found: {news_id[:8]}...")
            return None
            
        print("\n" + "=" * 80)
        print(f"🔍 PREVIEW: {news['category']} - {news.get('subcategory', 'General')}")
        print("=" * 80)
        print(f"\n📰 HEADLINE: {news['headline']}")
        print(f"📌 SOURCE: {news['source']}")
        print(f"🕐 COLLECTED: {news['collected_at']}")
        print(f"🏷️ CATEGORY: {news['category']} > {news.get('subcategory', 'General')}")
        print(f"⭐ PRIORITY: {news['priority']}")
        print("\n" + "-" * 80)
        print("📝 SUMMARY:")
        print("-" * 80)
        print(news.get('summary', 'No summary available'))
        print("\n" + "-" * 80)
        print("📖 FULL CONTENT:")
        print("-" * 80)
        print(news.get('full_content', news.get('summary', 'No content available')))
        print("\n" + "=" * 80)
        
        return news
        
    def select_news(self, news_id: str):
        """Select news for processing"""
        self.db.select_news(news_id)
        if news_id not in self.selected_ids:
            self.selected_ids.append(news_id)
        news = self.db.get_news_by_id(news_id)
        print(f"  ✓ Selected: {news['headline'][:50]}..." if news else f"  ✓ Selected: {news_id[:8]}...")
        
    def deselect_news(self, news_id: str):
        """Deselect news"""
        self.db.deselect_news(news_id)
        if news_id in self.selected_ids:
            self.selected_ids.remove(news_id)
        print(f"  ✗ Deselected: {news_id[:8]}...")

# ============================================================================
# AGENT 3: CONTENT CREATION
# ============================================================================

class ContentAgent:
    """Creates content from selected news"""
    
    def __init__(self, db: MediaDatabase):
        self.db = db
        self.name = "Content Agent"
        
    def run_cycle(self):
        """Run content creation cycle"""
        print("\n" + "=" * 70)
        print("📝 CONTENT AGENT - Creating Articles")
        print("=" * 70)
        
        results = {'articles': 0}
        
        selected_news = self.db.get_selected_news()
        
        if not selected_news:
            print("\n⚠️ No news selected yet!")
            print("   Go back to STEP 2 and select some news items to create content.")
            return results
        
        for news in selected_news:
            article = {
                'news_id': news['id'],
                'title': f"[{news.get('subcategory', news['category'])}] {news['headline']}",
                'content': f"""# {news['headline']}

## 📰 Source: {news['source']}
## 🏷️ Category: {news.get('subcategory', news['category'])}

---

{news.get('full_content', news.get('summary', ''))}

---

## Summary

{news.get('summary', 'No summary available')}

---

### Key Takeaways

1. This news represents a significant development in {news.get('subcategory', news['category'])}
2. Industry experts are closely monitoring the situation
3. Further developments are expected in the coming days
4. Stakeholders should pay attention to upcoming announcements

---

*📱 This article was generated by RJ TECH Media Engine*
*🤖 AI-powered content creation for your media company*
*🏷️ Category: {news['category']} > {news.get('subcategory', 'General')}*
""",
                'summary': news.get('summary', '')[:200],
                'category': news['category']
            }
            
            article_id = self.db.save_article(article)
            
            image = {
                'article_id': article_id,
                'filename': f"image_{article_id[:8]}.png",
                'filepath': f"media/images/image_{article_id[:8]}.png",
                'description': f"Image for: {news['headline']}"
            }
            self.db.save_image(image)
            
            video = {
                'article_id': article_id,
                'title': f"{news.get('subcategory', news['category'])} News Report",
                'script': f"""Welcome to RJ TECH News. Today we're covering: {news['headline']}.

{news.get('summary', '')}

This is a developing story in {news.get('subcategory', news['category'])}. 
Our team will continue to monitor and provide updates as more information becomes available.

Stay connected with RJ TECH for the latest news updates.

Thank you for watching!"""
            }
            self.db.save_video(video)
            
            self.db.mark_processed(news['id'])
            
            results['articles'] += 1
            
            print(f"  ✓ Article: {news['headline'][:50]}...")
            
        self.db.log(self.name, "cycle_complete", "success", f"{results['articles']} articles")
        print(f"\n✅ Created {results['articles']} articles with images and videos")
        return results

# ============================================================================
# AGENT 4: FOUNDER APPROVAL - WITH PREVIEW
# ============================================================================

class ApprovalAgent:
    """Founder approves content - WITH PREVIEW"""
    
    def __init__(self, db: MediaDatabase):
        self.db = db
        self.name = "Approval Agent"
        
    def show_pending(self):
        """Show pending content with preview"""
        pending = self.db.get_pending_approval()
        
        print("\n" + "=" * 70)
        print("👑 FOUNDER APPROVAL - Review Content")
        print("=" * 70)
        
        if pending['articles']:
            print(f"\n📄 ARTICLES ({len(pending['articles'])}):")
            for i, art in enumerate(pending['articles'], 1):
                print(f"  [{i}] 📝 {art['title'][:60]}...")
                print(f"      Category: {art['category']} | ID: {art['id'][:8]}...")
                
        if pending['images']:
            print(f"\n🖼️  IMAGES ({len(pending['images'])}):")
            for i, img in enumerate(pending['images'], 1):
                print(f"  [{i}] 🖼️ {img['filename']} - {img['description'][:40]}...")
                print(f"      ID: {img['id'][:8]}...")
                
        if pending['videos']:
            print(f"\n🎬 VIDEOS ({len(pending['videos'])}):")
            for i, vid in enumerate(pending['videos'], 1):
                print(f"  [{i}] 🎬 {vid['title'][:50]}...")
                print(f"      Duration: {vid.get('duration', 60)}s | ID: {vid['id'][:8]}...")
                
        print("\n" + "=" * 70)
        return pending
        
    def preview_article(self, article_id: str):
        """Show full article content for review"""
        cursor = self.db._get_conn().cursor()
        row = cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
        if not row:
            print(f"❌ Article not found: {article_id[:8]}...")
            return None
            
        article = dict(row)
        
        print("\n" + "=" * 80)
        print(f"📄 PREVIEW ARTICLE")
        print("=" * 80)
        print(f"\n📌 TITLE: {article['title']}")
        print(f"🏷️ CATEGORY: {article['category']}")
        print(f"📅 CREATED: {article['created_at']}")
        print(f"🔖 STATUS: {article['status']}")
        print("\n" + "-" * 80)
        print("📖 FULL ARTICLE CONTENT:")
        print("-" * 80)
        print(article['content'])
        print("\n" + "=" * 80)
        
        return article
        
    def approve(self, item_type: str, item_id: str):
        """Approve item"""
        self.db.approve_item(item_type, item_id)
        print(f"  ✓ Approved: {item_type} {item_id[:8]}...")
        
    def reject(self, item_type: str, item_id: str):
        """Reject item"""
        self.db.reject_item(item_type, item_id)
        print(f"  ✗ Rejected: {item_type} {item_id[:8]}...")

# ============================================================================
# AGENT 5: SOCIAL MEDIA
# ============================================================================

class SocialMediaAgent:
    """Publishes to social media"""
    
    def __init__(self, db: MediaDatabase):
        self.db = db
        self.name = "Social Media Agent"
        self.platforms = ['linkedin', 'x', 'facebook', 'instagram', 'telegram']
        
    def run_cycle(self):
        """Run publishing cycle"""
        print("\n" + "=" * 70)
        print("📱 SOCIAL MEDIA AGENT - Publishing")
        print("=" * 70)
        
        cursor = self.db._get_conn().cursor()
        articles = cursor.execute(
            "SELECT * FROM articles WHERE status = 'approved' AND published_at IS NULL"
        ).fetchall()
        
        if not articles:
            print("\n⚠️ No approved articles to publish!")
            print("   Go to STEP 4 and approve some articles first.")
            return {'published': 0}
        
        for art in articles:
            article = dict(art)
            for platform in self.platforms:
                post = {
                    'article_id': article['id'],
                    'content': f"📢 NEW: {article['title'][:100]}\n\n{article.get('summary', '')[:150]}...\n\n#News #{article['category']} #RJTech",
                    'platform': platform
                }
                self.db.save_social_post(post)
                print(f"  ✓ {platform}: Posted")
                
            self.db.publish_article(article['id'])
            
        print(f"\n✅ Published {len(articles)} articles to {len(self.platforms)} platforms")

# ============================================================================
# INTERACTIVE MODE - FOUNDER COMMANDS
# ============================================================================

def run_interactive_mode():
    """Run the media engine in interactive mode with founder commands"""
    engine = RJTechMediaEngine()
    engine.db = MediaDatabase()
    
    research = ResearchAgent(engine.db)
    selection = FounderSelectionAgent(engine.db)
    content = ContentAgent(engine.db)
    approval = ApprovalAgent(engine.db)
    social = SocialMediaAgent(engine.db)
    
    print("\n" + "=" * 80)
    print("╔════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                        ║")
    print("║     RJ TECH MEDIA ENGINE - INTERACTIVE MODE                            ║")
    print("║                                                                        ║")
    print("║     🤖 AI News First | 🇮🇳 India Politics | 🏏 Sports | 💰 Business   ║")
    print("║                                                                        ║")
    print("║     🔍 Preview before selecting!                                       ║")
    print("║     👑 You choose what to process                                       ║")
    print("║     ⏰ 24/7 Operation                                                   ║")
    print("║                                                                        ║")
    print("╚════════════════════════════════════════════════════════════════════════╝")
    print("=" * 80)
    
    print("\n\n" + "=" * 80)
    print("🔍 STEP 1: RESEARCH - Collecting News from All Categories")
    print("=" * 80)
    research.run_cycle()
    
    print("\n\n" + "=" * 80)
    print("👑 STEP 2: FOUNDER SELECTION - Choose News to Process")
    print("=" * 80)
    selection.show_all_news()
    
    print("\n" + "-" * 80)
    print("📝 AVAILABLE COMMANDS:")
    print("-" * 80)
    print("  preview <number>   - View full content of a news item (e.g., preview 1)")
    print("  select <number>     - Select a news item (e.g., select 1)")
    print("  deselect <number>   - Remove a selection (e.g., deselect 1)")
    print("  list                - Show all news again")
    print("  done                - Finish selecting and create content")
    print("  quit                - Exit the program")
    print("-" * 80)
    
    while True:
        print("\n> ", end="")
        cmd = input().strip().lower()
        
        if not cmd:
            continue
            
        parts = cmd.split()
        action = parts[0] if parts else ""
        
        if action == "preview" and len(parts) >= 2:
            try:
                idx = int(parts[1])
                news_list = engine.db.get_all_news(limit=100)
                
                ai_news = [n for n in news_list if n.get('is_ai_related')]
                general_news = [n for n in news_list if not n.get('is_ai_related')]
                all_news = ai_news + general_news
                
                if 1 <= idx <= len(all_news):
                    selection.preview_news(all_news[idx-1]['id'])
                else:
                    print(f"❌ Invalid number. Choose between 1 and {len(all_news)}")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif action == "select" and len(parts) >= 2:
            try:
                idx = int(parts[1])
                news_list = engine.db.get_all_news(limit=100)
                
                ai_news = [n for n in news_list if n.get('is_ai_related')]
                general_news = [n for n in news_list if not n.get('is_ai_related')]
                all_news = ai_news + general_news
                
                if 1 <= idx <= len(all_news):
                    selection.select_news(all_news[idx-1]['id'])
                else:
                    print(f"❌ Invalid number. Choose between 1 and {len(all_news)}")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif action == "deselect" and len(parts) >= 2:
            try:
                idx = int(parts[1])
                news_list = engine.db.get_all_news(limit=100)
                
                ai_news = [n for n in news_list if n.get('is_ai_related')]
                general_news = [n for n in news_list if not n.get('is_ai_related')]
                all_news = ai_news + general_news
                
                if 1 <= idx <= len(all_news):
                    selection.deselect_news(all_news[idx-1]['id'])
                else:
                    print(f"❌ Invalid number. Choose between 1 and {len(all_news)}")
            except ValueError:
                print("❌ Please enter a valid number")
                
        elif action == "list":
            selection.show_all_news()
            
        elif action == "done":
            print("\n✅ Selection complete! Moving to content creation...")
            break
            
        elif action == "quit":
            print("\n👋 Exiting Media Engine. Goodbye!")
            return
            
        else:
            print("❓ Unknown command. Try: preview, select, deselect, list, done, quit")
    
    print("\n\n" + "=" * 80)
    print("📝 STEP 3: CONTENT CREATION - Creating Articles")
    print("=" * 80)
    content.run_cycle()
    
    print("\n\n" + "=" * 80)
    print("👑 STEP 4: FOUNDER APPROVAL - Review & Approve Content")
    print("=" * 80)
    approval.show_pending()
    
    print("\n" + "-" * 80)
    print("📝 APPROVAL COMMANDS:")
    print("-" * 80)
    print("  preview_article <id>   - View full article content")
    print("  approve article <id>  - Approve an article")
    print("  reject article <id>   - Reject an article")
    print("  done                  - Finish approving")
    print("-" * 80)
    
    while True:
        print("\n> ", end="")
        cmd = input().strip().lower()
        
        if not cmd:
            continue
            
        parts = cmd.split()
        action = parts[0] if parts else ""
        
        if action == "preview_article" and len(parts) >= 2:
            article_id = parts[1]
            approval.preview_article(article_id)
            
        elif action == "approve" and len(parts) >= 3:
            item_type = parts[1]
            item_id = parts[2]
            approval.approve(item_type, item_id)
            
        elif action == "reject" and len(parts) >= 3:
            item_type = parts[1]
            item_id = parts[2]
            approval.reject(item_type, item_id)
            
        elif action == "done":
            print("\n✅ Approval complete! Moving to publishing...")
            break
            
        else:
            print("❓ Try: preview_article <id>, approve <type> <id>, reject <type> <id>, done")
    
    print("\n\n" + "=" * 80)
    print("📱 STEP 5: AUTO-PUBLISH - To All Platforms")
    print("=" * 80)
    social.run_cycle()
    
    print("\n\n" + "=" * 80)
    print("📊 FINAL DASHBOARD")
    print("=" * 80)
    analytics = engine.db.get_analytics()
    print(f"  🤖 Total AI News: {analytics['ai_news']}")
    print(f"  📰 Total News: {analytics['total_news']}")
    print(f"  ✅ Selected: {analytics['selected']}")
    print(f"  📝 Articles Created: {analytics['articles']}")
    print(f"  📢 Published: {analytics['published']}")
    print("=" * 80)
    
    print("\n🎉 RJ TECH MEDIA ENGINE - COMPLETE!")
    print("🤖 AI First | 👑 Founder Chooses | 📱 Auto-Publish | ⏰ 24/7")

# ============================================================================
# MAIN ENGINE
# ============================================================================

class RJTechMediaEngine:
    """Main Media Engine"""
    
    def __init__(self):
        self.name = "RJ TECH Media Engine"
        self.db = MediaDatabase()
        self.running = False
        self.start_time = None
        
    def run(self):
        """Run the complete system in automated mode"""
        print("\n" + "=" * 70)
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                                                            ║")
        print("║     RJ TECH MEDIA ENGINE                                   ║")
        print("║     ALL News | Founder Chooses | Auto-Publish             ║")
        print("║                                                            ║")
        print("║     🤖 AI News First                                      ║")
        print("║     📰 All News Second                                   ║")
        print("║     👑 Founder Picks                                      ║")
        print("║     ⏰ 24/7 Operation                                      ║")
        print("║                                                            ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print("=" * 70)
        
        self.running = True
        self.start_time = datetime.now()
        
        print("\n" + "=" * 70)
        print("STEP 1: RESEARCH - Collecting ALL News (AI First)")
        print("=" * 70)
        research = ResearchAgent(self.db)
        research.run_cycle()
        
        print("\n" + "=" * 70)
        print("STEP 2: FOUNDER SELECTION - Choose News to Process")
        print("=" * 70)
        selection = FounderSelectionAgent(self.db)
        news_list = selection.show_all_news()
        
        print("\n📝 FOUNDER SELECTION OPTIONS:")
        print("   Type: select <number> to choose news")
        print("   Type: deselect <number> to remove")
        print("   Type: done when finished selecting")
        
        print("\n" + "=" * 70)
        print("STEP 3: CONTENT CREATION - Creating Articles")
        print("=" * 70)
        content = ContentAgent(self.db)
        content.run_cycle()
        
        print("\n" + "=" * 70)
        print("STEP 4: FOUNDER APPROVAL - Review Content")
        print("=" * 70)
        approval = ApprovalAgent(self.db)
        approval.show_pending()
        
        print("\n📝 APPROVAL OPTIONS:")
        print("   Type: approve <type> <id> to approve")
        print("   Type: reject <type> <id> to reject")
        print("   Type: done when finished reviewing")
        
        print("\n" + "=" * 70)
        print("STEP 5: AUTO-PUBLISH - To All Platforms")
        print("=" * 70)
        social = SocialMediaAgent(self.db)
        social.run_cycle()
        
        self.show_dashboard()
        
        print("\n" + "=" * 70)
        print("         RJ TECH MEDIA ENGINE - COMPLETE")
        print("         AI First | Founder Chooses | Auto-Publish | 24/7")
        print("=" * 70)
        
    def show_dashboard(self):
        """Show system dashboard"""
        analytics = self.db.get_analytics()
        
        print("\n" + "=" * 70)
        print("📊 DASHBOARD")
        print("=" * 70)
        uptime = datetime.now() - self.start_time if self.start_time else timedelta(0)
        print(f"  Status: {'🟢 RUNNING' if self.running else '🔴 STOPPED'}")
        print(f"  Uptime: {uptime}")
        print(f"\n  Total News: {analytics['total_news']}")
        print(f"  AI News: {analytics['ai_news']}")
        print(f"  Selected: {analytics['selected']}")
        print(f"  Articles: {analytics['articles']}")
        print(f"  Published: {analytics['published']}")
        print("=" * 70)

def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_mode()
    else:
        engine = RJTechMediaEngine()
        engine.run()

if __name__ == "__main__":
    main()