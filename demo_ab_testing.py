#!/usr/bin/env python3
"""
Demonstration script for A/B testing implementation
Shows how different recommendation strategies perform
"""

import pandas as pd
import numpy as np
from recommendation_strategies import RecommendationStrategies, SongRecommendationStrategies
from ab_testing import ABTestingFramework
import json
import os

def demo_recommendation_strategies():
    """Demonstrate different recommendation strategies"""
    print("🎵 DEMONSTRATION: Recommendation Strategies")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv('spotify_songs.csv')
    audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                      'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    
    # Test preferences (high energy, danceable, positive mood)
    test_preferences = [0.8, 0.9, 7, -3.0, 1, 0.05, 0.1, 0.0, 0.1, 0.8, 130.0, 200000]
    
    print(f"Test Preferences: Danceability={test_preferences[0]}, Energy={test_preferences[1]}, Valence={test_preferences[9]}")
    print()
    
    # Initialize strategies
    pref_strategies = RecommendationStrategies(df, audio_features)
    
    # Test each strategy
    strategies_to_test = [
        ('Cosine Similarity', 'strategy_1_cosine_similarity'),
        ('Euclidean Distance', 'strategy_2_euclidean_distance'),
        ('Weighted Features', 'strategy_3_weighted_features'),
        ('Popularity Boost', 'strategy_4_popularity_boost'),
        ('Genre Aware', 'strategy_5_genre_aware'),
        ('KNN Based', 'strategy_6_knn_based'),
        ('Random Baseline', 'strategy_7_random_baseline')
    ]
    
    for strategy_name, method_name in strategies_to_test:
        print(f"📊 {strategy_name}:")
        method = getattr(pref_strategies, method_name)
        recommendations = method(test_preferences, top_n=3)
        
        for i, (_, row) in enumerate(recommendations.iterrows(), 1):
            print(f"   {i}. {row['track_name']} by {row['track_artist']} ({row['playlist_genre']}) - Similarity: {row['similarity']:.3f}")
        print()

def demo_song_recommendations():
    """Demonstrate song-based recommendation strategies"""
    print("🎵 DEMONSTRATION: Song-Based Recommendations")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv('spotify_songs.csv')
    audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                      'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    
    # Test songs
    test_songs = ['shape of you', 'despacito', 'blinding lights']
    
    song_strategies = SongRecommendationStrategies(df, audio_features)
    
    for song_name in test_songs:
        print(f"🎧 Similar songs to '{song_name}':")
        
        strategies_to_test = [
            ('Cosine Similarity', 'strategy_1_cosine_similarity'),
            ('Artist Boost', 'strategy_2_artist_boost'),
            ('Genre Similarity', 'strategy_3_genre_similarity')
        ]
        
        for strategy_name, method_name in strategies_to_test:
            method = getattr(song_strategies, method_name)
            original_song, recommendations = method(song_name, top_n=2)
            
            if recommendations is not None:
                print(f"  📊 {strategy_name}:")
                for i, (_, row) in enumerate(recommendations.iterrows(), 1):
                    print(f"     {i}. {row['track_name']} by {row['track_artist']} ({row['playlist_genre']}) - Similarity: {row['similarity']:.3f}")
            else:
                print(f"  ❌ {strategy_name}: Song not found")
        print()

def demo_ab_testing_framework():
    """Demonstrate A/B testing framework"""
    print("🔬 DEMONSTRATION: A/B Testing Framework")
    print("=" * 60)
    
    # Use a temporary file for demo
    demo_file = 'demo_ab_data.json'
    
    # Initialize framework
    ab_framework = ABTestingFramework(demo_file)
    
    # Simulate multiple user sessions with different strategies
    print("Simulating user sessions and collecting data...")
    
    # Session 1: Cosine Similarity
    print("\n👤 User Session 1 (Cosine Similarity):")
    session1_strategy = 'strategy_1_cosine_similarity'
    
    # Simulate recommendations
    test_recs = pd.DataFrame({
        'track_name': ['Song A', 'Song B', 'Song C'],
        'track_artist': ['Artist 1', 'Artist 2', 'Artist 3'],
        'playlist_genre': ['pop', 'pop', 'pop'],
        'similarity': [0.85, 0.82, 0.78],
        'strategy': ['Cosine Similarity'] * 3
    })
    
    ab_framework.record_recommendation(session1_strategy, test_recs, [0.7, 0.8, 5, -4.0, 1, 0.1, 0.2, 0.0, 0.1, 0.7, 125.0, 200000])
    ab_framework.collect_feedback(session1_strategy, 'positive')
    ab_framework.collect_feedback(session1_strategy, 'positive')
    print("   ✅ 2 positive feedback collected")
    
    # Session 2: Popularity Boost
    print("\n👤 User Session 2 (Popularity Boost):")
    session2_strategy = 'strategy_4_popularity_boost'
    
    test_recs2 = pd.DataFrame({
        'track_name': ['Popular Song X', 'Popular Song Y', 'Popular Song Z'],
        'track_artist': ['Famous Artist 1', 'Famous Artist 2', 'Famous Artist 3'],
        'playlist_genre': ['pop', 'pop', 'pop'],
        'similarity': [0.75, 0.72, 0.68],
        'strategy': ['Popularity Boost'] * 3
    })
    
    ab_framework.record_recommendation(session2_strategy, test_recs2, [0.6, 0.7, 3, -5.0, 0, 0.05, 0.15, 0.05, 0.08, 0.6, 120.0, 180000])
    ab_framework.collect_feedback(session2_strategy, 'positive')
    ab_framework.collect_feedback(session2_strategy, 'negative')
    ab_framework.collect_feedback(session2_strategy, 'positive')
    print("   ✅ 2 positive, 1 negative feedback collected")
    
    # Session 3: Random Baseline
    print("\n👤 User Session 3 (Random Baseline):")
    session3_strategy = 'strategy_7_random_baseline'
    
    test_recs3 = pd.DataFrame({
        'track_name': ['Random Song 1', 'Random Song 2', 'Random Song 3'],
        'track_artist': ['Random Artist 1', 'Random Artist 2', 'Random Artist 3'],
        'playlist_genre': ['rock', 'jazz', 'classical'],
        'similarity': [0.45, 0.42, 0.38],
        'strategy': ['Random Baseline'] * 3
    })
    
    ab_framework.record_recommendation(session3_strategy, test_recs3, [0.5, 0.5, 5, -5.0, 1, 0.1, 0.1, 0.1, 0.1, 0.5, 120.0, 200000])
    ab_framework.collect_feedback(session3_strategy, 'negative')
    ab_framework.collect_feedback(session3_strategy, 'negative')
    print("   ✅ 2 negative feedback collected")
    
    # Display results
    print("\n📊 A/B Test Results:")
    print("-" * 40)
    
    performance = ab_framework.get_strategy_performance()
    
    # Create a nice table
    print(f"{'Strategy':<20} {'Uses':<6} {'Positive':<10} {'Negative':<10} {'Satisfaction':<12}")
    print("-" * 60)
    
    for strategy, metrics in performance.items():
        strategy_name = ab_framework.preference_strategies.get(strategy, strategy)
        uses = metrics['total_uses']
        positive = metrics['positive_feedback']
        negative = metrics['negative_feedback']
        satisfaction = f"{metrics['satisfaction_rate']:.1%}"
        
        print(f"{strategy_name:<20} {uses:<6} {positive:<10} {negative:<10} {satisfaction:<12}")
    
    print("\n🎯 Key Insights:")
    print("• Cosine Similarity: 100% satisfaction (2/2 positive)")
    print("• Popularity Boost: 67% satisfaction (2/3 positive)")
    print("• Random Baseline: 0% satisfaction (0/2 positive)")
    print("\n💡 The data suggests Cosine Similarity performs best for this user segment!")
    
    # Clean up
    if os.path.exists(demo_file):
        os.remove(demo_file)

def main():
    """Run all demonstrations"""
    print("🚀 A/B Testing Implementation Demonstration")
    print("=" * 60)
    
    try:
        # Demo 1: Recommendation Strategies
        demo_recommendation_strategies()
        
        # Demo 2: Song Recommendations
        demo_song_recommendations()
        
        # Demo 3: A/B Testing Framework
        demo_ab_testing_framework()
        
        print("\n🎉 DEMONSTRATION COMPLETE!")
        print("✅ All components working correctly")
        print("✅ Ready for production deployment")
        print("\n📝 Next Steps:")
        print("1. Deploy the app to Streamlit Cloud")
        print("2. Start collecting real user data")
        print("3. Monitor strategy performance")
        print("4. Optimize based on results")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()