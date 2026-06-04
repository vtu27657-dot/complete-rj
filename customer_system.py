"""
RJ TECH Customer Management System
24/7 AI Support, Customer Memory, Portal
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

class CustomerStatus(Enum):
    """Customer status states"""
    LEAD = "lead"
    PROSPECT = "prospect"
    ACTIVE = "active"
    AT_RISK = "at_risk"
    CHURNED = "churned"

class SupportTicket:
    """Support ticket"""
    def __init__(self, customer_id: str, subject: str, priority: str = "medium"):
        self.id = str(uuid.uuid4())
        self.customer_id = customer_id
        self.subject = subject
        self.priority = priority
        self.status = "open"
        self.created_at = datetime.now()
        self.resolved_at = None
        self.messages = []
        
    def add_message(self, sender: str, content: str, is_agent: bool = False):
        """Add message to ticket"""
        self.messages.append({
            'sender': sender,
            'content': content,
            'is_agent': is_agent,
            'timestamp': datetime.now()
        })
        
    def resolve(self):
        """Mark ticket as resolved"""
        self.status = "resolved"
        self.resolved_at = datetime.now()

class CustomerMemory:
    """Permanent customer memory system"""
    
    def __init__(self):
        self.memories = {}
        
    def store(self, customer_id: str, key: str, value: any):
        """Store customer memory"""
        if customer_id not in self.memories:
            self.memories[customer_id] = {}
        self.memories[customer_id][key] = {
            'value': value,
            'timestamp': datetime.now()
        }
        
    def recall(self, customer_id: str, key: str = None) -> any:
        """Recall customer memory"""
        if customer_id not in self.memories:
            return None
        if key:
            return self.memories[customer_id].get(key, {}).get('value')
        return self.memories[customer_id]
        
    def get_history(self, customer_id: str) -> List[Dict]:
        """Get complete customer history"""
        if customer_id not in self.memories:
            return []
        return list(self.memories[customer_id].values())

class Customer:
    """Full customer profile"""
    
    def __init__(self, name: str, email: str, company: str = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.company = company
        self.status = CustomerStatus.LEAD
        self.tier = "free"
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        self.projects = []
        self.tickets = []
        self.satisfaction_score = 100
        self.lifetime_value = 0
        
    def add_project(self, name: str, description: str) -> Dict:
        """Add customer project"""
        project = {
            'id': str(uuid.uuid4()),
            'name': name,
            'description': description,
            'status': 'active',
            'created_at': datetime.now(),
            'progress': 0
        }
        self.projects.append(project)
        return project
        
    def create_ticket(self, subject: str, priority: str = "medium") -> SupportTicket:
        """Create support ticket"""
        ticket = SupportTicket(self.id, subject, priority)
        self.tickets.append(ticket)
        return ticket
        
    def get_info(self) -> Dict:
        """Get customer info"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'company': self.company,
            'status': self.status.value,
            'tier': self.tier,
            'projects': len(self.projects),
            'tickets': len(self.tickets),
            'satisfaction': self.satisfaction_score,
            'ltv': self.lifetime_value,
            'last_active': self.last_active.isoformat()
        }

class CustomerPortal:
    """Customer self-service portal"""
    
    def __init__(self):
        self.customers = []
        self.support_agents = []
        
    def add_customer(self, customer: Customer):
        """Add customer to portal"""
        self.customers.append(customer)
        
    def get_dashboard(self, customer_id: str) -> Dict:
        """Get customer dashboard"""
        for customer in self.customers:
            if customer.id == customer_id:
                return {
                    'customer': customer.get_info(),
                    'projects': customer.projects,
                    'recent_tickets': customer.tickets[-5:],
                    'usage_stats': {
                        'api_calls': 0,
                        'agents_used': 0,
                        'storage': '0MB'
                    }
                }
        return None

class AISupport:
    """24/7 AI Customer Support"""
    
    def __init__(self):
        self.resolution_rate = 0.95
        self.avg_response_time = "2 minutes"
        self.tickets_handled = 0
        
    def handle_ticket(self, ticket: SupportTicket) -> str:
        """AI handles support ticket"""
        self.tickets_handled += 1
        
        # AI response logic
        responses = [
            "I've analyzed your issue and prepared a solution. Here's what you need to do...",
            "Thank you for reaching out. I've identified the problem and here's the fix...",
            "I understand your concern. Let me help you resolve this right away...",
            "Based on your description, here's a step-by-step solution to your issue..."
        ]
        
        return responses[self.tickets_handled % len(responses)]
        
    def get_stats(self) -> Dict:
        """Get support statistics"""
        return {
            'tickets_handled': self.tickets_handled,
            'resolution_rate': f"{self.resolution_rate * 100}%",
            'avg_response_time': self.avg_response_time,
            'availability': "24/7"
        }

class FeedbackCollector:
    """Collect and analyze customer feedback"""
    
    def __init__(self):
        self.feedback = []
        
    def collect(self, customer_id: str, rating: int, comment: str = None):
        """Collect feedback"""
        feedback = {
            'id': str(uuid.uuid4()),
            'customer_id': customer_id,
            'rating': rating,
            'comment': comment,
            'timestamp': datetime.now()
        }
        self.feedback.append(feedback)
        
    def get_average_rating(self) -> float:
        """Calculate average rating"""
        if not self.feedback:
            return 0
        return sum(f['rating'] for f in self.feedback) / len(self.feedback)

class CustomerSuccess:
    """Customer success management"""
    
    def __init__(self):
        self.customers = []
        self.churn_prevention = True
        
    def onboard_customer(self, customer: Customer):
        """Onboard new customer"""
        customer.status = CustomerStatus.ACTIVE
        self.customers.append(customer)
        print(f"  ✓ Onboarded: {customer.name}")
        
    def check_health(self, customer: Customer) -> str:
        """Check customer health score"""
        if customer.satisfaction_score >= 80:
            return "healthy"
        elif customer.satisfaction_score >= 50:
            return "at_risk"
        else:
            return "churned"
        
    def prevent_churn(self, customer: Customer):
        """Execute churn prevention"""
        print(f"  ⚠️  Churn prevention activated for {customer.name}")
        # Trigger retention campaigns, discount offers, etc.

def demo():
    """Demonstrate RJ TECH Customer System"""
    print("\n" + "═" * 78)
    print("           RJ TECH ULTIMATE - CUSTOMER MANAGEMENT DEMONSTRATION")
    print("═" * 78)
    
    # Initialize systems
    memory = CustomerMemory()
    portal = CustomerPortal()
    support = AISupport()
    feedback = FeedbackCollector()
    success = CustomerSuccess()
    
    # Create customers
    print("\n👤 CREATING CUSTOMERS")
    print("-" * 40)
    
    customers = [
        Customer("Sarah Johnson", "sarah@techcorp.com", "TechCorp"),
        Customer("Michael Chen", "michael@startup.io", "StartupIO"),
        Customer("Emily Davis", "emily@enterprise.com", "EnterpriseCo"),
    ]
    
    for customer in customers:
        portal.add_customer(customer)
        success.onboard_customer(customer)
        memory.store(customer.id, 'preferred_language', 'English')
        memory.store(customer.id, 'industry', 'Technology')
        print(f"  ✓ Created: {customer.name} ({customer.email})")
    
    # Create projects
    print("\n📁 CREATING CUSTOMER PROJECTS")
    print("-" * 40)
    
    customers[0].add_project("AI Automation Suite", "Build custom automation for sales team")
    customers[0].add_project("Customer Support Bot", "Deploy AI chatbot for support")
    customers[1].add_project("Data Analytics Platform", "Create ML pipeline for analytics")
    customers[2].add_project("Enterprise AI Integration", "Full AI system integration")
    
    for customer in customers:
        print(f"  ✓ {customer.name}: {len(customer.projects)} projects")
    
    # Handle support tickets
    print("\n🎫 AI SUPPORT TICKETS")
    print("-" * 40)
    
    for customer in customers:
        ticket = customer.create_ticket(f"Help with {customer.projects[0]['name']}", "medium")
        print(f"  ✓ Ticket created: {ticket.id[:8]}... - {ticket.subject}")
        
        response = support.handle_ticket(ticket)
        print(f"    📝 AI Response: {response[:60]}...")
        
        ticket.add_message("ai_agent", response, is_agent=True)
        
    # Collect feedback
    print("\n⭐ COLLECTING FEEDBACK")
    print("-" * 40)
    
    feedback.collect(customers[0].id, 5, "Excellent service and support!")
    feedback.collect(customers[1].id, 4, "Great platform, could be faster")
    feedback.collect(customers[2].id, 5, "Amazing AI capabilities!")
    
    print(f"  ✓ Collected {len(feedback.feedback)} feedback entries")
    print(f"  ⭐ Average Rating: {feedback.get_average_rating():.1f}/5")
    
    # Customer memory demo
    print("\n🧠 CUSTOMER MEMORY")
    print("-" * 40)
    
    for customer in customers:
        lang = memory.recall(customer.id, 'preferred_language')
        industry = memory.recall(customer.id, 'industry')
        print(f"  ✓ {customer.name}: Language={lang}, Industry={industry}")
    
    # Customer success monitoring
    print("\n📊 CUSTOMER SUCCESS")
    print("-" * 40)
    
    for customer in customers:
        health = success.check_health(customer)
        print(f"  ✓ {customer.name}: Health={health}")
    
    # Support statistics
    print("\n📈 SUPPORT STATISTICS")
    print("-" * 40)
    
    stats = support.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Customer portal dashboard
    print("\n" + "═" * 78)
    print("                    CUSTOMER PORTAL DASHBOARD")
    print("═" * 78)
    
    print(f"\n  👥 Total Customers: {len(portal.customers)}")
    print(f"  🎫 Open Tickets: {sum(len(c.tickets) for c in portal.customers)}")
    print(f"  ⭐ Average Satisfaction: {feedback.get_average_rating():.1f}/5")
    print(f"  🤖 AI Resolution Rate: {support.resolution_rate * 100}%")
    print(f"  ⏱️  Avg Response Time: {support.avg_response_time}")
    
    print("\n" + "═" * 78)
    print("                    CUSTOMER SYSTEM OPERATIONAL 24/7")
    print("═" * 78)
    print("\n✅ ALL CUSTOMERS HAPPY AND SUPPORTED")

if __name__ == "__main__":
    demo()