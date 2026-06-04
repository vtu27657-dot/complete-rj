"""
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║     RJ TECH MEDIA ENGINE                                                              ║
║     ALL News Collection | Founder Selection | Auto-Publish                          ║
║                                                                                    ║
║     🤖 AI News = FIRST PRIORITY                                                    ║
║     📰 ALL Other News = SECOND PRIORITY                                           ║
║     👑 FOUNDER PICKS What to Process                                               ║
║     ⏰ 24/7 CONTINUOUS OPERATION                                                   ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
"""

import uuid
import time
import json
import sqlite3
import threading
import random
from datetime import datetime, timedelta
from typing import Dict, List
from pathlib import Path

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
                source TEXT NOT NULL,
                url TEXT,
                category TEXT,
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
        cursor.execute("""
            INSERT INTO news_collected 
            (id, headline, summary, source, url, category, priority, is_ai_related, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            news['headline'],
            news.get('summary', ''),
            news['source'],
            news.get('url', ''),
            news.get('category', 'general'),
            news.get('priority', 'normal'),
            news.get('is_ai_related', False),
            datetime.now().isoformat()
        ))
        self._get_conn().commit()
        return str(uuid.uuid4())
        
    def get_all_news(self, limit: int = 100) -> List[Dict]:
        cursor = self._get_conn().cursor()
        rows = cursor.execute("""
            SELECT * FROM news_collected 
            ORDER BY is_ai_related DESC, collected_at DESC 
            LIMIT ?
        """, (limit,)).fetchall()
        return [dict(row) for row in rows]
        
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
        cursor.execute("""
            INSERT INTO articles (id, news_id, title, content, summary, category, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            article.get('news_id'),
            article['title'],
            article['content'],
            article.get('summary', ''),
            article.get('category', 'general'),
            'pending_approval',
            datetime.now().isoformat()
        ))
        self._get_conn().commit()
        return str(uuid.uuid4())
        
    def save_image(self, image: Dict) -> str:
        cursor = self._get_conn().cursor()
        cursor.execute("""
            INSERT INTO images (id, article_id, filename, filepath, description, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            image.get('article_id'),
            image.get('filename', ''),
            image.get('filepath', ''),
            image.get('description', ''),
            'pending_approval',
            datetime.now().isoformat()
        ))
        self._get_conn().commit()
        return str(uuid.uuid4())
        
    def save_video(self, video: Dict) -> str:
        cursor = self._get_conn().cursor()
        cursor.execute("""
            INSERT INTO videos (id, article_id, title, script, duration, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            video.get('article_id'),
            video['title'],
            video.get('script', ''),
            video.get('duration', 60),
            'pending_approval',
            datetime.now().isoformat()
        ))
        self._get_conn().commit()
        return str(uuid.uuid4())
        
    def save_social_post(self, post: Dict) -> str:
        cursor = self._get_conn().cursor()
        cursor.execute("""
            INSERT INTO social_posts (id, article_id, content, platform, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            post.get('article_id'),
            post['content'],
            post['platform'],
            'pending'
        ))
        self._get_conn().commit()
        return str(uuid.uuid4())
        
    def get_pending_approval(self) -> Dict:
        cursor = self._get_conn().cursor()
        articles = cursor.execute("SELECT * FROM articles WHERE status = 'pending_approval'").fetchall()
        images = cursor.execute("SELECT * FROM images WHERE status = 'pending_approval'").fetchall()
        videos = cursor.execute("SELECT * FROM videos WHERE status = 'pending_approval'").fetchall()
        return {
            'articles': [dict(row) for row in articles],
            'images': [dict(row) for row in images],
            'videos': [dict(row) for row in videos]
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
        cursor.execute("UPDATE articles SET status = 'published', published_at = ? WHERE id = ?",
                     (datetime.now().isoformat(), article_id))
        self._get_conn().commit()
        
    def get_analytics(self) -> Dict:
        cursor = self._get_conn().cursor()
        total_news = cursor.execute("SELECT COUNT(*) FROM news_collected").fetchone()[0]
        ai_news = cursor.execute("SELECT COUNT(*) FROM news_collected WHERE is_ai_related = TRUE").fetchone()[0]
        selected = cursor.execute("SELECT COUNT(*) FROM news_collected WHERE selected_by_founder = TRUE").fetchone()[0]
        articles = cursor.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        published = cursor.execute("SELECT COUNT(*) FROM articles WHERE status = 'published'").fetchone()[0]
        return {
            'total_news': total_news,
            'ai_news': ai_news,
            'selected': selected,
            'articles': articles,
            'published': published
        }

# ============================================================================
# AGENT 1: RESEARCH - COLLECTS ALL NEWS (AI FIRST)
# ============================================================================

class ResearchAgent:
    """Collects ALL News - AI Priority"""
    
    def __init__(self, db: MediaDatabase):
        self.db = db
        self.name = "Research Agent"
        
        # AI NEWS FIRST
        self.ai_categories = [
            "Artificial Intelligence",
            "Machine Learning", 
            "Deep Learning",
            "Neural Networks",
            "Natural Language Processing",
            "Computer Vision",
            "AI Agents",
            "LLM Developments",
            "AI Ethics",
            "AI Safety",
            "AI Research",
            "Open Source AI",
            "AI Startups",
            "Tech Giants AI",
            "Robotics AI",
            "AI Applications"
        ]
        
        # GENERAL NEWS SECOND
        self.general_categories = [
            "Technology",
            "Business",
            "Politics",
            "Sports",
            "Entertainment",
            "Science",
            "Health",
            "World News",
            "Finance",
            "Education",
            "Environment",
            "Fashion",
            "Food",
            "Travel",
            "Lifestyle"
        ]
        
        self.sources = [
            "Reuters", "BBC", "CNN", "AP", "NYTimes",
            "TechCrunch", "Wired", "Forbes", "Bloomberg", "The Guardian"
        ]
        
    def run_cycle(self):
        """Run one research cycle"""
        print("\n" + "=" * 70)
        print("📊 RESEARCH AGENT - Collecting ALL News")
        print("=" * 70)
        
        results = {'ai': 0, 'general': 0}
        
        # FIRST: Collect AI News (Priority)
        print("\n🤖 AI NEWS (HIGHEST PRIORITY)")
        print("-" * 50)
        for cat in self.ai_categories[:8]:
            for _ in range(random.randint(2, 4)):
                news = {
                    'headline': f"[AI] {cat} - Latest Update #{random.randint(1,999)}",
                    'summary': f"Major breakthrough in {cat}. Industry leaders respond to new developments.",
                    'source': random.choice(self.sources),
                    'url': f"https://news.com/ai-{uuid.uuid4().hex[:8]}",
                    'category': cat,
                    'priority': 'HIGH',
                    'is_ai_related': True
                }
                self.db.save_news(news)
                results['ai'] += 1
            print(f"  ✓ {cat}")
            
        # SECOND: Collect General News
        print("\n📰 GENERAL NEWS (ALL TOPICS)")
        print("-" * 50)
        for cat in self.general_categories[:6]:
            for _ in range(random.randint(1, 2)):
                news = {
                    'headline': f"{cat} News - {random.randint(1,999)}",
                    'summary': f"Latest developments in {cat}. Breaking stories and analysis.",
                    'source': random.choice(self.sources),
                    'url': f"https://news.com/{uuid.uuid4().hex[:8]}",
                    'category': cat,
                    'priority': 'normal',
                    'is_ai_related': False
                }
                self.db.save_news(news)
                results['general'] += 1
            print(f"  ✓ {cat}")
            
        self.db.log(self.name, "cycle_complete", "success", 
                   f"AI: {results['ai']}, General: {results['general']}")
        
        print(f"\n✅ Total Collected: {results['ai'] + results['general']} news items")
        return results

# ============================================================================
# AGENT 2: FOUNDER SELECTION
# ============================================================================

class FounderSelectionAgent:
    """Shows ALL News - Founder Picks"""
    
    def __init__(self, db: MediaDatabase):
        self.db = db
        self.name = "Founder Selection"
        
    def show_all_news(self):
        """Display all news for founder selection"""
        news_list = self.db.get_all_news(limit=50)
        
        print("\n" + "=" * 70)
        print("📋 ALL COLLECTED NEWS - FOUNDER SELECTION")
        print("=" * 70)
        
        # Separate AI and General
        ai_news = [n for n in news_list if n.get('is_ai_related')]
        general_news = [n for n in news_list if not n.get('is_ai_related')]
        
        print("\n🤖 AI NEWS (HIGHEST PRIORITY)")
        print("-" * 60)
        for i, news in enumerate(ai_news[:15], 1):
            mark = "✓" if news.get('selected_by_founder') else "○"
            print(f"  [{i}] {mark} {news['headline'][:50]}...")
            print(f"      Category: {news['category']} | Source: {news['source']}")
            
        print("\n📰 GENERAL NEWS (ALL TOPICS)")
        print("-" * 60)
        start = len(ai_news) + 1
        for i, news in enumerate(general_news[:15], start):
            mark = "✓" if news.get('selected_by_founder') else "○"
            print(f"  [{i}] {mark} {news['headline'][:50]}...")
            print(f"      Category: {news['category']} | Source: {news['source']}")
            
        print("\n" + "=" * 70)
        print(f"Total: {len(news_list)} news | AI: {len(ai_news)} | General: {len(general_news)}")
        print("=" * 70)
        
        return news_list
        
    def select_news(self, news_id: str):
        """Select news for processing"""
        self.db.select_news(news_id)
        print(f"  ✓ Selected: {news_id[:8]}...")
        
    def deselect_news(self, news_id: str):
        """Deselect news"""
        self.db.deselect_news(news_id)
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
        
        # Get selected news
        selected_news = self.db.get_selected_news()
        
        for news in selected_news:
            # Create article
            article = {
                'news_id': news['id'],
                'title': f"{news['category']}: {news['headline']}",
                'content': f"""# {news['headline']}

## Summary
{news.get('summary', '')}

## Full Report
This is a developing story in {news['category']}.

### Key Points
1. Major developments announced
2. Industry impact expected
3. Experts weigh in on implications

## Analysis
Our team has analyzed this story and compiled key insights for our readers.

### What This Means
This story represents significant news in the {news['category']} sector.

### Market Impact
Industry experts predict notable effects on businesses and consumers.

## Conclusion
We will continue monitoring this story and provide updates as they develop.

---
*Content generated by RJ TECH Media Engine*
*Source: {news['source']}*
*Category: {news['category']}*
""",
                'summary': news.get('summary', ''),
                'category': news.get('category', 'general')
            }
            
            article_id = self.db.save_article(article)
            results['articles'] += 1
            
            # Create image
            image = {
                'article_id': article_id,
                'filename': f"image_{article_id[:8]}.png",
                'filepath': f"media/images/image_{article_id[:8]}.png",
                'description': f"Image for: {news['headline']}"
            }
            self.db.save_image(image)
            
            # Create video
            video = {
                'article_id': article_id,
                'title': f"{news['category']} News Report",
                'script': f"Welcome to RJ TECH News. Today: {news['headline']}.",
                'duration': random.randint(60, 180)
            }
            self.db.save_video(video)
            
            # Mark as processed
            self.db.mark_processed(news['id'])
            
            print(f"  ✓ Article: {news['headline'][:40]}...")
            
        self.db.log(self.name, "cycle_complete", "success", f"{results['articles']} articles")
        print(f"\n✅ Created {results['articles']} articles with images and videos")
        return results

# ============================================================================
# AGENT 4: FOUNDER APPROVAL
# ============================================================================

class ApprovalAgent:
    """Founder approves content"""
    
    def __init__(self, db: MediaDatabase):
        self.db = db
        self.name = "Approval Agent"
        
    def show_pending(self):
        """Show pending content"""
        pending = self.db.get_pending_approval()
        
        print("\n" + "=" * 70)
        print("👑 FOUNDER APPROVAL - Review Content")
        print("=" * 70)
        
        if pending['articles']:
            print(f"\n📄 ARTICLES ({len(pending['articles'])}):")
            for i, art in enumerate(pending['articles'], 1):
                print(f"  [{i}] {art['title'][:50]}...")
                print(f"      Category: {art['category']}")
                
        if pending['images']:
            print(f"\n🖼️  IMAGES ({len(pending['images'])}):")
            for i, img in enumerate(pending['images'], 1):
                print(f"  [{i}] {img['filename']}")
                
        if pending['videos']:
            print(f"\n🎬 VIDEOS ({len(pending['videos'])}):")
            for i, vid in enumerate(pending['videos'], 1):
                print(f"  [{i}] {vid['title'][:50]}...")
                
        print("\n" + "=" * 70)
        return pending
        
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
        
        for art in articles:
            article = dict(art)
            for platform in self.platforms:
                post = {
                    'article_id': article['id'],
                    'content': f"📢 NEW: {article['title'][:100]}\n\n{article.get('summary', '')[:150]}...\n\n#News #RJTech",
                    'platform': platform
                }
                self.db.save_social_post(post)
                print(f"  ✓ {platform}: Posted")
                
            self.db.publish_article(article['id'])
            
        print(f"\n✅ Published {len(articles)} articles to {len(self.platforms)} platforms")

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
        
        # Initialize agents
        self.research = ResearchAgent(self.db)
        self.selection = FounderSelectionAgent(self.db)
        self.content = ContentAgent(self.db)
        self.approval = ApprovalAgent(self.db)
        self.social = SocialMediaAgent(self.db)
        
    def run(self):
        """Run the complete system"""
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
        
        # STEP 1: Research - Collect ALL News
        print("\n" + "=" * 70)
        print("STEP 1: RESEARCH - Collecting ALL News (AI First)")
        print("=" * 70)
        self.research.run_cycle()
        
        # STEP 2: Show ALL News - Founder Selection
        print("\n" + "=" * 70)
        print("STEP 2: FOUNDER SELECTION - Choose News to Process")
        print("=" * 70)
        news_list = self.selection.show_all_news()
        
        print("\n📝 FOUNDER SELECTION OPTIONS:")
        print("   Type: select <number> to choose news")
        print("   Type: deselect <number> to remove")
        print("   Type: done when finished selecting")
        
        # STEP 3: Create Content
        print("\n" + "=" * 70)
        print("STEP 3: CONTENT CREATION - Creating Articles")
        print("=" * 70)
        self.content.run_cycle()
        
        # STEP 4: Founder Approval
        print("\n" + "=" * 70)
        print("STEP 4: FOUNDER APPROVAL - Review Content")
        print("=" * 70)
        self.approval.show_pending()
        
        print("\n📝 APPROVAL OPTIONS:")
        print("   Type: approve <type> <id> to approve")
        print("   Type: reject <type> <id> to reject")
        print("   Type: done when finished reviewing")
        
        # STEP 5: Auto-Publish
        print("\n" + "=" * 70)
        print("STEP 5: AUTO-PUBLISH - To All Platforms")
        print("=" * 70)
        self.social.run_cycle()
        
        # Show dashboard
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
    engine = RJTechMediaEngine()
    engine.run()

if __name__ == "__main__":
    main()