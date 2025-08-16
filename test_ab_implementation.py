#!/usr/bin/env python3
"""
Comprehensive test script for A/B testing implementation
Tests all recommendation strategies, data collection, and analytics
"""

import pandas as pd
import numpy as np
import json
import os
import tempfile
from datetime import datetime
import uuid

# Import our modules
from recommendation_strategies import RecommendationStrategies, SongRecommendationStrategies
from ab_testing import ABTestingFramework

def test_recommendation_strategies():
    """Test all recommendation strategies"""
    print("🧪 Testing Recommendation Strategies...")
    
    # Load data
    df = pd.read_csv('spotify_songs.csv')
    audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                      'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    
    # Test preference strategies
    pref_strategies = RecommendationStrategies(df, audio_features)
    test_preferences = [0.5, 0.7, 5, -5.0, 1, 0.1, 0.2, 0.0, 0.1, 0.6, 120.0, 200000]
    
    preference_strategies = [
        'strategy_1_cosine_similarity',
        'strategy_2_euclidean_distance', 
        'strategy_3_weighted_features',
        'strategy_4_popularity_boost',
        'strategy_5_genre_aware',
        'strategy_6_knn_based',
        'strategy_7_random_baseline'
    ]
    
    results = {}
    for strategy_name in preference_strategies:
        try:
            method = getattr(pref_strategies, strategy_name)
            recommendations = method(test_preferences, top_n=5)
            
            # Validate results
            assert len(recommendations) == 5, f"{strategy_name}: Expected 5 recommendations, got {len(recommendations)}"
            assert 'track_name' in recommendations.columns, f"{strategy_name}: Missing track_name column"
            assert 'track_artist' in recommendations.columns, f"{strategy_name}: Missing track_artist column"
            assert 'similarity' in recommendations.columns, f"{strategy_name}: Missing similarity column"
            assert 'strategy' in recommendations.columns, f"{strategy_name}: Missing strategy column"
            
            results[strategy_name] = {
                'count': len(recommendations),
                'sample_song': recommendations.iloc[0].track_name,
                'sample_artist': recommendations.iloc[0].track_artist,
                'avg_similarity': recommendations['similarity'].mean()
            }
            print(f"  ✅ {strategy_name}: {len(recommendations)} recommendations")
            
        except Exception as e:
            print(f"  ❌ {strategy_name}: Error - {str(e)}")
            return False
    
    # Test song strategies
    song_strategies = SongRecommendationStrategies(df, audio_features)
    song_test_cases = ['shape of you', 'despacito', 'blinding lights']
    
    song_strategy_names = [
        'strategy_1_cosine_similarity',
        'strategy_2_artist_boost', 
        'strategy_3_genre_similarity'
    ]
    
    for song_name in song_test_cases:
        for strategy_name in song_strategy_names:
            try:
                method = getattr(song_strategies, strategy_name)
                original_song, recommendations = method(song_name, top_n=5)
                
                if recommendations is not None:
                    assert len(recommendations) == 5, f"{strategy_name} for '{song_name}': Expected 5 recommendations"
                    assert 'track_name' in recommendations.columns, f"{strategy_name}: Missing track_name column"
                    print(f"  ✅ {strategy_name} for '{song_name}': {len(recommendations)} recommendations")
                else:
                    print(f"  ⚠️  {strategy_name} for '{song_name}': No recommendations (song not found)")
                    
            except Exception as e:
                print(f"  ❌ {strategy_name} for '{song_name}': Error - {str(e)}")
                return False
    
    print("✅ All recommendation strategies working correctly!")
    return True

def test_ab_testing_framework():
    """Test A/B testing framework functionality"""
    print("\n🧪 Testing A/B Testing Framework...")
    
    # Use temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        # Initialize framework
        ab_framework = ABTestingFramework(temp_file)
        
        # Test 1: Session management
        print("  1. Testing session management...")
        # Mock session state for testing
        import streamlit as st
        if not hasattr(st, 'session_state'):
            st.session_state = {}
        
        session_id = ab_framework.get_user_session()
        assert isinstance(session_id, str), "Session ID should be a string"
        assert len(session_id) > 0, "Session ID should not be empty"
        print(f"     ✅ Session ID generated: {session_id[:8]}...")
        
        # Test 2: Strategy assignment
        print("  2. Testing strategy assignment...")
        pref_strategy = ab_framework.assign_strategy('preferences')
        song_strategy = ab_framework.assign_strategy('song')
        
        assert pref_strategy in ab_framework.preference_strategies, f"Invalid preference strategy: {pref_strategy}"
        assert song_strategy in ab_framework.song_strategies, f"Invalid song strategy: {song_strategy}"
        print(f"     ✅ Preference strategy: {pref_strategy}")
        print(f"     ✅ Song strategy: {song_strategy}")
        
        # Test 3: Data recording
        print("  3. Testing data recording...")
        test_recommendations = pd.DataFrame({
            'track_name': ['Test Song 1', 'Test Song 2', 'Test Song 3'],
            'track_artist': ['Artist 1', 'Artist 2', 'Artist 3'],
            'playlist_genre': ['pop', 'rock', 'jazz'],
            'similarity': [0.8, 0.7, 0.6],
            'strategy': ['test_strategy', 'test_strategy', 'test_strategy']
        })
        
        ab_framework.record_recommendation(pref_strategy, test_recommendations, [0.5, 0.7, 5, -5.0, 1, 0.1, 0.2, 0.0, 0.1, 0.6, 120.0, 200000])
        
        # Verify data was recorded
        with open(temp_file, 'r') as f:
            data = json.load(f)
        
        assert 'sessions' in data, "Sessions data not found"
        assert session_id in data['sessions'], "Session data not recorded"
        assert len(data['sessions'][session_id]['recommendations']) > 0, "Recommendation not recorded"
        print("     ✅ Recommendation data recorded successfully")
        
        # Test 4: Feedback collection
        print("  4. Testing feedback collection...")
        ab_framework.collect_feedback(pref_strategy, 'positive')
        ab_framework.collect_feedback(pref_strategy, 'negative')
        ab_framework.collect_feedback(pref_strategy, 'positive')
        
        # Verify feedback was recorded
        with open(temp_file, 'r') as f:
            data = json.load(f)
        
        feedback_count = len(data['sessions'][session_id]['feedback'])
        assert feedback_count == 3, f"Expected 3 feedback entries, got {feedback_count}"
        print(f"     ✅ {feedback_count} feedback entries recorded")
        
        # Test 5: Performance metrics
        print("  5. Testing performance metrics...")
        performance = ab_framework.get_strategy_performance()
        
        assert isinstance(performance, dict), "Performance should be a dictionary"
        assert pref_strategy in performance, f"Strategy {pref_strategy} not in performance data"
        
        strategy_perf = performance[pref_strategy]
        assert 'total_uses' in strategy_perf, "Missing total_uses in performance data"
        assert 'satisfaction_rate' in strategy_perf, "Missing satisfaction_rate in performance data"
        assert strategy_perf['total_uses'] == 1, f"Expected 1 use, got {strategy_perf['total_uses']}"
        assert strategy_perf['positive_feedback'] == 2, f"Expected 2 positive feedback, got {strategy_perf['positive_feedback']}"
        assert strategy_perf['negative_feedback'] == 1, f"Expected 1 negative feedback, got {strategy_perf['negative_feedback']}"
        assert strategy_perf['satisfaction_rate'] == 2/3, f"Expected satisfaction rate 2/3, got {strategy_perf['satisfaction_rate']}"
        
        print(f"     ✅ Performance metrics calculated correctly")
        print(f"        - Total uses: {strategy_perf['total_uses']}")
        print(f"        - Positive feedback: {strategy_perf['positive_feedback']}")
        print(f"        - Negative feedback: {strategy_perf['negative_feedback']}")
        print(f"        - Satisfaction rate: {strategy_perf['satisfaction_rate']:.2%}")
        
        # Test 6: Multiple sessions
        print("  6. Testing multiple sessions...")
        # Simulate different session
        original_session_id = ab_framework.get_user_session()
        ab_framework.test_data['sessions']['test_session_2'] = {
            'start_time': datetime.now().isoformat(),
            'recommendations': [],
            'feedback': []
        }
        
        # Add some test data for second session
        ab_framework.record_recommendation('strategy_2_euclidean_distance', test_recommendations, [0.3, 0.8, 3, -3.0, 0, 0.05, 0.1, 0.1, 0.05, 0.4, 140.0, 180000])
        ab_framework.collect_feedback('strategy_2_euclidean_distance', 'positive')
        ab_framework.collect_feedback('strategy_2_euclidean_distance', 'positive')
        
        # Check performance with multiple strategies
        performance = ab_framework.get_strategy_performance()
        assert len(performance) == 2, f"Expected 2 strategies in performance, got {len(performance)}"
        print(f"     ✅ Multiple sessions and strategies working correctly")
        
        print("✅ A/B testing framework working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ A/B testing framework test failed: {str(e)}")
        return False
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)

def test_data_consistency():
    """Test data consistency and edge cases"""
    print("\n🧪 Testing Data Consistency...")
    
    # Load data
    df = pd.read_csv('spotify_songs.csv')
    audio_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                      'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    
    # Test edge cases
    pref_strategies = RecommendationStrategies(df, audio_features)
    
    # Test 1: Extreme preference values
    print("  1. Testing extreme preference values...")
    extreme_preferences = [0.0, 0.0, 0, -60.0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 50.0, 60000]
    try:
        results = pref_strategies.strategy_1_cosine_similarity(extreme_preferences, top_n=3)
        assert len(results) == 3, "Should return 3 recommendations even with extreme values"
        print("     ✅ Extreme values handled correctly")
    except Exception as e:
        print(f"     ❌ Error with extreme values: {str(e)}")
        return False
    
    # Test 2: Maximum preference values
    print("  2. Testing maximum preference values...")
    max_preferences = [1.0, 1.0, 11, 0.0, 1, 1.0, 1.0, 1.0, 1.0, 1.0, 200.0, 400000]
    try:
        results = pref_strategies.strategy_1_cosine_similarity(max_preferences, top_n=3)
        assert len(results) == 3, "Should return 3 recommendations with maximum values"
        print("     ✅ Maximum values handled correctly")
    except Exception as e:
        print(f"     ❌ Error with maximum values: {str(e)}")
        return False
    
    # Test 3: Song not found
    print("  3. Testing song not found...")
    song_strategies = SongRecommendationStrategies(df, audio_features)
    try:
        song_used, recs = song_strategies.strategy_1_cosine_similarity("nonexistent_song_xyz123", top_n=3)
        assert recs is None, "Should return None for non-existent song"
        print("     ✅ Non-existent song handled correctly")
    except Exception as e:
        print(f"     ❌ Error with non-existent song: {str(e)}")
        return False
    
    # Test 4: Empty string input
    print("  4. Testing empty string input...")
    try:
        song_used, recs = song_strategies.strategy_1_cosine_similarity("", top_n=3)
        # Should either return None or handle gracefully
        print("     ✅ Empty string handled correctly")
    except Exception as e:
        print(f"     ❌ Error with empty string: {str(e)}")
        return False
    
    print("✅ Data consistency tests passed!")
    return True

def test_performance_metrics():
    """Test performance metrics calculations"""
    print("\n🧪 Testing Performance Metrics...")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        # Mock session state for testing
        import streamlit as st
        if not hasattr(st, 'session_state'):
            st.session_state = {}
        
        ab_framework = ABTestingFramework(temp_file)
        
        # Create test data with known values
        test_data = {
            'sessions': {
                'session1': {
                    'start_time': datetime.now().isoformat(),
                    'recommendations': [
                        {'strategy': 'strategy_1', 'timestamp': datetime.now().isoformat()}
                    ],
                    'feedback': [
                        {'strategy': 'strategy_1', 'feedback_type': 'positive'},
                        {'strategy': 'strategy_1', 'feedback_type': 'positive'},
                        {'strategy': 'strategy_1', 'feedback_type': 'negative'}
                    ]
                },
                'session2': {
                    'start_time': datetime.now().isoformat(),
                    'recommendations': [
                        {'strategy': 'strategy_2', 'timestamp': datetime.now().isoformat()}
                    ],
                    'feedback': [
                        {'strategy': 'strategy_2', 'feedback_type': 'positive'},
                        {'strategy': 'strategy_2', 'feedback_type': 'positive'}
                    ]
                }
            },
            'metrics': {
                'total_sessions': 2,
                'total_recommendations': 2,
                'strategy_performance': {
                    'strategy_1': {
                        'total_uses': 1,
                        'user_feedback': [
                            {'feedback_type': 'positive'},
                            {'feedback_type': 'positive'},
                            {'feedback_type': 'negative'}
                        ]
                    },
                    'strategy_2': {
                        'total_uses': 1,
                        'user_feedback': [
                            {'feedback_type': 'positive'},
                            {'feedback_type': 'positive'}
                        ]
                    }
                }
            }
        }
        
        # Write test data
        with open(temp_file, 'w') as f:
            json.dump(test_data, f)
        
        # Reload framework with test data
        ab_framework = ABTestingFramework(temp_file)
        performance = ab_framework.get_strategy_performance()
        
        # Verify calculations
        assert 'strategy_1' in performance, "strategy_1 not found in performance"
        assert 'strategy_2' in performance, "strategy_2 not found in performance"
        
        strat1 = performance['strategy_1']
        strat2 = performance['strategy_2']
        
        # Strategy 1: 2 positive, 1 negative = 66.67% satisfaction
        expected_satisfaction_1 = 2 / (2 + 1)
        assert abs(strat1['satisfaction_rate'] - expected_satisfaction_1) < 0.01, f"Strategy 1 satisfaction rate incorrect: {strat1['satisfaction_rate']}"
        
        # Strategy 2: 2 positive, 0 negative = 100% satisfaction
        expected_satisfaction_2 = 1.0
        assert abs(strat2['satisfaction_rate'] - expected_satisfaction_2) < 0.01, f"Strategy 2 satisfaction rate incorrect: {strat2['satisfaction_rate']}"
        
        print(f"     ✅ Strategy 1 satisfaction rate: {strat1['satisfaction_rate']:.2%} (expected: {expected_satisfaction_1:.2%})")
        print(f"     ✅ Strategy 2 satisfaction rate: {strat2['satisfaction_rate']:.2%} (expected: {expected_satisfaction_2:.2%})")
        
        print("✅ Performance metrics calculations correct!")
        return True
        
    except Exception as e:
        print(f"❌ Performance metrics test failed: {str(e)}")
        return False
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

def main():
    """Run all tests"""
    print("🚀 Starting A/B Testing Implementation Tests\n")
    print("=" * 60)
    
    tests = [
        ("Recommendation Strategies", test_recommendation_strategies),
        ("A/B Testing Framework", test_ab_testing_framework),
        ("Data Consistency", test_data_consistency),
        ("Performance Metrics", test_performance_metrics)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} Test...")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test FAILED with exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! A/B testing implementation is working correctly.")
        print("\n✨ Ready to deploy and start collecting real user data!")
    else:
        print("⚠️  Some tests failed. Please review the implementation.")
    
    return passed == total

if __name__ == "__main__":
    main()