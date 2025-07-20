"""
Smart component naming utility that generates meaningful names without numbers.
"""

import re
from typing import List, Dict, Any, Optional

class ComponentNamer:
    """Generates meaningful component names based on content and purpose."""
    
    def __init__(self):
        # Common UI patterns and their suggested names
        self.ui_patterns = {
            'login': ['LoginForm', 'SignInPage', 'AuthenticationPage', 'UserLogin'],
            'signup': ['SignUpForm', 'RegistrationPage', 'CreateAccount', 'UserRegistration'],
            'dashboard': ['Dashboard', 'AdminPanel', 'ControlPanel', 'MainDashboard'],
            'profile': ['UserProfile', 'ProfilePage', 'AccountSettings', 'UserAccount'],
            'settings': ['SettingsPage', 'Configuration', 'Preferences', 'UserSettings'],
            'home': ['HomePage', 'LandingPage', 'MainPage', 'WelcomePage'],
            'about': ['AboutPage', 'AboutUs', 'CompanyInfo', 'AboutSection'],
            'contact': ['ContactPage', 'ContactForm', 'GetInTouch', 'ContactUs'],
            'product': ['ProductPage', 'ProductDetails', 'ProductCatalog', 'ProductListing'],
            'cart': ['ShoppingCart', 'CartPage', 'CheckoutCart', 'OrderSummary'],
            'checkout': ['CheckoutPage', 'PaymentForm', 'OrderCheckout', 'PurchaseForm'],
            'search': ['SearchPage', 'SearchResults', 'FindResults', 'SearchInterface'],
            'list': ['ItemList', 'DataTable', 'ContentList', 'RecordList'],
            'form': ['DataForm', 'InputForm', 'SubmissionForm', 'UserForm'],
            'nav': ['Navigation', 'NavBar', 'MenuBar', 'SiteNavigation'],
            'header': ['PageHeader', 'SiteHeader', 'TopHeader', 'MainHeader'],
            'footer': ['PageFooter', 'SiteFooter', 'BottomFooter', 'MainFooter'],
            'sidebar': ['Sidebar', 'SidePanel', 'NavigationPanel', 'MenuPanel'],
            'modal': ['ModalDialog', 'PopupModal', 'DialogBox', 'OverlayModal'],
            'card': ['InfoCard', 'ContentCard', 'DisplayCard', 'DataCard'],
            'table': ['DataTable', 'InfoTable', 'ContentTable', 'RecordTable'],
            'chart': ['DataChart', 'Analytics', 'ChartDisplay', 'GraphView'],
            'gallery': ['ImageGallery', 'PhotoGallery', 'MediaGallery', 'ContentGallery'],
            'blog': ['BlogPage', 'ArticlePage', 'BlogPost', 'ContentPage'],
            'news': ['NewsPage', 'NewsFeed', 'ArticleList', 'NewsSection'],
            'admin': ['AdminPanel', 'AdminDashboard', 'ManagementPanel', 'AdminInterface'],
            'user': ['UserInterface', 'UserPanel', 'UserDashboard', 'UserSection'],
            'report': ['ReportPage', 'Analytics', 'DataReport', 'ReportDashboard'],
            'calendar': ['CalendarView', 'EventCalendar', 'ScheduleView', 'DatePicker'],
            'chat': ['ChatInterface', 'MessagePanel', 'ConversationView', 'ChatWindow'],
            'notification': ['NotificationPanel', 'AlertCenter', 'MessageCenter', 'NotificationHub']
        }
        
        # Element-based naming
        self.element_patterns = {
            'button': 'ActionPage',
            'form': 'FormPage', 
            'table': 'DataTable',
            'card': 'InfoCard',
            'navbar': 'Navigation',
            'header': 'HeaderSection',
            'footer': 'FooterSection',
            'sidebar': 'SidePanel',
            'modal': 'DialogPage',
            'input': 'InputForm',
            'image': 'MediaPage',
            'video': 'VideoPage',
            'text': 'ContentPage',
            'list': 'ListPage',
            'grid': 'GridLayout',
            'menu': 'MenuPage',
            'tab': 'TabbedView',
            'accordion': 'AccordionView',
            'carousel': 'CarouselView',
            'slider': 'SliderView'
        }
        
        # Fallback names for different screen types
        self.fallback_names = [
            'MainPage', 'ContentPage', 'DisplayPage', 'InterfacePage',
            'ViewPage', 'ScreenPage', 'PanelPage', 'SectionPage',
            'LayoutPage', 'ComponentPage', 'FeaturePage', 'ModulePage'
        ]
        
        self.used_names = set()
    
    def clean_filename(self, filename: str) -> str:
        """Clean filename by removing numbers, extensions, and special characters."""
        # Remove file extension
        name = re.sub(r'\.[^.]+$', '', filename.lower())
        
        # Remove numbers
        name = re.sub(r'\d+', '', name)
        
        # Remove special characters and replace with spaces
        name = re.sub(r'[_\-\.]', ' ', name)
        
        # Remove extra spaces
        name = re.sub(r'\s+', ' ', name).strip()
        
        return name
    
    def analyze_elements(self, elements: List[Dict[str, Any]]) -> List[str]:
        """Analyze UI elements to suggest component type."""
        element_types = []
        
        for element in elements:
            element_type = element.get('type', '').lower()
            if element_type:
                element_types.append(element_type)
        
        return element_types
    
    def generate_component_name(self, 
                              filename: str, 
                              elements: Optional[List[Dict[str, Any]]] = None,
                              project_description: str = "") -> str:
        """Generate a meaningful component name without numbers."""
        
        # Clean the filename
        clean_name = self.clean_filename(filename)
        
        # Try to match with UI patterns
        for pattern, names in self.ui_patterns.items():
            if pattern in clean_name.lower():
                for name in names:
                    if name not in self.used_names:
                        self.used_names.add(name)
                        return name
        
        # Analyze elements if provided
        if elements:
            element_types = self.analyze_elements(elements)
            
            # Look for dominant element types
            element_counts = {}
            for elem_type in element_types:
                element_counts[elem_type] = element_counts.get(elem_type, 0) + 1
            
            if element_counts:
                # Get most common element type
                dominant_element = max(element_counts.keys(), key=lambda k: element_counts[k])
                
                # Generate name based on dominant element
                if dominant_element in self.element_patterns:
                    base_name = self.element_patterns[dominant_element]
                    if base_name not in self.used_names:
                        self.used_names.add(base_name)
                        return base_name
        
        # Try to extract meaningful words from filename
        words = clean_name.split()
        meaningful_words = []
        
        for word in words:
            if len(word) > 2 and word not in ['img', 'pic', 'image', 'screen', 'page']:
                meaningful_words.append(word.title())
        
        if meaningful_words:
            # Create name from meaningful words
            if len(meaningful_words) == 1:
                candidate_name = meaningful_words[0] + 'Page'
            else:
                candidate_name = ''.join(meaningful_words[:2]) + 'Page'
            
            if candidate_name not in self.used_names:
                self.used_names.add(candidate_name)
                return candidate_name
        
        # Use project description hints
        if project_description:
            desc_lower = project_description.lower()
            for pattern, names in self.ui_patterns.items():
                if pattern in desc_lower:
                    for name in names:
                        if name not in self.used_names:
                            self.used_names.add(name)
                            return name
        
        # Fallback to generic but meaningful names
        for fallback_name in self.fallback_names:
            if fallback_name not in self.used_names:
                self.used_names.add(fallback_name)
                return fallback_name
        
        # Final fallback with suffix
        base_name = 'GeneratedPage'
        counter = 1
        while f"{base_name}{self._number_to_word(counter)}" in self.used_names:
            counter += 1
        
        final_name = f"{base_name}{self._number_to_word(counter)}"
        self.used_names.add(final_name)
        return final_name
    
    def _number_to_word(self, num: int) -> str:
        """Convert number to word to avoid numbers in component names."""
        words = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten']
        if num < len(words):
            return words[num]
        else:
            return f"Number{num}"
    
    def reset_used_names(self):
        """Reset the used names set for a new project."""
        self.used_names.clear()

# Global instance
component_namer = ComponentNamer()

def generate_smart_component_name(filename: str, 
                                elements: Optional[List[Dict[str, Any]]] = None,
                                project_description: str = "") -> str:
    """Generate a smart component name without numbers."""
    return component_namer.generate_component_name(filename, elements, project_description)

def reset_component_names():
    """Reset component names for a new project."""
    component_namer.reset_used_names()
