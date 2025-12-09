from models.VisitorModel import VisitorModel

class VisitorController:
    def __init__(self):
        self.visitor_model = VisitorModel()

    def track_visit(self, page_title=''):
        """Track page visit"""
        try:
            # Get current page URL
            import streamlit as st
            page_url = st.experimental_get_query_params()
            page_url_str = str(page_url)
            
            # Record visit
            self.visitor_model.record_visit(page_url_str)
            
            # Update popular pages if page title provided
            if page_title:
                self.visitor_model.update_popular_page(page_url_str, page_title)
                
            return True
        except Exception as e:
            print(f"Tracking error: {e}")
            return False

    def get_visitor_stats(self):
        """Get all visitor statistics"""
        try:
            return {
                'today': self.visitor_model.get_today_visitors(),
                'month': self.visitor_model.get_month_visitors(),
                'online': self.visitor_model.get_online_visitors(),
                'popular_pages': self.visitor_model.get_today_popular_pages()
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {
                'today': 0,
                'month': 0,
                'online': 0,
                'popular_pages': []
            }