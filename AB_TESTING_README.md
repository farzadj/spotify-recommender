# 🔬 A/B Testing Framework for Spotify Recommender

This document explains the A/B testing implementation that allows you to test different recommendation strategies and measure their performance.

## 🎯 Overview

The A/B testing framework automatically assigns users to different recommendation strategies and collects feedback to determine which algorithms perform best. This helps optimize the recommendation system based on real user preferences.

## 🚀 Features

### **7 Recommendation Strategies for Audio Preferences:**

1. **Cosine Similarity** (Original)
   - Uses cosine similarity between user preferences and song features
   - Baseline algorithm for comparison

2. **Euclidean Distance**
   - Uses Euclidean distance instead of cosine similarity
   - May perform better for certain types of preferences

3. **Weighted Features**
   - Emphasizes energy and danceability (1.5x weight)
   - Gives higher weight to valence (1.2x)
   - Reduces importance of technical features like key and mode

4. **Popularity Boost**
   - Combines similarity (70%) with popularity (30%)
   - Balances personalization with mainstream appeal

5. **Genre Aware**
   - Ensures genre diversity in recommendations
   - Prevents recommendations from being too homogeneous

6. **KNN Based**
   - Uses K-Nearest Neighbors algorithm
   - May capture more complex patterns

7. **Random Baseline**
   - Random recommendations for comparison
   - Helps establish minimum performance threshold

### **3 Recommendation Strategies for Song-based Search:**

1. **Cosine Similarity** (Original)
   - Standard similarity matching

2. **Artist Boost**
   - 30% boost for songs from the same artist
   - Good for discovering more music from favorite artists

3. **Genre Similarity**
   - 20% boost for songs in the same genre
   - Helps stay within preferred musical styles

## 📊 How It Works

### **User Assignment:**
- Each user session is assigned a strategy based on session ID
- Assignment is consistent within a session
- Strategies are distributed evenly across users

### **Data Collection:**
- **Recommendation Events:** Track which strategy was used and what recommendations were given
- **User Feedback:** Collect positive/negative feedback on recommendations
- **Session Data:** Track user behavior across multiple recommendations

### **Performance Metrics:**
- **Total Uses:** How many times each strategy was used
- **Satisfaction Rate:** Percentage of positive feedback
- **Average Recommendations:** Number of recommendations per use

## 🛠️ Implementation Details

### **Files Structure:**
```
├── recommendation_strategies.py  # Strategy implementations
├── ab_testing.py                # A/B testing framework
├── config.py                    # Configuration settings
├── spotify_recommender_app_extended.py  # Main app with A/B testing
└── ab_test_data.json           # Collected test data
```

### **Key Classes:**

#### `RecommendationStrategies`
- Contains all preference-based recommendation algorithms
- Each strategy method takes user preferences and returns recommendations

#### `SongRecommendationStrategies`
- Contains song-based recommendation algorithms
- Each strategy method takes a song name and returns similar songs

#### `ABTestingFramework`
- Manages user sessions and strategy assignment
- Collects and stores test data
- Provides performance analytics

## 📈 Using the A/B Testing Results

### **Accessing Results:**
1. Open the app and select "A/B Test Results" tab
2. View performance metrics and charts
3. Use admin controls to reset data or view raw data

### **Interpreting Results:**
- **Satisfaction Rate:** Higher is better (0-100%)
- **Total Uses:** More data = more reliable results
- **Statistical Significance:** Consider sample size when comparing strategies

### **Making Decisions:**
- Wait for sufficient data (recommend 50+ uses per strategy)
- Compare satisfaction rates between strategies
- Consider user engagement patterns
- Use results to optimize or add new strategies

## 🔧 Configuration

### **Modifying Strategy Weights:**
Edit `config.py` to adjust:
- Feature weights for weighted strategy
- Popularity vs similarity balance
- Artist/genre boost factors

### **Adding New Strategies:**
1. Add new method to `RecommendationStrategies` or `SongRecommendationStrategies`
2. Update strategy dictionaries in `ABTestingFramework`
3. Add strategy call in main app

### **Adjusting Test Parameters:**
- Session timeout duration
- Minimum sample size for significance
- Confidence level for statistical tests

## 📊 Example Results

After collecting data, you might see results like:

| Strategy | Uses | Positive | Negative | Satisfaction Rate |
|----------|------|----------|----------|-------------------|
| Popularity Boost | 45 | 32 | 13 | 71.1% |
| Weighted Features | 38 | 25 | 13 | 65.8% |
| Cosine Similarity | 42 | 26 | 16 | 61.9% |
| Genre Aware | 40 | 24 | 16 | 60.0% |
| Random Baseline | 35 | 12 | 23 | 34.3% |

## 🚀 Best Practices

### **For Users:**
- Provide honest feedback on recommendations
- Try different types of searches to test various scenarios
- Use the app regularly to generate more test data

### **For Developers:**
- Monitor strategy performance regularly
- Add new strategies based on user feedback
- Consider seasonal or temporal patterns in the data
- Implement statistical significance testing for larger datasets

### **For Analysis:**
- Look for patterns in which strategies work best for different user types
- Consider combining successful strategies
- Use feedback to improve existing algorithms

## 🔮 Future Enhancements

### **Planned Features:**
- Statistical significance testing
- Multi-armed bandit optimization
- User segmentation analysis
- Real-time strategy switching
- Advanced visualization of results

### **Potential Strategies to Test:**
- Collaborative filtering
- Deep learning embeddings
- Context-aware recommendations
- Mood-based filtering
- Time-of-day optimization

## 📝 Troubleshooting

### **Common Issues:**
- **No data showing:** Make sure users are providing feedback
- **Uneven strategy distribution:** Check session assignment logic
- **Performance issues:** Consider data sampling for large datasets

### **Debug Mode:**
Enable raw data viewing in admin controls to inspect the collected data structure.

---

This A/B testing framework provides a solid foundation for optimizing your recommendation system based on real user feedback. Start collecting data and watch your recommendations improve over time! 🎵