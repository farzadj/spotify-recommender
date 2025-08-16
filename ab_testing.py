import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import uuid
from recommendation_strategies import RecommendationStrategies, SongRecommendationStrategies

class ABTestingFramework:
    """A/B Testing framework for recommendation strategies"""
    
    def __init__(self, data_file="ab_test_data.json"):
        self.data_file = data_file
        self.load_test_data()
        
        # Define test configurations
        self.preference_strategies = {
            'strategy_1_cosine_similarity': 'Cosine Similarity',
            'strategy_2_euclidean_distance': 'Euclidean Distance', 
            'strategy_3_weighted_features': 'Weighted Features',
            'strategy_4_popularity_boost': 'Popularity Boost',
            'strategy_5_genre_aware': 'Genre Aware',
            'strategy_6_knn_based': 'KNN Based',
            'strategy_7_random_baseline': 'Random Baseline'
        }
        
        self.song_strategies = {
            'strategy_1_cosine_similarity': 'Cosine Similarity',
            'strategy_2_artist_boost': 'Artist Boost',
            'strategy_3_genre_similarity': 'Genre Similarity'
        }
    
    def load_test_data(self):
        """Load existing test data or create new file"""
        if os.path.exists(self.data_file) and os.path.getsize(self.data_file) > 0:
            try:
                with open(self.data_file, 'r') as f:
                    self.test_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                # If file is corrupted or empty, initialize with default data
                self.test_data = {
                    'sessions': {},
                    'feedback': {},
                    'metrics': {
                        'total_sessions': 0,
                        'total_recommendations': 0,
                        'strategy_performance': {}
                    }
                }
        else:
            self.test_data = {
                'sessions': {},
                'feedback': {},
                'metrics': {
                    'total_sessions': 0,
                    'total_recommendations': 0,
                    'strategy_performance': {}
                }
            }
    
    def save_test_data(self):
        """Save test data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.test_data, f, indent=2)
    
    def get_user_session(self):
        """Get or create user session ID"""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.session_start = datetime.now().isoformat()
            
            # Initialize session data
            self.test_data['sessions'][st.session_state.session_id] = {
                'start_time': st.session_state.session_start,
                'recommendations': [],
                'feedback': []
            }
            self.save_test_data()
        
        return st.session_state.session_id
    
    def assign_strategy(self, mode="preferences"):
        """Assign a strategy to the current user session"""
        session_id = self.get_user_session()
        
        # Simple random assignment (can be improved with more sophisticated methods)
        if mode == "preferences":
            strategies = list(self.preference_strategies.keys())
        else:
            strategies = list(self.song_strategies.keys())
        
        # Use session ID to ensure consistent assignment
        strategy_index = hash(session_id) % len(strategies)
        assigned_strategy = strategies[strategy_index]
        
        return assigned_strategy
    
    def record_recommendation(self, strategy, recommendations, user_input=None):
        """Record a recommendation event"""
        session_id = self.get_user_session()
        
        recommendation_event = {
            'timestamp': datetime.now().isoformat(),
            'strategy': strategy,
            'recommendations_count': len(recommendations),
            'user_input': user_input,
            'top_recommendations': recommendations.head(3).to_dict('records') if len(recommendations) > 0 else []
        }
        
        self.test_data['sessions'][session_id]['recommendations'].append(recommendation_event)
        self.test_data['metrics']['total_recommendations'] += 1
        
        # Update strategy performance metrics
        if strategy not in self.test_data['metrics']['strategy_performance']:
            self.test_data['metrics']['strategy_performance'][strategy] = {
                'total_uses': 0,
                'avg_recommendations_per_use': 0,
                'user_feedback': []
            }
        
        self.test_data['metrics']['strategy_performance'][strategy]['total_uses'] += 1
        
        self.save_test_data()
    
    def collect_feedback(self, strategy, feedback_type, feedback_value=None):
        """Collect user feedback on recommendations"""
        session_id = self.get_user_session()
        
        feedback_event = {
            'timestamp': datetime.now().isoformat(),
            'strategy': strategy,
            'feedback_type': feedback_type,
            'feedback_value': feedback_value
        }
        
        self.test_data['sessions'][session_id]['feedback'].append(feedback_event)
        
        # Update strategy performance
        if strategy in self.test_data['metrics']['strategy_performance']:
            self.test_data['metrics']['strategy_performance'][strategy]['user_feedback'].append(feedback_event)
        
        self.save_test_data()
    
    def get_strategy_performance(self):
        """Get performance metrics for all strategies"""
        performance = {}
        
        for strategy, metrics in self.test_data['metrics']['strategy_performance'].items():
            total_uses = metrics['total_uses']
            feedback = metrics['user_feedback']
            
            # Calculate feedback scores
            positive_feedback = len([f for f in feedback if f.get('feedback_type') == 'positive'])
            negative_feedback = len([f for f in feedback if f.get('feedback_type') == 'negative'])
            
            satisfaction_rate = positive_feedback / (positive_feedback + negative_feedback) if (positive_feedback + negative_feedback) > 0 else 0
            
            performance[strategy] = {
                'total_uses': total_uses,
                'positive_feedback': positive_feedback,
                'negative_feedback': negative_feedback,
                'satisfaction_rate': satisfaction_rate,
                'avg_recommendations': metrics.get('avg_recommendations_per_use', 0)
            }
        
        return performance
    
    def display_ab_test_results(self):
        """Display A/B test results in Streamlit"""
        st.subheader("📊 A/B Test Results")
        
        performance = self.get_strategy_performance()
        
        if not performance:
            st.info("No A/B test data available yet. Start using the app to collect data!")
            return
        
        # Create performance DataFrame
        df_performance = pd.DataFrame.from_dict(performance, orient='index')
        df_performance['strategy_name'] = df_performance.index.map(
            {**self.preference_strategies, **self.song_strategies}
        )
        
        # Display summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sessions", self.test_data['metrics']['total_sessions'])
        with col2:
            st.metric("Total Recommendations", self.test_data['metrics']['total_recommendations'])
        with col3:
            avg_satisfaction = df_performance['satisfaction_rate'].mean()
            st.metric("Avg Satisfaction Rate", f"{avg_satisfaction:.2%}")
        
        # Display strategy performance
        st.subheader("Strategy Performance")
        
        # Sort by satisfaction rate
        df_performance = df_performance.sort_values('satisfaction_rate', ascending=False)
        
        # Display as a table
        display_df = df_performance[['strategy_name', 'total_uses', 'positive_feedback', 
                                   'negative_feedback', 'satisfaction_rate']].copy()
        display_df['satisfaction_rate'] = display_df['satisfaction_rate'].apply(lambda x: f"{x:.2%}")
        
        st.dataframe(display_df, use_container_width=True)
        
        # Create visualizations
        if len(df_performance) > 1:
            st.subheader("Performance Charts")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.bar_chart(df_performance.set_index('strategy_name')['satisfaction_rate'])
                st.caption("Satisfaction Rate by Strategy")
            
            with col2:
                st.bar_chart(df_performance.set_index('strategy_name')['total_uses'])
                st.caption("Total Uses by Strategy")
    
    def reset_test_data(self):
        """Reset all test data (for development/testing)"""
        self.test_data = {
            'sessions': {},
            'feedback': {},
            'metrics': {
                'total_sessions': 0,
                'total_recommendations': 0,
                'strategy_performance': {}
            }
        }
        self.save_test_data()
        st.success("A/B test data has been reset!")